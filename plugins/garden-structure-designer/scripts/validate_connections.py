#!/usr/bin/env python3
"""
validate_connections.py
=======================

Purpose:
    Hard pre-render gate: verifies physical surface contact and architectural coherence on the CAD
    scene built from the resolved model: beam soffits sit on the post tops, rafter tips land on the
    hub face radius, brace feet reach a post. With the structure.json it also reports seating and
    brace-foot warnings. Tolerances come from constants.py (CONTACT_*).

Layer: Execution / QA Gate (pre-render)

Key Input Dependencies:
    - context/staging/structure.json (geometry.joints.resolved_model, members.posts, layout)
    - cad_scene.py (Scene and vector helpers), constants.py, path_utils.py

Key Functions:
    validate_connections(scene, structure=None) -> list[str] | tuple[list[str], list[str]]
        (errors only without ``structure``; (errors, warnings) with it)
    assert_connections_physical(scene) -> None          raises ContactError
    main() -> None
    _check_beam_soffits(scene) -> list[str]             _check_rafter_tips(scene) -> list[str]
    _check_brace_feet(scene) -> list[str]               _structure_warnings(scene, structure) -> list[str]

Usage Examples:
    python3 validate_connections.py [structure.json]
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from cad_scene import Scene, build_structure_scene, v2_radius
from constants import (
    CONTACT_BEAM_SOFFIT_TOL_FT,
    CONTACT_BRACE_FOOT_MAX_FT,
    CONTACT_BRACE_RADIUS_WARN_FT,
    CONTACT_RAFTER_TIP_TOL_FT,
    CONTACT_SEAT_WARN_RANGE_FT,
)
from path_utils import staging_dir


class ContactError(ValueError):
    """Exception raised when physical contact validations fail."""


def assert_connections_physical(scene: Scene) -> None:
    """Raises ContactError listing every physical-contact error found in ``scene``."""
    errors = validate_connections(scene)
    if errors:
        raise ContactError(f"PHYSICAL CONTACT VALIDATION FAILED — {len(errors)} error(s):\n" + "\n".join(errors))


def _check_beam_soffits(scene: Scene) -> list[str]:
    """Every beam's bottom face must sit at Z_POST_TOP."""
    errors: list[str] = []
    for s in (s for s in scene.solids if s.role == "beam"):
        for f in (f for f in s.faces if f.normal[2] < -0.8):  # bottom faces
            for v in f.verts:
                if abs(v[2] - scene.Z_POST_TOP) > CONTACT_BEAM_SOFFIT_TOL_FT:
                    errors.append(f"beam_soffit: Beam {s.tag} bottom face is lifted (Z={v[2]:.4f}, expected {scene.Z_POST_TOP:.4f})")
                    break
    return errors


def _check_rafter_tips(scene: Scene) -> list[str]:
    """Primary rafter tips must land on the hub face radius (only when the scene has a hub)."""
    if not any(s.role == "hub" for s in scene.solids):
        return []
    hub_r_face = scene.hub_r * math.cos(math.pi / scene.qty)
    errors: list[str] = []
    for s in (s for s in scene.solids if s.role == "rafter" and not s.tag.startswith("J")):
        xy_r = v2_radius(s.p1)
        if abs(xy_r - hub_r_face) > CONTACT_RAFTER_TIP_TOL_FT:
            errors.append(f"rafter_tip: Rafter {s.tag} apex is disconnected from hub face (radius={xy_r:.4f}, expected {hub_r_face:.4f})")
    return errors


def _check_brace_feet(scene: Scene) -> list[str]:
    """Every brace's lower foot must be near a post."""
    errors: list[str] = []
    for s in (s for s in scene.solids if s.role == "brace"):
        lower_pt = s.p0 if s.p0[2] <= s.p1[2] else s.p1
        nearest = min(math.hypot(lower_pt[0] - px, lower_pt[1] - py) for px, py in scene.post_xy)
        if nearest > CONTACT_BRACE_FOOT_MAX_FT:
            errors.append(f"brace_foot: Brace {s.tag} lower foot is floating far from post face")
    return errors


def _structure_warnings(scene: Scene, structure: dict) -> list[str]:
    """Seating and brace-foot warnings derived from the resolved model in structure.json."""
    resolved = structure.get("geometry", {}).get("joints", {}).get("resolved_model")
    if not resolved:
        return []
    warnings: list[str] = []
    low, high = CONTACT_SEAT_WARN_RANGE_FT
    for m in resolved["members"]:
        if m["role"] == "rafter":
            for f in (f for f in m["faces"] if f["normal"][2] < -0.8):
                avg_z = sum(m["vertices"][idx][2] for idx in f["verts"]) / len(f["verts"])
                if low < abs(avg_z - scene.Z_BEAM_TOP) < high:
                    warnings.append(f"seating: {m['id']} seat at Z={avg_z:.3f} (expected {scene.Z_BEAM_TOP:.3f})")
        elif m["role"] == "brace":
            d_cl = v2_radius(tuple(m["p0"]))
            expected_r = structure["layout"]["inscribed_radius_ft"] - structure["members"]["posts"]["actual_width_in"] / 24.0
            if abs(d_cl - expected_r) > CONTACT_BRACE_RADIUS_WARN_FT:
                warnings.append(f"brace_foot: {m['id']} foot at {d_cl*12:.1f}\" radius")
    return warnings


def validate_connections(scene: Scene, structure: dict | None = None) -> list[str] | tuple[list[str], list[str]]:
    """Physical-contact checks; returns errors, or (errors, warnings) when ``structure`` is supplied."""
    errors = _check_beam_soffits(scene) + _check_rafter_tips(scene) + _check_brace_feet(scene)
    if structure is not None:
        return errors, _structure_warnings(scene, structure)
    return errors


def main() -> None:
    """CLI entrypoint: build the scene from structure.json, print warnings/errors, exit 1 on errors."""
    struct_path = sys.argv[1] if len(sys.argv) > 1 else str(staging_dir() / "structure.json")
    with open(struct_path) as f: structure = json.load(f)
    errors, warnings = validate_connections(build_structure_scene(structure, False), structure)
    if warnings:
        print(f"VALIDATION WARNINGS — {len(warnings)} issue(s):")
        for w in warnings: print(f"  ⚠ {w}")
    if errors:
        print(f"PHYSICAL CONTACT VALIDATION FAILED — {len(errors)} error(s):")
        for e in errors: print(f"  ✗ {e}")
        sys.exit(1)
    print("PHYSICAL CONTACT VALIDATION PASSED ✓")
    sys.exit(0)


if __name__ == "__main__": main()
