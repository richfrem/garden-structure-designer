#!/usr/bin/env python3
"""
cross_artifact_validator.py (CLI)
=====================================

Purpose:
    cross_artifact_validator.py Validates consistency across all generated artifacts (Markdown, SVG, JSON).

Layer: Execution

Usage Examples:
    python cross_artifact_validator.py [args]

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
import glob
import json
import os
import re
import sys

def check_paths(file_path: str, content: str) -> list[str]:
    errors = []
    if "output/" in content and "outputs/" not in content:
        # crude check, but often catches `../output/` typos
        errors.append(f"{file_path}: Found 'output/' path instead of 'outputs/'")
    return errors

def validate(staging_dir: str, outputs_dir: str) -> list[str]:
    errors = []
    calcs_path = os.path.join(staging_dir, "geometry-calculations.json")
    if not os.path.exists(calcs_path):
        return ["MISSING_GEOMETRY: geometry-calculations.json not found."]
        
    with open(calcs_path) as f:
        calcs = json.load(f)
        
    miter = str(round(calcs.get("compound_cut", {}).get("miter_deg", 0), 2))
    bevel = str(round(calcs.get("compound_cut", {}).get("bevel_deg", 0), 2))
    beam_miter = str(round(calcs.get("beam_ring", {}).get("beam_miter_deg", 0), 2))
    
    # Scan all .md and .svg
    files = glob.glob(os.path.join(outputs_dir, "**", "*.md"), recursive=True) + \
            glob.glob(os.path.join(outputs_dir, "**", "*.svg"), recursive=True)
            
    for fpath in files:
        with open(fpath) as f:
            content = f.read()
            
        errors.extend(check_paths(fpath, content))
        
        # Miter vs Beam miter check
        if miter != "0" and beam_miter != "0" and miter != beam_miter and "beam" in content.lower():
            # Check if rafter miter is accidentally applied to a beam context
            beam_miter_matches = re.finditer(r"(?i)beam.{0,30}?miter.{0,10}?(\d+\.?\d*)", content)
            for match in beam_miter_matches:
                found_miter = match.group(1)
                if found_miter == miter and found_miter != beam_miter:
                    errors.append(f"{fpath}: Beam miter incorrectly uses rafter miter ({miter}) instead of beam miter ({beam_miter}).")
            
        # Parse SAW_SETTINGS metadata
        saw_match = re.search(r"<!--\s*SAW_SETTINGS:\s*({.*?})\s*-->", content, re.DOTALL)
        if saw_match:
            try:
                saw_settings = json.loads(saw_match.group(1))
                if str(saw_settings.get("miter_deg", "")) != miter:
                    errors.append(f"{fpath}: SAW_SETTINGS miter mismatch.")
                if str(saw_settings.get("bevel_deg", "")) != bevel:
                    errors.append(f"{fpath}: SAW_SETTINGS bevel mismatch.")
            except json.JSONDecodeError:
                errors.append(f"{fpath}: Invalid SAW_SETTINGS JSON.")
                
    return errors

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 cross_artifact_validator.py <staging_dir> <outputs_dir>")
        sys.exit(1)
        
    staging_dir = sys.argv[1]
    outputs_dir = sys.argv[2]
    
    errors = validate(staging_dir, outputs_dir)
    if errors:
        print("CROSS-ARTIFACT VALIDATION FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("CROSS-ARTIFACT VALIDATION PASSED ✓")
        sys.exit(0)
