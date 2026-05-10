#!/usr/bin/env python3
"""
failure_to_test.py (CLI)
=====================================

Purpose:
    failure_to_test.py Generates regression tests from failure cases logged in drift_report.json

Layer: Execution

Usage Examples:
    python failure_to_test.py [args]

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

def generate_test_for_failure(drift_report_path: str, output_dir: str):
    if not os.path.exists(drift_report_path):
        return
        
    with open(drift_report_path) as f:
        report = json.load(f)
        
    failures = report.get("failures", [])
    for idx, f in enumerate(failures):
        axis = f.get("axis", f"unknown_{idx}")
        expected = f.get("expected", "")
        
        test_file = os.path.join(output_dir, f"test_regression_{axis}.py")
        content = f'''import json
import pytest

def test_regression_{axis.replace("-", "_")}():
    """Auto-generated test from drift_report.json"""
    expected = {repr(expected)}
    found = {repr(f.get("found", ""))}
    
    assert found == expected, f"Regression on {axis}: Expected {{expected}} but found {{found}}"
'''
        with open(test_file, "w") as out:
            out.write(content)
            
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 failure_to_test.py <drift_report.json> <output_dir>")
        sys.exit(1)
        
    generate_test_for_failure(sys.argv[1], sys.argv[2])
