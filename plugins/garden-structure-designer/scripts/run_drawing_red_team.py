#!/usr/bin/env python3
"""
run_drawing_red_team.py (CLI)
=====================================

Purpose:
    run_drawing_red_team.py =====================================

Layer: Execution

Usage Examples:
    python run_drawing_red_team.py [args]

Supported Object Types:
    JSON, SVG, Markdown

CLI Arguments:
    Varies per script, typically input file paths.

Input Files:
    context/staging/ *.json outputs/ *.svg

Output:
    Validation codes (0 or 1), generated JSON or SVG files.

Key Functions:
    Refer to module docstring or inner functions.

Script Dependencies:
    Standard library json, os, sys, math, hashlib, etc.

Consumed by:
    design-orchestrator, various skills in the pipeline.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REVIEWER = "run_drawing_red_team.py"

# Resolve canonical staging dir via path_utils (CWD-agnostic)
sys.path.insert(0, str(SCRIPT_DIR))
try:
    from path_utils import staging_dir as _staging_dir
    _STAGING = _staging_dir()
except Exception:
    _STAGING = Path("plugins/garden-structure-designer/context/staging")

# Sheets that MUST exist for a complete package
REQUIRED_SHEETS = [
    "blueprint-plan.svg",
    "blueprint-elevation.svg",
    "blueprint-isometric.svg",
    "blueprint-component-isolation.svg",
    "drawing-plan-view.svg",
    "drawing-elevation-view.svg",
    "drawing-isometric-view.svg",
    "drawing-perspective-view.svg",
]




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
    import re
    roles = ["post", "beam", "rafter", "brace", "footing", "dimension", "component", "title-block"]
    try:
        raw = Path(svg_path).read_text(encoding="utf-8")
        return {role: len(re.findall(rf'data-role="{role}"', raw)) for role in roles}
    except OSError:
        return {role: 0 for role in roles}


def _count_text_labels(svg_path: str) -> int:
    import re
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
    os.makedirs(os.path.dirname(report_path) or ".", exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


def _write_md_report(report: dict, md_path: str) -> None:
    status = report["status"]
    may_claim = report.get("may_claim_success", False)
    summary = report.get("summary", "")

    lines = [
        "# Drawing Red-Team Review Report",
        "",
        f"**Status:** {status}  ",
        f"**May claim success:** {str(may_claim).lower()}  ",
        f"**Reviewer:** {report.get('reviewer', REVIEWER)}  ",
        f"**Generated:** {report.get('generated', '')}  ",
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
        lines.append(f"- Text labels: {entry.get('text_label_count', 0)}")
        lines.append(f"- Total elements: {entry.get('total_elements', 0)}")
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
    red_team_report_path = os.path.join(report_dir, "drawing-red-team-report.json")
    md_report_path = os.path.join(md_dir, "drawing-red-team-report.md")

    # --- Pre-flight: check required deterministic staging artifacts ---
    required_staging_artifacts = [
        str(Path(report_dir) / "structure.json"),
        str(Path(report_dir) / "schema-validation-report.json"),
        str(Path(report_dir) / "physics-validation-report.json"),
    ]
    missing_artifacts = [
        a for a in required_staging_artifacts if not os.path.exists(a)
    ]
    if missing_artifacts:
        report = {
            "schema": "garden-structure-designer/drawing-red-team-report/1.0",
            "generated": datetime.now(timezone.utc).isoformat(),
            "status": "BLOCKED",
            "reviewer": REVIEWER,
            "summary": (
                f"BLOCKED: {len(missing_artifacts)} required staging artifact(s) missing. "
                "Run the full structural pipeline before the drawing red-team gate."
            ),
            "files": [],
            "overall_required_fixes": [
                f"Missing: {a}" for a in missing_artifacts
            ],
            "may_claim_success": False,
        }
        _write_json_report(report, red_team_report_path)
        _write_md_report(report, md_report_path)
        print(f"  BLOCKED: missing staging artifacts: {missing_artifacts}")
        return report

    # Collect SVG files
    svg_files = sorted(glob.glob(os.path.join(svg_dir, "*.svg")))
    if not svg_files:
        report = {
            "schema": "garden-structure-designer/drawing-red-team-report/1.0",
            "generated": datetime.now(timezone.utc).isoformat(),
            "status": "BLOCKED",
            "reviewer": REVIEWER,
            "summary": f"No SVG files found in '{svg_dir}'. Cannot review.",
            "files": [],
            "overall_required_fixes": ["Generate SVG drawings before running red-team review."],
            "may_claim_success": False,
        }
        _write_json_report(report, red_team_report_path)
        _write_md_report(report, md_report_path)
        return report

    # Check for required sheets
    present_names = {os.path.basename(f) for f in svg_files}
    missing_sheets = [s for s in REQUIRED_SHEETS if s not in present_names]

    report: dict = {
        "schema": "garden-structure-designer/drawing-red-team-report/1.0",
        "generated": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "reviewer": REVIEWER,
        "summary": "",
        "files": [],
        "overall_required_fixes": [],
        "may_claim_success": False,  # Starts false; only true if all pass
    }

    if missing_sheets:
        report["status"] = "BLOCKED"
        report["overall_required_fixes"].append(
            f"Missing required sheets: {', '.join(missing_sheets)}"
        )

    overall_pass = not missing_sheets
    first_append = True  # For content-report accumulation

    for svg_path in svg_files:
        sheet_status = "PASS"
        failure_codes: list[str] = []
        required_fixes: list[str] = []

        print(f"\n  Reviewing: {svg_path}")

        # Run svg_validator.py
        xml_ok, xml_out = _run_validator("svg_validator.py", svg_path, model_path)
        print(f"    svg_validator: {'PASS' if xml_ok else 'FAIL'}")
        if xml_out:
            print(f"    {xml_out}")
        if not xml_ok:
            failure_codes.append("SVG_XML_INVALID")
            required_fixes.append("Fix XML well-formedness errors reported by svg_validator.py.")
            sheet_status = "FAIL"
            overall_pass = False

        # Run drawing_content_validator.py (with JSON accumulation)
        content_ok, content_out = _run_content_validator_with_json(
            svg_path, model_path, content_report_path, append=not first_append
        )
        first_append = False
        print(f"    content_validator: {'PASS' if content_ok else 'FAIL'}")
        if content_out:
            for line in content_out.splitlines():
                print(f"    {line}")
        if not content_ok:
            sheet_status = "FAIL"
            overall_pass = False
            # Extract failure codes from output lines
            import re
            for line in content_out.splitlines():
                m = re.match(r"\s*✗\s*(SVG_[A-Z_]+):", line)
                if m:
                    failure_codes.append(m.group(1))
                    required_fixes.append(line.strip().lstrip("✗ "))

        # Direct semantic counts
        roles = _count_semantic_roles(svg_path)
        text_count = _count_text_labels(svg_path)

        report["files"].append({
            "file": svg_path,
            "status": sheet_status,
            "failure_codes": failure_codes,
            "semantic_counts": roles,
            "text_label_count": text_count,
            "assessment": (
                "Passed all deterministic checks — qualitative review still required."
                if sheet_status == "PASS"
                else "Failed one or more content-quality checks. See failure_codes."
            ),
            "required_fixes": required_fixes,
        })

    # Determine final status
    if overall_pass and not missing_sheets:
        report["status"] = "PASS"
        report["may_claim_success"] = True
        report["summary"] = (
            "All SVG sheets passed deterministic machine validation and sheet-specific "
            "content-quality checks. This executable red-team gate approves may_claim_success. "
            "Optional human or LLM qualitative review may still be performed for additional assurance."
        )
    elif missing_sheets:
        report["status"] = "BLOCKED"
        report["may_claim_success"] = False
        report["summary"] = (
            f"Package is BLOCKED: {len(missing_sheets)} required sheet(s) missing."
        )
    else:
        report["status"] = "FAIL"
        report["may_claim_success"] = False
        failed = [e["file"] for e in report["files"] if e["status"] == "FAIL"]
        report["summary"] = (
            f"FAIL — {len(failed)} of {len(svg_files)} sheet(s) failed content validation. "
            "These drawings are not builder-meaningful. Regenerate before claiming PASS."
        )

    _write_json_report(report, red_team_report_path)
    _write_md_report(report, md_report_path)

    print(f"\n  → Red-team report: {red_team_report_path}")
    print(f"  → Red-team MD:     {md_report_path}")
    print(f"  → may_claim_success: {report['may_claim_success']}")

    return report


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the adversarial drawing red-team gate for garden-structure-designer."
    )
    parser.add_argument(
        "--svg-dir",
        default="outputs",
        help="Directory containing generated SVG files (default: outputs).",
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
        default="outputs",
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
