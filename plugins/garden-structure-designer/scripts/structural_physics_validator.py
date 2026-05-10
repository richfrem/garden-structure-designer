#!/usr/bin/env python3
"""
structural_physics_validator.py
=====================================
Purpose:
    Core logic for structural_physics_validator.py functionality within garden-structure-designer pipeline.
Layer: Execution
"""
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir

def load_json(path):
    with open(path) as f: return json.load(f)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 structural_physics_validator.py <model.json>")
        sys.exit(1)
        
    model_path = Path(sys.argv[1])
    model = load_json(model_path)
    
    report = {
        "schema": "garden-structure-designer/physics-validation/1.1",
        "status": "PASS",
        "disclaimer": "Screening calculation only; not professional engineering certification.",
        "checks": [],
        "assumptions": []
    }
    
    posts = model.get("members", {}).get("posts", {})
    beams = model.get("members", {}).get("beams", {})
    
    # 1. Slenderness (L/d <= 50)
    post_length = posts.get("cutLength_ft", 8.0) * 12
    post_width = float(posts.get("width_in", 5.5))
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
    span_ft = posts.get("spanDistance_ft", 10.0)
    span_in = span_ft * 12
    allowable_deflection = span_in / 240
    # Dummy calculation for deflection using width/depth as proxy
    beam_w = float(beams.get("width_in", 3.5))
    beam_d = float(beams.get("depth_in", 7.25))
    # Approximation of stiffness proxy
    stiffness = (beam_w * (beam_d ** 3)) / 12
    deflection_proxy = (span_in ** 3) / (stiffness * 1000) if stiffness > 0 else 999
    
    def_check = {"name": "beam_deflection", "status": "PASS", "value": round(deflection_proxy, 3), "limit": round(allowable_deflection, 3)}
    if deflection_proxy > allowable_deflection:
        def_check["status"] = "WARNING"
        if report["status"] == "PASS": report["status"] = "WARNING"
    report["checks"].append(def_check)
    
    # 3. Bearing Area
    caisson_d = float(model.get("foundation", {}).get("caisson_diameter_in", 12))
    caisson_area = 3.14159 * (caisson_d / 2) ** 2
    post_area = float(posts.get("width_in", 5.5)) * float(posts.get("depth_in", 5.5))
    
    brg_check = {"name": "caisson_bearing", "status": "PASS", "value": round(post_area, 1), "limit": round(caisson_area, 1)}
    if post_area > caisson_area:
        brg_check["status"] = "FAIL"
        report["status"] = "FAIL"
    report["checks"].append(brg_check)
    
    # Defaults checking
    if model.get("roofStructure", {}).get("pitchDefaulted", False):
        report["assumptions"].append("Pitch was defaulted. Verify snow load capacity.")
        if report["status"] == "PASS": report["status"] = "REQUIRES_ENGINEER_REVIEW"
        
    out_path = staging_dir() / "physics-validation-report.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"Physics validation: {report['status']}")
    print(f"Disclaimer: {report['disclaimer']}")
    
    if report["status"] == "FAIL":
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
