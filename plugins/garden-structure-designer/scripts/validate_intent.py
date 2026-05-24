#!/usr/bin/env python3
"""
validate_intent.py
==================
Pre-geometry validation gate: verifies that all fields required by
geometry_engine.py are present, numeric, and have physically plausible values.

Pipeline position:
    intake-normalizer  (produces structure.json from user description)
        ↓
    validate_intent.py  (hard gate — rejects vague or incomplete structures)
        ↓
    geometry_engine.py  (computes and seals geometry)

Why this gate exists:
    geometry_engine.py must NOT silently guess missing values.
    validate_intent.py makes the contract explicit: if it passes, every
    field that geometry_engine reads will exist with a sensible numeric value.

Exit code 0 = all checks passed.
Exit code 1 = one or more fields missing, wrong type, or out of range.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


class IntentError(ValueError):
    """Raised when the structure is not ready for geometry computation."""


# ---------------------------------------------------------------------------
# Field accessor
# ---------------------------------------------------------------------------

def _get(structure: dict, dotpath: str) -> Any:
    """Navigate dotted path like 'layout.post_count'; raise KeyError if absent."""
    parts = dotpath.split(".")
    node: Any = structure
    for part in parts:
        if not isinstance(node, dict) or part not in node:
            raise KeyError(dotpath)
        node = node[part]
    return node


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def _check(
    structure: dict,
    field: str,
    expected_type: type | tuple[type, ...],
    valid: "Any",        # callable(value) → bool, or None to skip range check
    description: str,
) -> str | None:
    """Return an error string if the field fails, else None."""
    try:
        value = _get(structure, field)
    except KeyError:
        return f"MISSING: {field} — {description}"
    if not isinstance(value, expected_type):
        return f"WRONG_TYPE: {field} = {value!r} (expected {expected_type.__name__ if isinstance(expected_type, type) else 'number'})"
    if callable(valid) and not valid(value):
        return f"OUT_OF_RANGE: {field} = {value!r} — {description}"
    return None


# ---------------------------------------------------------------------------
# Unconditional required fields
# ---------------------------------------------------------------------------

_UNCONDITIONAL_CHECKS: list[tuple[str, type | tuple, Any, str]] = [
    ("layout.post_count",                     int,          lambda v: v >= 3,           "integer ≥ 3"),
    ("layout.inscribed_radius_ft",             (int, float), lambda v: v > 0,            "positive number (feet)"),
    ("roof.pitch",                             str,          lambda v: bool(re.match(r"^\d+:12$", v)),  "format N:12, e.g. '4:12'"),
    ("roof.primary_rafters.count",             int,          lambda v: v > 0,            "integer > 0"),
    ("roof.primary_rafters.overhang_ft",       (int, float), lambda v: v >= 0,           "non-negative number (feet)"),
    ("roof.primary_rafters.actual_width_in",   (int, float), lambda v: 0 < v <= 24,      "inches, range (0, 24]"),
    ("roof.primary_rafters.actual_depth_in",   (int, float), lambda v: 0 < v <= 24,      "inches, range (0, 24]"),
    ("members.posts.actual_width_in",          (int, float), lambda v: 0 < v <= 24,      "inches, range (0, 24]"),
    ("members.posts.cut_length_ft",            (int, float), lambda v: v > 0,            "positive number (feet)"),
    ("members.beams.actual_depth_in",          (int, float), lambda v: 0 < v <= 24,      "inches, range (0, 24]"),
    ("hub.type",                               str,          lambda v: len(v) > 0,       "non-empty string"),
    ("hub.radius_min_ft",                      (int, float), lambda v: v > 0,            "positive number (feet)"),
    ("cad.units",                              str,          lambda v: v == "feet",      "must be 'feet'"),
    ("cad.coordinate_system",                  str,          lambda v: v == "right_handed_z_up",  "must be 'right_handed_z_up'"),
    ("cad.precision",                          (int, float), lambda v: 0 < v < 1,        "float in (0, 1), e.g. 0.001"),
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_intent(structure: dict) -> list[str]:
    """
    Run all pre-geometry checks.
    Returns a list of error strings — empty list means all checks passed.
    """
    errors: list[str] = []

    for field, etype, valid, desc in _UNCONDITIONAL_CHECKS:
        err = _check(structure, field, etype, valid, desc)
        if err:
            errors.append(err)

    # Bracing: additional required fields when enabled
    if structure.get("bracing", {}).get("enabled"):
        for field, etype, valid, desc in [
            ("bracing.brace.length_ft",  (int, float), lambda v: 0 < v <= 10,     "feet, range (0, 10]"),
            ("bracing.brace.angle_deg",  (int, float), lambda v: 5 <= v <= 85,    "degrees, range [5, 85]"),
        ]:
            err = _check(structure, field, etype, valid, desc)
            if err:
                errors.append(err)

    return errors


def assert_intent_valid(structure: dict) -> None:
    """
    Run validate_intent; raise IntentError with details if any check fails.
    Call this after intake-normalizer writes structure.json and before geometry_engine.
    """
    errors = validate_intent(structure)
    if errors:
        lines = "\n".join(f"  {e}" for e in errors)
        raise IntentError(
            f"Intent validation FAILED ({len(errors)} error(s)) — "
            f"structure.json is incomplete or vague:\n{lines}"
        )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a structure.json is ready for geometry computation."
    )
    parser.add_argument("structure", help="Path to structure.json")
    args = parser.parse_args()

    with open(args.structure, encoding="utf-8") as f:
        structure = json.load(f)

    errors = validate_intent(structure)

    if errors:
        print(f"INTENT VALIDATION FAILED — {len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print(f"INTENT VALIDATION PASSED — structure.json is ready for geometry_engine")
        sys.exit(0)


if __name__ == "__main__":
    main()
