#!/usr/bin/env python3
"""
generate_quality_dashboard.py
=============================

Purpose:
    Builds ``outputs/quality-dashboard.md`` and ``outputs/run-insights.json`` from the staging reports
    (repair, physics, drift, drawing content, drawing red-team, learning and evidence registries).
    Overall status is COMPLETED only when nothing is open AND the red-team approval is bound to the
    current ``structure.json`` revision; an approval for another revision yields
    "BLOCKED / FAILED (STALE_APPROVAL)". Both outputs are derived artifacts (purged by every C5 commit).

Layer: Execution / Reporting

Key Input Dependencies:
    - context/staging/{repair-report,physics-validation-report,drift_report,drawing-content-report,
      drawing-red-team-report,learning-registry,evidence-registry}.json, structure.json
    - path_utils.py, revision_identity.py

Key Functions:
    safe_load(path, default=None) -> dict
    main() -> None
    _overall_status(repair, drift, content, red_team, approval_is_current, structure_exists) -> str
    _approval_is_current(red_team, structure) -> bool
    _content_sheet_lines(content_report) -> str        _physics_lines(physics) -> str
    _render_dashboard(...) -> str

Usage Examples:
    python3 generate_quality_dashboard.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import outputs_dir, staging_dir
from revision_identity import compute_revision_hash, verify_receipt_binding


def safe_load(path, default=None) -> dict:
    """Loads a JSON file; returns ``default`` ({} if None) when it is absent or malformed."""
    if default is None: default = {}
    p = Path(path)
    if p.exists():
        try:
            with open(p) as f: return json.load(f)
        except Exception:
            return default
    return default


def _approval_is_current(red_team: dict, structure: dict) -> bool:
    """True when the red-team report is bound to the revision of ``structure``."""
    meta = structure.get("meta") or {}
    return bool(structure) and verify_receipt_binding(red_team, meta.get("revision_id"), compute_revision_hash(structure))


def _overall_status(repair: dict, drift: dict, content: dict, red_team: dict, approval_is_current: bool, structure_exists: bool) -> str:
    """COMPLETED / PARTIAL / BLOCKED status label for the run."""
    if repair.get("status") in ["FAIL", "BLOCKED"] or drift.get("failed_axes"):
        return "BLOCKED / FAILED"
    content_status = content.get("status") or "MISSING"
    red_team_status = red_team.get("status") or "MISSING"
    status = "COMPLETED"
    if content_status == "MISSING" or red_team_status == "MISSING":
        status = "PARTIAL — drawing reports missing"
    if content_status == "FAIL" or not red_team.get("may_claim_success") or not structure_exists:
        status = "BLOCKED / FAILED (DASHBOARD_STALE_OR_WRONG_PATH)"
    elif status == "COMPLETED" and not approval_is_current:
        status = "BLOCKED / FAILED (STALE_APPROVAL)"
    return status


def _content_sheet_lines(content_report: dict) -> str:
    """Per-sheet content validation summary lines."""
    files = content_report.get("files", [])
    if not files:
        return "- No content-validation report found. Run run_drawing_red_team.py."
    rows = []
    for cf in files:
        icon = "✅" if cf.get("status") == "PASS" else "❌"
        codes = ", ".join(cf.get("failure_codes", [])) or "none"
        rows.append(f"- {icon} `{cf['file']}`: {cf.get('status') or '?'} — codes: {codes}")
    return "\n".join(rows)


def _physics_lines(physics: dict) -> str:
    """Physics check lines, or a placeholder when none ran."""
    lines = "\n".join([f"- {c['name']}: {c['status']} (Val: {c['value']}, Lim: {c['limit']})" for c in physics.get("checks", [])])
    return lines or "- No checks executed."


def _render_dashboard(ctx: dict) -> str:
    """Renders the dashboard markdown from the collected report context."""
    repair, evidence, drift, learning = ctx["repair"], ctx["evidence"], ctx["drift"], ctx["learning"]
    red_team, meta = ctx["red_team"], ctx["meta"]
    may_claim = str(bool(red_team.get("may_claim_success"))).lower()
    repair_str = "None"
    if repair.get("attempts"):
        repair_str = "\n".join([f"- Attempt {a['attempt']}: {a['repair_stage']} for {a['failure_axis']} -> {a['validation_status']}" for a in repair["attempts"]])
    ev_str = "None"
    if evidence.get("evidence"):
        ev_str = "\n".join([f"- {e['evidence_id']}: {e['claim']} -> {e['artifact']}" for e in evidence["evidence"]])
    summary_desc = red_team.get("summary") or "No red-team report found. Run run_drawing_red_team.py before claiming PASS."

    return f"""# Garden Structure Designer Quality Dashboard

## Run Status
- Overall status: {ctx['overall']}
- Revision: {meta.get('revision_id') or 'Unknown'} ({meta.get('revision_hash') or 'Unknown'})
- Physics status: {ctx['physics'].get("status") or "UNKNOWN"}
- Drawing content validation: {ctx['content'].get("status") or "MISSING"}
- Drawing red-team review: {red_team.get("status") or "MISSING"}
- May claim success: {may_claim}
- Last updated: Auto-generated

## Drawing Red-Team Status
- Reviewer: {red_team.get("reviewer") or "N/A"}
- Status: {red_team.get("status") or "MISSING"}
- May claim success: {may_claim}
- Summary: {summary_desc}

## Drawing Content Validation (Stage 5.75)
{_content_sheet_lines(ctx['content'])}

## Physics Validations
{_physics_lines(ctx['physics'])}

## Repair Attempts
{repair_str}

## Learning / Self-Healing
- Lessons available: {len(learning.get("active_lessons", []))}
- Active failures: {len(drift.get("failed_axes", []))}

## Evidence IDs
{ev_str}
"""


def main() -> None:
    """CLI entrypoint: write quality-dashboard.md and run-insights.json from the staging reports."""
    stage_dir, out_dir = staging_dir(), outputs_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    ctx = {
        "repair": safe_load(stage_dir / "repair-report.json", {"status": "NONE", "attempts": []}),
        "physics": safe_load(stage_dir / "physics-validation-report.json", {"status": "UNKNOWN", "checks": []}),
        "learning": safe_load(stage_dir / "learning-registry.json", {"active_lessons": []}),
        "evidence": safe_load(stage_dir / "evidence-registry.json", {"evidence": []}),
        "drift": safe_load(stage_dir / "drift_report.json", {"failed_axes": []}),
        "red_team": safe_load(stage_dir / "drawing-red-team-report.json", {}),
        "content": safe_load(stage_dir / "drawing-content-report.json", {}),
    }
    structure = safe_load(stage_dir / "structure.json", {})
    ctx["meta"] = structure.get("meta") or {}
    ctx["overall"] = _overall_status(
        ctx["repair"], ctx["drift"], ctx["content"], ctx["red_team"],
        _approval_is_current(ctx["red_team"], structure), (stage_dir / "structure.json").exists(),
    )

    with open(out_dir / "quality-dashboard.md", "w") as f:
        f.write(_render_dashboard(ctx))
    with open(out_dir / "run-insights.json", "w") as f:
        json.dump({"status": ctx["overall"], "physics": ctx["physics"].get("status"), "revision_id": ctx["meta"].get("revision_id")}, f, indent=2)

    print("Dynamic quality dashboard generated.")


if __name__ == "__main__":
    main()
