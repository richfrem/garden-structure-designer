#!/usr/bin/env python3
"""
constraint_solver.py
====================

Purpose:
    Named connection constraint checker for the garden-structure-designer pipeline.
    Verifies sealed geometry from geometry_engine.py against physical joint requirements
    (Z-plane monotonicity, hub perimeter fit, brace plane alignment, zero CAD scene drift)
    before 3D scene construction or SVG rendering.

Layer: Execution / QA Gate

Key Input Dependencies:
    - context/staging/structure.json containing geometry._sealed == True
    - geometry.joints.resolved_model member coordinates and z-planes

Key Functions:
    solve_connections(structure: dict) -> list[ConstraintResult]
    assert_connections_valid(structure: dict) -> None
    vdist_pt(a, b) -> float
    check_single_brace_planes(b, posts, beams, tol) -> list[str]
    main() -> None

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/constraint_solver.py [structure.json] [--fail-on-warn]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Tuple, TypedDict

sys.path.append(str(Path(__file__).parent))
from path_utils import staging_dir


class ConstraintResult(TypedDict):
    name: str
    status: Literal["PASS", "FAIL", "WARN", "SKIP"]
    detail: str


class ConstraintError(ValueError):
    """Raised by assert_connections_valid when any constraint has status FAIL."""


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
    z_grade = float(zp["Z_GRADE"])
    z_post_top = float(zp["Z_POST_TOP"])
    z_beam_top = float(zp["Z_BEAM_TOP"])
    z_apex = float(zp["Z_APEX"])
    if not (z_grade < z_post_top < z_beam_top < z_apex):
        return {
            "name": "z_plane_ordering",
            "status": "FAIL",
            "detail": (
                f"Z planes are not strictly ascending: "
                f"Z_GRADE={z_grade}, Z_POST_TOP={z_post_top}, "
                f"Z_BEAM_TOP={z_beam_top}, Z_APEX={z_apex}"
            ),
        }
    return {
        "name": "z_plane_ordering",
        "status": "PASS",
        "detail": f"Z_GRADE={z_grade} < Z_POST_TOP={z_post_top} < Z_BEAM_TOP={z_beam_top} < Z_APEX={z_apex}",
    }


def _hub_radius_within_beam_ring(structure: dict) -> ConstraintResult:
    """Hub polygon must fit inside the beam ring: hub_r < inscribed_r * cos(π/qty)."""
    geom = structure.get("geometry", {})
    layout = structure.get("layout", {})
    hub_r = float(geom.get("hub_radius_ft") or 0.0)
    inscribed_r = float(layout.get("inscribed_radius_ft") or 0.0)
    qty = int(layout.get("post_count") or 0)
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
    """All brace upper endpoints must equal Z_POST_TOP within 1 inch."""
    zp = structure.get("geometry", {}).get("joints", {}).get("z_planes", {})
    z_post_top = float(zp.get("Z_POST_TOP") or 0.0)
    ep_data = structure.get("geometry", {}).get("joints", {}).get("braces", {}).get("endpoints", {})
    if isinstance(ep_data, dict):
        pairs = ep_data.get("pairs", [])
    elif isinstance(ep_data, list):
        pairs = ep_data
    else:
        pairs = []
    if not pairs:
        return {
            "name": "brace_upper_endpoints_at_beam_soffit",
            "status": "SKIP",
            "detail": "No brace endpoint data in geometry.joints.braces.endpoints.pairs",
        }
    in_tol = 1.0 / 12.0
    violations: List[str] = []
    for pair in pairs:
        brace_id = pair.get("brace_id", "?")
        end_z = float(pair["end"][2])
        delta = abs(end_z - z_post_top)
        if delta > in_tol:
            violations.append(f"{brace_id}: end_z={end_z:.4f} differs from Z_POST_TOP={z_post_top:.4f} by {delta * 12:.2f}\"")
    if violations:
        return {
            "name": "brace_upper_endpoints_at_beam_soffit",
            "status": "FAIL",
            "detail": "Brace upper endpoints not flush with beam soffit: " + "; ".join(violations),
        }
    return {
        "name": "brace_upper_endpoints_at_beam_soffit",
        "status": "PASS",
        "detail": f"All {len(pairs)} brace upper endpoints within 1\" of Z_POST_TOP={z_post_top:.4f}",
    }


def _beam_span_matches_post_chord(structure: dict) -> ConstraintResult:
    """Beam span must match 2 * inscribed_r * sin(π/qty) within 0.5 ft."""
    geom = structure.get("geometry", {})
    spans = geom.get("spans", {})
    beam_span = float(spans.get("beam_span_ft") or 0.0)
    if beam_span <= 0:
        return {
            "name": "beam_span_matches_post_chord",
            "status": "SKIP",
            "detail": "geometry.spans.beam_span_ft not present or zero",
        }
    layout = structure.get("layout", {})
    inscribed_r = float(layout.get("inscribed_radius_ft") or 0.0)
    qty = int(layout.get("post_count") or 0)
    if inscribed_r <= 0 or qty < 3:
        return {
            "name": "beam_span_matches_post_chord",
            "status": "SKIP",
            "detail": "Insufficient layout data",
        }
    expected = 2.0 * inscribed_r * math.sin(math.pi / qty)
    delta = abs(beam_span - expected)
    if delta > 0.5:
        return {
            "name": "beam_span_matches_post_chord",
            "status": "WARN",
            "detail": f"beam_span_ft={beam_span:.4f} deviates from post chord {expected:.4f} ft by {delta:.4f} ft",
        }
    return {
        "name": "beam_span_matches_post_chord",
        "status": "PASS",
        "detail": f"beam_span_ft={beam_span:.4f} ≈ post chord {expected:.4f} ft (Δ={delta:.4f})",
    }


def vdist_pt(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
    """Calculates Euclidean distance between two 3D points."""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def check_single_brace_planes(
    b: Dict[str, Any],
    posts: Dict[str, Any],
    beams: Dict[str, Any],
    tol: float,
) -> List[str]:
    """Validates that a single brace connects to post vertical face and beam bottom plane."""
    bid = b["id"]
    try:
        post_idx = int(bid[1:-1])
        qty = len(posts)
        suffix = bid[-1]
        post_id = f"P{post_idx}" if suffix == "A" else f"P{(post_idx % qty) + 1}"
        beam_id = f"B{post_idx}"
    except Exception as e:
        return [f"{bid}: Failed to parse post/beam connection: {e}"]

    if post_id not in posts or beam_id not in beams:
        return [f"{bid}: Connected post {post_id} or beam {beam_id} not found"]

    post = posts[post_id]
    beam = beams[beam_id]
    p0 = tuple(b["p0"])
    p1 = tuple(b["p1"])

    px, py = post["p0"][0], post["p0"][1]
    beam_dir = tuple(beam["axis_u"])
    ux, uy = (beam_dir[0], beam_dir[1]) if suffix == "A" else (-beam_dir[0], -beam_dir[1])

    post_w = vdist_pt(post["vertices"][0], post["vertices"][1])
    phw = post_w / 2.0
    pf_pt = (px + ux * phw, py + uy * phw, p0[2])
    pf_normal = (ux, uy, 0.0)

    violations = []
    dist_to_post_face = abs((p0[0] - pf_pt[0]) * pf_normal[0] + (p0[1] - pf_pt[1]) * pf_normal[1])
    if dist_to_post_face > tol:
        violations.append(f"{bid}: start point p0 is {dist_to_post_face * 12:.4f}\" off the post face")

    beam_soffit_z = post["p1"][2]
    dist_to_beam_soffit = abs(p1[2] - beam_soffit_z)
    if dist_to_beam_soffit > tol:
        violations.append(f"{bid}: end point p1 is {dist_to_beam_soffit * 12:.4f}\" off the beam soffit")

    return violations


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
        return {"name": "brace_endpoints_on_planes", "status": "PASS", "detail": "No braces to validate"}

    posts = {m["id"]: m for m in resolved.get("members", []) if m["role"] == "post"}
    beams = {m["id"]: m for m in resolved.get("members", []) if m["role"] == "beam"}
    tol = 1e-4

    violations: List[str] = []
    for b in braces:
        violations.extend(check_single_brace_planes(b, posts, beams, tol))

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
    """Verify CAD scene solid endpoints match resolved_model exactly."""
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
    violations: List[str] = []
    for solid in scene.solids:
        if solid.tag not in member_map:
            violations.append(f"{solid.tag}: not in resolved_model")
            continue
        rm = member_map[solid.tag]
        for coord, label in ((solid.p0, "p0"), (solid.p1, "p1")):
            expected = tuple(rm[label])
            dist = sum((a - b) ** 2 for a, b in zip(coord, expected)) ** 0.5
            if dist > 1e-6:
                violations.append(f"{solid.tag} {label} drifted {dist * 12:.4f}\" (scene={coord}, resolved={expected})")

    if violations:
        return {"name": "cad_scene_zero_drift", "status": "FAIL", "detail": "; ".join(violations)}
    return {
        "name": "cad_scene_zero_drift",
        "status": "PASS",
        "detail": f"All {len(member_map)} members match resolved_model endpoints",
    }


def _rafter_on_roof_planes(structure: dict) -> ConstraintResult:
    """All rafter solved points must lie on their assigned roof plane."""
    resolved = structure.get("geometry", {}).get("joints", {}).get("resolved_model", {})
    if not resolved:
        return {
            "name": "rafter_on_roof_planes",
            "status": "SKIP",
            "detail": "No resolved_model found — run geometry_engine first",
        }

    violations: List[str] = []
    for m in resolved.get("members", []):
        if m.get("role") != "rafter":
            continue
        cs = m.get("constraints_satisfied", {})
        for key in ("tail_on_roof_plane", "hub_on_roof_plane", "seat_on_roof_plane"):
            if key in cs and not cs[key]:
                violations.append(f"{m['id']}: {key} = False")

    if violations:
        return {"name": "rafter_on_roof_planes", "status": "FAIL", "detail": "; ".join(violations)}
    return {"name": "rafter_on_roof_planes", "status": "PASS", "detail": "All rafter members satisfy roof plane constraints"}


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
    """Runs all named connection constraints against a sealed structure dict."""
    return [fn(structure) for fn in _ALL_CONSTRAINTS]


def assert_connections_valid(structure: dict) -> None:
    """Runs all constraints and raises ConstraintError if any FAIL."""
    results = solve_connections(structure)
    failures = [r for r in results if r["status"] == "FAIL"]
    if failures:
        lines = "\n".join(f"  [{r['name']}] {r['detail']}" for r in failures)
        raise ConstraintError(f"Connection constraints FAILED:\n{lines}")


def main() -> None:
    """CLI entrypoint evaluating connection constraints on structure.json."""
    parser = argparse.ArgumentParser(description="Run connection constraint checks on a sealed structure.json.")
    parser.add_argument("structure", nargs="?", default=None, help="Path to sealed structure.json")
    parser.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="Exit 1 if any constraint status is WARN (default: only FAIL)",
    )
    args = parser.parse_args()

    struct_path = Path(args.structure) if args.structure else (staging_dir() / "structure.json")
    with open(struct_path, encoding="utf-8") as f:
        structure = json.load(f)

    results = solve_connections(structure)
    print(f"{'CONSTRAINT':<45}  {'STATUS':<6}  DETAIL")
    print("-" * 100)
    any_fail = False
    for r in results:
        icon = "✓" if r["status"] == "PASS" else ("⚠" if r["status"] == "WARN" else ("✗" if r["status"] == "FAIL" else "–"))
        print(f"  {icon} {r['name']:<43}  {r['status']:<6}  {r['detail']}")
        if r["status"] == "FAIL" or (r["status"] == "WARN" and args.fail_on_warn):
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
