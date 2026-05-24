#!/usr/bin/env python3
"""
constraint_solver.py
====================
Named connection constraint checker for the garden-structure-designer pipeline.

Pipeline position:
    geometry_engine.py  (computes and seals geometry)
        ↓
    constraint_solver.py  (verifies sealed geometry satisfies connection requirements)
        ↓
    cad_scene.py  (builds 3D solids from sealed geometry)
        ↓
    render_drawings.py  (renders SVGs + PNGs)

Each constraint is a named function accepting the sealed structure dict and
returning a ConstraintResult.  Constraints work on structure.json data only —
they do NOT build a 3D scene, so they are fast and call-able before rendering.

Distinct roles:
  geometry_engine  → compute/seal geometry values
  constraint_solver → verify connection requirements against sealed values
  cad_scene.validate_scene_geometry → verify built 3D solids satisfy invariants
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Literal, TypedDict


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

class ConstraintResult(TypedDict):
    name: str
    status: Literal["PASS", "FAIL", "WARN", "SKIP"]
    detail: str


class ConstraintError(ValueError):
    """Raised by assert_connections_valid when any constraint has status FAIL."""


# ---------------------------------------------------------------------------
# Individual constraint functions
# ---------------------------------------------------------------------------

def _geometry_is_sealed(structure: dict) -> ConstraintResult:
    """Geometry must be sealed before connection solving."""
    if not structure.get("geometry", {}).get("_sealed"):
        return {
            "name": "geometry_is_sealed",
            "status": "FAIL",
            "detail": "geometry._sealed is False — run geometry_engine.py before constraint_solver",
        }
    return {
        "name": "geometry_is_sealed",
        "status": "PASS",
        "detail": "geometry._sealed == True",
    }


def _z_plane_ordering(structure: dict) -> ConstraintResult:
    """Z-planes must be strictly monotone: Z_GRADE < Z_POST_TOP < Z_BEAM_TOP < Z_APEX."""
    zp = structure.get("geometry", {}).get("joints", {}).get("z_planes", {})
    needed = ("Z_GRADE", "Z_POST_TOP", "Z_BEAM_TOP", "Z_APEX")
    missing = [k for k in needed if k not in zp]
    if missing:
        return {
            "name": "z_plane_ordering",
            "status": "FAIL",
            "detail": f"Missing Z-plane fields: {missing}",
        }
    Z_GRADE    = float(zp["Z_GRADE"])
    Z_POST_TOP = float(zp["Z_POST_TOP"])
    Z_BEAM_TOP = float(zp["Z_BEAM_TOP"])
    Z_APEX     = float(zp["Z_APEX"])
    if not (Z_GRADE < Z_POST_TOP < Z_BEAM_TOP < Z_APEX):
        return {
            "name": "z_plane_ordering",
            "status": "FAIL",
            "detail": (
                f"Z planes are not strictly ascending: "
                f"Z_GRADE={Z_GRADE}, Z_POST_TOP={Z_POST_TOP}, "
                f"Z_BEAM_TOP={Z_BEAM_TOP}, Z_APEX={Z_APEX}"
            ),
        }
    return {
        "name": "z_plane_ordering",
        "status": "PASS",
        "detail": (
            f"Z_GRADE={Z_GRADE} < Z_POST_TOP={Z_POST_TOP} "
            f"< Z_BEAM_TOP={Z_BEAM_TOP} < Z_APEX={Z_APEX}"
        ),
    }


def _hub_radius_within_beam_ring(structure: dict) -> ConstraintResult:
    """Hub polygon must fit inside the beam ring: hub_r < inscribed_r * cos(π/qty)."""
    geom   = structure.get("geometry", {})
    layout = structure.get("layout", {})
    hub_r       = float(geom.get("hub_radius_ft", 0.0))
    inscribed_r = float(layout.get("inscribed_radius_ft", 0.0))
    qty         = int(layout.get("post_count", 0))
    if inscribed_r <= 0 or qty < 3:
        return {
            "name": "hub_radius_within_beam_ring",
            "status": "SKIP",
            "detail": "Insufficient layout data (inscribed_radius_ft or post_count missing)",
        }
    beam_ring_r = inscribed_r * math.cos(math.pi / qty)
    if hub_r <= 0:
        return {
            "name": "hub_radius_within_beam_ring",
            "status": "FAIL",
            "detail": f"hub_radius_ft={hub_r} is zero or negative",
        }
    if hub_r >= beam_ring_r:
        return {
            "name": "hub_radius_within_beam_ring",
            "status": "FAIL",
            "detail": (
                f"hub_radius_ft={hub_r:.4f} >= beam_ring_r={beam_ring_r:.4f} ft — "
                "hub overflows or exactly matches beam ring radius"
            ),
        }
    return {
        "name": "hub_radius_within_beam_ring",
        "status": "PASS",
        "detail": f"hub_r={hub_r:.4f} ft < beam_ring_r={beam_ring_r:.4f} ft",
    }


def _brace_upper_endpoints_at_beam_soffit(structure: dict) -> ConstraintResult:
    """
    All brace upper endpoints (end[2]) must equal Z_POST_TOP within 1 inch.
    Uses the explicit endpoint coordinates stored in geometry.joints.braces.
    """
    zp         = structure.get("geometry", {}).get("joints", {}).get("z_planes", {})
    Z_POST_TOP = float(zp.get("Z_POST_TOP", 0.0))
    pairs      = (
        structure.get("geometry", {})
                 .get("joints", {})
                 .get("braces", {})
                 .get("endpoints", {})
                 .get("pairs", [])
    )
    if not pairs:
        return {
            "name": "brace_upper_endpoints_at_beam_soffit",
            "status": "SKIP",
            "detail": "No brace endpoint data in geometry.joints.braces.endpoints.pairs",
        }
    _IN_TOL = 1.0 / 12.0   # 1 inch in feet
    violations: list[str] = []
    for pair in pairs:
        brace_id = pair.get("brace_id", "?")
        end_z    = float(pair["end"][2])
        delta    = abs(end_z - Z_POST_TOP)
        if delta > _IN_TOL:
            violations.append(
                f"{brace_id}: end_z={end_z:.4f} differs from "
                f"Z_POST_TOP={Z_POST_TOP:.4f} by {delta * 12:.2f}\""
            )
    if violations:
        return {
            "name": "brace_upper_endpoints_at_beam_soffit",
            "status": "FAIL",
            "detail": "Brace upper endpoints not flush with beam soffit: " + "; ".join(violations),
        }
    return {
        "name": "brace_upper_endpoints_at_beam_soffit",
        "status": "PASS",
        "detail": f"All {len(pairs)} brace upper endpoints within 1\" of Z_POST_TOP={Z_POST_TOP:.4f}",
    }


def _beam_span_matches_post_chord(structure: dict) -> ConstraintResult:
    """
    geometry.spans.beam_span_ft must match 2 * inscribed_r * sin(π/qty) within 0.5 ft.
    SKIP if beam_span_ft is absent (field is optional in some schema versions).
    """
    geom      = structure.get("geometry", {})
    spans     = geom.get("spans", {})
    beam_span = float(spans.get("beam_span_ft", 0.0))
    if beam_span <= 0:
        return {
            "name": "beam_span_matches_post_chord",
            "status": "SKIP",
            "detail": "geometry.spans.beam_span_ft not present or zero",
        }
    layout      = structure.get("layout", {})
    inscribed_r = float(layout.get("inscribed_radius_ft", 0.0))
    qty         = int(layout.get("post_count", 0))
    if inscribed_r <= 0 or qty < 3:
        return {
            "name": "beam_span_matches_post_chord",
            "status": "SKIP",
            "detail": "Insufficient layout data",
        }
    expected = 2.0 * inscribed_r * math.sin(math.pi / qty)
    delta    = abs(beam_span - expected)
    if delta > 0.5:
        return {
            "name": "beam_span_matches_post_chord",
            "status": "WARN",
            "detail": (
                f"beam_span_ft={beam_span:.4f} deviates from post chord "
                f"{expected:.4f} ft by {delta:.4f} ft "
                f"(>0.5 ft threshold) — verify beam-to-post geometry"
            ),
        }
    return {
        "name": "beam_span_matches_post_chord",
        "status": "PASS",
        "detail": f"beam_span_ft={beam_span:.4f} ≈ post chord {expected:.4f} ft (Δ={delta:.4f})",
    }


# ---------------------------------------------------------------------------
# Composite public API
# ---------------------------------------------------------------------------

_ALL_CONSTRAINTS = [
    _geometry_is_sealed,
    _z_plane_ordering,
    _hub_radius_within_beam_ring,
    _brace_upper_endpoints_at_beam_soffit,
    _beam_span_matches_post_chord,
]


def solve_connections(structure: dict) -> list[ConstraintResult]:
    """
    Run all named connection constraints against a sealed structure dict.
    Returns the full result list — caller decides how to handle FAIL/WARN/SKIP.
    """
    return [fn(structure) for fn in _ALL_CONSTRAINTS]


def assert_connections_valid(structure: dict) -> None:
    """
    Run all constraints; raise ConstraintError with details if any result is FAIL.
    Call this after geometry_engine.py seals geometry and before build_structure_scene().
    """
    results  = solve_connections(structure)
    failures = [r for r in results if r["status"] == "FAIL"]
    if failures:
        lines = "\n".join(f"  [{r['name']}] {r['detail']}" for r in failures)
        raise ConstraintError(f"Connection constraints FAILED:\n{lines}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run connection constraint checks on a sealed structure.json."
    )
    parser.add_argument("structure", help="Path to sealed structure.json")
    parser.add_argument("--fail-on-warn", action="store_true",
                        help="Exit 1 if any constraint status is WARN (default: only FAIL)")
    args = parser.parse_args()

    with open(args.structure, encoding="utf-8") as f:
        structure = json.load(f)

    results = solve_connections(structure)

    print(f"{'CONSTRAINT':<45}  {'STATUS':<6}  DETAIL")
    print("-" * 100)
    any_fail = False
    for r in results:
        icon = "✓" if r["status"] == "PASS" else ("⚠" if r["status"] == "WARN" else ("✗" if r["status"] == "FAIL" else "–"))
        print(f"  {icon} {r['name']:<43}  {r['status']:<6}  {r['detail']}")
        if r["status"] == "FAIL":
            any_fail = True
        if r["status"] == "WARN" and args.fail_on_warn:
            any_fail = True

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    warned = sum(1 for r in results if r["status"] == "WARN")
    skipped = sum(1 for r in results if r["status"] == "SKIP")
    print()
    print(f"  {total} constraints: {passed} PASS, {failed} FAIL, {warned} WARN, {skipped} SKIP")
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
