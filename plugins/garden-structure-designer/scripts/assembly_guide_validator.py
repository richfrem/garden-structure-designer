#!/usr/bin/env python3
"""
assembly_guide_validator.py
===========================

Purpose:
    Validates markdown assembly guides against structural geometry calculations,
    verifying required erection procedures (e.g. tripod hoisting method for hex),
    compound cut angle match (miter, bevel, beam miter), and mandatory test-cut warnings.

Layer: Execution / QA Gate

Key Input Dependencies:
    - outputs/assembly-guide.md (or specified path)
    - context/staging/structure.json (structure.sides is authoritative; legacy geometry.sides /
      layout.post_count are fallbacks)
    - path_utils.py (default staging/outputs directories)

Key Functions:
    validate(guide_path, calcs_path, spec_path=None) -> list[str]
    check_tripod_first(sides, guide, errors) -> None
    check_saw_settings(geom, guide, errors) -> None
    check_test_cut_warning(guide, errors) -> None

Usage Examples:
    python3 assembly_guide_validator.py outputs/assembly-guide.md context/staging/structure.json
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, List, Optional

sys.path.append(str(Path(__file__).parent))
from path_utils import outputs_dir, staging_dir


def check_tripod_first(sides: Optional[int], guide: str, errors: List[str]) -> None:
    """Verifies that hexagonal structures specify tripod-first hub hoisting."""
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


def check_saw_settings(geom: dict[str, Any], guide: str, errors: List[str]) -> None:
    """Verifies that saw settings in assembly guide match computed geometry."""
    compound = geom.get("compound_cut", {})
    beam_ring = geom.get("beam_ring", {})

    miter = str(compound.get("miter_deg") or "")
    bevel = str(compound.get("bevel_deg") or "")
    beam_miter = str(beam_ring.get("beam_miter_deg") or "")

    if miter and miter not in guide:
        errors.append(f"MISSING_MITER: Rafter miter {miter}° not found in guide.")
    if bevel and bevel not in guide:
        errors.append(f"MISSING_BEVEL: Bevel {bevel}° not found in guide.")
    if beam_miter and beam_miter not in guide:
        errors.append(
            f"MISSING_BEAM_MITER: Beam ring miter {beam_miter}° not found. "
            f"Guide may be using rafter miter for beams."
        )


def check_test_cut_warning(guide: str, errors: List[str]) -> None:
    """Verifies that the guide includes a test-cut-on-scrap safety warning."""
    if "test" not in guide.lower() or "scrap" not in guide.lower():
        errors.append("MISSING_TEST_CUT: Must include test-cut-on-scrap warning.")


def validate(
    guide_path: str,
    calcs_path: str,
    spec_path: Optional[str] = None,
) -> List[str]:
    """Validates an assembly guide markdown against computed geometry specs."""
    with open(guide_path, encoding="utf-8") as f:
        guide = f.read()

    resolved_calcs_path = calcs_path
    if not os.path.exists(resolved_calcs_path):
        if spec_path and os.path.exists(spec_path):
            resolved_calcs_path = spec_path
        elif os.path.exists("context/staging/structure.json"):
            resolved_calcs_path = "context/staging/structure.json"

    with open(resolved_calcs_path, encoding="utf-8") as f:
        calcs_data = json.load(f)

    geom = calcs_data.get("geometry") if "geometry" in calcs_data else calcs_data
    layout = calcs_data.get("layout") or {}

    errors: List[str] = []
    sides = (calcs_data.get("structure") or {}).get("sides") or geom.get("sides") or layout.get("post_count")

    check_tripod_first(sides, guide, errors)
    check_saw_settings(geom, guide, errors)
    check_test_cut_warning(guide, errors)

    return errors


if __name__ == "__main__":
    target_guide = sys.argv[1] if len(sys.argv) > 1 else str(outputs_dir() / "assembly-guide.md")
    target_calcs = sys.argv[2] if len(sys.argv) > 2 else str(staging_dir() / "structure.json")
    target_spec = sys.argv[3] if len(sys.argv) > 3 else None

    validation_errors = validate(target_guide, target_calcs, target_spec)
    if validation_errors:
        print("ASSEMBLY GUIDE VALIDATION FAILED:")
        for e in validation_errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("ASSEMBLY GUIDE VALIDATION PASSED ✓")
        sys.exit(0)
