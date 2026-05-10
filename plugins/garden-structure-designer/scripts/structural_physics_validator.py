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
        "schema": "garden-structure-designer/physics-validation/1.0",
        "status": "PASS",
        "disclaimer": "Screening calculation only; not professional engineering certification.",
        "checks": [],
        "assumptions": []
    }
    
    # Check slenderness (L/d <= 50)
    posts = model.get("members", {}).get("posts", {})
    length = posts.get("cutLength_ft", 8.0) * 12
    width = 5.5 # assuming 6x6
    slenderness = length / width
    
    check = {
        "name": "post_slenderness",
        "status": "PASS",
        "value": round(slenderness, 1),
        "limit": 50
    }
    
    if slenderness > 50:
        check["status"] = "FAIL"
        report["status"] = "FAIL"
    elif slenderness > 40:
        check["status"] = "WARNING"
        if report["status"] == "PASS": report["status"] = "WARNING"
        
    report["checks"].append(check)
    
    # Defaults checking
    if model.get("roofStructure", {}).get("pitchDefaulted", False):
        report["assumptions"].append("Pitch was defaulted. Verify snow load capacity.")
        if report["status"] == "PASS": report["status"] = "REQUIRES_ENGINEER_REVIEW"
        
    # Output
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
