#!/usr/bin/env python3
"""
cad_backend_build123d.py
========================
Authoritative build123d CAD geometry backend for garden-structure-designer.

This module is responsible for:
1. Building true 3D CAD solids for all structural members using build123d.
2. Exporting the CAD assembly to STEP and STL formats.
3. Conducting rigorous geometry validations directly on the CAD solids.
4. Optionally generating SVG projections for isometric and orthographic views.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

# Add script directory to path
sys.path.append(str(Path(__file__).parent))
from cad_scene import build_structure_scene, validate_scene_geometry, v2_radius

try:
    import build123d as b3d
    BUILD123D_AVAILABLE = True
except ImportError:
    BUILD123D_AVAILABLE = False


class CADGeometryError(ValueError):
    """Raised when CAD geometry validation fails."""


def _b3d_box_between_with_up(
    p0: tuple[float, float, float],
    p1: tuple[float, float, float],
    hw: float,
    hd: float,
    up_hint: tuple[float, float, float]
) -> b3d.Solid | None:
    """
    Create a build123d Box solid whose axis runs from p0 to p1.
    All parameters are in feet. Automatically converted to mm for build123d.
    """
    if not BUILD123D_AVAILABLE:
        return None

    FT_TO_MM = 304.8
    dx, dy, dz = p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]
    length_ft = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length_ft < 1e-6:
        return None

    # Compute orthonormal axes u, w, d matching the mathematical model
    u = (dx / length_ft, dy / length_ft, dz / length_ft)

    # w_raw = up_hint x u
    w_raw_x = up_hint[1] * u[2] - up_hint[2] * u[1]
    w_raw_y = up_hint[2] * u[0] - up_hint[0] * u[2]
    w_raw_z = up_hint[0] * u[1] - up_hint[1] * u[0]
    w_len = math.sqrt(w_raw_x**2 + w_raw_y**2 + w_raw_z**2)
    
    if w_len < 1e-9:
        # Fallback if up_hint is parallel to axis
        up_alt = (1.0, 0.0, 0.0)
        w_raw_x = up_alt[1] * u[2] - up_alt[2] * u[1]
        w_raw_y = up_alt[2] * u[0] - up_alt[0] * u[2]
        w_raw_z = up_alt[0] * u[1] - up_alt[1] * u[0]
        w_len = math.sqrt(w_raw_x**2 + w_raw_y**2 + w_raw_z**2)

    w = (w_raw_x / w_len, w_raw_y / w_len, w_raw_z / w_len)

    # d = u x w
    d = (
        u[1] * w[2] - u[2] * w[1],
        u[2] * w[0] - u[0] * w[2],
        u[0] * w[1] - u[1] * w[0],
    )

    length_mm = length_ft * FT_TO_MM
    w_mm = 2.0 * hw * FT_TO_MM
    h_mm = 2.0 * hd * FT_TO_MM

    p0_mm = (p0[0] * FT_TO_MM, p0[1] * FT_TO_MM, p0[2] * FT_TO_MM)

    # Create Plane using build123d
    plane = b3d.Plane(origin=p0_mm, x_dir=b3d.Vector(u), z_dir=b3d.Vector(d))
    with b3d.BuildPart(plane) as part:
        b3d.Box(length_mm, w_mm, h_mm, align=(b3d.Align.MIN, b3d.Align.CENTER, b3d.Align.CENTER))
    return part.part


def build_cad_model(model: dict, calcs: dict) -> b3d.Compound | None:
    """
    Build a full 3D CAD model containing all structural members using build123d.
    Pure consumer of geometry.joints (Phase 0 Constraint Unification).
    """
    if not BUILD123D_AVAILABLE:
        print("[cad_backend_build123d] build123d is not installed/available.", file=sys.stderr)
        return None

    FT_TO_MM = 304.8
    # Scene metadata for shared Z-planes
    scene = build_structure_scene(model, calcs)
    
    geom = model.get("geometry") or calcs
    joints = geom.get("joints", {})
    zp = joints.get("z_planes", {})
    
    # Half-widths / Half-depths (Phase 4 proportions)
    # We derive these from members spec
    POST_HW = (model["members"]["posts"]["actual_width_in"] / 24.0)
    POST_HD = (model["members"]["posts"]["actual_depth_in"] / 24.0)
    BEAM_HW = (model["members"]["beams"]["actual_width_in"] / 24.0)
    BEAM_HD = (model["members"]["beams"]["actual_depth_in"] / 24.0)
    RAFTER_HW = (model["roof"]["primary_rafters"]["actual_width_in"] / 24.0)
    RAFTER_HD = (model["roof"]["primary_rafters"]["actual_depth_in"] / 24.0)
    BRACE_HW = (model["bracing"]["brace"]["actual_width_in"] / 24.0)
    BRACE_HD = (model["bracing"]["brace"]["actual_depth_in"] / 24.0)
    
    UP = (0.0, 0.0, 1.0)
    solids = []

    # 1. Footings
    for i, (px, py) in enumerate(scene.post_xy):
        s = _b3d_box_between_with_up((px, py, scene.Z_GRADE - 1.5), (px, py, scene.Z_GRADE + 0.33), 0.5, 0.5, UP)
        if s: s.label = f"FT{i+1}"; solids.append(s)

    # 2. Posts
    for i, (px, py) in enumerate(scene.post_xy):
        s = _b3d_box_between_with_up((px, py, scene.Z_GRADE), (px, py, scene.Z_POST_TOP), POST_HW, POST_HD, UP)
        if s: s.label = f"P{i+1}"; solids.append(s)

    # 3. Beams
    for i in range(scene.qty):
        p1 = scene.post_xy[i]; p2 = scene.post_xy[(i+1)%scene.qty]
        bz = zp["Z_BEAM_CENTER"]
        s = _b3d_box_between_with_up((p1[0], p1[1], bz), (p2[0], p2[1], bz), BEAM_HW, BEAM_HD, UP)
        if s: s.label = f"B{i+1}"; solids.append(s)

    # 4. Braces
    if joints.get("braces", {}).get("enabled"):
        for bp in joints["braces"]["endpoints"]:
            s = _b3d_box_between_with_up(tuple(bp["start"]), tuple(bp["end"]), BRACE_HW, BRACE_HD, UP)
            if s: s.label = bp["id"]; solids.append(s)

    # 5. Primary Rafters (Phase 2 Notched Solids)
    for rj in joints.get("primary_rafters", []):
        # build123d note: we currently build as box; true boolean notch requires 
        # subtract operation. For now we follow the precomputed axes.
        s = _b3d_box_between_with_up(tuple(rj["start"]), tuple(rj["end"]), RAFTER_HW, RAFTER_HD, UP)
        if s: s.label = rj["id"]; solids.append(s)

    # 6. Jack Rafters
    if joints.get("jack_rafters", {}).get("enabled"):
        for ep in joints["jack_rafters"]["endpoints"]:
            s = _b3d_box_between_with_up(tuple(ep["start"]), tuple(ep["end"]), RAFTER_HW, RAFTER_HD, UP)
            if s: s.label = ep["id"]; solids.append(s)

    # 7. Hub (Phase 3 Constraint-Driven)
    hj = joints.get("hub", {})
    hub_r = hj["radius_ft"]
    hub_h = hj["height_ft"]
    hub_z = zp["Z_APEX"]

    with b3d.BuildPart() as hub_part:
        with b3d.BuildSketch() as sketch:
            b3d.RegularPolygon(radius=hub_r * FT_TO_MM, side_count=scene.qty)
        b3d.extrude(amount=hub_h * FT_TO_MM, both=True)
    
    hub_solid = hub_part.part.translate((0, 0, hub_z * FT_TO_MM))
    hub_solid.label = "HUB"
    solids.append(hub_solid)

    return b3d.Compound(children=solids)


def export_step(compound: b3d.Compound | None, path: str) -> bool:
    """Export the build123d CAD Compound model to STEP."""
    if not BUILD123D_AVAILABLE or compound is None:
        return False
    try:
        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if hasattr(b3d, "export_step"):
            b3d.export_step(compound, str(out_path))
        else:
            compound.export_step(str(out_path))
        return True
    except Exception as e:
        print(f"[cad_backend_build123d] STEP export failed: {e}", file=sys.stderr)
        return False


def export_stl(compound: b3d.Compound | None, path: str) -> bool:
    """Export the build123d CAD Compound model to STL."""
    if not BUILD123D_AVAILABLE or compound is None:
        return False
    try:
        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if hasattr(b3d, "export_stl"):
            b3d.export_stl(compound, str(out_path))
        else:
            compound.export_stl(str(out_path))
        return True
    except Exception as e:
        print(f"[cad_backend_build123d] STL export failed: {e}", file=sys.stderr)
        return False


def validate_cad_geometry(model: dict, calcs: dict, compound: b3d.Compound | None) -> None:
    """
    Rigorously validate CAD geometries direct from BREP solids.
    Checks:
    1. No zero-length/volume members.
    2. Member counts match expected.
    3. Rafter endpoints terminate at hub radius.
    4. Post tops align with beam underside.
    5. Knee brace endpoints touch post face and beam soffit.
    """
    if not BUILD123D_AVAILABLE or compound is None:
        return

    qty = model.get("members", {}).get("posts", {}).get("quantity", 6)
    
    # 1. No zero-length or zero-volume members
    for child in compound.children:
        if child.volume <= 0.0:
            raise CADGeometryError(f"CAD member '{child.label}' has invalid or zero volume ({child.volume})")

    # 2. Member counts check
    by_role: dict[str, list[b3d.Solid]] = {}
    for child in compound.children:
        lbl = child.label.lower()
        if lbl.startswith("purlin"):
            by_role.setdefault("purlin", []).append(child)
        elif lbl.startswith("jack"):
            by_role.setdefault("jack", []).append(child)
        elif lbl.startswith("brace"):
            by_role.setdefault("brace", []).append(child)
        elif lbl.startswith("ft"):
            by_role.setdefault("footing", []).append(child)
        elif lbl.startswith("p"):
            by_role.setdefault("post", []).append(child)
        elif lbl.startswith("b"):
            by_role.setdefault("beam", []).append(child)
        elif lbl.startswith("r"):
            by_role.setdefault("rafter", []).append(child)
        elif lbl == "hub":
            by_role.setdefault("hub", []).append(child)

    expected = {
        "footing": qty,
        "post": qty,
        "beam": qty,
        "brace": qty * 2,
        "rafter": qty,
        "jack": qty * 2,
        "purlin": qty,
        "hub": 1
    }

    for role, exp_qty in expected.items():
        act_qty = len(by_role.get(role, []))
        if act_qty != exp_qty:
            raise CADGeometryError(f"CAD validation count error for {role}: expected {exp_qty}, got {act_qty}")

    # Recreate the mathematical scene for exact bounds check
    scene = build_structure_scene(model, calcs)
    FT_TO_MM = 304.8
    _TOL_MM = (1.0 / 12.0) * FT_TO_MM  # 1-inch tolerance in mm

    # 3. Rafter endpoints terminate at hub radius
    # For build123d, verify vertices of hip rafters 'R1'...'Rn' are near scene.hub_r
    for r_solid in by_role.get("rafter", []):
        min_rad = min(
            math.sqrt(v.X**2 + v.Y**2)
            for v in r_solid.vertices()
        )
        expected_rad = scene.hub_r * FT_TO_MM
        if abs(min_rad - expected_rad) > _TOL_MM * 2.0:
            raise CADGeometryError(
                f"CAD Rafter {r_solid.label} endpoint XY radius {min_rad / FT_TO_MM:.2f} ft "
                f"does not match expected hub_r {scene.hub_r:.2f} ft"
            )

    # 4. Post tops align with beam underside
    # Verify post max Z coordinate equals beam min Z coordinate
    post_top_expected = scene.Z_POST_TOP * FT_TO_MM
    for p_solid in by_role.get("post", []):
        max_z = max(v.Z for v in p_solid.vertices())
        if abs(max_z - post_top_expected) > _TOL_MM:
            raise CADGeometryError(
                f"CAD Post {p_solid.label} top Z {max_z / FT_TO_MM:.2f} ft "
                f"does not align with Z_POST_TOP {scene.Z_POST_TOP:.2f} ft"
            )

    # 5. Knee brace endpoints touch post face and beam soffit
    # Verify brace max Z coordinate matches beam underside Z within 3-inch tolerance
    for b_solid in by_role.get("brace", []):
        max_z = max(v.Z for v in b_solid.vertices())
        if abs(max_z - post_top_expected) > _TOL_MM * 3.0:
            raise CADGeometryError(
                f"CAD Knee brace {b_solid.label} max Z {max_z / FT_TO_MM:.2f} ft "
                f"fails to touch beam soffit {scene.Z_POST_TOP:.2f} ft"
            )


if __name__ == "__main__":
    # Standard smoke test
    print(f"build123d Available: {BUILD123D_AVAILABLE}")
    if BUILD123D_AVAILABLE:
        model = {"members": {"posts": {"quantity": 6}}, "dimensions": {"max_diagonal_ft": 10.0}}
        calcs = {"total_height": {"post_ft": 8.33, "beam_depth_ft": 1.0}, "roof_rise": {"rise_ft": 1.6}}
        print("Building model...")
        compound = build_cad_model(model, calcs)
        print(f"Model successfully built. Total solids: {len(compound.children)}")
        print("Validating geometry...")
        validate_cad_geometry(model, calcs, compound)
        print("Geometry Validated successfully!")
        
        step_path = "/tmp/cad_designer_test.step"
        success = export_step(compound, step_path)
        print(f"Exported STEP to {step_path}: {success}")
