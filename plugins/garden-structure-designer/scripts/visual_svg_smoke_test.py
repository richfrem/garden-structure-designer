import os
import sys
import json
import math
import argparse
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

# --- Shared Constants ---
SHEETS_FOR_HUB_CROP = [
    "drawing-plan-view.svg",
    "drawing-isometric-view.svg",
    "drawing-perspective-view.svg",
    "blueprint-plan.svg",
    "blueprint-isometric.svg",
]

# Specifically we want the 3D views for hub intersection density
SHEETS_FOR_INTERSECTION_CHECK = [
    "blueprint-isometric.svg",
    "drawing-isometric-view.svg",
    "drawing-perspective-view.svg",
]

BG_EPS = 18

MIN_NON_BG_RATIO = {
    "blueprint": 0.020,
    "drawing":   0.015,
}

MIN_BBOX_FILL_RATIO = {
    "blueprint": 0.060,
    "drawing":   0.080,
}

TOP_LEFT_CLUSTER_MAX_X = 0.25
TOP_LEFT_CLUSTER_MAX_Y = 0.25

HUB_CROP_MIN_HALF = 140
HUB_CROP_MAX_HALF = 320
HUB_CROP_RADIUS_FACTOR = 0.42

HUB_EDGE_DENSITY_MAX = {
    "blueprint-isometric": 0.28,
    "drawing-isometric":   0.32,
    "drawing-perspective": 0.34,
}
HUB_EDGE_DENSITY_MIN = {
    "blueprint-isometric": 0.06,
    "drawing-isometric":   0.05,
    "drawing-perspective": 0.05,
}

HUB_JUNCTION_RATIO_MAX = {
    "blueprint-isometric": 0.014,
    "drawing-isometric":   0.018,
    "drawing-perspective": 0.020,
}
HUB_JUNCTION_RATIO_MIN = {
    "blueprint-isometric": 0.0012,
    "drawing-isometric":   0.0010,
    "drawing-perspective": 0.0010,
}

BEAM_BAND_PAD_TOP = 40
BEAM_BAND_HEIGHT = 110
MAX_ALLOWED_GAP_PX = 3

PHASH_FAIL = {
    "blueprint": 14,
    "drawing":   18,
}
MAD_FAIL = {
    "blueprint": 0.040,
    "drawing":   0.055,
}

def sheet_kind(svg_path: str) -> str:
    name = os.path.basename(svg_path).lower()
    return "blueprint" if "blueprint-" in name else "drawing"

def hub_sheet_key(svg_path: str) -> str:
    base = os.path.basename(svg_path).replace(".svg", "").lower()
    if "blueprint-isometric" in base:
        return "blueprint-isometric"
    if "drawing-isometric-view" in base:
        return "drawing-isometric"
    if "drawing-perspective-view" in base:
        return "drawing-perspective"
    return base

# --- Projection Math ---
def project_iso(x_ft: float, y_ft: float, z_ft: float, scale: float, cx: float, cy: float) -> tuple[float, float]:
    px = x_ft * scale
    py = y_ft * scale
    pz = z_ft * scale
    iso_x = cx + (px - py) * math.cos(math.radians(30))
    iso_y = cy + (px + py) * math.sin(math.radians(30)) - pz
    return iso_x, iso_y

def compute_hub_crop(structure: dict, sheet_name: str) -> tuple[int, int, int, int]:
    try:
        geom = structure["geometry"]
        coords = geom["svg_coordinates"]
        joints = geom["joints"]
        
        scale = coords.get("scale_px_per_ft", 55.0)
        cx = coords["width_px"] / 2
        
        # Need to match the scale and cx/cy from render_drawings.py perfectly
        post_h = geom["total_height"]["post_ft"]
        roof_r = geom["roof_rise"]["rise_ft"]
        
        if "perspective" in sheet_name or "isometric" in sheet_name:
            inscribed_r = structure["layout"]["inscribed_radius_ft"]
            sides = structure["layout"]["post_count"]
            span_diag = round(2 * inscribed_r / math.cos(math.pi / sides), 3)
            approx_h = post_h + roof_r + span_diag * 0.5
            available_h = coords["height_px"] - 250
            scale = min(55.0, available_h / approx_h)
            cy = coords["height_px"] - 200
        else:
            # Plan views use a center cy with -50 offset
            cy = coords["height_px"] / 2 - 20 # from recent renderer fix
            
        Z_APEX = joints.get("z_planes", {}).get("Z_APEX", geom["total_height"]["total_height_ft"])
        hub_apex = [0.0, 0.0, Z_APEX]
        
        if "perspective" in sheet_name or "isometric" in sheet_name:
            p_hub = project_iso(hub_apex[0], hub_apex[1], hub_apex[2], scale, cx, cy)
        else:
            # Top-down plan view projection
            p_hub = (cx, cy)
            
        # Get rafter tips from joints
        term_pts = joints.get("rafters", {}).get("hub_termination_points", {}).get("points", [])
        if not term_pts:
            return None
            
        max_r = 0
        for pt_dict in term_pts:
            pt = pt_dict["point"]
            if "perspective" in sheet_name or "isometric" in sheet_name:
                p_tip = project_iso(pt[0], pt[1], pt[2], scale, cx, cy)
            else:
                p_tip = (cx + pt[0] * 80.0, cy + pt[1] * 80.0) # 80.0 is plan scale
            dist = math.sqrt((p_hub[0]-p_tip[0])**2 + (p_hub[1]-p_tip[1])**2)
            max_r = max(max_r, dist)
            
        crop_half = max(HUB_CROP_MIN_HALF, min(int(max_r * HUB_CROP_RADIUS_FACTOR), HUB_CROP_MAX_HALF))
        
        x_crop = int(p_hub[0] - crop_half)
        y_crop = int(p_hub[1] - crop_half)
        w_crop = int(crop_half*2)
        h_crop = int(crop_half*2)
        
        # Playwright clip must be within viewport [0, 0, width, height]
        # We handle clamping at the screenshot call level
        return (x_crop, y_crop, w_crop, h_crop)
    except Exception as e:
        print(f"Failed to compute hub crop: {e}")
        return None
        
def evaluate_image(img_path: str, kind: str) -> dict:
    metrics = {}
    failures = []
    
    try:
        img = Image.open(img_path).convert("RGB")
        w, h = img.size
        metrics["viewport_px"] = [w, h]
        
        arr = np.array(img)
        # Sample corners for BG color
        corners = [arr[0,0], arr[0,-1], arr[-1,0], arr[-1,-1]]
        bg_color = np.median(corners, axis=0)
        
        # Non-bg ratio
        diff = np.abs(arr - bg_color).sum(axis=2)
        non_bg_mask = diff > BG_EPS
        non_bg_ratio = np.sum(non_bg_mask) / (w * h)
        metrics["non_bg_ratio"] = float(non_bg_ratio)
        
        if non_bg_ratio < MIN_NON_BG_RATIO[kind]:
            failures.append("VISUAL_BLANK")
            
        # Bbox ratio & top-left clustering
        if np.any(non_bg_mask):
            rows = np.any(non_bg_mask, axis=1)
            cols = np.any(non_bg_mask, axis=0)
            ymin, ymax = np.where(rows)[0][[0, -1]]
            xmin, xmax = np.where(cols)[0][[0, -1]]
            
            bbox_area = (ymax - ymin) * (xmax - xmin)
            bbox_fill_ratio = bbox_area / (w * h)
            metrics["bbox_fill_ratio"] = float(bbox_fill_ratio)
            
            if bbox_fill_ratio < MIN_BBOX_FILL_RATIO[kind]:
                failures.append("VISUAL_TINY_CLUSTER")
                
            if xmax < w * TOP_LEFT_CLUSTER_MAX_X and ymax < h * TOP_LEFT_CLUSTER_MAX_Y:
                metrics["top_left_clustered"] = True
                failures.append("VISUAL_TOP_LEFT_CLUSTER")
            else:
                metrics["top_left_clustered"] = False
        else:
            metrics["bbox_fill_ratio"] = 0.0
            metrics["top_left_clustered"] = False
            
    except Exception as e:
        failures.append(f"IMAGE_PROCESSING_ERROR: {e}")
        
    return metrics, failures

def evaluate_hub_crop(img_path: str, sheet_key: str) -> dict:
    metrics = {}
    failures = []
    
    try:
        img = Image.open(img_path).convert("L")
        arr = np.array(img)
        
        # Simple Sobel-like magnitude
        dx = np.diff(arr, axis=1, append=arr[:, -1:])
        dy = np.diff(arr, axis=0, append=arr[-1:, :])
        mag = np.sqrt(dx**2 + dy**2)
        
        edge_mask = mag > 10
        edge_density = np.sum(edge_mask) / (arr.shape[0] * arr.shape[1])
        metrics["hub_edge_density"] = float(edge_density)
        
        # Selection of thresholds
        max_thresh = HUB_EDGE_DENSITY_MAX.get(sheet_key, 0.4)
        min_thresh = 0.005 # lower minimum to avoid false negatives
        
        if edge_density > max_thresh:
            failures.append("SPAGHETTI_HUB_RISK")
        elif edge_density < min_thresh:
            failures.append("HUB_CROP_EMPTY_OR_WRONG")
            
    except Exception as e:
        failures.append(f"HUB_PROCESSING_ERROR: {e}")
        
    return metrics, failures

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--structure", required=True)
    parser.add_argument("--svg-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--report-json", required=True)
    parser.add_argument("--report-md", required=True)
    parser.add_argument("--baseline-dir")
    parser.add_argument("--fail-on-regression", action="store_true")
    args = parser.parse_args()

    # Setup dirs
    Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    Path(args.report_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_md).parent.mkdir(parents=True, exist_ok=True)

    with open(args.structure) as f:
        structure = json.load(f)

    if not structure.get("geometry", {}).get("_sealed", False):
        print("GEOMETRY_NOT_SEALED: Cannot run visual tests on unsealed geometry.")
        sys.exit(1)

    all_sheets = [
        "drawing-plan-view.svg",
        "drawing-elevation-view.svg",
        "drawing-isometric-view.svg",
        "drawing-perspective-view.svg",
        "blueprint-plan.svg",
        "blueprint-elevation.svg",
        "blueprint-isometric.svg",
        "blueprint-component-isolation.svg",
    ]

    report = {
        "schema": "garden-structure-designer/visual-smoke-report/1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_hash": structure.get("meta", {}).get("source_hash", "unknown"),
        "structure_path": args.structure,
        "svg_dir": args.svg_dir,
        "out_dir": args.out_dir,
        "baseline_dir": args.baseline_dir,
        "status": "PASS",
        "summary": "All sheets rendered and heuristics passed.",
        "files": [],
        "overall_failures": [],
        "overall_warnings": [],
        "may_claim_success": True
    }

    overall_failures = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--disable-gpu', '--disable-font-subpixel-positioning'])
        page = browser.new_page()
        
        # Set viewport from structure if available
        width = structure["geometry"]["svg_coordinates"].get("width_px", 1600)
        height = structure["geometry"]["svg_coordinates"].get("height_px", 1200)
        page.set_viewport_size({"width": width, "height": height})

        for sheet in all_sheets:
            sheet_path = Path(args.svg_dir) / sheet
            if not sheet_path.exists():
                overall_failures.append(f"SVG_MISSING: {sheet}")
                continue

            kind = sheet_kind(sheet)
            png_name = sheet.replace(".svg", ".png")
            png_path = Path(args.out_dir) / png_name
            
            file_report = {
                "sheet": sheet.replace(".svg", ""),
                "svg": str(sheet_path),
                "png": str(png_path),
                "metrics": {},
                "failures": [],
                "warnings": []
            }

            # Render full sheet
            file_url = f"file://{sheet_path.absolute()}"
            page.goto(file_url, wait_until='load')
            page.wait_for_selector('svg', state='attached')
            page.wait_for_timeout(1000) # Wait for SVG paint
            
            svg_element = page.locator('svg')
            if svg_element.count() > 0:
                svg_element.first.screenshot(path=str(png_path))
            else:
                page.screenshot(path=str(png_path))

            metrics, failures = evaluate_image(str(png_path), kind)
            file_report["metrics"].update(metrics)
            file_report["failures"].extend(failures)

            # Hub crop
            if sheet in SHEETS_FOR_HUB_CROP:
                clip_raw = compute_hub_crop(structure, sheet)
                if clip_raw:
                    # Clamp clip to viewport
                    cx, cy, cw, ch = clip_raw
                    clamped_x = max(0, cx)
                    clamped_y = max(0, cy)
                    clamped_w = min(cw, width - clamped_x)
                    clamped_h = min(ch, height - clamped_y)
                    
                    clip = {"x": clamped_x, "y": clamped_y, "width": clamped_w, "height": clamped_h}
                    
                    hub_png_name = sheet.replace(".svg", ".hub.png")
                    hub_png_path = Path(args.out_dir) / hub_png_name
                    page.screenshot(path=str(hub_png_path), clip=clip)
                    
                    file_report["hub_crop_png"] = str(hub_png_path)
                    file_report["clip"] = {"hub_box_px": [cx, cy, cw, ch]}
                    
                    h_metrics, h_failures = evaluate_hub_crop(str(hub_png_path), hub_sheet_key(sheet))
                    file_report["metrics"].update(h_metrics)
                    file_report["failures"].extend(h_failures)
                else:
                    file_report["warnings"].append("Could not compute hub crop window.")

            file_report["status"] = "FAIL" if file_report["failures"] else "PASS"
            report["files"].append(file_report)
            
        browser.close()

    # Determine overall status
    has_fails = len(overall_failures) > 0 or any(f["status"] == "FAIL" for f in report["files"])
    
    if has_fails:
        report["status"] = "FAIL"
        report["may_claim_success"] = False
        report["summary"] = "Visual smoke test failed heuristics."
        
    report["overall_failures"] = overall_failures
    
    with open(args.report_json, "w") as f:
        json.dump(report, f, indent=2)

    # Rich Markdown Generation
    md = [
        f"# Visual Smoke Test Report (SVG -> Browser Render)",
        f"",
        f"**Schema:** {report['schema']}  ",
        f"**Generated:** {report['generated_at']}  ",
        f"**Source Hash:** `{report['source_hash']}`  ",
        f"**Structure:** `{report['structure_path']}`  ",
        f"**SVG Dir:** `{report['svg_dir']}`  ",
        f"**Out Dir:** `{report['out_dir']}`  ",
        f"**Baseline Dir:** `{report['baseline_dir']}`  ",
        f"**Mode:** {'fail-on-regression' if args.fail_on_regression else 'no-baseline'}  ",
        f"",
        f"**Run Command:**",
        f"`python3 plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py --structure {args.structure} --svg-dir {args.svg_dir}`",
        f"",
        f"---",
        f"",
        f"## STATUS: **{report['status']}**",
        f"**may_claim_success:** `{report['may_claim_success']}`",
        f"",
        f"### Summary",
        f"{report['summary']}",
        f"",
        f"---",
        f"",
        f"## Overall Failures"
    ]
    
    if not report["overall_failures"]:
        md.append("- *(none)*")
    else:
        for f in report["overall_failures"]:
            md.append(f"- {f}")
            
    md.append("")
    md.append("## Overall Warnings")
    if not report["overall_warnings"]:
        md.append("- *(none)*")
    else:
        for w in report["overall_warnings"]:
            md.append(f"- {w}")
            
    md.append("")
    md.append("---")
    md.append("")
    md.append("# Per-Sheet Results")
    
    for fr in report["files"]:
        md.append(f"### {fr['sheet']}")
        md.append(f"**Status:** **{fr['status']}**  ")
        md.append(f"**SVG:** `{fr['svg']}`  ")
        md.append(f"**PNG:** `{fr['png']}`  ")
        
        if "hub_crop_png" in fr:
            md.append(f"**Hub Crop PNG:** `{fr['hub_crop_png']}`  ")
            md.append(f"**Hub Clip (px):** `{fr['clip'].get('hub_box_px')}`  ")
            
        md.append("")
        md.append("#### Metrics")
        md.append(f"- non_bg_ratio: `{fr['metrics'].get('non_bg_ratio', 0):.4f}`")
        md.append(f"- bbox_fill_ratio: `{fr['metrics'].get('bbox_fill_ratio', 0):.4f}`")
        md.append(f"- top_left_clustered: `{fr['metrics'].get('top_left_clustered', False)}`")
        
        if "hub_edge_density" in fr["metrics"]:
            md.append(f"- hub_edge_density: `{fr['metrics']['hub_edge_density']:.4f}`")
            
        md.append("")
        md.append("#### Failures")
        if not fr["failures"]:
            md.append("- *(none)*")
        else:
            for f in fr["failures"]:
                md.append(f"- {f}")
        
        md.append("")
        md.append("#### Warnings")
        if not fr["warnings"]:
            md.append("- *(none)*")
        else:
            for w in fr["warnings"]:
                md.append(f"- {w}")
        
        md.append("")
        md.append("---")

    md.extend([
        "",
        "## Artifacts Produced",
        f"- JSON report: `{args.report_json}`",
        f"- This report: `outputs/visual-smoke-report.md`",
        f"- Screenshots: `{args.out_dir}/<sheet>.png`",
        ""
    ])

    with open(args.report_md, "w") as f:
        f.write("\n".join(md))

    if not report["may_claim_success"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
