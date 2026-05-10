#!/usr/bin/env python3
"""
load_applicable_lessons.py (CLI)
=====================================

Purpose:
    load_applicable_lessons.py Filters learning-registry.json to return only lessons that apply to the current design spec.

Layer: Execution

Usage Examples:
    python load_applicable_lessons.py [args]

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

def load_lessons(category: str, design_path: str, registry_path: str) -> dict:
    if not os.path.exists(registry_path):
        return {"lessons": []}
        
    with open(registry_path) as f:
        registry = json.load(f)
        
    design = {}
    if os.path.exists(design_path):
        with open(design_path) as f:
            design = json.load(f)
            
    shape = design.get("planShape", "hexagon")
    roof = design.get("roofType", "hub-and-hip-rafter")
    
    applicable = []
    for lesson in registry.get("active_lessons", []):
        if lesson.get("category") != category:
            continue
            
        conditions = lesson.get("applies_when", {})
        if "planShape" in conditions and conditions["planShape"] != shape:
            continue
        if "roofType" in conditions and conditions["roofType"] != roof:
            continue
            
        applicable.append({
            "id": lesson["id"],
            "file": lesson["lesson_file"],
            "severity": lesson["severity"]
        })
        
    return {"lessons": applicable}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", required=True)
    parser.add_argument("--design", required=True)
    parser.add_argument("--registry", required=True)
    args = parser.parse_args()
    
    result = load_lessons(args.category, args.design, args.registry)
    print(json.dumps(result, indent=2))
