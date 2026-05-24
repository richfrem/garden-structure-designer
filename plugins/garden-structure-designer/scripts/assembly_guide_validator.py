#!/usr/bin/env python3
"""
assembly_guide_validator.py (CLI)
=====================================

Purpose:
    assembly_guide_validator.py (CLI) =====================================

Layer: Execution

Usage Examples:
    python assembly_guide_validator.py [args]

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
import json, re, sys

def validate(guide_path, calcs_path, spec_path=None):
    with open(guide_path) as f:
        guide = f.read()
    with open(calcs_path) as f:
        calcs = json.load(f)

    errors = []
    sides = calcs.get("sides", 4)

    # ── Hex tripod-first check ──
    if sides == 6:
        if "tripod" not in guide.lower():
            errors.append(
                "HEX_TRIPOD_MISSING: Hexagonal structure assembly guide "
                "must include tripod-first hub hoisting method."
            )
        if "three alternating" not in guide.lower():
            errors.append(
                "HEX_TRIPOD_INCOMPLETE: Must describe installing "
                "three alternating rafters first."
            )

    # ── Saw settings match geometry ──
    miter = str(calcs.get("compound_cut", {}).get("miter_deg", ""))
    bevel = str(calcs.get("compound_cut", {}).get("bevel_deg", ""))
    beam_miter = str(calcs.get("beam_ring", {}).get("beam_miter_deg", ""))

    if miter and miter not in guide:
        errors.append(f"MISSING_MITER: Rafter miter {miter}° not found in guide.")
    if bevel and bevel not in guide:
        errors.append(f"MISSING_BEVEL: Bevel {bevel}° not found in guide.")
    if beam_miter and beam_miter not in guide:
        errors.append(
            f"MISSING_BEAM_MITER: Beam ring miter {beam_miter}° not found. "
            f"Guide may be using rafter miter for beams."
        )

    # ── Test-cut warning ──
    if "test" not in guide.lower() or "scrap" not in guide.lower():
        errors.append("MISSING_TEST_CUT: Must include test-cut-on-scrap warning.")

    return errors

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 assembly_guide_validator.py <guide_path> <calcs_path> [spec_path]")
        sys.exit(1)
        
    guide_path = sys.argv[1]
    calcs_path = sys.argv[2]
    spec_path = sys.argv[3] if len(sys.argv) > 3 else None
    errors = validate(guide_path, calcs_path, spec_path)
    if errors:
        print("ASSEMBLY GUIDE VALIDATION FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("ASSEMBLY GUIDE VALIDATION PASSED ✓")
        sys.exit(0)
