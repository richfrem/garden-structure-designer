#!/usr/bin/env python3
"""
compile_package.py (CLI)
=====================================

Purpose:
    Integrates SVG/PNG embedding (embed_svgs.py logic) and Playwright/Chromium or md-to-pdf PDF export
    with graceful fallback for compilation of structural design packets.

Layer: Execution / Compilation Gate

Usage Examples:
    python compile_package.py [staging_dir] [outputs_dir] [md_filename]

Input Files:
    context/staging/drawing-red-team-report.json
    context/staging/structure.json
    outputs/high-resolution-image/*_render_1.png
    outputs/<md_filename>

Output:
    outputs/cad/SB01-structure.dxf, outputs/cad/SB02-plan.dxf (listed under ``cad_deliverables``)
    outputs/<stem>_embedded.md
    outputs/<stem>.pdf (or COMPILATION_BLOCKED.md / PDF_GENERATION_FAILED.md on failure/fallback)
"""

import sys
import os
import json
import subprocess
from pathlib import Path

# Ensure path_utils can be imported
sys.path.append(str(Path(__file__).parent))
from path_utils import staging_dir as default_staging_dir, outputs_dir as default_outputs_dir
from embed_svgs import process as embed_process
from export_cad import SHEET_FILENAMES, export_sheets

CAD_SUBDIR = "cad"

def verify_preflight_gates(staging_dir: Path, outputs_dir: Path) -> tuple[bool, str]:
    report_path = staging_dir / "drawing-red-team-report.json"
    if not report_path.exists():
        return False, f"BLOCKED: {report_path} not found. Run Stage 5.75 first."
        
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            r = json.load(f)
    except Exception as e:
        return False, f"BLOCKED: Could not parse {report_path}: {e}"
        
    if not r.get("may_claim_success"):
        summary_txt = r.get("summary") or ""
        return False, f"BLOCKED: drawing-red-team-report.json has may_claim_success: false. Summary: {summary_txt}"
        
    img_dir = outputs_dir / "high-resolution-image"
    renders = list(img_dir.glob("*.png")) if img_dir.exists() else []
    if not renders:
        return False, f"BLOCKED: No photorealistic renders found in {img_dir}"

    structure_path = staging_dir / "structure.json"
    if not structure_path.exists():
        return False, f"BLOCKED: {structure_path} not found; required for CAD export."

    return True, f"Gate approved. Found {len(renders)} renders."

def compile_package(staging_dir: Path = None, outputs_dir: Path = None, md_filename: str = "pergola_plan.md") -> dict:
    if staging_dir is None:
        staging_dir = default_staging_dir()
    if outputs_dir is None:
        outputs_dir = default_outputs_dir()
        
    staging_dir = Path(staging_dir)
    outputs_dir = Path(outputs_dir)
    
    passed, msg = verify_preflight_gates(staging_dir, outputs_dir)
    if not passed:
        blocked_path = outputs_dir / "COMPILATION_BLOCKED.md"
        with open(blocked_path, "w", encoding="utf-8") as f:
            f.write(f"# Compilation Blocked\n\n{msg}\n")
        return {"status": "BLOCKED", "reason": msg, "blocked_file": str(blocked_path)}
        
    raw_md_path = outputs_dir / md_filename
    if not raw_md_path.exists():
        # Fallback to pergola_plan.md or design-package.md
        alt_paths = [outputs_dir / "pergola_plan.md", outputs_dir / "design-package.md"]
        found = None
        for p in alt_paths:
            if p.exists():
                found = p
                break
        if not found:
            return {"status": "FAIL", "reason": f"No input markdown file found at {raw_md_path}"}
        raw_md_path = found
        
    stem = raw_md_path.stem
    embedded_md_path = outputs_dir / f"{stem}_embedded.md"
    pdf_path = outputs_dir / f"{stem}.pdf"
    
    # 0. Export CAD deliverables (SB01 3D structure, SB02 plan) from the sealed structure
    cad_dir = outputs_dir / CAD_SUBDIR
    try:
        structure = json.loads((staging_dir / "structure.json").read_text(encoding="utf-8"))
        export_sheets(structure, cad_dir)
    except Exception as e:
        return {"status": "FAIL", "reason": f"CAD export failed: {e}"}
    cad_deliverables = [cad_dir / name for name in SHEET_FILENAMES.values()]
    missing = [str(p) for p in cad_deliverables if not p.exists() or p.stat().st_size == 0]
    if missing:
        return {"status": "FAIL", "reason": f"CAD deliverables missing or empty: {missing}"}
    cad_manifest = [str(p) for p in cad_deliverables]

    # 1. Embed SVGs and PNGs into single standalone embedded markdown
    try:
        embed_process(str(raw_md_path), str(embedded_md_path))
    except Exception as e:
        return {"status": "FAIL", "reason": f"Embedding assets failed: {e}"}
        
    # 2. Attempt PDF export via npx md-to-pdf
    pdf_success = False
    pdf_error = ""
    
    try:
        cmd = ["npx", "-y", "md-to-pdf", str(embedded_md_path)]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if proc.returncode == 0:
            # md-to-pdf creates <stem>_embedded.pdf
            produced_pdf = outputs_dir / f"{stem}_embedded.pdf"
            if produced_pdf.exists():
                produced_pdf.rename(pdf_path)
                pdf_success = True
            elif pdf_path.exists():
                pdf_success = True
        else:
            pdf_error = proc.stderr or proc.stdout
    except Exception as e:
        pdf_error = str(e)
        
    # 3. Generate outputs/package-manifest.json with SHA-256 digests
    import hashlib
    manifest_records = []
    # Collect all outputs files
    for fpath in sorted(outputs_dir.rglob("*")):
        if fpath.is_file() and fpath.name != "package-manifest.json":
            rel = fpath.relative_to(outputs_dir).as_posix()
            digest = hashlib.sha256(fpath.read_bytes()).hexdigest()
            manifest_records.append({
                "path": rel,
                "sha256": digest,
                "size_bytes": fpath.stat().st_size
            })

    meta = structure.get("meta", {})
    package_manifest = {
        "version": "1.5",
        "revision_id": meta.get("revision_id"),
        "revision_hash": meta.get("revision_hash"),
        "schema_version": meta.get("schema_version", "1.5"),
        "topology_family": meta.get("topology_family", "RadialHubTopology"),
        "artifacts": manifest_records,
    }
    manifest_path = outputs_dir / "package-manifest.json"
    manifest_path.write_text(json.dumps(package_manifest, indent=2), encoding="utf-8")

    if pdf_success and pdf_path.exists():
        return {
            "status": "COMPLETE",
            "pdf_output": str(pdf_path),
            "embedded_md": str(embedded_md_path),
            "cad_deliverables": cad_manifest,
            "manifest": str(manifest_path)
        }
    else:
        fail_path = outputs_dir / "PDF_GENERATION_FAILED.md"
        with open(fail_path, "w", encoding="utf-8") as f:
            f.write(f"# PDF Generation Failed / Degraded\n\nError: {pdf_error}\n\nFallback HTML/Markdown is available at: {embedded_md_path}\n")
        return {
            "status": "FALLBACK",
            "reason": pdf_error,
            "embedded_md": str(embedded_md_path),
            "cad_deliverables": cad_manifest,
            "failed_file": str(fail_path),
            "manifest": str(manifest_path)
        }

def main():
    s_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    o_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    md_name = sys.argv[3] if len(sys.argv) > 3 else "pergola_plan.md"
    
    res = compile_package(s_dir, o_dir, md_name)
    print(json.dumps(res, indent=2))
    if res["status"] in ("FAIL", "BLOCKED"):
        sys.exit(1)

if __name__ == "__main__":
    main()
