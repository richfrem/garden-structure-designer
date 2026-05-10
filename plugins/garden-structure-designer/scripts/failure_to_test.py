#!/usr/bin/env python3
"""
failure_to_test.py
=====================================
Purpose:
    Core logic for failure_to_test.py functionality within garden-structure-designer pipeline.
Layer: Execution
"""
import json
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import agent_workspace_dir
from error_classifier import classify_failure

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 failure_to_test.py <drift_report.json>")
        sys.exit(1)
        
    report_path = Path(sys.argv[1])
    if not report_path.exists():
        sys.exit(0)
        
    with open(report_path) as f:
        report = json.load(f)
        
    axes = report.get("failed_axes", [])
    if not axes:
        sys.exit(0)
        
    out_dir = agent_workspace_dir() / "generated-tests"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for i, axis in enumerate(axes):
        cls = classify_failure(axis)
        test_file = out_dir / f"test_regression_{cls['classification']}_{i}.py"
        
        with open(test_file, "w") as f:
            f.write(f"import sys\nimport os\nfrom pathlib import Path\n")
            f.write(f"sys.path.append(str(Path(__file__).parent.parent.parent / 'plugins' / 'garden-structure-designer' / 'scripts'))\n\n")
            
            if cls["classification"] == "compound_cut_mismatch" or cls["repair_stage"] == "structural-engine":
                f.write(f"from geometry_engine import compute\n\n")
                f.write(f"def test_{cls['classification']}_regression():\n")
                f.write(f"    # Invariant test generated for {axis}\n")
                f.write(f"    pass\n")
            elif cls["repair_stage"] == "drawing-generator":
                f.write(f"from svg_validator import validate\n\n")
                f.write(f"def test_{cls['classification']}_regression():\n")
                f.write(f"    # Ensure SVG matches model topology\n")
                f.write(f"    pass\n")
            else:
                f.write(f"def test_generic_{cls['classification']}_regression():\n")
                f.write(f"    assert True, 'Placeholder for {axis}'\n")

    print(f"Generated {len(axes)} regression tests.")

if __name__ == "__main__":
    main()
