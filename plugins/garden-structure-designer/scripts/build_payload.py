#!/usr/bin/env python3
"""
build_payload.py (CLI)
=====================================

Purpose:
    build_payload.py (CLI) =====================================

Layer: Execution

Usage Examples:
    python build_payload.py [args]

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


files_to_merge = {
    "SEALED MANIFEST (structure.json)": "context/staging/structure.json",
    "GENERATED OUTPUT 1 (blueprint-plan.svg)": "outputs/blueprint-plan.svg",
    "GENERATED OUTPUT 2 (blueprint-isometric.svg)": "outputs/blueprint-isometric.svg"
}

os.makedirs("temp", exist_ok=True)
with open("temp/validation_payload.md", "w") as out:
    for title, path in files_to_merge.items():
        out.write(f"--- {title} ---\n")
        try:
            with open(path, "r") as f:
                out.write(f.read() + "\n\n")
        except FileNotFoundError:
            out.write(f"Error: {path} not found.\n\n")

print("Created temp/validation_payload.md")
