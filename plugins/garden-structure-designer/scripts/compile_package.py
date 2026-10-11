#!/usr/bin/env python3
"""
compile_package.py
==================

Purpose:
    Stage 7 package compiler: embeds SVG/PNG assets (embed_svgs.py), validates the
    Stage 4 DXF sheets with the parsed cross-artifact validator against the exact bytes
    being packaged (C4: Stage 7 never regenerates drawings), exports the PDF through
    md-to-pdf, and writes outputs/package-manifest.json with SHA-256 digests.

Layer: Execution / Stage 7 Compilation Gate

Key Input Dependencies:
    - context/staging/drawing-red-team-report.json (may_claim_success AND bound to the current revision_id/hash)
    - context/staging/structure.json (sealed model with revision_id)
    - outputs/cad/SB01-structure.dxf and SB02-plan.dxf (written at Stage 4 by export_cad.py)
    - constants.py (CAD_SUBDIR, SHEET_FILENAMES), cross_artifact_validator.py, revision_identity.py
    - outputs/high-resolution-image/*_render_1.png (photorealistic render)
    - outputs/pergola_plan.md (or design-package.md)

Key Functions:
    verify_preflight_gates(staging_dir, outputs_dir) -> tuple[bool, str]
    verify_cad_deliverables(staging_dir, outputs_dir) -> tuple[bool, list[str], str]
    convert_md_to_pdf(embedded_md_path, pdf_path, outputs_dir, stem) -> tuple[bool, str]
    write_package_manifest(outputs_dir, structure) -> Path
    _resolve_markdown(outputs_dir, md_filename) -> Path | None
    compile_package(staging_dir=None, outputs_dir=None, md_filename="pergola_plan.md") -> dict
    main() -> None

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/compile_package.py [staging_dir] [outputs_dir] [md_filename]
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.append(str(Path(__file__).parent))
from constants import CAD_SUBDIR, SHEET_FILENAMES
from cross_artifact_validator import validate_dxf_artifacts
from embed_svgs import process as embed_process
from path_utils import outputs_dir as default_outputs_dir
from path_utils import staging_dir as default_staging_dir
from revision_identity import compute_revision_hash, verify_receipt_binding

MAX_REPORTED_CAD_ERRORS = 10


def verify_preflight_gates(staging_dir: Path, outputs_dir: Path) -> Tuple[bool, str]:
    """Verifies the red-team approval (bound to the current revision), high-res renders, and structure.json."""
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

    structure = json.loads(structure_path.read_text(encoding="utf-8"))
    meta = structure.get("meta") or {}
    if not verify_receipt_binding(r, meta.get("revision_id"), compute_revision_hash(structure)):
        return False, (
            "BLOCKED: drawing-red-team-report.json is not bound to the current revision "
            f"(report revision_id={r.get('revision_id')!r}, structure revision_id={meta.get('revision_id')!r}); "
            "re-run the Stage 5 red-team gate for this revision."
        )

    return True, f"Gate approved. Found {len(renders)} renders."


def verify_cad_deliverables(staging_dir: Path, outputs_dir: Path) -> Tuple[bool, List[str], str]:
    """Validates the existing SB01/SB02 DXF bytes with the parsed validator; never regenerates them (C4 Stage 7)."""
    errors = validate_dxf_artifacts(str(staging_dir), str(outputs_dir))
    if errors:
        shown = "; ".join(errors[:MAX_REPORTED_CAD_ERRORS])
        return False, [], f"CAD validation failed ({len(errors)} errors): {shown}"

    cad_dir = outputs_dir / CAD_SUBDIR
    return True, [str(cad_dir / name) for name in SHEET_FILENAMES.values()], ""


def convert_md_to_pdf(
    embedded_md_path: Path,
    pdf_path: Path,
    outputs_dir: Path,
    stem: str,
) -> Tuple[bool, str]:
    """Invokes npx md-to-pdf to compile standalone embedded markdown into PDF."""
    try:
        cmd = ["npx", "-y", "md-to-pdf", str(embedded_md_path)]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if proc.returncode == 0:
            produced_pdf = outputs_dir / f"{stem}_embedded.pdf"
            if produced_pdf.exists():
                produced_pdf.rename(pdf_path)
                return True, ""
            if pdf_path.exists():
                return True, ""
        return False, proc.stderr or proc.stdout
    except Exception as e:
        return False, str(e)


def write_package_manifest(outputs_dir: Path, structure: Dict[str, Any]) -> Path:
    """Computes SHA-256 hashes for all output deliverables and writes package-manifest.json."""
    manifest_records = []
    for fpath in sorted(outputs_dir.rglob("*")):
        if fpath.is_file() and fpath.name != "package-manifest.json":
            rel = fpath.relative_to(outputs_dir).as_posix()
            digest = hashlib.sha256(fpath.read_bytes()).hexdigest()
            manifest_records.append({
                "path": rel,
                "sha256": digest,
                "size_bytes": fpath.stat().st_size,
            })

    meta = structure.get("meta", {})
    package_manifest = {
        "version": "1.5",
        "revision_id": meta["revision_id"],
        "revision_hash": meta.get("revision_hash") or compute_revision_hash(structure),
        "schema_version": meta.get("schema_version"),
        "topology_family": meta.get("topology_family"),
        "artifacts": manifest_records,
    }
    manifest_path = outputs_dir / "package-manifest.json"
    manifest_path.write_text(json.dumps(package_manifest, indent=2), encoding="utf-8")
    return manifest_path


def _resolve_markdown(outputs_dir: Path, md_filename: str) -> Optional[Path]:
    """Returns the requested markdown file, else the first existing default package markdown, else None."""
    for candidate in (outputs_dir / md_filename, outputs_dir / "pergola_plan.md", outputs_dir / "design-package.md"):
        if candidate.exists():
            return candidate
    return None


def compile_package(
    staging_dir: Optional[Path] = None,
    outputs_dir: Optional[Path] = None,
    md_filename: str = "pergola_plan.md",
) -> Dict[str, Any]:
    """Assembles all CAD, SVG, Markdown, and PDF deliverables into a verified final package."""
    s_dir = Path(staging_dir) if staging_dir is not None else default_staging_dir()
    o_dir = Path(outputs_dir) if outputs_dir is not None else default_outputs_dir()

    passed, msg = verify_preflight_gates(s_dir, o_dir)
    if not passed:
        blocked_path = o_dir / "COMPILATION_BLOCKED.md"
        with open(blocked_path, "w", encoding="utf-8") as f:
            f.write(f"# Compilation Blocked\n\n{msg}\n")
        return {"status": "BLOCKED", "reason": msg, "blocked_file": str(blocked_path)}

    raw_md_path = _resolve_markdown(o_dir, md_filename)
    if raw_md_path is None:
        return {"status": "FAIL", "reason": f"No input markdown file found at {o_dir / md_filename}"}

    stem = raw_md_path.stem
    embedded_md_path = o_dir / f"{stem}_embedded.md"
    pdf_path = o_dir / f"{stem}.pdf"

    cad_ok, cad_manifest, cad_err = verify_cad_deliverables(s_dir, o_dir)
    if not cad_ok:
        return {"status": "FAIL", "reason": cad_err}

    try:
        embed_process(str(raw_md_path), str(embedded_md_path))
    except Exception as e:
        return {"status": "FAIL", "reason": f"Embedding assets failed: {e}"}

    pdf_success, pdf_error = convert_md_to_pdf(embedded_md_path, pdf_path, o_dir, stem)
    structure = json.loads((s_dir / "structure.json").read_text(encoding="utf-8"))
    manifest_path = write_package_manifest(o_dir, structure)

    if pdf_success and pdf_path.exists():
        return {
            "status": "COMPLETE",
            "pdf_output": str(pdf_path),
            "embedded_md": str(embedded_md_path),
            "cad_deliverables": cad_manifest,
            "manifest": str(manifest_path),
        }

    fail_path = o_dir / "PDF_GENERATION_FAILED.md"
    with open(fail_path, "w", encoding="utf-8") as f:
        f.write(f"# PDF Generation Failed / Degraded\n\nError: {pdf_error}\n\nFallback HTML/Markdown is available at: {embedded_md_path}\n")
    return {
        "status": "FALLBACK",
        "reason": pdf_error,
        "embedded_md": str(embedded_md_path),
        "cad_deliverables": cad_manifest,
        "failed_file": str(fail_path),
        "manifest": str(manifest_path),
    }


def main() -> None:
    """CLI entrypoint for running package compilation."""
    s_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    o_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    md_name = sys.argv[3] if len(sys.argv) > 3 else "pergola_plan.md"

    res = compile_package(s_dir, o_dir, md_name)
    print(json.dumps(res, indent=2))
    if res["status"] in ("FAIL", "BLOCKED"):
        sys.exit(1)


if __name__ == "__main__":
    main()
