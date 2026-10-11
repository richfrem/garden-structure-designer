#!/usr/bin/env python3
"""
repair_orchestrator.py
======================

Purpose:
    Self-healing loop driver. Reads a drift report, classifies each failed axis (error_classifier),
    and either blocks it (human review required, non-retryable structured error, sealed geometry,
    repeated failures, no repair action) or runs the mapped repair command and re-runs the matching
    validator. Writes ``context/staging/repair-report.json`` (status PASS / FAIL / BLOCKED). Repairs
    that rewrite structure.json must go through the C5 transaction authority (structure_io); sealed
    geometry is never overwritten.

Layer: Execution / Self-Healing

Key Input Dependencies:
    - context/staging/drift_report.json (failed_axes or failures)
    - plugins/garden-structure-designer/repair-map.json (axis -> {action})
    - context/staging/structure.json (geometry._sealed lock)
    - error_classifier.py, run_history.py, path_utils.py; validators it re-runs:
      svg_validator.py, schema_validator.py, package_consistency_validator.py, cross_artifact_validator.py

Key Functions:
    main(argv=None) -> None
    load_json(path) -> dict                         save_json(data, path) -> None
    _failed_axes(drift_report) -> list[str]         _is_locked(model_path) -> bool
    _resolve_action(axis, stage, repair_map, model_path) -> str | None
    _validation_command(stage, model_path) -> list[str] | None
    _run_validation(stage, model_path) -> str       _repair_axis(axis, cls, ctx) -> tuple[dict | None, str]

Usage Examples:
    python3 repair_orchestrator.py [drift_report.json] [repair-map.json] [--max-attempts 2]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

# Add path_utils
sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir, plugin_root, scripts_dir, outputs_dir
from error_classifier import classify_failure
from run_history import should_halt, record_run


def load_json(path) -> Any:
    """Reads a JSON file."""
    with open(path) as f: return json.load(f)


def save_json(data, path) -> None:
    """Writes ``data`` as indented JSON."""
    with open(path, 'w') as f: json.dump(data, f, indent=2)


def _failed_axes(drift_report: dict) -> list[str]:
    """Failed axes from either report shape: ``failed_axes`` or a ``failures`` list of dicts/strings."""
    axes = drift_report.get("failed_axes", [])
    if not axes and "failures" in drift_report:
        axes = [f.get("axis") or f.get("classification") or str(f) for f in drift_report["failures"]]
    return axes


def _is_locked(model_path: Path) -> bool:
    """True when structure.json has sealed geometry or members (structural repairs must not overwrite it)."""
    if not model_path.exists():
        return False
    model = load_json(model_path)
    return bool(model.get("geometry", {}).get("_sealed") or model.get("members", {}).get("_sealed"))


def _resolve_action(axis: str, stage: str, repair_map: dict, model_path: Path) -> Optional[str]:
    """Repair command for an axis: the repair-map entry, else a stage default, else None (no automatic repair)."""
    action = repair_map.get(axis, {}).get("action")
    if action:
        return action
    if stage == "drawing-generator":
        return f"python3 {scripts_dir()}/render_drawings.py {model_path}"
    if stage == "structural-engine":
        return f"python3 {scripts_dir()}/geometry_engine.py {model_path}"
    return None


def _validation_command(stage: str, model_path: Path) -> Optional[list[str]]:
    """The validator to re-run after a repair at ``stage`` (None when the stage has no validator)."""
    script = lambda name: str(scripts_dir() / name)  # noqa: E731
    commands = {
        "drawing-generator": [sys.executable, script("svg_validator.py"), str(outputs_dir() / "drawing-plan-view.svg"), str(model_path)],
        "structural-engine": [sys.executable, script("schema_validator.py")],
        "package": [sys.executable, script("package_consistency_validator.py")],
        "cross-artifact": [sys.executable, script("cross_artifact_validator.py")],
    }
    return commands.get(stage)


def _run_validation(stage: str, model_path: Path) -> str:
    """PASS/FAIL of the stage validator (callers only invoke it after a successful repair command)."""
    command = _validation_command(stage, model_path)
    if command is None:
        return "PASS"
    return "PASS" if subprocess.run(command, capture_output=True, text=True).returncode == 0 else "FAIL"


def _repair_axis(axis: str, cls: dict, ctx: dict) -> tuple[Optional[dict], str]:
    """Attempts one axis; returns (attempt record or None, outcome) with outcome in BLOCKED / PASS / FAIL."""
    stage = cls["repair_stage"]
    if cls["requires_human_review"] or not cls["retryable"]:
        return None, "BLOCKED"
    if stage == "structural-engine" and ctx["locked"]:
        return None, "BLOCKED"
    action = _resolve_action(axis, stage, ctx["repair_map"], ctx["model_path"])
    if not action:
        return None, "BLOCKED"
    script_name = action.split()[1].split('/')[-1]
    if should_halt(script_name, cls["classification"], ctx["max_attempts"]):
        return None, "BLOCKED"

    cmd_args = action.split()
    result = subprocess.run(cmd_args, capture_output=True, text=True)
    record_run(script_name, cmd_args[1:], result.returncode, cls["classification"])
    status = _run_validation(stage, ctx["model_path"]) if result.returncode == 0 else "FAIL"
    attempt = {"attempt": 1, "failure_axis": axis, "repair_stage": stage, "commands": [action], "validation_status": status}
    return attempt, status


def main(argv: Optional[list[str]] = None) -> None:
    """CLI entrypoint: repair every failed axis of the drift report and write repair-report.json."""
    parser = argparse.ArgumentParser()
    parser.add_argument("drift_report", nargs="?", default=str(staging_dir() / "drift_report.json"), type=str)
    parser.add_argument("repair_map", nargs="?", default=str(plugin_root() / "repair-map.json"), type=str)
    parser.add_argument("--max-attempts", type=int, default=2)
    args = parser.parse_args(argv)

    drift_report_path = Path(args.drift_report)
    if not drift_report_path.exists():
        print("No drift report found.")
        sys.exit(0)

    report = {
        "schema": "garden-structure-designer/repair-report/1.0",
        "status": "PASS",
        "attempts": [],
        "remaining_failures": []
    }
    axes = _failed_axes(load_json(drift_report_path))
    if not axes:
        print("No failures reported.")
        save_json(report, staging_dir() / "repair-report.json")
        sys.exit(0)

    model_path = staging_dir() / "structure.json"
    ctx = {
        "repair_map": load_json(Path(args.repair_map)),
        "model_path": model_path,
        "locked": _is_locked(model_path),
        "max_attempts": args.max_attempts,
    }
    for axis in axes:
        attempt, outcome = _repair_axis(axis, classify_failure(axis), ctx)
        if attempt:
            report["attempts"].append(attempt)
        if outcome != "PASS":
            report["remaining_failures"].append(axis)
            report["status"] = outcome

    save_json(report, staging_dir() / "repair-report.json")
    print(f"Repair complete. Status: {report['status']}")


if __name__ == "__main__":
    main()
