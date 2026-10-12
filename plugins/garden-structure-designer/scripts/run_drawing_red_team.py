#!/usr/bin/env python3
"""
run_drawing_red_team.py
=======================

Purpose:
    Stage 5 independent approval gate. Runs the peer validators on every SVG sheet, consumes the
    visual-smoke report, validates the parsed DXF sheets (SB01/SB02) and the fabrication cut list,
    and writes ``drawing-red-team-report.json/.md``. ``may_claim_success`` is true only when every
    artifact passes. The report is bound to the reviewed revision (``revision_id``, ``revision_hash``,
    ``hash_algorithm``), so approvals can never be carried over to a different revision (spec C4/C5).

Layer: Execution / Stage 5 Adversarial QA Gate

Key Input Dependencies:
    - context/staging/structure.json (stamped: meta.revision_id, meta.source_hash)
    - context/staging/{schema-validation,physics-validation,visual-smoke}-report.json
    - outputs/*.svg (8 sheets), outputs/cad/SB01-structure.dxf + SB02-plan.dxf,
      outputs/fabrication/cut-list.json
    - svg_validator.py, drawing_content_validator.py (run as subprocesses),
      cross_artifact_validator.py, package_consistency_validator.py, revision_identity.py, constants.py

Key Functions:
    run_review(svg_dir, model_path, report_dir, md_dir) -> dict
    main() -> None
    _run_validator / _run_content_validator_with_json / _count_semantic_roles / _count_text_labels
    _write_json_report / _write_md_report
    _identity(model_path) -> dict                       _blocked(identity, code, summary, fixes, paths) -> dict
    _missing_staging_artifacts(report_dir) -> list      _stale_source_hashes(report_dir) -> list
    _load_smoke(report_dir, svg_dir) -> tuple           _review_sheet(...) -> tuple[dict, bool]
    _artifact_errors(svg_dir, report_dir) -> list       _finalize(...) -> None

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/run_drawing_red_team.py [--svg-dir outputs] [--model structure.json]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
REVIEWER = "run_drawing_red_team.py"

# Resolve canonical staging dir via path_utils (CWD-agnostic)
sys.path.insert(0, str(SCRIPT_DIR))
from constants import CAD_SUBDIR, CUT_LIST_FILENAME, FABRICATION_SUBDIR, SVG_SHEET_FILENAMES
from cross_artifact_validator import validate_dxf_artifacts
from package_consistency_validator import check_revision_binding
from path_utils import staging_dir as _staging_dir, outputs_dir as _outputs_dir
from revision_identity import HASH_ALGORITHM, compute_revision_hash

_STAGING = _staging_dir()
_OUTPUTS = _outputs_dir()
SCHEMA = "garden-structure-designer/drawing-red-team-report/1.0"
STAGING_REPORTS = ("schema-validation-report.json", "physics-validation-report.json", "visual-smoke-report.json")

# Sheets that MUST exist for a complete package (single source: constants.SVG_SHEET_FILENAMES)
REQUIRED_SHEETS = list(SVG_SHEET_FILENAMES)




# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_validator(script_name: str, svg_path: str, model_path: str) -> tuple[bool, str]:
    """
    Run a peer validator script as a subprocess.

    Returns:
        (passed: bool, output: str)
    """
    script = SCRIPT_DIR / script_name
    if not script.exists():
        return True, f"[SKIP] {script_name} not found — skipped."

    cmd = [sys.executable, str(script), svg_path]
    if model_path and os.path.exists(model_path):
        cmd.append(model_path)

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def _run_content_validator_with_json(
    svg_path: str,
    model_path: str,
    report_path: str,
    append: bool,
) -> tuple[bool, str]:
    """Run drawing_content_validator.py with --json-output."""
    script = SCRIPT_DIR / "drawing_content_validator.py"
    if not script.exists():
        return True, "[SKIP] drawing_content_validator.py not found."

    cmd = [sys.executable, str(script), svg_path]
    if model_path and os.path.exists(model_path):
        cmd.append(model_path)
    cmd += ["--json-output", report_path]
    if append:
        cmd.append("--append")

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def _count_semantic_roles(svg_path: str) -> dict[str, int]:
    """Quick role count directly from SVG text without importing the validator."""
    roles = ["post", "beam", "rafter", "brace", "footing", "dimension", "component", "title-block"]
    try:
        raw = Path(svg_path).read_text(encoding="utf-8")
        return {role: len(re.findall(rf'data-role="{role}"', raw)) for role in roles}
    except OSError:
        return {role: 0 for role in roles}


def _count_text_labels(svg_path: str) -> int:
    """Number of non-empty <text> elements in the SVG."""
    try:
        raw = Path(svg_path).read_text(encoding="utf-8")
        matches = re.findall(r"<text[^>]*>([^<]+)</text>", raw)
        return sum(1 for m in matches if m.strip())
    except OSError:
        return 0


# ---------------------------------------------------------------------------
# Report writers
# ---------------------------------------------------------------------------

def _write_json_report(report: dict, report_path: str) -> None:
    """Writes the red-team report as JSON, creating parent directories."""
    os.makedirs(os.path.dirname(report_path) or ".", exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


def _write_md_report(report: dict, md_path: str) -> None:
    """Writes the human-readable Markdown rendering of the red-team report."""
    status = report["status"]
    may_claim = bool(report.get("may_claim_success"))
    summary = report.get("summary", "")

    lines = [
        "# Drawing Red-Team Review Report",
        "",
        f"**Status:** {status}  ",
        f"**May claim success:** {str(may_claim).lower()}  ",
        f"**Reviewer:** {report.get('reviewer', REVIEWER)}  ",
        f"**Generated:** {report.get('generated', '')}  ",
        f"**Revision:** {report.get('revision_id')} ({report.get('revision_hash')})  ",
        "",
        f"> {summary}",
        "",
        "---",
        "",
        "## Per-Sheet Results",
        "",
    ]

    for entry in report.get("files", []):
        sheet_status = entry.get("status", "UNKNOWN")
        icon = "✅" if sheet_status == "PASS" else "❌"
        lines.append(f"### {icon} `{entry['file']}` — {sheet_status}")
        lines.append("")
        counts = entry.get("semantic_counts", {})
        if counts:
            lines.append("**Semantic counts:**")
            for role, n in counts.items():
                lines.append(f"- `data-role=\"{role}\"`: {n}")
        lines.append(f"- Text labels: {entry.get('text_label_count') or 0}")
        lines.append(f"- Total elements: {entry.get('total_elements') or 0}")
        lines.append("")
        codes = entry.get("failure_codes", [])
        if codes:
            lines.append("**Failure codes:**")
            for code in codes:
                lines.append(f"- `{code}`")
            lines.append("")
        fixes = entry.get("required_fixes", [])
        if fixes:
            lines.append("**Required fixes:**")
            for fix in fixes:
                lines.append(f"- {fix}")
            lines.append("")
        lines.append("---")
        lines.append("")

    overall_fixes = report.get("overall_required_fixes", [])
    if overall_fixes:
        lines.append("## Overall Required Fixes")
        for fix in overall_fixes:
            lines.append(f"- {fix}")
        lines.append("")

    os.makedirs(os.path.dirname(md_path) or ".", exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ---------------------------------------------------------------------------
# Main review logic
# ---------------------------------------------------------------------------

def _identity(model_path: str) -> dict:
    """Revision identity of the reviewed structure.json (recomputed hash; None fields when unstamped)."""
    try:
        data = json.loads(Path(model_path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"revision_id": None, "revision_hash": None, "hash_algorithm": HASH_ALGORITHM}
    meta = data.get("meta") or {}
    stored = meta.get("revision_hash")
    recomputed = compute_revision_hash(data)
    return {
        "revision_id": meta.get("revision_id"),
        "revision_hash": recomputed,
        "hash_algorithm": HASH_ALGORITHM,
        "stored_hash_matches": stored is None or stored == recomputed,
    }


def _blocked(identity: dict, code: str, summary: str, fixes: list[str], paths: tuple[str, str]) -> dict:
    """Writes and returns a BLOCKED report (no approval) bound to ``identity``."""
    report = {
        "schema": SCHEMA,
        "generated": datetime.now(timezone.utc).isoformat(),
        "status": "BLOCKED",
        "reviewer": REVIEWER,
        **{k: identity[k] for k in ("revision_id", "revision_hash", "hash_algorithm")},
        "failure_classification": [code],
        "recommended_next_action": "RERUN_REPORTS_FIRST",
        "summary": summary,
        "files": [],
        "overall_required_fixes": fixes,
        "may_claim_success": False,
    }
    _write_json_report(report, paths[0])
    _write_md_report(report, paths[1])
    return report


def _missing_staging_artifacts(report_dir: str) -> list[str]:
    """Required deterministic staging artifacts that do not exist."""
    required = [str(Path(report_dir) / name) for name in ("structure.json", *STAGING_REPORTS)]
    return [path for path in required if not os.path.exists(path)]


def _stale_source_hashes(report_dir: str) -> list[str]:
    """Staging reports whose source_hash differs from structure.json: stale evidence from another run."""
    try:
        current = json.loads((Path(report_dir) / "structure.json").read_text(encoding="utf-8")).get("meta", {}).get("source_hash")
    except (OSError, ValueError):
        return []
    mismatches: list[str] = []
    for name in STAGING_REPORTS[:3]:
        path = Path(report_dir) / name
        if not (current and path.exists()):
            continue
        try:
            found = json.loads(path.read_text(encoding="utf-8")).get("source_hash")
        except (OSError, ValueError):
            continue
        if found and found != current:
            mismatches.append(f"{name}: hash {found!r} != current {current!r}")
    return mismatches


def _smoke_is_stale(smoke_data: dict, svg_dir: str) -> Optional[str]:
    """STALE_SMOKE_REPORT message when the smoke run predates the newest SVG, else None."""
    generated = smoke_data.get("generated_at", "")
    if not generated:
        return None
    try:
        smoke_dt = datetime.fromisoformat(generated)
    except ValueError:
        return None
    if smoke_dt.tzinfo is None:
        smoke_dt = smoke_dt.replace(tzinfo=timezone.utc)
    mtimes = [os.path.getmtime(os.path.join(svg_dir, s)) for s in REQUIRED_SHEETS if os.path.exists(os.path.join(svg_dir, s))]
    if not mtimes:
        return None
    latest = datetime.fromtimestamp(max(mtimes), tz=timezone.utc)
    if smoke_dt < latest:
        return (
            f"STALE_SMOKE_REPORT: generated_at {generated!r} is older than latest SVG mtime "
            f"{latest.isoformat()!r} — re-run visual_svg_smoke_test.py"
        )
    return None


def _load_smoke(report_dir: str, svg_dir: str) -> tuple[bool, list[str], list[str]]:
    """Visual-smoke verdict: (approved, failures, warnings), including the freshness check."""
    path = os.path.join(report_dir, "visual-smoke-report.json")
    if not os.path.exists(path):
        return True, [], []
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        return False, [f"Failed to load visual-smoke-report.json: {err}"], []
    approved = bool(data.get("may_claim_success"))
    failures = list(data.get("overall_failures", []))
    stale = _smoke_is_stale(data, svg_dir) if approved else None
    if stale:
        approved = False
        failures.append(stale)
    return approved, failures, list(data.get("overall_warnings", []))


def _review_sheet(svg_path: str, model_path: str, content_report_path: str, append: bool) -> tuple[dict, bool]:
    """Runs both peer validators on one SVG; returns (report entry, passed)."""
    status, failure_codes, fixes = "PASS", [], []
    print(f"\n  Reviewing: {svg_path}")

    xml_ok, xml_out = _run_validator("svg_validator.py", svg_path, model_path)
    print(f"    svg_validator: {'PASS' if xml_ok else 'FAIL'}")
    if xml_out:
        print(f"    {xml_out}")
    if not xml_ok:
        failure_codes.append("SVG_XML_INVALID")
        fixes.append("Fix XML well-formedness errors reported by svg_validator.py.")
        status = "FAIL"

    content_ok, content_out = _run_content_validator_with_json(svg_path, model_path, content_report_path, append=append)
    print(f"    content_validator: {'PASS' if content_ok else 'FAIL'}")
    for line in content_out.splitlines():
        print(f"    {line}")
    if not content_ok:
        status = "FAIL"
        for line in content_out.splitlines():
            match = re.match(r"\s*✗\s*(SVG_[A-Z_]+):", line)
            if match:
                failure_codes.append(match.group(1))
                fixes.append(line.strip().lstrip("✗ "))

    entry = {
        "file": svg_path,
        "status": status,
        "failure_codes": failure_codes,
        "semantic_counts": _count_semantic_roles(svg_path),
        "text_label_count": _count_text_labels(svg_path),
        "assessment": (
            "Passed all deterministic checks — qualitative review still required."
            if status == "PASS"
            else "Failed one or more content-quality checks. See failure_codes."
        ),
        "required_fixes": fixes,
    }
    return entry, status == "PASS"


def _artifact_errors(svg_dir: str, report_dir: str) -> list[str]:
    """Parsed-DXF validation and revision-bound cut-list check for the reviewed package (spec C4)."""
    errors = list(validate_dxf_artifacts(report_dir, svg_dir))
    cut_list = Path(svg_dir) / FABRICATION_SUBDIR / CUT_LIST_FILENAME
    if not cut_list.is_file():
        errors.append(f"MISSING_OUTPUT: {FABRICATION_SUBDIR}/{CUT_LIST_FILENAME} was not generated.")
    else:
        errors.extend(check_revision_binding(Path(report_dir) / "structure.json", cut_list))
    return errors


def _finalize(report: dict, overall_pass: bool, missing_sheets: list[str], smoke: tuple, artifact_errors: list[str]) -> None:
    """Sets status, summary and may_claim_success from the collected verdicts."""
    smoke_ok, smoke_failures, smoke_warnings = smoke
    report["overall_required_fixes"].extend(f"Visual smoke test failure: {m}" for m in smoke_failures if not smoke_ok)
    report["overall_required_fixes"].extend(artifact_errors)
    if overall_pass and smoke_ok and not artifact_errors:
        report["status"], report["may_claim_success"] = "PASS", True
        report["summary"] = (
            "All SVG sheets passed deterministic machine validation, sheet-specific "
            "content-quality checks, and headless browser visual smoke heuristics, and the parsed DXF "
            "sheets and fabrication cut list match the reviewed revision. "
            "This executable red-team gate approves may_claim_success. "
            "Optional human or LLM qualitative review may still be performed for additional assurance."
        )
    elif missing_sheets:
        report["status"], report["may_claim_success"] = "BLOCKED", False
        report["summary"] = f"Package is BLOCKED: {len(missing_sheets)} required sheet(s) missing."
    else:
        report["status"], report["may_claim_success"] = "FAIL", False
        failed = [e["file"] for e in report["files"] if e["status"] == "FAIL"]
        if not smoke_ok:
            failed.append("visual-smoke-heuristics")
        failed.extend(f"artifact:{e.split(':')[0]}" for e in artifact_errors)
        report["summary"] = (
            f"FAIL — {len(failed)} sheet(s) or validation layers failed content/visual validation. "
            "These drawings are not builder-meaningful. Regenerate before claiming PASS."
        )
    if smoke_warnings:
        report.setdefault("overall_warnings", []).extend(smoke_warnings)


def _preflight(svg_dir: str, model_path: str, report_dir: str, paths: tuple[str, str]) -> tuple[dict, Optional[dict]]:
    """Identity plus the first BLOCKED report any pre-review gate produces (or None)."""
    identity = _identity(model_path)
    missing = _missing_staging_artifacts(report_dir)
    if missing:
        summary = f"BLOCKED: {len(missing)} required staging artifact(s) missing. Run the full structural pipeline before the drawing red-team gate."
        return identity, _blocked(identity, "MISSING_STAGING_ARTIFACT", summary, [f"Missing: {a}" for a in missing], paths)
    if not identity["revision_id"] or not identity.get("stored_hash_matches", False):
        why = "meta.revision_id is missing" if not identity["revision_id"] else "meta.revision_hash does not match the structure bytes"
        code = "MISSING_REVISION_IDENTITY" if not identity["revision_id"] else "REVISION_HASH_MISMATCH"
        return identity, _blocked(identity, code, f"BLOCKED: {why}; stamp the revision through the transaction authority first.", [why], paths)
    stale = _stale_source_hashes(report_dir)
    if stale:
        summary = f"BLOCKED: {len(stale)} staging artifact(s) carry a stale source_hash. Re-run the structural pipeline so all reports are derived from the same model."
        return identity, _blocked(identity, "SOURCE_HASH_MISMATCH", summary, stale, paths)
    if not glob.glob(os.path.join(svg_dir, "*.svg")):
        return identity, _blocked(identity, "NO_SVG_FILES", f"No SVG files found in '{svg_dir}'. Cannot review.", ["Generate SVG drawings before running red-team review."], paths)
    return identity, None


def run_review(
    svg_dir: str,
    model_path: str,
    report_dir: str,
    md_dir: str,
) -> dict:
    """
    Enumerate SVGs, run validators, build and write the red-team report.

    Returns the report dict.
    """
    content_report_path = os.path.join(report_dir, "drawing-content-report.json")
    paths = (os.path.join(report_dir, "drawing-red-team-report.json"), os.path.join(md_dir, "drawing-red-team-report.md"))

    identity, blocked = _preflight(svg_dir, model_path, report_dir, paths)
    if blocked is not None:
        print(f"  BLOCKED: {blocked['summary']}")
        return blocked

    svg_files = sorted(glob.glob(os.path.join(svg_dir, "*.svg")))
    present = {os.path.basename(f) for f in svg_files}
    missing_sheets = [s for s in REQUIRED_SHEETS if s not in present]
    report: dict = {
        "schema": SCHEMA,
        "generated": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "reviewer": REVIEWER,
        **{k: identity[k] for k in ("revision_id", "revision_hash", "hash_algorithm")},
        "summary": "",
        "files": [],
        "overall_required_fixes": [f"Missing required sheets: {', '.join(missing_sheets)}"] if missing_sheets else [],
        "may_claim_success": False,  # Starts false; only true if all pass
    }
    if missing_sheets:
        report["status"] = "BLOCKED"

    overall_pass = not missing_sheets
    for index, svg_path in enumerate(svg_files):
        entry, passed = _review_sheet(svg_path, model_path, content_report_path, append=index > 0)
        report["files"].append(entry)
        overall_pass = overall_pass and passed

    _finalize(report, overall_pass, missing_sheets, _load_smoke(report_dir, svg_dir), _artifact_errors(svg_dir, report_dir))
    _write_json_report(report, paths[0])
    _write_md_report(report, paths[1])

    print(f"\n  → Red-team report: {paths[0]}")
    print(f"  → Red-team MD:     {paths[1]}")
    print(f"  → may_claim_success: {report['may_claim_success']}")
    return report


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entrypoint: run the red-team gate and exit 0 only when may_claim_success is true."""
    parser = argparse.ArgumentParser(
        description="Run the adversarial drawing red-team gate for garden-structure-designer."
    )
    parser.add_argument(
        "--svg-dir",
        default=str(_OUTPUTS),
        help="Directory containing generated SVG files (default: outputs/<project>).",
    )
    parser.add_argument(
        "--model",
        default=str(_STAGING / "structure.json"),
        help="Path to structure.json.",
    )
    parser.add_argument(
        "--report-dir",
        default=str(_STAGING),
        help="Directory to write JSON reports.",
    )
    parser.add_argument(
        "--md-dir",
        default=str(_OUTPUTS),
        help="Directory to write the Markdown red-team report.",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  ADVERSARIAL DRAWING RED-TEAM GATE")
    print("=" * 60)
    print(f"  SVG dir:    {args.svg_dir}")
    print(f"  Model:      {args.model}")
    print(f"  Report dir: {args.report_dir}")

    report = run_review(args.svg_dir, args.model, args.report_dir, args.md_dir)

    print()
    print("=" * 60)
    print(f"  RESULT: {report['status']}")
    print(f"  may_claim_success: {report['may_claim_success']}")
    print("=" * 60)

    sys.exit(0 if report["may_claim_success"] else 1)


if __name__ == "__main__":
    main()
