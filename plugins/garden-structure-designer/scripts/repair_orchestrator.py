#!/usr/bin/env python3
import json
import sys
import subprocess
from pathlib import Path

# Add path_utils
sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir, plugin_root, scripts_dir
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

    if not drift_report.get("failed_axes"):
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
    for axis in drift_report.get("failed_axes", []):
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
        
        attempt = {
            "attempt": 1,
            "failure_axis": axis,
            "repair_stage": stage,
            "commands": [action],
            "validation_status": "PASS" if result.returncode == 0 else "FAIL"
        }
        report["attempts"].append(attempt)
        
        if result.returncode != 0:
            report["remaining_failures"].append(axis)
            report["status"] = "FAIL"

    save_json(report, staging_dir() / "repair-report.json")
    print(f"Repair complete. Status: {report['status']}")

if __name__ == "__main__":
    main()
