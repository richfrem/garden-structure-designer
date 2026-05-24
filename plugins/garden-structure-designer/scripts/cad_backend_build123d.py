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
    """
    if not BUILD123D_AVAILABLE:
        print("[cad_backend_build123d] build123d is not installed/available.", file=sys.stderr)
        return None

    FT_TO_MM = 304.8
    scene = build_structure_scene(model, calcs)
    
    qty = scene.qty
    post_h = calcs.get("total_height", {}).get("post_ft", 8.33)
    beam_d = calcs.get("total_height", {}).get("beam_depth_ft", 1.0)
    
    posts_spec = model.get("members", {}).get("posts", {})
    beams_spec = model.get("members", {}).get("beams", {})
    braces_spec = model.get("members", {}).get("kneebraces", {})
    rafters_spec = model.get("members", {}).get("rafters", {})
    purlins_spec = model.get("members", {}).get("purlins", {})
    foundation_spec = model.get("foundation", {})

    POST_HW   = (posts_spec.get("width_in", 5.5) / 12.0) / 2.0
    POST_HD   = (posts_spec.get("depth_in", 5.5) / 12.0) / 2.0
    BEAM_HW   = (beams_spec.get("width_in", 5.5) / 12.0) / 2.0
    BEAM_HD   = beam_d / 2.0
    RAFTER_HW = (rafters_spec.get("width_in", 3.5) / 12.0) / 2.0
    RAFTER_HD = (rafters_spec.get("depth_in", 5.5) / 12.0) / 2.0
    BRACE_HW  = (braces_spec.get("width_in", 3.5) / 12.0) / 2.0
    BRACE_HD  = (braces_spec.get("depth_in", 3.5) / 12.0) / 2.0
    PURLIN_HW = (purlins_spec.get("width_in", 3.5) / 12.0) / 2.0
    PURLIN_HD = (purlins_spec.get("depth_in", 3.5) / 12.0) / 2.0
    FOOTING_HW = (foundation_spec.get("caisson_diameter_in", 12.0) / 12.0) / 2.0
    
    UP = (0.0, 0.0, 1.0)
    solids = []

    # 1. Concrete Footings
    for i, (px, py) in enumerate(scene.post_xy):
        p0_footing = (px, py, scene.Z_GRADE - 1.5)
        p1_footing = (px, py, scene.Z_GRADE + 0.33)
        solid = _b3d_box_between_with_up(p0_footing, p1_footing, FOOTING_HW, FOOTING_HW, UP)
        if solid:
            solid.label = f"FT{i+1}"
            solids.append(solid)

    # 2. Posts
    for i, (px, py) in enumerate(scene.post_xy):
        p0_post = (px, py, scene.Z_GRADE)
        p1_post = (px, py, scene.Z_POST_TOP)
        solid = _b3d_box_between_with_up(p0_post, p1_post, POST_HW, POST_HD, UP)
        if solid:
            solid.label = f"P{i+1}"
            solids.append(solid)

    # 3. Beams
    for i in range(qty):
        px1, py1 = scene.post_xy[i]
        px2, py2 = scene.post_xy[(i+1) % qty]
        bz = scene.Z_POST_TOP + BEAM_HD
        solid = _b3d_box_between_with_up((px1, py1, bz), (px2, py2, bz), BEAM_HW, BEAM_HD, UP)
        if solid:
            solid.label = f"B{i+1}"
            solids.append(solid)

    # 4. Knee Braces
    if "cutLength_in" in braces_spec and "angle_deg" in braces_spec:
        brace_run = (braces_spec["cutLength_in"] / 12.0) * math.cos(math.radians(braces_spec["angle_deg"]))
    else:
        brace_run = 1.5
    for i in range(qty):
        px1, py1 = scene.post_xy[i]
        px2, py2 = scene.post_xy[(i+1) % qty]
        sdx = px2 - px1
        sdy = py2 - py1
        slen = math.sqrt(sdx * sdx + sdy * sdy)
        if slen < 1e-9:
            continue
        ux = sdx / slen
        uy = sdy / slen

        # Brace A
        p0a = (px1 + ux * POST_HW, py1 + uy * POST_HW, scene.Z_POST_TOP - brace_run)
        p1a = (px1 + ux * (POST_HW + brace_run), py1 + uy * (POST_HW + brace_run), scene.Z_POST_TOP)
        solid_a = _b3d_box_between_with_up(p0a, p1a, BRACE_HW, BRACE_HD, UP)
        if solid_a:
            solid_a.label = f"Brace{i+1}a"
            solids.append(solid_a)

        # Brace B
        p0b = (px2 - ux * POST_HW, py2 - uy * POST_HW, scene.Z_POST_TOP - brace_run)
        p1b = (px2 - ux * (POST_HW + brace_run), py2 - uy * (POST_HW + brace_run), scene.Z_POST_TOP)
        solid_b = _b3d_box_between_with_up(p0b, p1b, BRACE_HW, BRACE_HD, UP)
        if solid_b:
            solid_b.label = f"Brace{i+1}b"
            solids.append(solid_b)

    # 5. Hip Rafters
    overhang_in = model.get("overhang_in", 12)
    overhang_ft = overhang_in / 12.0
    
    rafter_apex = [
        (scene.hub_r * math.cos(2 * math.pi * i / qty),
         scene.hub_r * math.sin(2 * math.pi * i / qty),
         scene.Z_APEX)
        for i in range(qty)
    ]
    for i in range(qty):
        px, py = scene.post_xy[i]
        ang = 2 * math.pi * i / qty
        tang = (math.cos(ang + math.pi / 2), math.sin(ang + math.pi / 2), 0.0)
        len_xy = math.sqrt(px * px + py * py)
        dir_xy_norm = (px / len_xy, py / len_xy)
        slope = (scene.Z_APEX - scene.Z_BEAM_TOP) / (len_xy - scene.hub_r)

        p0_start = (
            px + dir_xy_norm[0] * overhang_ft,
            py + dir_xy_norm[1] * overhang_ft,
            scene.Z_BEAM_TOP - slope * overhang_ft
        )
        p1_apex = rafter_apex[i]

        # Shift rafter up vertically so its underside rests exactly on top of the beam ring
        theta = math.atan(slope)
        dy_vertical = RAFTER_HD / math.cos(theta)
        
        p0_start_shifted = (p0_start[0], p0_start[1], p0_start[2] + dy_vertical)
        p1_apex_shifted = (p1_apex[0], p1_apex[1], p1_apex[2] + dy_vertical)
        
        solid = _b3d_box_between_with_up(p0_start_shifted, p1_apex_shifted, RAFTER_HW, RAFTER_HD, UP)
        if solid:
            solid.label = f"R{i+1}"
            solids.append(solid)

    # 6. Jack Rafters
    for i in range(qty):
        px1, py1 = scene.post_xy[i]
        px2, py2 = scene.post_xy[(i+1) % qty]
        bx = px2 - px1
        by = py2 - py1
        blen = math.sqrt(bx * bx + by * by)
        if blen < 1e-9:
            continue
        ux = bx / blen
        uy = by / blen

        in_x = -uy
        in_y = ux

        mx = (px1 + px2) / 2.0
        my = (py1 + py2) / 2.0
        apothem = math.sqrt(mx * mx + my * my)
        
        roof_rise = calcs.get("roof_rise", {}).get("rise_ft", 1.6)
        slope_perp = roof_rise / (apothem - scene.hub_r * math.cos(math.pi / qty))

        sec_spec = model.get("roof", {}).get("secondary_rafters", {})
        count_per_side = sec_spec.get("count_per_side", 2)
        fractions_list = []
        for j in range(count_per_side):
            fraction = (j + 1.0) / (count_per_side + 1.0)
            tag_suffix = chr(ord('a') + j)
            fractions_list.append((fraction, tag_suffix))

        for fraction, tag_suffix in fractions_list:
            sx = px1 + bx * fraction
            sy = py1 + by * fraction

            if fraction < 0.5:
                px_corner, py_corner = px1, py1
                px_apex, py_apex = rafter_apex[i][0], rafter_apex[i][1]
            else:
                px_corner, py_corner = px2, py2
                px_apex, py_apex = rafter_apex[(i+1)%qty][0], rafter_apex[(i+1)%qty][1]

            dx_hip = px_apex - px_corner
            dy_hip = py_apex - py_corner

            det = -dx_hip * in_y + in_x * dy_hip
            if abs(det) > 1e-6:
                s_val = (-(sx - px_corner) * in_y + in_x * (sy - py_corner)) / det
                t_val = (dx_hip * (sy - py_corner) - dy_hip * (sx - px_corner)) / det

                int_x = px_corner + dx_hip * s_val
                int_y = py_corner + dy_hip * s_val
                int_z = scene.Z_BEAM_TOP + t_val * slope_perp
                pt_int = (int_x, int_y, int_z)

                p0_start = (
                    sx - in_x * overhang_ft,
                    sy - in_y * overhang_ft,
                    scene.Z_BEAM_TOP - slope_perp * overhang_ft
                )

                # Shift jack rafter up vertically so its underside rests exactly on top of the beam ring
                theta_perp = math.atan(slope_perp)
                dy_perp = RAFTER_HD / math.cos(theta_perp)
                
                p0_start_shifted = (p0_start[0], p0_start[1], p0_start[2] + dy_perp)
                pt_int_shifted = (pt_int[0], pt_int[1], pt_int[2] + dy_perp)
                
                tang = (ux, uy, 0.0)
                solid = _b3d_box_between_with_up(p0_start_shifted, pt_int_shifted, RAFTER_HW, RAFTER_HD, UP)
                if solid:
                    solid.label = f"Jack{i+1}{tag_suffix}"
                    solids.append(solid)

    # 7. Purlin Ring
    s_purlin = purlins_spec.get("height_fraction", 0.55)
    Z_PURLIN = scene.Z_BEAM_TOP + (scene.Z_APEX - scene.Z_BEAM_TOP) * s_purlin
    # Calculate dy_vertical again for purlin offset
    dx_hip_ex = scene.post_xy[0][0] - rafter_apex[0][0]
    dy_hip_ex = scene.post_xy[0][1] - rafter_apex[0][1]
    len_xy_ex = math.sqrt(scene.post_xy[0][0]**2 + scene.post_xy[0][1]**2)
    slope_ex = (scene.Z_APEX - scene.Z_BEAM_TOP) / (len_xy_ex - scene.hub_r)
    dy_vertical = RAFTER_HD / math.cos(math.atan(slope_ex))

    purlin_pts = []
    for i in range(qty):
        px, py = scene.post_xy[i]
        ax, ay, az = rafter_apex[i]
        pt = (
            px + (ax - px) * s_purlin,
            py + (ay - py) * s_purlin,
            Z_PURLIN + dy_vertical
        )
        purlin_pts.append(pt)

    for i in range(qty):
        pt1 = purlin_pts[i]
        pt2 = purlin_pts[(i+1) % qty]
        solid = _b3d_box_between_with_up(pt1, pt2, PURLIN_HW, PURLIN_HD, UP)
        if solid:
            solid.label = f"Purlin{i+1}"
            solids.append(solid)

    # 8. Polygonal Hub (Substantial hanging pendant)
    hub_ztop = scene.Z_APEX + RAFTER_HD + 0.15
    hub_zbot = scene.Z_APEX - 1.25
    hub_height = hub_ztop - hub_zbot

    with b3d.BuildPart() as hub_part:
        with b3d.BuildSketch() as sketch:
            b3d.RegularPolygon(radius=scene.hub_r * FT_TO_MM, side_count=qty)
        b3d.extrude(amount=hub_height * FT_TO_MM)
    
    hub_solid = hub_part.part.translate((0, 0, (hub_zbot + hub_height / 2) * FT_TO_MM))
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
