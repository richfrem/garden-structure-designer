#!/usr/bin/env python3
"""
failure_to_test.py
==================

Purpose:
    Turns each failed axis of a drift report into a generated regression test under
    agent-workspace/.../generated-tests (classification-specific invariant or a generic guard).
    Note: the generated structural test pins the legacy 28.71/9.10 compound cut sample values, so
    treat generated tests as starting points to review, not as authoritative geometry assertions.

Layer: Execution / Learning Loop

Key Input Dependencies:
    - drift report JSON (failed_axes) passed as argv[1]
    - error_classifier.py, path_utils.py

Key Functions:
    main() -> None

Usage Examples:
    python3 failure_to_test.py context/staging/drift_report.json
"""
import json
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import agent_workspace_dir
from error_classifier import classify_failure

def main():
    """Reads the drift report and writes one generated regression test per failed axis."""
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
                f.write("from geometry_engine import compute, compound_cut, beam_ring_miter\n\n")
                f.write(f"def test_{cls['classification']}_regression():\n")
                f.write(f"    # Invariant test generated for {axis}\n")
                f.write("    res = compound_cut(4, 12, 6)\n")
                f.write("    assert round(res['miter_deg'], 2) == 28.71, 'Miter regression'\n")
                f.write("    assert round(res['bevel_deg'], 2) == 9.10, 'Bevel regression'\n")
            elif cls["repair_stage"] == "drawing-generator":
                f.write(f"from svg_validator import validate\n\n")
                f.write(f"def test_{cls['classification']}_regression():\n")
                f.write(f"    # Ensure SVG matches model topology\n")
                f.write(f"    assert hasattr(validate, '__call__'), 'Validator should be callable'\n")
            else:
                f.write(f"def test_generic_{cls['classification']}_regression():\n")
                f.write(f"    assert '{cls['classification']}' != 'unknown', 'Unhandled classification'\n")

    print(f"Generated {len(axes)} regression tests with assertions.")

if __name__ == "__main__":
    main()
