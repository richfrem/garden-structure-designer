#!/usr/bin/env python3
"""
run_obstacle_triage.py
======================

Purpose:
    Classifies why a design run is blocked and recommends the next action, writing
    ``context/staging/obstacle-triage-report.json`` and ``outputs/obstacle-triage-report.md``.
    Detected obstacles: PATH_SPLIT (structure.json in both the root staging directory and the
    legacy plugin staging directory), RECOVERY_REQUIRED (a C5 journal stuck in COMMITTING),
    MISSING_STAGING_ARTIFACT, DASHBOARD_STALE_OR_WRONG_PATH, STALE_APPROVAL (a red-team approval
    bound to another revision), RENDERER_PLACEHOLDER_OUTPUT (tiny SVG stubs), else UNKNOWN_OBSTACLE.
    The report never claims PASS and forbids weakening validators or compiling the PDF.

Layer: Execution / Diagnostics

Key Input Dependencies:
    - context/staging/ (structure.json, drawing-red-team-report.json, journal/*.json)
    - outputs/ (quality-dashboard.md, *.svg)
    - path_utils.py, revision_identity.py

Key Functions:
    main() -> None
    _detect_path_split() -> tuple[bool, str | None]      _detect_recovery(staging) -> bool
    _detect_stale_approval(staging) -> bool              _detect_placeholder_svgs(outputs) -> bool
    _classify() -> tuple[list[str], list[str], bool]     _next_action(classifications) -> str
    _build_report(...) -> dict                           _render_markdown(report) -> str

Usage Examples:
    python3 run_obstacle_triage.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Optional

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import outputs_dir, plugin_root, staging_dir
from revision_identity import compute_revision_hash, verify_receipt_binding

PLACEHOLDER_SVG_MAX_BYTES = 3000
DO_NOT_DO = ["Do not weaken validators", "Do not claim PASS", "Do not compile PDF"]
NEXT_ACTIONS = (  # first matching classification wins
    ("PATH_SPLIT", "FIX_PATHS_FIRST"),
    ("RECOVERY_REQUIRED", "RUN_RECOVERY_FIRST"),
    ("MISSING_STAGING_ARTIFACT", "RERUN_REPORTS_FIRST"),
    ("DASHBOARD_STALE_OR_WRONG_PATH", "RERUN_REPORTS_FIRST"),
    ("STALE_APPROVAL", "RERUN_REPORTS_FIRST"),
    ("RENDERER_PLACEHOLDER_OUTPUT", "FIX_RENDERER_FIRST"),
)


def _load_json(path: Path) -> Optional[dict]:
    """Parsed JSON, or None when the file is absent or malformed."""
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def _detect_path_split() -> tuple[bool, Optional[str]]:
    """True (plus the legacy path) when structure.json exists in both the root and the legacy plugin staging dirs."""
    legacy, root = plugin_root() / "context" / "staging", staging_dir()
    split = (
        legacy.exists() and root.exists() and legacy.resolve() != root.resolve()
        and (legacy / "structure.json").exists() and (root / "structure.json").exists()
    )
    return split, str(legacy) if split else None


def _detect_recovery(staging: Path) -> bool:
    """True when a C5 transaction journal is stuck in COMMITTING (run structure_io.recover_journals first)."""
    return any((_load_json(j) or {}).get("state") == "COMMITTING" for j in (staging / "journal").glob("*.json"))


def _red_team_approval(staging: Path) -> Optional[dict]:
    """The red-team report when it claims success, else None."""
    report = _load_json(staging / "drawing-red-team-report.json")
    return report if report and report.get("may_claim_success") else None


def _detect_stale_approval(staging: Path) -> bool:
    """True when an approving red-team report is not bound to the current structure.json revision."""
    approval, structure = _red_team_approval(staging), _load_json(staging / "structure.json")
    if approval is None or structure is None:
        return False
    meta = structure.get("meta") or {}
    return not verify_receipt_binding(approval, meta.get("revision_id"), compute_revision_hash(structure))


def _detect_placeholder_svgs(outputs: Path) -> bool:
    """True when any generated SVG is a tiny placeholder stub."""
    return any(svg.stat().st_size < PLACEHOLDER_SVG_MAX_BYTES for svg in outputs.glob("*.svg"))


def _classify() -> tuple[list[str], list[str], Optional[str]]:
    """(classifications, evidence, legacy staging path when split)."""
    staging, outputs = staging_dir(), outputs_dir()
    classifications: list[str] = []
    evidence: list[str] = []

    split, legacy = _detect_path_split()
    if split:
        classifications.append("PATH_SPLIT")
        evidence.append("structure.json found in both context/staging and plugin staging")
    if _detect_recovery(staging):
        classifications.append("RECOVERY_REQUIRED")
        evidence.append("a transaction journal is in state COMMITTING; run structure_io.recover_journals before anything else")

    missing = not (staging / "structure.json").exists()
    if missing:
        classifications.append("MISSING_STAGING_ARTIFACT")
        evidence.append(f"Missing staging artifacts in {staging}: structure.json")

    red_team = staging / "drawing-red-team-report.json"
    approved = _red_team_approval(staging) is not None
    dashboard = outputs / "quality-dashboard.md"
    if dashboard.exists() and not approved and "Overall status: COMPLETED" in dashboard.read_text():
        classifications.append("DASHBOARD_STALE_OR_WRONG_PATH")
        evidence.append("quality-dashboard.md says COMPLETED while red-team report does not approve (or is missing)")
    if _detect_stale_approval(staging):
        classifications.append("STALE_APPROVAL")
        evidence.append("drawing-red-team-report.json approves a different revision than structure.json")
    if not missing and red_team.exists() and not approved and _detect_placeholder_svgs(outputs):
        classifications.append("RENDERER_PLACEHOLDER_OUTPUT")
        evidence.append("Generated SVGs are extremely small (likely placeholder stubs)")

    if not classifications:
        classifications.append("UNKNOWN_OBSTACLE")
        evidence.append("No specific obstacle pattern matched")
    return classifications, evidence, legacy


def _next_action(classifications: list[str]) -> str:
    """Recommended next action for the highest-priority classification (BLOCK_AND_REPORT otherwise)."""
    return next((action for code, action in NEXT_ACTIONS if code in classifications), "BLOCK_AND_REPORT")


def _build_report(classifications: list[str], evidence: list[str], legacy: Optional[str]) -> dict:
    """Assembles the triage report dict."""
    return {
        "schema": "garden-structure-designer/obstacle-triage-report/1.0",
        "status": "ACTION_REQUIRED",
        "failure_classification": classifications,
        "active_staging_path": str(staging_dir()),
        "conflicting_staging_paths": [legacy] if legacy else [],
        "evidence": evidence,
        "recommended_next_action": _next_action(classifications),
        "do_not_do": list(DO_NOT_DO),
    }


def _render_markdown(report: dict) -> str:
    """Markdown rendering of the triage report."""
    lines = ["# Obstacle Triage Report", "", f"**Status:** {report['status']}",
             f"**Recommended Next Action:** `{report['recommended_next_action']}`", "", "## Failure Classifications"]
    lines += [f"- **{c}**" for c in report["failure_classification"]]
    lines += ["", "## Evidence"] + [f"- {e}" for e in report["evidence"]]
    lines += ["", "## Constraints"] + [f"- 🛑 {d}" for d in report["do_not_do"]]
    return "\n".join(lines) + "\n"


def main() -> None:
    """CLI entrypoint: classify the obstacle, write the JSON and Markdown reports, print the recommendation."""
    classifications, evidence, legacy = _classify()
    report = _build_report(classifications, evidence, legacy)

    os.makedirs(str(staging_dir()), exist_ok=True)
    with open(staging_dir() / "obstacle-triage-report.json", "w") as f:
        json.dump(report, f, indent=2)
    os.makedirs(str(outputs_dir()), exist_ok=True)
    with open(outputs_dir() / "obstacle-triage-report.md", "w") as f:
        f.write(_render_markdown(report))

    print(f"Obstacle triage complete. Action required: {report['recommended_next_action']}")
    for c in classifications:
        print(f" - {c}")


if __name__ == "__main__":
    main()
