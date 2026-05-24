#!/usr/bin/env python3
"""
svg_validator.py (CLI)
=====================================

Purpose:
    svg_validator.py (CLI) =====================================

Layer: Execution

Usage Examples:
    python svg_validator.py [args]

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
from __future__ import annotations

import json
import os
import re
import sys
import xml.etree.ElementTree as ET
import hashlib
from typing import Optional


# ---------------------------------------------------------------------------
# Validation logic
# ---------------------------------------------------------------------------


def _load_geometry_calcs(model_path: str) -> Optional[dict]:
    """
    Load geometry calculations from structure.json or geometry-calculations.json.
    """
    if not os.path.exists(model_path):
        return None
    with open(model_path) as f:
        try:
            data = json.load(f)
        except Exception:
            return None
    if "meta" in data and "schema_version" in data.get("meta", {}):
        return data.get("geometry")

    calc_path = os.path.join(os.path.dirname(model_path), "geometry-calculations.json")
    if os.path.exists(calc_path):
        with open(calc_path) as f:
            try:
                return json.load(f)
            except Exception:
                return None
    return None


def _check_xml_validity(svg_path: str, raw: str) -> list[str]:
    """
    Validate SVG XML well-formedness.

    Checks:
    - Parseable by ElementTree (no broken tags, unescaped characters, etc.).
    - No double-hyphen (--) inside XML comment bodies (illegal per XML 1.0).

    Args:
        svg_path: File path for error messages.
        raw: Raw SVG file contents as string.

    Returns:
        List of error message strings (empty if all pass).
    """
    errors: list[str] = []

    try:
        ET.fromstring(raw)
    except ET.ParseError as exc:
        errors.append(f"XML_INVALID: {exc}")
        return errors  # Cannot safely proceed with further checks

    for match in re.finditer(r"<!--(.*?)-->", raw, re.DOTALL):
        body = match.group(1)
        if "--" in body:
            errors.append(
                "XML_COMMENT: Illegal double-hyphen (--) found inside comment body. "
                "XML 1.0 §2.5 forbids this."
            )
    return errors


def _check_dimension_labels(
    raw: str,
    model: dict,
    calcs: Optional[dict],
) -> list[str]:
    """
    Verify that critical dimension labels are present in the SVG text content.

    Args:
        raw: Raw SVG file contents.
        model: Parsed structural-model.json or structure.json.
        calcs: Parsed geometry-calculations.json, or None.

    Returns:
        List of error strings for any missing labels.
    """
    errors: list[str] = []

    # --- Roof pitch label ---
    if "roof" in model and "pitch" in model["roof"]:
        pitch = model["roof"]["pitch"]
    else:
        members = model.get("members") or model.get("structuralElements", {})
        roof = members.get("roofStructure") or model.get("roofStructure", {})
        pitch = roof.get("pitch", "4:12")

    pitch_prefix = pitch.split(":")[0]  # e.g. "4" for "4:12"
    if pitch_prefix + ":12" not in raw:
        errors.append(
            f"MISSING_PITCH_LABEL: '{pitch}' pitch label not found in SVG text nodes."
        )

    # --- Compound angle labels (only when geometry-calculations.json / geometry section is available) ---
    if calcs:
        cuts = calcs.get("compound_cut", {})
        miter = str(round(cuts.get("miter_deg", 0), 2))
        bevel = str(round(cuts.get("bevel_deg", 0), 2))
        
        if miter not in raw:
            errors.append(
                f"MISSING_MITER_ANGLE: miter angle {miter}° not found in SVG. "
                f"Expected from geometry."
            )
        if bevel not in raw:
            errors.append(
                f"MISSING_BEVEL_ANGLE: bevel angle {bevel}° not found in SVG. "
                f"Expected from geometry."
            )

    return errors


def _check_topology_count(raw: str, model: dict) -> list[str]:
    """
    Count structural post elements in the SVG against the JSON quantity.

    Uses the canonical cedar fill colour (#c8a96e) as a proxy for post elements.
    Sheets that are not topology views should include <!-- TOPOLOGY_SKIP -->
    in their XML to suppress this check.

    Args:
        raw: Raw SVG file contents.
        model: Parsed structural-model.json or structure.json.

    Returns:
        List of error strings if count mismatches (empty if skip or pass).
    """
    if "TOPOLOGY_SKIP" in raw:
        # Only allow on component/detail sheets
        if any(kw in raw.lower() for kw in ["plan view", "elevation view", "isometric"]):
            return ["TOPOLOGY_SKIP_ABUSE: Cannot skip topology on full-structure sheets."]
        return []

    if "layout" in model and "post_count" in model["layout"]:
        expected_qty: int = model["layout"]["post_count"]
    else:
        members = model.get("members") or model.get("structuralElements", {})
        posts = members.get("posts", {})
        expected_qty = posts.get("quantity", 6)

    # Count elements with the canonical post cedar fill colour or data-role
    found = len(re.findall(r'data-role="post"', raw))
    if found == 0:
        # Fallback to color-based (legacy SVGs)
        found = len(re.findall(r'fill="#c8a96e"', raw))

    if found != expected_qty:
        return [
            f"TOPOLOGY_COUNT: Expected exactly {expected_qty} posts, "
            f"found {found}. Extra posts fail just like missing posts."
        ]
    return []

def _check_source_hash(model_path: str, calcs: dict) -> list[str]:
    errors = []
    with open(model_path, 'rb') as f:
        current_hash = hashlib.sha256(f.read()).hexdigest()
    
    # If the file itself is structure.json, it is self-consistent
    with open(model_path) as f:
        try:
            data = json.load(f)
            if "meta" in data and "schema_version" in data.get("meta", {}):
                return []
        except Exception:
            pass

    recorded_hash = calcs.get("source_hash")
    if recorded_hash and current_hash != recorded_hash:
        errors.append(
            f"SOURCE_HASH_MISMATCH: structural-model.json changed since "
            f"geometry was computed. Re-run geometry_engine.py."
        )
    return errors

def _check_geometry_coordinates(raw: str, calcs: dict) -> list[str]:
    errors = []
    map_match = re.search(r"<!--\s*COORDINATE MAP:\s*({.*?})\s*-->", raw, re.DOTALL)
    if not map_match:
        return []
    try:
        coord_map = json.loads(map_match.group(1))
    except json.JSONDecodeError:
        return ["COORDINATE_MAP_INVALID: Could not parse JSON from COORDINATE MAP comment."]
        
    svg_coords = calcs.get("svg_coordinates", {})
    if not svg_coords:
        return []
        
    for key, expected in svg_coords.items():
        if key in coord_map:
            try:
                found = float(coord_map[key])
                if abs(found - float(expected)) > 5.0:
                    errors.append(f"COORDINATE_DRIFT: {key} drifted. Expected {expected}, found {found}")
            except ValueError:
                pass
                
    canonical_grade = svg_coords.get("grade_y")
    if canonical_grade is not None:
        if "grade_y" in coord_map and float(coord_map["grade_y"]) != float(canonical_grade):
            errors.append(f"CANONICAL_GRADE_MISMATCH: SVG uses grade_y={coord_map['grade_y']} but canonical is {canonical_grade}.")
            
    return errors


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def validate(svg_path: str, model_path: str) -> list[str]:
    """
    Run all validation checks on a single SVG against structural-model.json.

    Args:
        svg_path: Path to the SVG file to validate.
        model_path: Path to context/staging/structural-model.json.

    Returns:
        List of error strings. Empty list means PASS.
    """
    with open(svg_path) as f:
        raw = f.read()

    with open(model_path) as f:
        model = json.load(f)

    calcs = _load_geometry_calcs(model_path)

    errors: list[str] = []
    errors.extend(_check_xml_validity(svg_path, raw))

    # Abort further checks if XML is broken — other checks will give false results
    if errors:
        return errors

    if calcs:
        errors.extend(_check_source_hash(model_path, calcs))
        errors.extend(_check_geometry_coordinates(raw, calcs))

    errors.extend(_check_dimension_labels(raw, model, calcs))
    errors.extend(_check_topology_count(raw, model))
    return errors


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Parse CLI arguments and run validation, printing results to stdout."""
    if len(sys.argv) < 3:
        print(
            "Usage: python3 scripts/svg_validator.py "
            "<svg_file> <path-to-structural-model.json>",
            file=sys.stderr,
        )
        sys.exit(1)

    svg_path, model_path = sys.argv[1], sys.argv[2]
    errors = validate(svg_path, model_path)

    if errors:
        print("VALIDATION FAILED:")
        for err in errors:
            print(f"  ✗ {err}")
        sys.exit(1)
    else:
        print(f"VALIDATION PASSED ✓  ({svg_path})")
        sys.exit(0)


if __name__ == "__main__":
    main()
