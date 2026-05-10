#!/usr/bin/env python3
"""
repair_orchestrator.py
=====================================
Purpose:
    Core logic for repair_orchestrator.py functionality within garden-structure-designer pipeline.
Layer: Execution
"""
import json
import sys
import subprocess
from pathlib import Path

# Add path_utils
sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir, plugin_root, scripts_dir, outputs_dir
from error_classifier import classify_failure
from run_history import should_halt, record_run

def load_json(path):
    with open(path) as f: return json.load(f)

def save_json(data, path):
    with open(path, 'w') as f: json.dump(data, f, indent=2)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("drift_report", type=str)
    parser.add_argument("repair_map", type=str)
    parser.add_argument("--max-attempts", type=int, default=2)
    args = parser.parse_args()

    drift_report_path = Path(args.drift_report)
    repair_map_path = Path(args.repair_map)

    if not drift_report_path.exists():
        print("No drift report found.")
        sys.exit(0)

    drift_report = load_json(drift_report_path)
    repair_map = load_json(repair_map_path)
    
    report = {
        "schema": "garden-structure-designer/repair-report/1.0",
        "status": "PASS",
        "attempts": [],
        "remaining_failures": []
    }

    axes = drift_report.get("failed_axes", [])
    if not axes and "failures" in drift_report:
        axes = [f.get("axis") or f.get("classification") or str(f) for f in drift_report["failures"]]
        
    if not axes:
        print("No failures reported.")
        save_json(report, staging_dir() / "repair-report.json")
        sys.exit(0)

    # Check structural-model.json lock
    model_path = staging_dir() / "structural-model.json"
    is_locked = False
    if model_path.exists():
        model = load_json(model_path)
        is_locked = model.get("_locked", False)

    # Try repairs
    for axis in axes:
        cls = classify_failure(axis)
        
        if cls["requires_human_review"]:
            report["remaining_failures"].append(axis)
            report["status"] = "BLOCKED"
            continue
            
        stage = cls["repair_stage"]
        
        if stage == "structural-engine" and is_locked:
            report["remaining_failures"].append(axis)
            report["status"] = "BLOCKED"
            continue
            
        # Run corresponding action
        action = repair_map.get(axis, {}).get("action")
        if not action:
            # Fallback based on stage
            if stage == "drawing-generator":
                action = f"python3 {scripts_dir()}/render_drawings.py {model_path}"
            elif stage == "structural-engine":
                action = f"python3 {scripts_dir()}/geometry_engine.py {model_path}"
            else:
                report["remaining_failures"].append(axis)
                report["status"] = "BLOCKED"
                continue
                
        script_name = action.split()[1].split('/')[-1]
        
        if should_halt(script_name, cls["classification"], args.max_attempts):
            report["remaining_failures"].append(axis)
            report["status"] = "BLOCKED"
            continue
            
        # Execute action
        cmd_args = action.split()
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        
        record_run(script_name, cmd_args[1:], result.returncode, cls["classification"])
        
        # Re-run validator
        val_status = "PASS" if result.returncode == 0 else "FAIL"
        if result.returncode == 0:
            if stage == "drawing-generator":
                svg_path = outputs_dir() / "drawing-plan-view.svg"
                val_cmd = [sys.executable, str(scripts_dir() / "svg_validator.py"), str(svg_path), str(model_path)]
                vr = subprocess.run(val_cmd, capture_output=True, text=True)
                val_status = "PASS" if vr.returncode == 0 else "FAIL"
            elif stage == "structural-engine":
                val_cmd = [sys.executable, str(scripts_dir() / "schema_validator.py")]
                vr = subprocess.run(val_cmd, capture_output=True, text=True)
                val_status = "PASS" if vr.returncode == 0 else "FAIL"
            elif stage == "package":
                val_cmd = [sys.executable, str(scripts_dir() / "package_consistency_validator.py")]
                vr = subprocess.run(val_cmd, capture_output=True, text=True)
                val_status = "PASS" if vr.returncode == 0 else "FAIL"
            elif stage == "cross-artifact":
                val_cmd = [sys.executable, str(scripts_dir() / "cross_artifact_validator.py")]
                vr = subprocess.run(val_cmd, capture_output=True, text=True)
                val_status = "PASS" if vr.returncode == 0 else "FAIL"
        
        attempt = {
            "attempt": 1,
            "failure_axis": axis,
            "repair_stage": stage,
            "commands": [action],
            "validation_status": val_status
        }
        report["attempts"].append(attempt)
        
        if val_status != "PASS":
            report["remaining_failures"].append(axis)
            report["status"] = "FAIL"

    save_json(report, staging_dir() / "repair-report.json")
    print(f"Repair complete. Status: {report['status']}")

if __name__ == "__main__":
    main()
