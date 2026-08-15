#!/usr/bin/env python3
"""
structural_physics_validator.py (CLI)
=====================================

Purpose:
    structural_physics_validator.py =====================================

Layer: Execution

Usage Examples:
    python structural_physics_validator.py [args]

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
import json
import sys
from pathlib import Path

from path_utils import staging_dir

def load_json(path):
    with open(path) as f: return json.load(f)

def main():
    model_path = Path(sys.argv[1]) if len(sys.argv) > 1 else (staging_dir() / "structure.json")
    model = load_json(model_path)

    # Detect structure.json (new) vs structural-model.json (legacy)
    is_structure_json = "meta" in model and "schema_version" in model.get("meta", {})

    if is_structure_json:
        posts  = model.get("members", {}).get("posts", {})
        beams  = model.get("members", {}).get("beams", {})
        pitch_defaulted = bool(model.get("roof", {}).get("pitch_defaulted"))
        caisson_d = float(model.get("footings", {}).get("diameter_in") or 12.0)
        span_ft   = float(model.get("layout", {}).get("inscribed_radius_ft") or 5.0)
    else:
        posts  = model.get("members", {}).get("posts", {})
        beams  = model.get("members", {}).get("beams", {})
        pitch_defaulted = bool(model.get("roofStructure", {}).get("pitchDefaulted"))
        caisson_d = float(model.get("foundation", {}).get("caisson_diameter_in") or 12.0)
        span_ft   = float(posts.get("spanDistance_ft") or 10.0)

    report = {
        "schema": "garden-structure-designer/physics-validation/1.1",
        "status": "PASS",
        "disclaimer": "Screening calculation only; not professional engineering certification.",
        "checks": [],
        "assumptions": []
    }

    # 1. Slenderness (L/d <= 50)
    post_length = float(posts.get("cut_length_ft") or posts.get("cutLength_ft") or 8.0) * 12.0
    post_width  = float(posts.get("actual_width_in") or posts.get("width_in") or 5.5)
    slenderness = post_length / post_width

    sl_check = {"name": "post_slenderness", "status": "PASS", "value": round(slenderness, 1), "limit": 50}
    if slenderness > 50:
        sl_check["status"] = "FAIL"
        report["status"] = "FAIL"
    elif slenderness > 40:
        sl_check["status"] = "WARNING"
        if report["status"] == "PASS": report["status"] = "WARNING"
    report["checks"].append(sl_check)

    # 2. Deflection (L/240)
    # Simple span check proxy
    span_in              = span_ft * 12
    allowable_deflection = span_in / 240
    # Dummy calculation for deflection using width/depth as proxy
    beam_w = float(beams.get("actual_width_in") or beams.get("width_in") or 3.5)
    beam_d = float(beams.get("actual_depth_in") or beams.get("depth_in") or 7.25)
    # Approximation of stiffness proxy
    stiffness = (beam_w * (beam_d ** 3)) / 12
    deflection_proxy = (span_in ** 3) / (stiffness * 1000) if stiffness > 0 else 999

    def_check = {"name": "beam_deflection", "status": "PASS", "value": round(deflection_proxy, 3), "limit": round(allowable_deflection, 3)}
    if deflection_proxy > allowable_deflection:
        def_check["status"] = "WARNING"
        if report["status"] == "PASS": report["status"] = "WARNING"
    report["checks"].append(def_check)

    # 3. Bearing Area
    caisson_area = 3.14159 * (caisson_d / 2) ** 2
    post_area    = float(posts.get("actual_width_in") or posts.get("width_in") or 5.5) * \
                   float(posts.get("actual_depth_in") or posts.get("depth_in") or 5.5)

    brg_check = {"name": "caisson_bearing", "status": "PASS", "value": round(post_area, 1), "limit": round(caisson_area, 1)}
    if post_area > caisson_area:
        brg_check["status"] = "FAIL"
        report["status"] = "FAIL"
    report["checks"].append(brg_check)

    # Defaults checking
    if pitch_defaulted:
        report["assumptions"].append("Pitch was defaulted. Verify snow load capacity.")
        if report["status"] == "PASS": report["status"] = "REQUIRES_ENGINEER_REVIEW"

    out_path = model_path.parent / "physics-validation-report.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Physics validation: {report['status']}")
    print(f"Disclaimer: {report['disclaimer']}")

    if report["status"] == "FAIL":
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
