#!/usr/bin/env python3
"""
update_design_run_summary.py (CLI)
=====================================

Purpose:
    update_design_run_summary.py =====================================

Layer: Execution

Usage Examples:
    python update_design_run_summary.py [args]

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
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir

def safe_load(path):
    if Path(path).exists():
        with open(path) as f: return json.load(f)
    return {}

def main():
    structure = safe_load(staging_dir() / "structure.json")
    
    meta = structure.get("meta", {})
    intent = structure.get("intent", {})
    layout = structure.get("layout", {})
    roof = structure.get("roof", {})
    geom = structure.get("geometry", {})
    
    structure_type = structure.get("structure", {}).get("type") or "Unknown"
    plan_shape = structure.get("structure", {}).get("shape") or "Unknown"
    jurisdiction = intent.get("jurisdiction") or "Unknown"
    post_count = layout.get("post_count") or "Unknown"
    pitch = roof.get("pitch") or "Unknown"
    
    cuts = geom.get("compound_cut") or {}
    miter = cuts.get("miter_deg") or "Unknown"
    bevel = cuts.get("bevel_deg") or "Unknown"
    
    beam_ring = geom.get("beam_ring") or {}
    beam_miter = beam_ring.get("beam_miter_deg") or "Unknown"
    
    total_height = (geom.get("total_height") or {}).get("total_height_ft") or "Unknown"
    
    source_hash = meta.get("source_hash") or "Unknown"
    svg_coords = geom.get("svg_coordinates") or {}
    viewbox = svg_coords.get("viewBox") or "Unknown"
    grade_y = svg_coords.get("grade_y") or "Unknown"
    
    summary = f"""# Design Run Summary
 
 ## Active Task
 Generate validated garden structure design package.
 
 ## Locked Parameters
 - Structure type: {structure_type}
 - Plan shape: {plan_shape}
 - Jurisdiction: {jurisdiction}
 - Post count: {post_count}
 - Pitch: {pitch}
 - Rafter miter: {miter}
 - Rafter bevel: {bevel}
 - Beam ring miter: {beam_miter}
 - Total height: {total_height}
 
 ## Deterministic Calculations
 - Source: structure.json
 - Source hash: {source_hash}
 - SVG viewBox: {viewbox}
 - Grade Y: {grade_y}
 
 ## Completed Stages
 Generated dynamically as pipeline executes.
 
 ## Validation Findings
 Check repair-report.json and drift_report.json.
 """
    with open(staging_dir() / "design-run-summary.md", "w") as f:
        f.write(summary)
        
    print("Design run summary updated.")

if __name__ == "__main__":
    main()
