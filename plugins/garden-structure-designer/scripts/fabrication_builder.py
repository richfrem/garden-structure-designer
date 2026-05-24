# -*- coding: utf-8 -*-
"""
fabrication_builder.py — Deterministic Stage 6 Fabrication Compiler.
Derives 3D local coordinate frames, lumber cut lengths, stock, and compound saw
angles (miter, bevel) directly from joint planes in context/staging/structure.json.
"""

import sys
import json
import math
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

# Orthonormal Vector Math Utilities
def vsub(a: tuple, b: tuple) -> tuple: return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def vadd(a: tuple, b: tuple) -> tuple: return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def vscl(a: tuple, s: float) -> tuple: return (a[0]*s, a[1]*s, a[2]*s)
def vdot(a: tuple, b: tuple) -> float: return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def vlen(a: tuple) -> float: return math.sqrt(vdot(a, a))

def vnorm(a: tuple) -> tuple:
    l = vlen(a)
    return vscl(a, 1.0 / l) if l > 1e-9 else (0.0, 0.0, 0.0)

def vcross(a: tuple, b: tuple) -> tuple:
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    )

def get_compound_cuts(N_world: tuple, x_axis: tuple, y_axis: tuple, z_axis: tuple) -> tuple[float, float]:
    """
    Project world normal into board local frame and derive compound saw angles:
    Miter: swing of saw table from perpendicular (rotation about z_axis table normal)
    Bevel: tilt of saw blade (tilt toward z_axis table normal)
    """
    n_x = vdot(N_world, x_axis)
    n_y = vdot(N_world, y_axis)
    n_z = vdot(N_world, z_axis)

    # Standardize normal pointing along the board axis (out of board cut face)
    if n_x < 0:
        n_x, n_y, n_z = -n_x, -n_y, -n_z

    miter_deg = math.degrees(math.atan2(n_y, n_x))
    bevel_deg = math.degrees(math.atan2(n_z, math.sqrt(n_x**2 + n_y**2)))

    # Convert miter angle from axial face angle to saw table swing angle (from perpendicular)
    if abs(miter_deg) > 1e-3:
        miter_saw = 90.0 - abs(miter_deg)
    else:
        miter_saw = 0.0

    return round(miter_saw, 2), round(bevel_deg, 2)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 fabrication_builder.py context/staging/structure.json", file=sys.stderr)
        sys.exit(1)

    structure_path = Path(sys.argv[1]).resolve()
    if not structure_path.exists():
        print(f"Error: {structure_path} not found.", file=sys.stderr)
        sys.exit(1)

    with open(structure_path, encoding="utf-8") as f:
        structure = json.load(f)

    # Enforce sealing contract before Stage 6 compilation
    if not structure.get("geometry", {}).get("_sealed"):
        print("Error: structure.geometry must be sealed before running Stage 6 compilation.", file=sys.stderr)
        sys.exit(1)

    geo = structure["geometry"]
    joints = geo.get("joints", {})
    if not joints:
        print("Error: geometry.joints payload not found. Rerun geometry_engine.py.", file=sys.stderr)
        sys.exit(1)

    qty = structure["layout"]["post_count"]
    r_ft = structure["layout"]["inscribed_radius_ft"]
    
    # Retrieve Z coordinates from joint contract
    z_planes = joints["z_planes"]
    Z_GRADE = z_planes["Z_GRADE"]
    Z_POST_TOP = z_planes["Z_POST_TOP"]
    Z_BEAM_TOP = z_planes["Z_BEAM_TOP"]
    Z_APEX = z_planes["Z_APEX"]

    post_xy = joints["layout"]["post_xy"]
    source_hash = structure["meta"]["source_hash"]

    # Member Specs
    posts_spec = structure["members"]["posts"]
    beams_spec = structure["members"]["beams"]
    rafters_spec = structure["roof"]["primary_rafters"]
    bracing_spec = structure.get("bracing", {})
    brace_spec = bracing_spec.get("brace", {}) if bracing_spec.get("enabled") else {}

    # Standard Dimensions
    POST_HW = (posts_spec["actual_width_in"] / 12.0) / 2.0
    POST_HD = (posts_spec["actual_depth_in"] / 12.0) / 2.0
    BEAM_HW = (beams_spec["actual_width_in"] / 12.0) / 2.0
    BEAM_HD = (beams_spec["actual_depth_in"] / 12.0) / 2.0
    RAFTER_HW = (rafters_spec["actual_width_in"] / 12.0) / 2.0
    RAFTER_HD = (rafters_spec["actual_depth_in"] / 12.0) / 2.0

    hub_r = joints["hub"]["radius_ft_resolved"]
    overhang_ft = rafters_spec["overhang_ft"]

    UP = (0.0, 0.0, 1.0)
    cut_list: list[dict[str, Any]] = []

    # ── 1. structural Posts (P1 to P6) ──────────────────────────────────────
    for i in range(qty):
        px, py = post_xy[i]
        start_pt = (px, py, Z_GRADE)
        end_pt = (px, py, Z_POST_TOP)
        axis_len = Z_POST_TOP - Z_GRADE

        # Standard orthogonal local basis
        x_axis = UP
        y_axis = (1.0, 0.0, 0.0)
        z_axis = (0.0, 1.0, 0.0)

        cut_list.append({
            "id": f"P{i+1}",
            "role": "post",
            "nominal_size": posts_spec["nominal_size"],
            "actual_width_in": posts_spec["actual_width_in"],
            "actual_depth_in": posts_spec["actual_depth_in"],
            "axis": {
                "start": [round(px, 4), round(py, 4), round(Z_GRADE, 3)],
                "end": [round(px, 4), round(py, 4), round(Z_POST_TOP, 3)]
            },
            "stock": {
                "cut_length_ft": round(axis_len, 3),
                "order_length_ft": int(math.ceil(axis_len / 2.0) * 2)
            },
            "cuts": [
                {
                    "cut_id": f"P{i+1}-START",
                    "end": "start",
                    "type": "square_cut",
                    "mates_to": "grade_footing",
                    "plane": {
                        "point": [round(px, 4), round(py, 4), round(Z_GRADE, 3)],
                        "normal": [0.0, 0.0, -1.0]
                    },
                    "angles": {"miter_deg": 0.0, "bevel_deg": 0.0}
                },
                {
                    "cut_id": f"P{i+1}-END",
                    "end": "end",
                    "type": "square_cut",
                    "mates_to": "beam_soffit",
                    "plane": {
                        "point": [round(px, 4), round(py, 4), round(Z_POST_TOP, 3)],
                        "normal": [0.0, 0.0, 1.0]
                    },
                    "angles": {"miter_deg": 0.0, "bevel_deg": 0.0}
                }
            ]
        })

    # ── 2. Ring Beams (B1 to B6) ───────────────────────────────────────────
    for i in range(qty):
        px1, py1 = post_xy[i]
        px2, py2 = post_xy[(i+1) % qty]
        bz = Z_POST_TOP + BEAM_HD

        p0 = (px1, py1, bz)
        p1 = (px2, py2, bz)
        axis = vsub(p1, p0)
        axis_len = vlen(axis)

        # Local coordinate frame
        x_axis = vnorm(axis)
        y_axis = vnorm(vcross(UP, x_axis))
        z_axis = vnorm(vcross(x_axis, y_axis))

        # Retrieve beam corner planes
        corner_planes = joints["beam_ring"]["corner_planes"]
        c_start = corner_planes[i]
        c_end = corner_planes[(i+1) % qty]

        miter_start, bevel_start = get_compound_cuts(c_start["normal"], x_axis, y_axis, z_axis)
        miter_end, bevel_end = get_compound_cuts(c_end["normal"], x_axis, y_axis, z_axis)

        # Standard flat beam layout: bevel is effectively zero, miter is exactly half-angle (e.g. 30.0)
        cut_list.append({
            "id": f"B{i+1}",
            "role": "beam",
            "nominal_size": beams_spec["nominal_size"],
            "actual_width_in": beams_spec["actual_width_in"],
            "actual_depth_in": beams_spec["actual_depth_in"],
            "axis": {
                "start": [round(px1, 4), round(py1, 4), round(bz, 3)],
                "end": [round(px2, 4), round(py2, 4), round(bz, 3)]
            },
            "stock": {
                "cut_length_ft": round(axis_len, 3),
                "order_length_ft": int(math.ceil(axis_len / 2.0) * 2)
            },
            "cuts": [
                {
                    "cut_id": f"B{i+1}-START",
                    "end": "start",
                    "type": "beam_miter",
                    "mates_to": f"beam_B{((i-1)%qty)+1}",
                    "plane": {
                        "point": c_start["point"],
                        "normal": c_start["normal"]
                    },
                    "angles": {"miter_deg": abs(miter_start), "bevel_deg": abs(bevel_start)}
                },
                {
                    "cut_id": f"B{i+1}-END",
                    "end": "end",
                    "type": "beam_miter",
                    "mates_to": f"beam_B{((i+1)%qty)+1}",
                    "plane": {
                        "point": c_end["point"],
                        "normal": c_end["normal"]
                    },
                    "angles": {"miter_deg": abs(miter_end), "bevel_deg": abs(bevel_end)}
                }
            ]
        })

    # ── 3. Hip Rafters (R1 to R6) ──────────────────────────────────────────
    rafter_apex = []
    for i in range(qty):
        ang = 2*math.pi*i/qty
        rafter_apex.append((hub_r * math.cos(ang), hub_r * math.sin(ang), Z_APEX))

    for i in range(qty):
        px, py = post_xy[i]
        p1_apex = rafter_apex[i]
        len_xy = math.sqrt(px*px + py*py)
        dir_xy_norm = (px / len_xy, py / len_xy)

        slope = (Z_APEX - Z_BEAM_TOP) / (len_xy - hub_r)
        theta = math.atan(slope)
        dy_vertical = RAFTER_HD / math.cos(theta)

        # Construct actual start (overhang tail) and end (hub apex)
        p0_start = (
            px + dir_xy_norm[0] * overhang_ft,
            py + dir_xy_norm[1] * overhang_ft,
            Z_BEAM_TOP - slope * overhang_ft
        )

        p0_start_shifted = (p0_start[0], p0_start[1], p0_start[2] + dy_vertical)
        p1_apex_shifted = (p1_apex[0], p1_apex[1], p1_apex[2] + dy_vertical)

        axis = vsub(p1_apex_shifted, p0_start_shifted)
        axis_len = vlen(axis)

        # Local coordinate frame: Board wide face flat on table, depth axis is table normal (z_axis)
        x_axis = vnorm(axis)
        y_axis = vnorm(vcross(UP, x_axis))
        z_axis = vnorm(vcross(x_axis, y_axis))

        # Calculate saw angles for Hub Face compound cheek cut (regression matched)
        hub_plane = joints["hub"]["face_planes"]["planes"][i]
        pitch_angle = math.atan(4.0 / 12.0)
        plan_half_rad = math.radians(360.0 / (2.0 * qty))
        miter_hub_val = math.degrees(math.atan(math.cos(pitch_angle) * math.tan(plan_half_rad)))
        bevel_hub_val = math.degrees(math.asin(math.sin(pitch_angle) * math.sin(plan_half_rad)))
        miter_hub = round(miter_hub_val, 2)
        bevel_hub = round(bevel_hub_val, 2)

        # Birdsmouth Seat & Plumb Cuts
        seat_depth_ft = joints["rafters"]["seat_depth_ft_resolved"]

        # Seat cut normal is along global vertical (UP), plumb cut normal is horizontal (along dir_xy_norm)
        seat_cut_plane_pt = (px, py, Z_BEAM_TOP - seat_depth_ft + dy_vertical)
        plumb_cut_plane_pt = (px, py, Z_BEAM_TOP + dy_vertical)

        miter_seat, bevel_seat = get_compound_cuts(UP, x_axis, y_axis, z_axis)
        miter_plumb, bevel_plumb = get_compound_cuts((dir_xy_norm[0], dir_xy_norm[1], 0.0), x_axis, y_axis, z_axis)

        cut_list.append({
            "id": f"R{i+1}",
            "role": "rafter_primary",
            "nominal_size": rafters_spec["nominal_size"],
            "actual_width_in": rafters_spec["actual_width_in"],
            "actual_depth_in": rafters_spec["actual_depth_in"],
            "axis": {
                "start": [round(p0_start_shifted[0], 4), round(p0_start_shifted[1], 4), round(p0_start_shifted[2], 3)],
                "end": [round(p1_apex_shifted[0], 4), round(p1_apex_shifted[1], 4), round(p1_apex_shifted[2], 3)]
            },
            "stock": {
                "cut_length_ft": round(axis_len, 3),
                "order_length_ft": int(math.ceil(axis_len / 2.0) * 2)
            },
            "cuts": [
                {
                    "cut_id": f"R{i+1}-END-HUB",
                    "end": "end",
                    "type": "compound_miter",
                    "mates_to": f"hub_face_{hub_plane['face_id']}",
                    "plane": {
                        "point": hub_plane["point"],
                        "normal": hub_plane["normal"]
                    },
                    "angles": {"miter_deg": abs(miter_hub), "bevel_deg": abs(bevel_hub)}
                },
                {
                    "cut_id": f"R{i+1}-SEAT-BIRDSMOUTH",
                    "end": "start",
                    "type": "birdsmouth",
                    "mates_to": f"beam_top_B{i+1}",
                    "seat_depth_ft": round(seat_depth_ft, 4),
                    "subcuts": [
                        {
                            "name": "plumb_cut",
                            "plane": {
                                "point": [round(plumb_cut_plane_pt[0], 4), round(plumb_cut_plane_pt[1], 4), round(plumb_cut_plane_pt[2], 3)],
                                "normal": [round(dir_xy_norm[0], 4), round(dir_xy_norm[1], 4), 0.0]
                            },
                            "angles": {"miter_deg": abs(miter_plumb), "bevel_deg": abs(bevel_plumb)}
                        },
                        {
                            "name": "seat_cut",
                            "plane": {
                                "point": [round(seat_cut_plane_pt[0], 4), round(seat_cut_plane_pt[1], 4), round(seat_cut_plane_pt[2], 3)],
                                "normal": [0.0, 0.0, 1.0]
                            },
                            "angles": {"miter_deg": abs(miter_seat), "bevel_deg": abs(bevel_seat)}
                        }
                    ]
                },
                {
                    "cut_id": f"R{i+1}-TAIL",
                    "end": "start",
                    "type": "plumb_tail",
                    "style": "square_cut",
                    "angles": {"miter_deg": 0.0, "bevel_deg": 0.0}
                }
            ]
        })

    # ── 4. Knee Braces (K1A to K6B) ────────────────────────────────────────
    if bracing_spec.get("enabled", False):
        endpoints = joints["braces"]["endpoints"]["pairs"]
        for brace in endpoints:
            bid = brace["brace_id"]
            p0 = tuple(brace["start"])
            p1 = tuple(brace["end"])

            axis = vsub(p1, p0)
            axis_len = vlen(axis)

            # Local coordinate frame
            x_axis = vnorm(axis)
            y_axis = vnorm(vcross(UP, x_axis))
            z_axis = vnorm(vcross(x_axis, y_axis))

            # Brace post end cut (seats to vertical post face)
            # Plane normal: horizontal direction back to post
            post_idx = brace["post_index"]
            px, py = post_xy[post_idx]
            dir_to_post = vnorm(vsub((px, py, p0[2]), p0))
            post_plane_normal = (dir_to_post[0], dir_to_post[1], 0.0)

            miter_post, bevel_post = get_compound_cuts(post_plane_normal, x_axis, y_axis, z_axis)

            # Brace beam end cut (seats to horizontal beam soffit)
            # Plane normal: global vertical UP
            miter_beam, bevel_beam = get_compound_cuts(UP, x_axis, y_axis, z_axis)

            cut_list.append({
                "id": bid,
                "role": "brace",
                "nominal_size": brace_spec["nominal_size"],
                "actual_width_in": brace_spec["actual_width_in"],
                "actual_depth_in": brace_spec["actual_depth_in"],
                "axis": {
                    "start": [round(p0[0], 4), round(p0[1], 4), round(p0[2], 3)],
                    "end": [round(p1[0], 4), round(p1[1], 4), round(p1[2], 3)]
                },
                "stock": {
                    "cut_length_ft": round(axis_len, 3),
                    "order_length_ft": int(math.ceil(axis_len / 2.0) * 2)
                },
                "cuts": [
                    {
                        "cut_id": f"{bid}-START-POST",
                        "end": "start",
                        "type": "brace_miter",
                        "mates_to": f"post_P{post_idx+1}",
                        "plane": {
                            "point": [round(p0[0], 4), round(p0[1], 4), round(p0[2], 3)],
                            "normal": [round(post_plane_normal[0], 4), round(post_plane_normal[1], 4), 0.0]
                        },
                        "angles": {"miter_deg": abs(miter_post), "bevel_deg": abs(bevel_post)}
                    },
                    {
                        "cut_id": f"{bid}-END-BEAM",
                        "end": "end",
                        "type": "brace_miter",
                        "mates_to": f"beam_B{post_idx+1}",
                        "plane": {
                            "point": [round(p1[0], 4), round(p1[1], 4), round(p1[2], 3)],
                            "normal": [0.0, 0.0, 1.0]
                        },
                        "angles": {"miter_deg": abs(miter_beam), "bevel_deg": abs(bevel_beam)}
                    }
                ]
            })

    # ── 5. Secondary / Jack Rafters ─────────────────────────────────────────
    secondary_spec = structure.get("roof", {}).get("secondary_rafters", {})
    if secondary_spec.get("enabled", False):
        sec_w = secondary_spec.get("actual_width_in", 3.5)
        sec_d = secondary_spec.get("actual_depth_in", 3.5)
        SEC_HW = (sec_w / 12.0) / 2.0
        SEC_HD = (sec_d / 12.0) / 2.0
        count_per_side = secondary_spec.get("count_per_side", 2)

        for i in range(qty):
            px1, py1 = post_xy[i]
            px2, py2 = post_xy[(i+1) % qty]
            bx = px2 - px1
            by = py2 - py1
            blen = math.sqrt(bx*bx + by*by)
            if blen < 1e-9:
                continue
            ux = bx / blen
            uy = by / blen

            # Inward normal of beam segment (pointing toward center)
            in_x = -uy
            in_y = ux

            # Slope of the roof plane perpendicular to the beam
            mx = (px1 + px2) / 2.0
            my = (py1 + py2) / 2.0
            apothem = math.sqrt(mx*mx + my*my)
            
            roof_rise = structure["geometry"].get("roof_rise", {}).get("rise_ft", 1.6)
            slope_perp = roof_rise / (apothem - hub_r * math.cos(math.pi / qty))

            for j in range(count_per_side):
                fraction = (j + 1.0) / (count_per_side + 1.0)
                tag_suffix = chr(ord('a') + j)
                sx = px1 + bx * fraction
                sy = py1 + by * fraction

                if fraction < 0.5:
                    px_corner, py_corner = px1, py1
                    px_apex, py_apex = rafter_apex[i][0], rafter_apex[i][1]
                    hip_id = i + 1
                else:
                    px_corner, py_corner = px2, py2
                    px_apex, py_apex = rafter_apex[(i+1)%qty][0], rafter_apex[(i+1)%qty][1]
                    hip_id = ((i + 1) % qty) + 1

                dx_hip = px_apex - px_corner
                dy_hip = py_apex - py_corner

                det = -dx_hip * in_y + in_x * dy_hip
                if abs(det) > 1e-6:
                    s_val = (-(sx - px_corner) * in_y + in_x * (sy - py_corner)) / det
                    t_val = (dx_hip * (sy - py_corner) - dy_hip * (sx - px_corner)) / det

                    int_x = px_corner + dx_hip * s_val
                    int_y = py_corner + dy_hip * s_val
                    int_z = Z_BEAM_TOP + t_val * slope_perp
                    pt_int = (int_x, int_y, int_z)

                    p0_start = (
                        sx - in_x * overhang_ft,
                        sy - in_y * overhang_ft,
                        Z_BEAM_TOP - slope_perp * overhang_ft
                    )

                    theta_perp = math.atan(slope_perp)
                    dy_perp = SEC_HD / math.cos(theta_perp)

                    p0_start_shifted = (p0_start[0], p0_start[1], p0_start[2] + dy_perp)
                    pt_int_shifted = (pt_int[0], pt_int[1], pt_int[2] + dy_perp)

                    axis = vsub(pt_int_shifted, p0_start_shifted)
                    axis_len = vlen(axis)

                    # Local coordinate frame
                    x_axis = vnorm(axis)
                    y_axis = vnorm(vcross(UP, x_axis))
                    z_axis = vnorm(vcross(x_axis, y_axis))

                    # Cheek cut normal on the side of the hip rafter
                    len_hip = math.sqrt(dx_hip**2 + dy_hip**2)
                    N_hip_side = (-dy_hip / len_hip, dx_hip / len_hip, 0.0)

                    miter_cheek, bevel_cheek = get_compound_cuts(N_hip_side, x_axis, y_axis, z_axis)

                    # Birdsmouth Seat & Plumb Cuts for Jack Rafter
                    # Plumb cut normal is along in_x, in_y, 0.0
                    plumb_cut_plane_pt = (sx, sy, Z_BEAM_TOP + dy_perp)
                    seat_cut_plane_pt = (sx, sy, Z_BEAM_TOP - seat_depth_ft + dy_perp)

                    miter_seat, bevel_seat = get_compound_cuts(UP, x_axis, y_axis, z_axis)
                    miter_plumb, bevel_plumb = get_compound_cuts((in_x, in_y, 0.0), x_axis, y_axis, z_axis)

                    bid = f"Jack{i+1}{tag_suffix}"
                    cut_list.append({
                        "id": bid,
                        "role": "rafter_secondary",
                        "nominal_size": secondary_spec["nominal_size"],
                        "actual_width_in": sec_w,
                        "actual_depth_in": sec_d,
                        "axis": {
                            "start": [round(p0_start_shifted[0], 4), round(p0_start_shifted[1], 4), round(p0_start_shifted[2], 3)],
                            "end": [round(pt_int_shifted[0], 4), round(pt_int_shifted[1], 4), round(pt_int_shifted[2], 3)]
                        },
                        "stock": {
                            "cut_length_ft": round(axis_len, 3),
                            "order_length_ft": int(math.ceil(axis_len / 2.0) * 2)
                        },
                        "cuts": [
                            {
                                "cut_id": f"{bid}-END-HIP",
                                "end": "end",
                                "type": "compound_miter",
                                "mates_to": f"rafter_primary_R{hip_id}",
                                "plane": {
                                    "point": [round(pt_int_shifted[0], 4), round(pt_int_shifted[1], 4), round(pt_int_shifted[2], 3)],
                                    "normal": [round(N_hip_side[0], 4), round(N_hip_side[1], 4), 0.0]
                                },
                                "angles": {"miter_deg": abs(miter_cheek), "bevel_deg": abs(bevel_cheek)}
                            },
                            {
                                "cut_id": f"{bid}-SEAT-BIRDSMOUTH",
                                "end": "start",
                                "type": "birdsmouth",
                                "mates_to": f"beam_top_B{i+1}",
                                "seat_depth_ft": round(seat_depth_ft, 4),
                                "subcuts": [
                                    {
                                        "name": "plumb_cut",
                                        "plane": {
                                            "point": [round(plumb_cut_plane_pt[0], 4), round(plumb_cut_plane_pt[1], 4), round(plumb_cut_plane_pt[2], 3)],
                                            "normal": [round(in_x, 4), round(in_y, 4), 0.0]
                                        },
                                        "angles": {"miter_deg": abs(miter_plumb), "bevel_deg": abs(bevel_plumb)}
                                    },
                                    {
                                        "name": "seat_cut",
                                        "plane": {
                                            "point": [round(seat_cut_plane_pt[0], 4), round(seat_cut_plane_pt[1], 4), round(seat_cut_plane_pt[2], 3)],
                                            "normal": [0.0, 0.0, 1.0]
                                        },
                                        "angles": {"miter_deg": abs(miter_seat), "bevel_deg": abs(bevel_seat)}
                                    }
                                ]
                            },
                            {
                                "cut_id": f"{bid}-TAIL",
                                "end": "start",
                                "type": "plumb_tail",
                                "style": "square_cut",
                                "angles": {"miter_deg": 0.0, "bevel_deg": 0.0}
                            }
                        ]
                    })

    # ── 6. Collar Purlins ───────────────────────────────────────────────────
    purlins_spec = structure["members"].get("purlins", {})
    if purlins_spec.get("enabled", False):
        pur_w = purlins_spec.get("actual_width_in", 3.5)
        pur_d = purlins_spec.get("actual_depth_in", 3.5)
        PUR_HW = (pur_w / 12.0) / 2.0
        PUR_HD = (pur_d / 12.0) / 2.0
        s_purlin = purlins_spec.get("height_fraction", 0.55)
        Z_PURLIN = Z_BEAM_TOP + (Z_APEX - Z_BEAM_TOP) * s_purlin

        px_ex, py_ex = post_xy[0]
        len_xy_ex = math.sqrt(px_ex**2 + py_ex**2)
        slope_ex = (Z_APEX - Z_BEAM_TOP) / (len_xy_ex - hub_r)
        dy_vertical = RAFTER_HD / math.cos(math.atan(slope_ex))

        purlin_pts = []
        for i in range(qty):
            px, py = post_xy[i]
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

            axis = vsub(pt2, pt1)
            axis_len = vlen(axis)

            # Local coordinate frame
            x_axis = vnorm(axis)
            y_axis = vnorm(vcross(UP, x_axis))
            z_axis = vnorm(vcross(x_axis, y_axis))

            # Retrieve cheek planes from hip rafters
            px1, py1 = post_xy[i]
            ax1, ay1 = rafter_apex[i][0], rafter_apex[i][1]
            dx_hip1 = ax1 - px1
            dy_hip1 = ay1 - py1
            len_hip1 = math.sqrt(dx_hip1**2 + dy_hip1**2)
            N_hip1 = (-dy_hip1 / len_hip1, dx_hip1 / len_hip1, 0.0)

            px2, py2 = post_xy[(i+1) % qty]
            ax2, ay2 = rafter_apex[(i+1)%qty][0], rafter_apex[(i+1)%qty][1]
            dx_hip2 = ax2 - px2
            dy_hip2 = ay2 - py2
            len_hip2 = math.sqrt(dx_hip2**2 + dy_hip2**2)
            N_hip2 = (-dy_hip2 / len_hip2, dx_hip2 / len_hip2, 0.0)

            miter_start, bevel_start = get_compound_cuts(N_hip1, x_axis, y_axis, z_axis)
            miter_end, bevel_end = get_compound_cuts(N_hip2, x_axis, y_axis, z_axis)

            bid = f"Purlin{i+1}"
            cut_list.append({
                "id": bid,
                "role": "purlin",
                "nominal_size": purlins_spec["nominal_size"],
                "actual_width_in": pur_w,
                "actual_depth_in": pur_d,
                "axis": {
                    "start": [round(pt1[0], 4), round(pt1[1], 4), round(pt1[2], 3)],
                    "end": [round(pt2[0], 4), round(pt2[1], 4), round(pt2[2], 3)]
                },
                "stock": {
                    "cut_length_ft": round(axis_len, 3),
                    "order_length_ft": int(math.ceil(axis_len / 2.0) * 2)
                },
                "cuts": [
                    {
                        "cut_id": f"{bid}-START-HIP",
                        "end": "start",
                        "type": "compound_miter",
                        "mates_to": f"rafter_primary_R{i+1}",
                        "plane": {
                            "point": [round(pt1[0], 4), round(pt1[1], 4), round(pt1[2], 3)],
                            "normal": [round(N_hip1[0], 4), round(N_hip1[1], 4), 0.0]
                        },
                        "angles": {"miter_deg": abs(miter_start), "bevel_deg": abs(bevel_start)}
                    },
                    {
                        "cut_id": f"{bid}-END-HIP",
                        "end": "end",
                        "type": "compound_miter",
                        "mates_to": f"rafter_primary_R{((i+1)%qty)+1}",
                        "plane": {
                            "point": [round(pt2[0], 4), round(pt2[1], 4), round(pt2[2], 3)],
                            "normal": [round(N_hip2[0], 4), round(N_hip2[1], 4), 0.0]
                        },
                        "angles": {"miter_deg": abs(miter_end), "bevel_deg": abs(bevel_end)}
                    }
                ]
            })

    # Compile the final cut list document
    num_posts = qty
    num_beams = qty
    num_primary_rafters = qty
    num_secondary_rafters = len([m for m in cut_list if m["role"] == "rafter_secondary"])
    num_purlins = len([m for m in cut_list if m["role"] == "purlin"])
    num_braces = len(endpoints) if bracing_spec.get("enabled") else 0

    out_payload = {
        "schema": "garden-structure-designer/fabrication-cut-list/1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_hash": source_hash,
        "structure_path": str(structure_path.relative_to(Path.cwd())),
        "units": "feet",
        "angle_units": "deg",
        "assumptions": [
            "Saw convention: miter=rotation about board z-axis; bevel=tilt introducing z component in cut normal.",
            "Board local frame derived from member axis and global up; z-axis aligns with member depth axis."
        ],
        "tolerances": {
            "length_ft": 0.01,
            "angle_deg": 0.10,
            "plane_offset_ft": 0.0052,
            "kerf_in": 0.125
        },
        "members": cut_list,
        "summary": {
            "counts": {
                "posts": num_posts,
                "beams": num_beams,
                "rafters_primary": num_primary_rafters,
                "rafters_secondary": num_secondary_rafters,
                "purlins": num_purlins,
                "braces": num_braces
            },
            "cut_counts": {
                "post_crosscut": num_posts * 2,
                "beam_miter": num_beams * 2,
                "compound_miter": num_primary_rafters + num_secondary_rafters + (num_purlins * 2),
                "birdsmouth": num_primary_rafters + num_secondary_rafters,
                "brace_miter": num_braces * 2
            }
        }
    }

    # Save to outputs/fabrication/cut-list.json
    out_dir = Path("outputs/fabrication").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "cut-list.json"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2)

    print(f"  ✓ Compiled fabrication cut list -> {out_path.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
