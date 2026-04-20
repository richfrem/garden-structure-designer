#!/usr/bin/env python3
"""
geometry_engine.py
=====================================

Purpose:
    Canonical geometry calculator for the garden-structure-designer plugin.
    Computes all structural math (compound cut angles, rafter lengths, roof rise,
    SVG pixel coordinates) from a structural-model.json input file.

    This is the **Sole Source of Truth** for all dimensional calculations.
    Agent skills are forbidden from computing these values mentally.

Layer: Codify

Usage:
    python3 scripts/geometry_engine.py context/staging/structural-model.json

Output:
    Writes context/staging/geometry-calculations.json and prints JSON to stdout.
    Exits non-zero if warnings are raised (e.g. height limit breach).
"""
from __future__ import annotations

import json
import math
import os
import sys
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCALE_PX_PER_FT: float = 42.0  # standard plugin coordinate scale
GRADE_Y: int = 640              # canonical SVG grade baseline (pixels)
DEFAULT_BEAM_DEPTH_IN: float = 7.25
DEFAULT_POST_CUT_FT: float = 8.33
DEFAULT_SPAN_FT: float = 5.0
DEFAULT_OVERHANG_IN: float = 12.0
DEFAULT_PITCH: str = "4:12"
DEFAULT_SIDES: int = 6

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _deg(radians: float) -> float:
    """Convert radians to degrees."""
    return math.degrees(radians)


def _rad(degrees: float) -> float:
    """Convert degrees to radians."""
    return math.radians(degrees)


# ---------------------------------------------------------------------------
# Structural Math
# ---------------------------------------------------------------------------


def compound_cut(pitch_rise: float, pitch_run: float, sides: int) -> dict[str, float]:
    """
    Compute compound miter and bevel angles for a hip rafter at a regular polygon hub.

    Uses the canonical timber-framing formula:
        Miter = arctan(cos(pitch_angle) × tan(plan_half_angle))
        Bevel = arcsin(sin(pitch_angle) × sin(plan_half_angle))

    Source: Gross, M. "Roof Framing" (Tab Books, 1984); validated against
    Granlund & Bartholomew "Compound Angle Calculator for Regular Polygons."

    CRITICAL: For a hexagonal (sides=6) structure at 4:12 pitch:
        - pitch_angle  = 18.43°
        - plan_half    = 30°
        - Miter        = 28.71°  ← NOT 18.43° (common hallucination)
        - Bevel        = 9.10°   ← NOT 15.6°  (common hallucination)

    Args:
        pitch_rise: Numerator of the pitch ratio (e.g. 4 for 4:12).
        pitch_run: Denominator of the pitch ratio (e.g. 12 for 4:12).
        sides: Number of sides of the polygon (e.g. 6 for hexagon).

    Returns:
        Dictionary with miter_deg, bevel_deg, pitch_angle_deg, plan_half_angle_deg.
    """
    pitch_angle = math.atan(pitch_rise / pitch_run)
    plan_half = _rad(360.0 / (2.0 * sides))
    miter = math.atan(math.cos(pitch_angle) * math.tan(plan_half))
    bevel = math.asin(math.sin(pitch_angle) * math.sin(plan_half))
    return {
        "miter_deg": round(_deg(miter), 2),
        "bevel_deg": round(_deg(bevel), 2),
        "pitch_angle_deg": round(_deg(pitch_angle), 2),
        "plan_half_angle_deg": round(_deg(plan_half), 2),
    }


def rafter_length(
    run_ft: float,
    pitch_rise: float,
    pitch_run: float,
    overhang_ft: float = 0.0,
) -> dict[str, float]:
    """
    Compute actual rafter length from beam-bearing to tail (including overhang).

    Args:
        run_ft: Horizontal run from post centre-line to hub centre (feet).
        pitch_rise: Pitch rise numerator (e.g. 4).
        pitch_run: Pitch run denominator (e.g. 12).
        overhang_ft: Horizontal overhang beyond post CL (feet).

    Returns:
        Dictionary with structural_length_ft, total_with_overhang_ft,
        total_with_overhang_in.
    """
    slope_factor = math.sqrt(1 + (pitch_rise / pitch_run) ** 2)
    structural_ft = run_ft * slope_factor
    total_ft = (run_ft + overhang_ft) * slope_factor
    return {
        "structural_length_ft": round(structural_ft, 3),
        "total_with_overhang_ft": round(total_ft, 3),
        "total_with_overhang_in": round(total_ft * 12, 2),
    }


def roof_rise(
    run_ft: float,
    pitch_rise: float,
    pitch_run: float,
) -> dict[str, float]:
    """
    Compute vertical rise of the roof over a given horizontal run.

    Args:
        run_ft: Horizontal run from post CL to hub (feet).
        pitch_rise: Pitch rise numerator.
        pitch_run: Pitch run denominator.

    Returns:
        Dictionary with rise_ft and rise_in.
    """
    rise_ft = run_ft * (pitch_rise / pitch_run)
    return {
        "rise_ft": round(rise_ft, 3),
        "rise_in": round(rise_ft * 12, 2),
    }


def total_height(
    post_length_ft: float,
    beam_depth_in: float,
    roof_run_ft: float,
    pitch_rise: float,
    pitch_run: float,
) -> dict[str, float]:
    """
    Compute grade-to-apex total building height.

    Args:
        post_length_ft: Post cut length in feet.
        beam_depth_in: Beam depth in inches.
        roof_run_ft: Horizontal run from post to hub (feet).
        pitch_rise: Pitch rise numerator.
        pitch_run: Pitch run denominator.

    Returns:
        Dictionary with post_ft, beam_depth_ft, roof_rise_ft, total_height_ft,
        total_height_in.
    """
    beam_ft = beam_depth_in / 12.0
    rise_ft = roof_run_ft * (pitch_rise / pitch_run)
    total_ft = post_length_ft + beam_ft + rise_ft
    return {
        "post_ft": round(post_length_ft, 3),
        "beam_depth_ft": round(beam_ft, 3),
        "roof_rise_ft": round(rise_ft, 3),
        "total_height_ft": round(total_ft, 3),
        "total_height_in": round(total_ft * 12, 2),
    }


def svg_scale_map(
    structural_model: dict[str, Any],
    scale_px_per_ft: float = SCALE_PX_PER_FT,
) -> dict[str, Any]:
    """
    Derive canonical SVG pixel Y-coordinates from structural model values.

    All drawing-generator and shop-blueprint-generator agents must read their
    pixel coordinates from this output — never compute them independently.

    Args:
        structural_model: Parsed structural-model.json content.
        scale_px_per_ft: Pixels per foot (default 42.0).

    Returns:
        Dictionary mapping datum names to pixel coordinates.
    """
    # Support both 'members' (canonical schema) and 'structuralElements' (legacy)
    members = structural_model.get("members") or structural_model.get("structuralElements", {})
    posts = members.get("posts", {})
    beams = members.get("beams") or members.get("ringBeams", {})
    roof = members.get("roofStructure") or structural_model.get("roofStructure", {})

    post_ft = posts.get("cutLength_ft", DEFAULT_POST_CUT_FT)
    beam_in = beams.get("depth_in", DEFAULT_BEAM_DEPTH_IN)
    pitch_str = roof.get("pitch", DEFAULT_PITCH)
    rise_n, run_n = [int(x) for x in pitch_str.split(":")]
    span_ft = posts.get("spanDistance_ft", DEFAULT_SPAN_FT)

    post_px = post_ft * scale_px_per_ft
    beam_px = (beam_in / 12.0) * scale_px_per_ft
    rise_px = span_ft * (rise_n / run_n) * scale_px_per_ft

    return {
        "scale_px_per_ft": scale_px_per_ft,
        "grade_y": GRADE_Y,
        "post_top_y": round(GRADE_Y - post_px),
        "beam_soffit_y": round(GRADE_Y - post_px),
        "beam_top_y": round(GRADE_Y - post_px - beam_px),
        "hub_apex_y": round(GRADE_Y - post_px - beam_px - rise_px),
        "rise_px": round(rise_px),
        "beam_px": round(beam_px),
        "post_px": round(post_px),
    }


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------


def compute(model_path: str) -> dict[str, Any]:
    """
    Load structural-model.json and compute the full geometry calculation set.

    Args:
        model_path: Absolute or relative path to structural-model.json.

    Returns:
        Complete geometry-calculations dict ready for JSON serialisation.
    """
    with open(model_path) as f:
        model = json.load(f)

    # Support both 'members' (canonical) and 'structuralElements' (legacy)
    members = model.get("members") or model.get("structuralElements", {})
    posts = members.get("posts", {})
    beams = members.get("beams") or members.get("ringBeams", {})
    roof = members.get("roofStructure") or model.get("roofStructure", {})

    sides = posts.get("quantity", DEFAULT_SIDES)
    pitch = roof.get("pitch", DEFAULT_PITCH)
    pr, rr = [int(x) for x in pitch.split(":")]
    span_ft = posts.get("spanDistance_ft", DEFAULT_SPAN_FT)
    overhang_in = model.get("overhang_in", DEFAULT_OVERHANG_IN)
    beam_depth_in = beams.get("depth_in", DEFAULT_BEAM_DEPTH_IN)
    post_cut_ft = posts.get("cutLength_ft", DEFAULT_POST_CUT_FT)

    cuts = compound_cut(pr, rr, sides)
    rl = rafter_length(span_ft, pr, rr, overhang_in / 12.0)
    rise = roof_rise(span_ft, pr, rr)
    height = total_height(post_cut_ft, beam_depth_in, span_ft, pr, rr)
    svg = svg_scale_map(model)

    result: dict[str, Any] = {
        "schema": "geometry-calculations/1.0",
        "source": model_path,
        "pitch": pitch,
        "sides": sides,
        "compound_cut": cuts,
        "rafter": rl,
        "roof_rise": rise,
        "total_height": height,
        "svg_coordinates": svg,
        "warnings": [],
    }

    # Height limit guard — reads from sibling design-spec.json if present
    design_spec_path = os.path.join(os.path.dirname(model_path), "design-spec.json")
    if os.path.exists(design_spec_path):
        with open(design_spec_path) as f:
            spec = json.load(f)
        limit = spec.get("heightConstraints", {}).get("totalHeightLimit_ft")
        if limit and height["total_height_ft"] > limit:
            result["warnings"].append(
                f"FAIL: total_height_ft={height['total_height_ft']:.3f} "
                f"exceeds design-spec limit of {limit} ft."
            )

    return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Parse CLI arguments, compute geometry, write output file, exit."""
    if len(sys.argv) < 2:
        print(
            "Usage: python3 scripts/geometry_engine.py "
            "<path-to-structural-model.json>",
            file=sys.stderr,
        )
        sys.exit(1)

    model_path = sys.argv[1]
    result = compute(model_path)

    out_path = os.path.join(os.path.dirname(model_path), "geometry-calculations.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))

    if result.get("warnings"):
        print("\n⚠️  WARNINGS:", file=sys.stderr)
        for w in result["warnings"]:
            print(f"  {w}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
