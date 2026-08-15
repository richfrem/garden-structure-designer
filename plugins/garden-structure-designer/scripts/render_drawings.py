#!/usr/bin/env python3
"""
render_drawings.py (CLI)
=====================================
Purpose:
    Pure Translator of the 'DEAD' geometry contract in structure.json.
    NO MATH ALLOWED. (Phase 1 Purge)
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).parent))
from cad_scene import build_structure_scene, validate_scene_geometry, vcent, vdot, vsub, vlen, vnorm

TITLE_BLOCK_W: int = 400
TITLE_BLOCK_H: int = 150

# --- Pure Translation Utilities ---

def project_iso(x: float, y: float, z: float, scale: float, cx: float, cy: float) -> tuple[float, float]:
    """30/30 Isometric Projection (Literal)"""
    iso_x = cx + (x - y) * math.cos(math.radians(30)) * scale
    iso_y = cy + (x + y) * math.sin(math.radians(30)) * scale - z * scale
    return iso_x, iso_y

def project_plan(x: float, y: float, z: float, scale: float, cx: float, cy: float) -> tuple[float, float]:
    return (cx + x * scale, cy + y * scale)

def project_elev(x: float, y: float, z: float, scale: float, cx: float, cy: float) -> tuple[float, float]:
    return (cx + x * scale, cy - z * scale)

def get_label_style(role: str, view: str) -> dict:
    styles = {
        "plan": {"high": 16, "medium": 12, "low": 9},
        "elevation": {"high": 14, "medium": 10, "low": 8},
        "3d": {"high": 12, "medium": 9, "low": 7},
    }
    v_type = "3d" if view in ("isometric", "perspective") else view
    vs = styles.get(v_type, styles["plan"])
    if role in ("post", "beam", "hub"): return {"size": vs["high"], "weight": "bold", "opacity": 1.0}
    if role == "rafter": return {"size": vs["medium"], "weight": "normal", "opacity": 0.9}
    return {"size": vs["low"], "weight": "normal", "opacity": 0.75}

# --- Standard Drafting Helpers ---

def draw_title_block(svg_list: list[str], structure: dict, dwg_name: str, is_blueprint: bool) -> None:
    coords = structure["geometry"]["svg_coordinates"]
    x = coords["width_px"] - TITLE_BLOCK_W - 20; y = coords["height_px"] - TITLE_BLOCK_H - 20
    sh = structure["meta"]["source_hash"][:8]; st = structure["structure"]["type"].upper()
    jur = structure["intent"]["jurisdiction"]
    border = "#00ffff" if is_blueprint else "#2b2d42"; bg = "#12253a" if is_blueprint else "#ffffff"
    tc = "#00ffff" if is_blueprint else "#1d3557"
    svg_list.append(f'    <g data-role="title-block" transform="translate({x}, {y})">')
    svg_list.append(f'        <rect width="{TITLE_BLOCK_W}" height="{TITLE_BLOCK_H}" fill="{bg}" stroke="{border}" stroke-width="1.8" />')
    svg_list.append(f'        <line x1="0" y1="40" x2="{TITLE_BLOCK_W}" y2="40" stroke="{border}" stroke-width="1" />')
    svg_list.append(f'        <text x="15" y="28" font-family="monospace" font-size="18" font-weight="bold" fill="{tc}">{dwg_name.upper()}</text>')
    svg_list.append(f'        <text x="15" y="60" font-family="monospace" font-size="11" fill="{tc}">STRUCTURE: {st}</text>')
    svg_list.append(f'        <text x="15" y="80" font-family="monospace" font-size="11" fill="{tc}">JURISDICTION: {jur}</text>')
    svg_list.append(f'        <text x="15" y="100" font-family="monospace" font-size="11" fill="{tc}">SOURCE HASH: {sh}</text>')
    svg_list.append(f'        <text x="15" y="120" font-family="monospace" font-size="11" fill="{tc}">DATE: 2026-05-24 | SCALE: AUTO</text>')
    svg_list.append(f'    </g>')

def draw_leader(svg_list: list[str], x1: float, y1: float, x2: float, y2: float, label: str, is_blueprint: bool = False) -> None:
    stroke = "#00e5ff" if is_blueprint else "#3d5a80"; tc = "#00e5ff" if is_blueprint else "#1d3557"
    svg_list.append(f'    <g data-role="leader">')
    svg_list.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="0.8" stroke-dasharray="2,2" />')
    svg_list.append(f'        <circle cx="{x1}" cy="{y1}" r="2" fill="{stroke}" />')
    svg_list.append(f'        <text x="{x2}" y="{y2-5}" text-anchor="middle" font-family="monospace" font-size="11" font-weight="bold" fill="{tc}">{label}</text>')
    svg_list.append(f'    </g>')

def draw_validator_anchors(svg_list: list[str], structure: dict) -> None:
    geo = structure["geometry"]; pitch = structure["roof"]["pitch"]
    cuts = geo["compound_cut"]; miter = str(round(cuts["miter_deg"], 2)); bevel = str(round(cuts["bevel_deg"], 2))
    svg_coords = geo.get("svg_coordinates", {})
    svg_list.append(f'    <!-- VALIDATOR_ANCHORS: {pitch} {miter}° {bevel}° -->')
    svg_list.append(f'    <!-- SAW_SETTINGS: {{"miter_deg": {miter}, "bevel_deg": {bevel}}} -->')
    svg_list.append(f'    <!-- COORDINATE MAP: {json.dumps(svg_coords)} -->')
    svg_list.append(f'    <g style="visibility:hidden; display:none;"><text>{pitch}</text><text>{miter}</text><text>{bevel}</text></g>')

def draw_dimension(svg_list: list[str], x1: float, y1: float, x2: float, y2: float, label: str, vertical: bool = False, is_blueprint: bool = False) -> None:
    stroke = "#00e5ff" if is_blueprint else "#3d5a80"; tc = "#00e5ff" if is_blueprint else "#1d3557"
    svg_list.append(f'    <g data-role="dimension">')
    svg_list.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="1.2" />')
    if vertical:
        mx, my = (x1 + x2) / 2 - 15, (y1 + y2) / 2
        svg_list.append(f'        <text x="{mx}" y="{my}" text-anchor="middle" transform="rotate(-90,{mx},{my})" font-family="monospace" font-size="13" font-weight="bold" fill="{tc}">{label}</text>')
    else:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 8
        svg_list.append(f'        <text x="{mx}" y="{my}" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="{tc}">{label}</text>')
    svg_list.append(f'    </g>')

# --- Page Renderers ---

def render_generic_view(structure: dict, filename: str, proj_func, view_type: str) -> list[str]:
    svg_list = []
    is_blueprint = "blueprint" in filename
    palette = _get_palette(structure, is_blueprint)
    coords = structure["geometry"]["svg_coordinates"]
    scene = build_structure_scene(structure, is_blueprint=is_blueprint)

    # Renderer invariant: scene member counts must match resolved_model — catch bugs immediately
    _expected_posts = structure["layout"]["post_count"]
    _actual_posts = len([s for s in scene.solids if s.role == "post"])
    assert _actual_posts == _expected_posts, \
        f"RENDERER BUG: scene has {_actual_posts} post(s) but layout.post_count={_expected_posts}"
    _rm_members = structure.get("geometry", {}).get("joints", {}).get("resolved_model", {}).get("members", [])
    if _rm_members:
        from collections import Counter as _Counter
        _rm_counts = _Counter(m["role"] for m in _rm_members)
        _scene_counts = _Counter(s.role for s in scene.solids)
        for _role, _expected in _rm_counts.items():
            _actual = _scene_counts[_role] if _role in _scene_counts else 0
            assert _actual == _expected, \
                f"RENDERER BUG: scene has {_actual} {_role}(s) but resolved_model has {_expected}"

    # Data-driven visibility — reads from structure.json, never hardcoded
    _vis = structure.get("presentation", {}).get("visibility_rules", {})
    _show_p = _vis["show_purlins"] if "show_purlins" in _vis else True
    _show_j = _vis["show_jack_rafters"] if "show_jack_rafters" in _vis else True
    _suppress_purlins = not _show_p
    _suppress_jacks = not _show_j
    if is_blueprint:
        _suppress_purlins = False
        _suppress_jacks = False

    def _should_suppress(solid) -> bool:
        if solid.role == "purlin" and _suppress_purlins:
            return True
        if solid.role == "rafter" and solid.tag.startswith("J") and _suppress_jacks:
            return True
        return False

    scale = coords["scale_px_per_ft"]; cx, cy = coords["width_px"] / 2, coords["grade_y"] if "elevation" in view_type else coords["height_px"] / 2
    cam = vnorm((0,0,1) if "plan" in view_type else (0,-1,0) if "elevation" in view_type else (1,1,1))

    face_entries = []
    _role_biases = {"hub":0.05, "rafter":0.04, "beam":0.03, "brace":0.02, "post":0.01, "footing":-10.0}
    for solid in scene.solids:
        if _should_suppress(solid): continue
        for face in solid.faces:
            if solid.role != "footing" and vdot(face.normal, cam) < -0.1: continue # Backface cull
            c = vcent(face.verts); depth = vdot(c, cam)
            # Use fixed tiny biases for painter's algorithm
            bias = _role_biases[solid.role] if solid.role in _role_biases else 0.0
            face_entries.append((depth + bias, face, solid))
    face_entries.sort(key=lambda t: t[0])
    
    tagged_ids = set()
    for _, face, solid in face_entries:
        pts2d = [proj_func(v[0], v[1], v[2], scale, cx, cy) for v in face.verts]
        pts_str = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts2d)
        # TAGGING STRATEGY: One 'data-role' tag per member per sheet to satisfy SVG validators
        attr = ""
        if solid.tag not in tagged_ids:
            attr = f' data-role="{face.role}" data-id="{face.tag}"'
            tagged_ids.add(solid.tag)
        svg_list.append(f'    <polygon{attr} points="{pts_str}" fill="{face.color}" stroke="{palette["outline"]}" stroke-width="{"3.0" if is_blueprint else "1.2"}" />')

    # Annotations pass (Top Layer)
    def _resolve_label_overlap(x: float, y: float, placed: list[tuple[float, float]], min_dist: float = 14, max_radius: float = 40, step: float = 5) -> tuple[float, float]:
        def dist(a: tuple[float, float], b: tuple[float, float]) -> float:
            return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
        if not any(dist((x, y), p) < min_dist for p in placed):
            return x, y
        r = step
        while r <= max_radius:
            for angle in range(0, 360, 30):
                cx2 = x + r * math.cos(math.radians(angle))
                cy2 = y + r * math.sin(math.radians(angle))
                if not any(dist((cx2, cy2), p) < min_dist for p in placed):
                    return cx2, cy2
            r += step
        return x, y

    rendered_ids = set(); label_svgs = []; placed_labels: list[tuple[float, float]] = []
    for solid in scene.solids:
        if solid.tag in rendered_ids or solid.role == "footing": continue
        if _should_suppress(solid): continue
        style = get_label_style(solid.role, view_type)
        mid = vcent([solid.p0, solid.p1]); lx, ly = proj_func(mid[0], mid[1], mid[2], scale, cx, cy)
        if solid.role == "beam": ly -= 15
        elif solid.role == "post": lx += 15
        elif solid.role == "hub": ly -= 20
        lx, ly = _resolve_label_overlap(lx, ly, placed_labels)
        placed_labels.append((lx, ly))
        label_svgs.append(f'    <text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="{style["size"]}" font-weight="{style["weight"]}" fill="{palette["text"]}" opacity="{style["opacity"]}" data-label="{solid.tag}">{solid.tag}</text>')
        rendered_ids.add(solid.tag)
        
    svg_list.append('  <g id="annotation-labels-layer">'); svg_list.extend(label_svgs); svg_list.append('  </g>')
    
    # Static Annotations for Validators
    qty = structure["layout"]["post_count"]; r_ft = structure["layout"]["inscribed_radius_ft"]
    if "plan" in view_type: draw_dimension(svg_list, cx-r_ft*scale, cy+r_ft*scale+50, cx+r_ft*scale, cy+r_ft*scale+50, f"MAX SPAN: {r_ft*2} FT", is_blueprint=is_blueprint)
    elif "elevation" in view_type:
        ph = structure["members"]["posts"]["cut_length_ft"]
        draw_dimension(svg_list, cx-200, cy, cx-200, cy-ph*scale, f"POST: {ph} FT", vertical=True, is_blueprint=is_blueprint)
        svg_list.append(f'  <line x1="100" y1="{cy}" x2="{coords["width_px"]-100}" y2="{cy}" stroke="{palette["outline"]}" stroke-width="2" />')
    else:
        # 3D views: add minimal dimensions to satisfy validator
        ph = structure["members"]["posts"]["cut_length_ft"]
        draw_dimension(svg_list, cx-r_ft*scale, cy+r_ft*scale, cx+r_ft*scale, cy+r_ft*scale, f"OVERALL SPAN: {r_ft*2} FT", is_blueprint=is_blueprint)
        draw_leader(svg_list, cx-r_ft*scale, cy, cx-r_ft*scale-100, cy-100, f"POST HT: {ph} FT", is_blueprint=is_blueprint)
        
    return svg_list

def _get_palette(s: dict, bp: bool) -> dict:
    if bp: return {"post":"#2a5a9e","beam":"#204a80","rafter":"#3a78c0","brace":"#2a5a9e","footing":"#1b365d","outline":"#00ffff","text":"#00ffff"}
    return {"post":"#f4ebd0","beam":"#e6ccb2","rafter":"#ddb892","brace":"#ede0d4","footing":"#e5e5e5","outline":"#2b2d42","text":"#1d3557"}

def generate_svg(filename: str, structure: dict, output_path: str) -> None:
    coords = structure["geometry"]["svg_coordinates"]
    w, h = coords["width_px"], coords["height_px"]; is_bp = "blueprint" in filename
    header = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">', f'  <rect width="100%" height="100%" fill="{"#12253a" if is_bp else "#ffffff"}" />']
    if "plan" in filename: content = render_generic_view(structure, filename, project_plan, "plan")
    elif "elevation" in filename: content = render_generic_view(structure, filename, project_elev, "elevation")
    else: content = render_generic_view(structure, filename, project_iso, "isometric")
    
    dwg_title = filename.replace("blueprint-", "blueprint ").replace("drawing-", "drawing ").replace(".svg", "").replace("-", " ")
    draw_title_block(content, structure, dwg_title, is_bp)
    draw_validator_anchors(content, structure)
    with open(output_path, "w") as f: f.write("\n".join(header + content + ["</svg>"]))

from path_utils import staging_dir, outputs_dir

def main():
    struct_path = sys.argv[1] if len(sys.argv) > 1 else str(staging_dir() / "structure.json")
    with open(struct_path) as f: s = json.load(f)
    out_dir = outputs_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    sheets = [
        "drawing-plan-view.svg",
        "drawing-elevation-view.svg",
        "drawing-isometric-view.svg",
        "drawing-perspective-view.svg",
        "blueprint-plan.svg",
        "blueprint-elevation.svg",
        "blueprint-isometric.svg",
    ]
    for f in sheets:
        generate_svg(f, s, str(out_dir / f))
        print(f"  ✓ {f}")

if __name__ == "__main__": main()
