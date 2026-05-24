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


def _brace_endpoints_on_planes(structure: dict) -> ConstraintResult:
    """Brace endpoints must lie exactly on their respective post and beam planes."""
    resolved = structure.get("geometry", {}).get("joints", {}).get("resolved_model", {})
    if not resolved:
        return {
            "name": "brace_endpoints_on_planes",
            "status": "SKIP",
            "detail": "No resolved_model found in geometry.joints",
        }
    
    braces = [m for m in resolved.get("members", []) if m["role"] == "brace"]
    if not braces:
        return {
            "name": "brace_endpoints_on_planes",
            "status": "PASS",
            "detail": "No braces to validate",
        }
        
    posts = {m["id"]: m for m in resolved.get("members", []) if m["role"] == "post"}
    beams = {m["id"]: m for m in resolved.get("members", []) if m["role"] == "beam"}
    
    violations: list[str] = []
    tol = 1e-4
    
    def vdist(a, b):
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)
        
    for b in braces:
        bid = b["id"]
        try:
            post_idx = int(bid[1:-1])
            qty = len(posts)
            suffix = bid[-1]
            if suffix == 'A':
                post_id = f"P{post_idx}"
                beam_id = f"B{post_idx}"
            else:
                post_id = f"P{(post_idx % qty) + 1}"
                beam_id = f"B{post_idx}"
        except Exception as e:
            violations.append(f"{bid}: Failed to parse post/beam connection: {e}")
            continue
            
        if post_id not in posts or beam_id not in beams:
            violations.append(f"{bid}: Connected post {post_id} or beam {beam_id} not found")
            continue
            
        post = posts[post_id]
        beam = beams[beam_id]
        
        p0 = tuple(b["p0"])
        p1 = tuple(b["p1"])
        
        px, py = post["p0"][0], post["p0"][1]
        dx, dy = p0[0] - px, p0[1] - py
        beam_dir = tuple(beam["axis_u"])
        ux, uy = beam_dir[0], beam_dir[1]
        if suffix == 'B':
            ux, uy = -ux, -uy
            
        post_w = vdist(post["vertices"][0], post["vertices"][1])
        phw = post_w / 2.0
        
        pf_pt = (px + ux * phw, py + uy * phw, p0[2])
        pf_normal = (ux, uy, 0.0)
        
        dist_to_post_face = abs((p0[0] - pf_pt[0]) * pf_normal[0] + (p0[1] - pf_pt[1]) * pf_normal[1])
        if dist_to_post_face > tol:
            violations.append(f"{bid}: start point p0 is {dist_to_post_face*12:.4f}\" off the post face")
            
        beam_soffit_z = post["p1"][2]
        dist_to_beam_soffit = abs(p1[2] - beam_soffit_z)
        if dist_to_beam_soffit > tol:
            violations.append(f"{bid}: end point p1 is {dist_to_beam_soffit*12:.4f}\" off the beam soffit")
            
    if violations:
        return {
            "name": "brace_endpoints_on_planes",
            "status": "FAIL",
            "detail": "Brace endpoints do not lie exactly on post/beam planes: " + "; ".join(violations),
        }
    return {
        "name": "brace_endpoints_on_planes",
        "status": "PASS",
        "detail": f"All {len(braces)} brace endpoints lie exactly on their constraint planes",
    }


def _cad_scene_zero_drift(structure: dict) -> ConstraintResult:
    """Verify CAD scene solid endpoints match resolved_model exactly (zero downstream math)."""
    resolved = structure.get("geometry", {}).get("joints", {}).get("resolved_model", {})
    if not resolved:
        return {
            "name": "cad_scene_zero_drift",
            "status": "SKIP",
            "detail": "No resolved_model found — run geometry_engine first",
        }
    try:
        from cad_scene import build_structure_scene
        scene = build_structure_scene(structure)
    except Exception as e:
        return {
            "name": "cad_scene_zero_drift",
            "status": "FAIL",
            "detail": f"Cannot build scene for drift check: {e}",
        }

    member_map = {m["id"]: m for m in resolved.get("members", [])}
    violations: list[str] = []
    for solid in scene.solids:
        if solid.tag not in member_map:
            violations.append(f"{solid.tag}: not in resolved_model")
            continue
        rm = member_map[solid.tag]
        for coord, label in ((solid.p0, "p0"), (solid.p1, "p1")):
            expected = tuple(rm[label])
            dist = sum((a - b) ** 2 for a, b in zip(coord, expected)) ** 0.5
            if dist > 1e-6:
                violations.append(
                    f"{solid.tag} {label} drifted {dist * 12:.4f}\" "
                    f"(scene={coord}, resolved={expected})"
                )

    if violations:
        return {
            "name": "cad_scene_zero_drift",
            "status": "FAIL",
            "detail": "; ".join(violations),
        }
    return {
        "name": "cad_scene_zero_drift",
        "status": "PASS",
        "detail": f"All {len(member_map)} members match resolved_model endpoints",
    }


def _rafter_on_roof_planes(structure: dict) -> ConstraintResult:
    """All rafter solved points must lie on their assigned roof plane (per constraints_satisfied)."""
    resolved = structure.get("geometry", {}).get("joints", {}).get("resolved_model", {})
    if not resolved:
        return {
            "name": "rafter_on_roof_planes",
            "status": "SKIP",
            "detail": "No resolved_model found — run geometry_engine first",
        }

    violations: list[str] = []
    for m in resolved.get("members", []):
        if m.get("role") != "rafter":
            continue
        cs = m.get("constraints_satisfied", {})
        for key in ("tail_on_roof_plane", "hub_on_roof_plane", "seat_on_roof_plane"):
            if key in cs and not cs[key]:
                violations.append(f"{m['id']}: {key} = False")

    if violations:
        return {
            "name": "rafter_on_roof_planes",
            "status": "FAIL",
            "detail": "; ".join(violations),
        }
    return {
        "name": "rafter_on_roof_planes",
        "status": "PASS",
        "detail": f"All rafter members satisfy roof plane constraints",
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
    _brace_endpoints_on_planes,
    _cad_scene_zero_drift,
    _rafter_on_roof_planes,
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
