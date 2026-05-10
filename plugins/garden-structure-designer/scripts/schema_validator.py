#!/usr/bin/env python3
"""
schema_validator.py (CLI)
=====================================

Purpose:
    schema_validator.py Validates JSON artifacts against schemas.

Layer: Execution

Usage Examples:
    python schema_validator.py [args]

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
import os
import sys
import glob

import jsonschema

def validate_schemas(staging_dir: str, schemas_dir: str) -> list[str]:
    errors = []
    
    json_files = glob.glob(os.path.join(staging_dir, "*.json"))
    for jf in json_files:
        filename = os.path.basename(jf)
        name = filename.replace(".json", "")
        schema_path = os.path.join(schemas_dir, f"{name}.schema.json")
        
        if os.path.exists(schema_path):
            with open(schema_path) as sf:
                schema = json.load(sf)
                
            with open(jf) as f:
                try:
                    data = json.load(f)
                    try:
                        jsonschema.validate(instance=data, schema=schema)
                    except jsonschema.exceptions.ValidationError as e:
                        errors.append(f"{filename} validation failed: {e.message}")
                except json.JSONDecodeError:
                    errors.append(f"{filename}: Invalid JSON format")
    return errors

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 schema_validator.py <staging_dir> <schemas_dir>")
        sys.exit(1)
        
    staging = sys.argv[1]
    schemas = sys.argv[2]
    
    errors = validate_schemas(staging, schemas)
    if errors:
        print("SCHEMA VALIDATION FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("SCHEMA VALIDATION PASSED ✓")
        sys.exit(0)
