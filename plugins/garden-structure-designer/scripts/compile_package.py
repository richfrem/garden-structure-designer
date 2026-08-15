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
    outputs/high-resolution-image/*_render_1.png
    outputs/<md_filename>

Output:
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
        
    if pdf_success and pdf_path.exists():
        return {
            "status": "COMPLETE",
            "pdf_output": str(pdf_path),
            "embedded_md": str(embedded_md_path)
        }
    else:
        fail_path = outputs_dir / "PDF_GENERATION_FAILED.md"
        with open(fail_path, "w", encoding="utf-8") as f:
            f.write(f"# PDF Generation Failed / Degraded\n\nError: {pdf_error}\n\nFallback HTML/Markdown is available at: {embedded_md_path}\n")
        return {
            "status": "FALLBACK",
            "reason": pdf_error,
            "embedded_md": str(embedded_md_path),
            "failed_file": str(fail_path)
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
