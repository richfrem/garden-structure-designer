#!/usr/bin/env python3
"""
structural_physics_validator.py (CLI)
=====================================

Purpose:
    structural_physics_validator.py Deterministic physics validation for garden structures (deflection, L/d ratio).

Layer: Execution

Usage Examples:
    python structural_physics_validator.py [args]

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

def validate_physics(model_path: str, code_path: str) -> list[str]:
    errors = []
    with open(model_path) as f:
        model = json.load(f)
        
    code_data = {}
    if os.path.exists(code_path):
        with open(code_path) as f:
            code_data = json.load(f)
            
    members = model.get("members") or model.get("structuralElements", {})
    posts = members.get("posts", {})
    
    # Check post slenderness ratio L/d < 50
    post_len_in = posts.get("cutLength_ft", 8.33) * 12
    post_d = min(posts.get("width_in", 6), posts.get("depth_in", 6))
    if post_d > 0:
        slenderness = post_len_in / post_d
        if slenderness > 50:
            errors.append(f"SLENDERNESS_FAIL: Post slenderness L/d = {slenderness:.1f} > 50 (max).")
            
    # Check beam deflection L/240
    beams = members.get("beams", {})
    beam_len_in = beams.get("span_ft", 10) * 12
    beam_w = beams.get("width_in", 6)
    beam_d = beams.get("depth_in", 8)
    E = 1_200_000  # Modulus of elasticity (psi) for typical timber
    I_val = (beam_w * (beam_d ** 3)) / 12  # Moment of inertia
    
    # Calculate load w (lb/in) from snow/wind
    snow_load = code_data.get("snowLoad_psf", 40)
    # Assume 10ft tributary width -> 10 * 40 = 400 lb/ft = 33.3 lb/in
    w_load = (snow_load * 10) / 12
    
    if I_val > 0:
        deflection = (5 * w_load * (beam_len_in ** 4)) / (384 * E * I_val)
        max_deflection = beam_len_in / 240
        if deflection > max_deflection:
            errors.append(f"DEFLECTION_FAIL: Beam deflection {deflection:.2f}in > {max_deflection:.2f}in (L/240).")

    # Check caisson bearing capacity
    footings = model.get("footings", {})
    bearing_capacity_psf = code_data.get("bearingCapacity_psf", 1500)
    footing_area_sqft = footings.get("area_sqft", 3.14)  # ~24" diameter
    
    # Total load on footing ~ 10ft x 10ft tributary = 100 sqft * (snow_load + dead_load(15))
    total_load = 100 * (snow_load + 15)
    actual_pressure = total_load / footing_area_sqft
    
    if actual_pressure > bearing_capacity_psf:
        errors.append(f"BEARING_FAIL: Soil pressure {actual_pressure:.0f} psf > capacity {bearing_capacity_psf} psf.")
    return errors

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 structural_physics_validator.py <model.json> <code.json>")
        sys.exit(1)
        
    errors = validate_physics(sys.argv[1], sys.argv[2])
    if errors:
        print("PHYSICS VALIDATION FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("PHYSICS VALIDATION PASSED ✓")
        sys.exit(0)
