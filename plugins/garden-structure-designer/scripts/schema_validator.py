#!/usr/bin/env python3
"""
schema_validator.py
=====================================
Purpose:
    Core logic for schema_validator.py functionality within garden-structure-designer pipeline.
Layer: Execution
"""
import json
import sys
import jsonschema
from pathlib import Path
import argparse

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir, schemas_dir

def load_json(path):
    with open(path) as f: return json.load(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_dir", nargs='?', default=str(staging_dir()))
    parser.add_argument("schema_dir", nargs='?', default=str(schemas_dir()))
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json-output", type=str)
    args = parser.parse_args()

    target_path = Path(args.target_dir)
    schema_path = Path(args.schema_dir)
    
    report = {
        "schema": "garden-structure-designer/schema-validation-report/1.0",
        "status": "PASS",
        "files": []
    }
    
    overall_status = "PASS"

    for file in target_path.glob("*.json"):
        if file.name in ["repair-report.json", "drift_report.json", "learning-registry.json", "script-run-history.jsonl"]:
            continue
            
        schema_file = schema_path / f"{file.stem}.schema.json"
        if not schema_file.exists():
            continue
            
        data = load_json(file)
        schema = load_json(schema_file)
        
        file_report = {
            "path": str(file),
            "schema": str(schema_file),
            "status": "PASS",
            "errors": [],
            "warnings": []
        }
        
        try:
            jsonschema.validate(data, schema)
            
            if args.strict and file.name == "design-spec.json":
                known_keys = set(schema.get("properties", {}).keys())
                data_keys = set(data.keys())
                unknown = data_keys - known_keys
                if unknown:
                    file_report["warnings"].append(f"Unknown keys in design-spec: {unknown}")
                    if overall_status == "PASS": overall_status = "WARNING"
                    file_report["status"] = "WARNING"
                    
        except jsonschema.ValidationError as e:
            file_report["status"] = "FAIL"
            file_report["errors"].append(e.message)
            overall_status = "FAIL"
            
        report["files"].append(file_report)

    report["status"] = overall_status

    if args.json_output:
        with open(args.json_output, "w") as f:
            json.dump(report, f, indent=2)
            
    if overall_status == "FAIL":
        print("SCHEMA VALIDATION FAILED")
        for f in report["files"]:
            if f["errors"]: print(f"  {f['path']}: {f['errors']}")
        sys.exit(1)
    else:
        print(f"SCHEMA VALIDATION PASSED ✓ ({overall_status})")
        sys.exit(0)

if __name__ == "__main__":
    main()
