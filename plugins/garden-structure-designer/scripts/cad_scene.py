#!/usr/bin/env python3
"""
cad_scene.py
============

Purpose:
    Pure-Python 3D CAD scene graph and geometric solid representations.
    Translates geometry compiler output (resolved_model) into Face and Solid
    primitives for 2D projective SVG rendering and view filtering.

Layer: Execution / Geometric Scene Translation

Key Input Dependencies:
    - structure.json containing geometry.joints.resolved_model
    - geometry_engine.py (for legacy conversion support)

Key Functions:
    vadd(a, b) -> V3
    vsub(a, b) -> V3
    vscl(a, s) -> V3
    vmul(a, s) -> V3
    vdot(a, b) -> float
    vcross(a, b) -> V3
    vlen(a) -> float
    vnorm(a) -> V3
    vdist(a, b) -> float
    vcent(pts) -> V3
    vfinite(v) -> bool
    v2_radius(v) -> float
    build_structure_scene(structure, is_blueprint=False) -> Scene
    validate_beam_alignment(solid, post_xy) -> None
    validate_brace_alignment(solid, post_xy, z_post_top, solids) -> None
    validate_scene_geometry(scene: Scene) -> None
    filter_scene_for_view(scene, mode, camera_dir=None) -> list[Solid]

Usage Examples:
    from cad_scene import build_structure_scene, validate_scene_geometry
    scene = build_structure_scene(structure_dict)
    validate_scene_geometry(scene)
"""
from __future__ import annotations

import math
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class GeometryError(ValueError):
    """Raised when a scene geometry invariant is violated."""


V3 = Tuple[float, float, float]


def vadd(a: V3, b: V3) -> V3:
    """Adds two 3D vectors component-wise."""
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vsub(a: V3, b: V3) -> V3:
    """Subtracts vector b from vector a component-wise."""
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def vscl(a: V3, s: float) -> V3:
    """Multiplies a 3D vector by a scalar value."""
    return (a[0] * s, a[1] * s, a[2] * s)


def vmul(a: V3, s: float) -> V3:
    """Alias for vscl: multiplies vector by scalar."""
    return (a[0] * s, a[1] * s, a[2] * s)


def vdot(a: V3, b: V3) -> float:
    """Computes Euclidean dot product of two 3D vectors."""
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vcross(a: V3, b: V3) -> V3:
    """Computes cross product of two 3D vectors."""
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def vlen(a: V3) -> float:
    """Calculates Euclidean length / magnitude of vector."""
    return math.sqrt(vdot(a, a))


def vnorm(a: V3) -> V3:
    """Normalizes vector to unit length, returning zero-vector if degenerate."""
    l = vlen(a)
    return vmul(a, 1.0 / l) if l > 1e-12 else (0.0, 0.0, 0.0)


def vdist(a: V3, b: V3) -> float:
    """Calculates Euclidean distance between two points."""
    return vlen(vsub(a, b))


def vcent(pts: List[V3]) -> V3:
    """Computes arithmetic centroid center of a list of points."""
    n = len(pts)
    return (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n, sum(p[2] for p in pts) / n)


def vfinite(v: V3) -> bool:
    """Returns True if all coordinates in vector are finite."""
    return all(math.isfinite(c) for c in v)


def v2_radius(v: V3) -> float:
    """Calculates horizontal radius in XY plane from origin."""
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


@dataclass
class Face:
    verts: List[V3]
    normal: V3
    color: str
    role: str
    tag: Optional[str]
    depth: float = 0.0


@dataclass
class Solid:
    role: str
    tag: str
    faces: List[Face] = field(default_factory=list)
    p0: V3 = (0.0, 0.0, 0.0)
    p1: V3 = (0.0, 0.0, 0.0)


@dataclass
class Scene:
    solids: List[Solid]
    qty: int
    hub_r: float
    Z_GRADE: float
    Z_POST_TOP: float
    Z_BEAM_TOP: float
    Z_APEX: float
    post_xy: List[Tuple[float, float]]


def _build_scene_legacy(model: dict, calcs: dict) -> Tuple[dict, dict]:
    """DEPRECATED: Builds (resolved_model, joints) from old dual-dict format."""
    warnings.warn(
        "build_structure_scene(model, calcs) is DEPRECATED. "
        "Pass a single structure.json dict that contains resolved_model.",
        DeprecationWarning,
        stacklevel=3,
    )
    members_sec = model.get("members", {})
    posts_sec = members_sec["posts"] if "posts" in members_sec else {}
    qty = posts_sec["quantity"] if "quantity" in posts_sec else 6

    dims_sec = model.get("dimensions", {})
    max_diag = dims_sec["max_diagonal_ft"] if "max_diagonal_ft" in dims_sec else 10.0
    r_ft = max_diag / 2.0

    tot_h_sec = calcs["total_height"] if "total_height" in calcs else {}
    post_h = tot_h_sec["post_ft"] if "post_ft" in tot_h_sec else 8.33
    beam_d = tot_h_sec["beam_depth_ft"] if "beam_depth_ft" in tot_h_sec else 0.604

    roof_r_sec = calcs["roof_rise"] if "roof_rise" in calcs else {}
    roof_r = roof_r_sec["rise_ft"] if "rise_ft" in roof_r_sec else 1.667

    bracing_sec = model.get("bracing", {})
    bracing_enabled = bracing_sec["enabled"] if "enabled" in bracing_sec else True

    structure_dict = {
        "layout": {"post_count": qty, "inscribed_radius_ft": r_ft},
        "members": {
            "posts": {"nominal_size": "6x6", "actual_width_in": 5.5, "actual_depth_in": 5.5, "cut_length_ft": post_h},
            "beams": {"nominal_size": "6x12", "actual_width_in": 6.0, "actual_depth_in": beam_d * 12.0},
        },
        "roof": {
            "pitch": f"{roof_r * 12.0 / r_ft:.6f}:12",
            "primary_rafters": {
                "count": qty,
                "nominal_size": "4x6",
                "actual_width_in": 3.5,
                "actual_depth_in": 5.5,
                "overhang_ft": 0.75,
            },
        },
        "hub": {"type": "polygonal", "radius_min_ft": 0.6},
        "bracing": {
            "enabled": bracing_enabled,
            "brace": {
                "nominal_size": "4x4",
                "actual_width_in": 3.5,
                "actual_depth_in": 3.5,
                "count_per_post": 2,
                "constraints": {"start_surface": "post_face", "end_surface": "beam_soffit", "run_ft": 1.5},
            },
        },
    }
    from geometry_engine import compute_joints, rafter_length, svg_layout

    cuts = {"miter_deg": 28.71, "bevel_deg": 9.1}
    rl = rafter_length(r_ft, 4, 12, 0.75)
    rise = {"rise_ft": roof_r}
    height = {"total_height_ft": post_h + beam_d + roof_r}
    hr = 0.75
    svg = svg_layout(height["total_height_ft"], r_ft, qty)
    joints = compute_joints(structure_dict, cuts, rl, rise, height, hr, svg)
    return joints["resolved_model"], joints


def _palettes(is_bp: bool) -> dict:
    """Returns color palettes for architectural presentation or technical blueprint."""
    if is_bp:
        return {
            "post": {"top": "#1e4272", "bottom": "#0d1e30", "left": "#162e50", "right": "#0f2238", "start": "#1a3560", "end": "#1a3560", "other": "#162e50"},
            "beam": {"top": "#1d3e68", "bottom": "#0c1d2e", "left": "#122840", "right": "#0d2035", "start": "#162e4e", "end": "#162e4e", "other": "#122840"},
            "rafter": {"top": "#1f4070", "bottom": "#0e2032", "left": "#132842", "right": "#0e2234", "start": "#172d4c", "end": "#172d4c", "other": "#132842"},
            "brace": {"top": "#1b3760", "bottom": "#0d1f32", "left": "#132440", "right": "#0e1e34", "start": "#162c4e", "end": "#162c4e", "other": "#132440"},
            "hub": {"top": "#204878", "bottom": "#0e2035", "left": "#1a3868", "right": "#152d56", "start": "#1d4070", "end": "#1d4070", "other": "#1a3868"},
            "purlin": {"top": "#1b3760", "bottom": "#0d1f32", "left": "#132440", "right": "#0e1e34", "start": "#162c4e", "end": "#162c4e", "other": "#132440"},
            "footing": {"top": "#183050", "bottom": "#0d1e30", "left": "#122440", "right": "#0e1e34", "start": "#162c4e", "end": "#162c4e", "other": "#122440"},
        }
    return {
        "post": {"top": "#f1e5cd", "bottom": "#c8b090", "left": "#ecdfc8", "right": "#e0c9a4", "start": "#e8dabc", "end": "#e8dabc", "other": "#ecdfc8"},
        "beam": {"top": "#e8d4b0", "bottom": "#b89070", "left": "#d4a878", "right": "#c89860", "start": "#d0a070", "end": "#d0a070", "other": "#d4a878"},
        "rafter": {"top": "#ddb892", "bottom": "#a87850", "left": "#c89870", "right": "#b88860", "start": "#c08060", "end": "#c08060", "other": "#c89870"},
        "brace": {"top": "#f0e4cc", "bottom": "#c0a080", "left": "#e8d8b8", "right": "#d8c4a0", "start": "#e0d0b0", "end": "#e0d0b0", "other": "#e8d8b8"},
        "hub": {"top": "#f5ecd8", "bottom": "#d0b888", "left": "#e8d8c0", "right": "#dcc8a8", "start": "#e4d4b8", "end": "#e4d4b8", "other": "#e8d8c0"},
        "purlin": {"top": "#f0e4cc", "bottom": "#c0a080", "left": "#e8d8b8", "right": "#d8c4a0", "start": "#e0d0b0", "end": "#e0d0b0", "other": "#e8d8b8"},
        "footing": {"top": "#e0e0e0", "bottom": "#b0b0b0", "left": "#d3d3d3", "right": "#c0c0c0", "start": "#c8c8c8", "end": "#c8c8c8", "other": "#d3d3d3"},
    }


def build_structure_scene(structure: dict, is_blueprint: bool = False) -> Scene:
    """Build the scene by strictly translating the resolved_model from Step 2."""
    if isinstance(is_blueprint, dict):
        resolved, joints = _build_scene_legacy(structure, is_blueprint)
        is_blueprint = False
    else:
        geom = structure.get("geometry", {})
        joints = geom.get("joints", {})
        resolved = joints.get("resolved_model", {})

    pal = _palettes(is_blueprint)

    if not resolved or not resolved.get("constraints_resolved"):
        raise GeometryError("MISSING_REQUIRED_GEOMETRY: geometry.joints.resolved_model must be fully resolved.")

    solids: List[Solid] = []
    for m in resolved["members"]:
        role = m["role"]
        bid = m["id"]
        role_pal = pal.get(role, pal.get("other", "#888888"))
        solid = Solid(role=role, tag=bid, p0=tuple(m["p0"]), p1=tuple(m["p1"]))
        for f in m["faces"]:
            verts = [tuple(m["vertices"][idx]) for idx in f["verts"]]
            color = role_pal if isinstance(role_pal, str) else role_pal.get(f["color_key"], role_pal.get("other", "#888888"))
            solid.faces.append(Face(verts=verts, normal=tuple(f["normal"]), color=color, role=role, tag=bid))
        solids.append(solid)

    zp = joints["z_planes"]
    layout = joints["layout"]
    return Scene(
        solids=solids,
        qty=layout["post_count"],
        hub_r=joints["hub"]["radius_ft"],
        Z_GRADE=zp["Z_GRADE"],
        Z_POST_TOP=zp["Z_POST_TOP"],
        Z_BEAM_TOP=zp["Z_BEAM_TOP"],
        Z_APEX=zp["Z_APEX"],
        post_xy=[tuple(xy) for xy in layout["post_xy"]],
    )


def validate_beam_alignment(solid: Solid, post_xy: List[Tuple[float, float]]) -> None:
    """Verifies that beam endpoints snap to the post grid layout points."""
    beam_post_snap = 0.125 / 12.0
    for end_pt, label in ((solid.p0, "p0"), (solid.p1, "p1")):
        nearest_dist = min(math.sqrt((end_pt[0] - px) ** 2 + (end_pt[1] - py) ** 2) for px, py in post_xy)
        if nearest_dist > beam_post_snap:
            raise GeometryError(f"Invariant 9: Beam {solid.tag} {label} XY is displaced from post grid")


def validate_brace_alignment(
    solid: Solid,
    post_xy: List[Tuple[float, float]],
    z_post_top: float,
    solids: List[Solid],
) -> None:
    """Verifies that knee braces connect properly between post vertical axis and beam soffit."""
    lower_pt = solid.p0 if solid.p0[2] <= solid.p1[2] else solid.p1
    nearest_dist = min(math.sqrt((lower_pt[0] - px) ** 2 + (lower_pt[1] - py) ** 2) for px, py in post_xy)
    if nearest_dist > 1.0:
        raise GeometryError(f"Invariant 10: Brace {solid.tag} lower foot is floating")

    upper_pt = solid.p0 if solid.p0[2] > solid.p1[2] else solid.p1
    if abs(upper_pt[2] - z_post_top) > 1.0 / 12.0:
        raise GeometryError(f"Invariant 10: Brace {solid.tag} upper head is floating")

    min_beam_dist = float("inf")
    for b in solids:
        if b.role == "beam":
            ax, ay, bx, by = b.p0[0], b.p0[1], b.p1[0], b.p1[1]
            px, py = upper_pt[0], upper_pt[1]
            dx, dy = bx - ax, by - ay
            ab2 = dx * dx + dy * dy
            if ab2 > 1e-6:
                t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / ab2))
                cx, cy = ax + t * dx, ay + t * dy
                dist = math.sqrt((px - cx) ** 2 + (py - cy) ** 2)
                if dist < min_beam_dist:
                    min_beam_dist = dist
    if min_beam_dist > 0.5:
        raise GeometryError(f"Invariant 10: Brace {solid.tag} upper head is floating")


def validate_scene_geometry(scene: Scene) -> None:
    """Ensures scene solids satisfy non-zero length and alignment invariants."""
    for s in scene.solids:
        if vdist(s.p0, s.p1) < 1e-6:
            raise GeometryError(f"zero-length member {s.tag}")
        if not all(vfinite(f.normal) for f in s.faces):
            raise GeometryError(f"Non-finite normal in {s.tag}")

        if s.role == "beam":
            validate_beam_alignment(s, scene.post_xy)
        elif s.role == "brace":
            validate_brace_alignment(s, scene.post_xy, scene.Z_POST_TOP, scene.solids)


class ViewMode(Enum):
    PRESENTATION = "presentation"
    STRUCTURAL = "structural"
    FABRICATION = "fabrication"


def filter_scene_for_view(
    scene: Scene,
    mode: ViewMode,
    camera_dir: Optional[Tuple[float, float, float]] = None,
) -> List[Solid]:
    """Filters solids based on sheet view mode and camera line-of-sight."""
    if mode in (ViewMode.STRUCTURAL, ViewMode.FABRICATION):
        return scene.solids

    visible = []
    braces = [s for s in scene.solids if s.role == "brace"]
    if braces and camera_dir:
        depths = [vdot(camera_dir, vcent([s.p0, s.p1])) for s in braces]
        b_min = min(depths)
        b_range = max(max(depths) - b_min, 1e-6)
    else:
        b_min = 0.0
        b_range = 1.0

    for s in scene.solids:
        if s.role == "purlin" or (s.role == "rafter" and (s.tag.startswith("Jack") or s.tag.startswith("J"))):
            continue
        if s.role == "brace" and camera_dir:
            if (vdot(camera_dir, vcent([s.p0, s.p1])) - b_min) / b_range < 0.45:
                continue
        visible.append(s)
    return visible
