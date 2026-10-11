#!/usr/bin/env python3
"""
structural_physics_validator.py
===============================

Purpose:
    Stage 3 screening checks on ``structure.json``: post slenderness (L/d <= 50), a beam deflection
    proxy against L/240, and caisson bearing area vs post area. Every structural input is REQUIRED:
    a missing dimension yields status BLOCKED listing the missing fields instead of a result computed
    from invented defaults. The report records the inputs used (provenance) and is bound to the
    structure's ``source_hash`` and revision (``revision_id``/``revision_hash``).

    SCREENING ONLY: the deflection value is a stiffness proxy and the bearing check compares areas.
    These do not replace the jurisdiction-specific design checks (snow/wind loads, member capacity)
    that the spec requires before structural sign-off; see the review tracker (F-20).

Layer: Execution / Stage 3 Structural Physics Gate

Key Input Dependencies:
    - context/staging/structure.json: members.posts (cut_length_ft, actual_width_in, actual_depth_in),
      members.beams (actual_width_in, actual_depth_in), layout.inscribed_radius_ft, footings.diameter_in,
      roof.pitch_defaulted (optional flag), meta.source_hash / revision_id / revision_hash
    - strict_access.py, path_utils.py

Key Functions:
    validate(model) -> dict
    load_json(path) -> dict
    main() -> None
    _required_inputs(model) -> tuple[dict, list[str]]
    _slenderness_check(inputs) -> dict    _deflection_check(inputs) -> dict    _bearing_check(inputs) -> dict
    _combine(statuses) -> str

Usage Examples:
    python3 structural_physics_validator.py [structure.json]    # writes physics-validation-report.json beside it
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.resolve()))
from path_utils import staging_dir
from strict_access import MissingInputError, require_path

SLENDERNESS_LIMIT = 50
SLENDERNESS_WARN = 40
DEFLECTION_DIVISOR = 240
DEFLECTION_STIFFNESS_SCALE = 1000  # screening-proxy scale factor (not an engineering constant)
REQUIRED_PATHS = {
    "post_cut_length_ft": ("members", "posts", "cut_length_ft"),
    "post_width_in": ("members", "posts", "actual_width_in"),
    "post_depth_in": ("members", "posts", "actual_depth_in"),
    "beam_width_in": ("members", "beams", "actual_width_in"),
    "beam_depth_in": ("members", "beams", "actual_depth_in"),
    "span_ft": ("layout", "inscribed_radius_ft"),
    "caisson_diameter_in": ("footings", "diameter_in"),
}
STATUS_ORDER = ("PASS", "WARNING", "FAIL")


def load_json(path) -> dict:
    """Reads a JSON file."""
    with open(path) as f: return json.load(f)


def _required_inputs(model: dict) -> tuple[dict, list[str]]:
    """The numeric screening inputs and the dotted paths of any that are missing (never defaulted)."""
    inputs: dict = {}
    missing: list[str] = []
    for name, path in REQUIRED_PATHS.items():
        try:
            inputs[name] = float(require_path(model, *path))
        except MissingInputError:
            missing.append(".".join(path))
    if not missing:
        inputs["post_length_in"] = inputs["post_cut_length_ft"] * 12.0
        inputs["span_in"] = inputs["span_ft"] * 12.0
    return inputs, missing


def _slenderness_check(inputs: dict) -> dict:
    """L/d <= 50 (WARNING above 40)."""
    value = inputs["post_length_in"] / inputs["post_width_in"]
    status = "FAIL" if value > SLENDERNESS_LIMIT else "WARNING" if value > SLENDERNESS_WARN else "PASS"
    return {"name": "post_slenderness", "status": status, "value": round(value, 1), "limit": SLENDERNESS_LIMIT}


def _deflection_check(inputs: dict) -> dict:
    """Beam deflection stiffness proxy against span/240 (WARNING only; screening, not a design check)."""
    allowable = inputs["span_in"] / DEFLECTION_DIVISOR
    stiffness = (inputs["beam_width_in"] * inputs["beam_depth_in"] ** 3) / 12
    proxy = (inputs["span_in"] ** 3) / (stiffness * DEFLECTION_STIFFNESS_SCALE) if stiffness > 0 else 999
    return {"name": "beam_deflection", "status": "WARNING" if proxy > allowable else "PASS",
            "value": round(proxy, 3), "limit": round(allowable, 3)}


def _bearing_check(inputs: dict) -> dict:
    """Post cross-section must fit within the caisson bearing area."""
    caisson_area = math.pi * (inputs["caisson_diameter_in"] / 2) ** 2
    post_area = inputs["post_width_in"] * inputs["post_depth_in"]
    return {"name": "caisson_bearing", "status": "FAIL" if post_area > caisson_area else "PASS",
            "value": round(post_area, 1), "limit": round(caisson_area, 1)}


def _combine(statuses: list[str]) -> str:
    """Worst of PASS < WARNING < FAIL."""
    return max(statuses, key=STATUS_ORDER.index) if statuses else "PASS"


def validate(model: dict) -> dict:
    """Runs the screening checks and returns the physics report (status BLOCKED when inputs are missing)."""
    meta = model.get("meta") or {}
    report = {
        "schema": "garden-structure-designer/physics-validation/1.2",
        "status": "PASS",
        "disclaimer": "Screening calculation only; not professional engineering certification.",
        "source_hash": meta.get("source_hash"),
        "revision_id": meta.get("revision_id"),
        "revision_hash": meta.get("revision_hash"),
        "checks": [],
        "assumptions": [],
    }
    inputs, missing = _required_inputs(model)
    if missing:
        report.update(status="BLOCKED", missing_inputs=[f"MISSING_INPUT: {path}" for path in missing])
        return report

    report["inputs"] = inputs
    report["checks"] = [_slenderness_check(inputs), _deflection_check(inputs), _bearing_check(inputs)]
    report["status"] = _combine([c["status"] for c in report["checks"]])
    if (model.get("roof") or {}).get("pitch_defaulted"):
        report["assumptions"].append("Pitch was defaulted. Verify snow load capacity.")
        if report["status"] == "PASS":
            report["status"] = "REQUIRES_ENGINEER_REVIEW"
    return report


def main() -> None:
    """CLI entrypoint: validate structure.json, write physics-validation-report.json, exit 1 on FAIL/BLOCKED."""
    model_path = Path(sys.argv[1]) if len(sys.argv) > 1 else (staging_dir() / "structure.json")
    report = validate(load_json(model_path))

    with open(model_path.parent / "physics-validation-report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"Physics validation: {report['status']}")
    print(f"Disclaimer: {report['disclaimer']}")
    for item in report.get("missing_inputs", []):
        print(f"  {item}")
    sys.exit(1 if report["status"] in ("FAIL", "BLOCKED") else 0)


if __name__ == "__main__":
    main()
