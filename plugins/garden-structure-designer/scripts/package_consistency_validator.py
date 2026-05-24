#!/usr/bin/env python3
"""
package_consistency_validator.py (CLI)
=====================================

Purpose:
    package_consistency_validator.py (CLI) =====================================

Layer: Execution

Usage Examples:
    python package_consistency_validator.py [args]

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
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import outputs_dir, staging_dir, schemas_dir, scripts_dir, agent_workspace_dir

import sys

def validate_package() -> list[str]:
    errors = []
    out_dir_path = str(outputs_dir())
    if not os.path.exists(out_dir_path):
        return ["Outputs directory not found"]
        
    required_files = [
        "blueprint-plan.svg",
        "drawing-plan-view.svg",
        "shop-blueprint/SB01-cut-list.json"
    ]
    for rf in required_files:
        if not os.path.exists(os.path.join(out_dir_path, rf)):
            errors.append(f"MISSING_OUTPUT: {rf} was not generated.")
            
    import glob
    # Check for photorealistic renders
    render_dir = os.path.join(out_dir_path, "high-resolution-image")
    renders = glob.glob(os.path.join(render_dir, "*_render_*.png"))
    if not renders:
        errors.append("MISSING_RENDERS: No photorealistic renders found in outputs/high-resolution-image/")
    import re
    svg_files = glob.glob(os.path.join(out_dir_path, "**", "*.svg"), recursive=True)
    dates = set()
    titles = set()
    for svg in svg_files:
        with open(svg) as f:
            content = f.read()
            date_match = re.search(r"data-date=[\"'](.*?)[\"']", content)
            if date_match:
                dates.add(date_match.group(1))
            title_match = re.search(r"data-title=[\"'](.*?)[\"']", content)
            if title_match:
                titles.add(title_match.group(1))
                
    if len(dates) > 1:
        errors.append(f"INCONSISTENT_DATES: Found multiple generation dates in SVGs: {dates}")
    if len(titles) > 1:
        errors.append(f"INCONSISTENT_TITLES: Found multiple project titles in SVGs: {titles}")
        
    return errors

if __name__ == "__main__":
    errors = validate_package()
    if errors:
        print("PACKAGE CONSISTENCY VALIDATION FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("PACKAGE CONSISTENCY VALIDATION PASSED ✓")
        sys.exit(0)
