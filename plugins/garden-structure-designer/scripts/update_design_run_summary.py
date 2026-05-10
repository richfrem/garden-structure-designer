#!/usr/bin/env python3
"""
update_design_run_summary.py
=====================================
Purpose:
    Core logic for update_design_run_summary.py functionality within garden-structure-designer pipeline.
Layer: Execution
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
    model = safe_load(staging_dir() / "structural-model.json")
    spec = safe_load(staging_dir() / "design-spec.json")
    calcs = safe_load(staging_dir() / "geometry-calculations.json")
    
    summary = f"""# Design Run Summary

## Active Task
Generate validated garden structure design package.

## Locked Parameters
- Structure type: {spec.get("structureType", "Unknown")}
- Plan shape: {spec.get("planShape", "Unknown")}
- Jurisdiction: {spec.get("jurisdiction", "Unknown")}
- Post count: {model.get("members", {}).get("posts", {}).get("quantity", "Unknown")}
- Pitch: {model.get("roofStructure", {}).get("pitch", "Unknown")}
- Rafter miter: {calcs.get("compound_cut", {}).get("miter_deg", "Unknown")}
- Rafter bevel: {calcs.get("compound_cut", {}).get("bevel_deg", "Unknown")}
- Beam ring miter: {calcs.get("beam_ring", {}).get("beam_miter_deg", "Unknown")}
- Total height: {calcs.get("total_height", {}).get("total_height_ft", "Unknown")}

## Deterministic Calculations
- Source: geometry-calculations.json
- Source hash: {calcs.get("source_hash", "Unknown")}
- SVG viewBox: {calcs.get("svg_coordinates", {}).get("viewBox", "Unknown")}
- Grade Y: {calcs.get("svg_coordinates", {}).get("grade_y", "Unknown")}

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
