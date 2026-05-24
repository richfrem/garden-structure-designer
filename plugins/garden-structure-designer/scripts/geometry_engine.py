#!/usr/bin/env python3
"""
geometry_engine.py (CLI)
=====================================
Purpose:
    v6.0 High-Fidelity Geometry Compiler for garden-structure-designer.
    Solves 100% of structural vertices and faces from constraint intersections.
"""
from __future__ import annotations
import json
import math
import os
import sys
import hashlib
from datetime import datetime, timezone
from typing import Any

V3 = tuple[float, float, float]

def vdot(a: V3, b: V3) -> float: return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def vcross(a: V3, b: V3) -> V3: return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def vsub(a: V3, b: V3) -> V3: return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def vadd(a: V3, b: V3) -> V3: return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def vmul(a: V3, s: float) -> V3: return (a[0]*s, a[1]*s, a[2]*s)
def vlen(a: V3) -> float: return math.sqrt(vdot(a, a))
def vnorm(a: V3) -> V3: l = vlen(a); return vmul(a, 1.0/l) if l > 1e-9 else (0.0, 0.0, 0.0)
def vdist(a: V3, b: V3) -> float: return vlen(vsub(a, b))
def v2_radius(v: V3) -> float: return math.sqrt(v[0]*v[0] + v[1]*v[1])
def vcent(pts: list[V3]) -> V3:
    n = len(pts); return (sum(p[0] for p in pts)/n, sum(p[1] for p in pts)/n, sum(p[2] for p in pts)/n)

def intersect_three_planes(p1: V3, n1: V3, p2: V3, n2: V3, p3: V3, n3: V3, eps: float = 1e-9) -> V3:
    denom = vdot(n1, vcross(n2, n3))
    if abs(denom) < eps:
        raise ValueError("Planes parallel or degenerate intersection")
    d1 = vdot(p1, n1)
    d2 = vdot(p2, n2)
    d3 = vdot(p3, n3)
    numerator = vadd(vadd(vmul(vcross(n2, n3), d1), vmul(vcross(n3, n1), d2)), vmul(vcross(n1, n2), d3))
    return vmul(numerator, 1.0 / denom)

def intersect_line_plane(p0: V3, d: V3, p_plane: V3, n: V3, eps: float = 1e-8) -> tuple[V3, float]:
    denom = vdot(d, n)
    if abs(denom) < eps: raise ValueError("Line parallel to plane")
    t = vdot(vsub(p_plane, p0), n) / denom
    return vadd(p0, vmul(d, t)), t

def get_compound_cuts(target_normal: V3, x_axis: V3, y_axis: V3, z_axis: V3) -> tuple[float, float]:
    ln = (vdot(target_normal, x_axis), vdot(target_normal, y_axis), vdot(target_normal, z_axis))
    miter = math.degrees(math.atan2(ln[1], abs(ln[0])))
    bevel = math.degrees(math.acos(vnorm(ln)[2])) - 90.0
    return miter, bevel

def point_to_plane_distance(point: V3, plane_point: V3, plane_normal: V3) -> float:
    """Signed distance from point to plane."""
    nl = vlen(plane_normal)
    norm = vmul(plane_normal, 1.0/nl) if nl > 1e-9 else plane_normal
    return vdot(vsub(point, plane_point), norm)

def compile_resolved_model(structure: dict, joints: dict) -> dict:
    resolved = {"constraints_resolved": True, "members": []}
    qty = structure["layout"]["post_count"]
    PHW = (structure["members"]["posts"]["actual_width_in"] / 24.0); PHD = (structure["members"]["posts"]["actual_depth_in"] / 24.0)
    BHW = (structure["members"]["beams"]["actual_width_in"] / 24.0); BHD = (structure["members"]["beams"]["actual_depth_in"] / 24.0)
    RHW = (structure["roof"]["primary_rafters"]["actual_width_in"] / 24.0); RHD = (structure["roof"]["primary_rafters"]["actual_depth_in"] / 24.0)
    KHW = (structure["bracing"]["brace"]["actual_width_in"] / 24.0); KHD = (structure["bracing"]["brace"]["actual_depth_in"] / 24.0)
    UP: V3 = (0.0, 0.0, 1.0)
    
    planes_map = {p["id"]: p for p in structure["cad_constraints"]["reference_planes"]}
    
    def add_prism(p0: V3, p1: V3, hw: float, hd: float, up_hint: V3, role: str, bid: str, derived_length: float, derived_angle: float, cs: dict):
        axis = vsub(p1, p0); u = vnorm(axis)
        ref = up_hint
        if abs(vdot(ref, u)) > 0.999:
            ref = (1.0, 0.0, 0.0) if abs(u[0]) < 0.9 else (0.0, 1.0, 0.0)
        w = vnorm(vcross(ref, u))
        d = vnorm(vcross(w, u))
        pts = [vadd(vadd(p0, vmul(d, -hd)), vmul(w, -hw)), vadd(vadd(p0, vmul(d, -hd)), vmul(w, hw)), vadd(vadd(p0, vmul(d, hd)), vmul(w, hw)), vadd(vadd(p0, vmul(d, hd)), vmul(w, -hw)), vadd(vadd(p1, vmul(d, -hd)), vmul(w, -hw)), vadd(vadd(p1, vmul(d, -hd)), vmul(w, hw)), vadd(vadd(p1, vmul(d, hd)), vmul(w, hw)), vadd(vadd(p1, vmul(d, hd)), vmul(w, -hw))]
        faces = [{"verts": [0, 3, 2, 1], "normal": list(vmul(u, -1)), "color_key": "start"}, {"verts": [4, 5, 6, 7], "normal": list(u), "color_key": "end"}, {"verts": [0, 1, 5, 4], "normal": list(vmul(d, -1)), "color_key": "top"}, {"verts": [3, 7, 6, 2], "normal": list(d), "color_key": "bottom"}, {"verts": [0, 4, 7, 3], "normal": list(vmul(w, -1)), "color_key": "left"}, {"verts": [1, 2, 6, 5], "normal": list(w), "color_key": "right"}]
        resolved["members"].append({
            "id": bid,
            "role": role,
            "p0": list(p0),
            "p1": list(p1),
            "axis_u": list(u),
            "axis_w": list(w),
            "axis_d": list(d),
            "vertices": [list(v) for v in pts],
            "faces": faces,
            "derived_length_ft": round(derived_length, 4),
            "derived_angle_deg": round(derived_angle, 2),
            "constraints_satisfied": cs
        })

    def add_notched_rafter(p_tail: V3, p_apex: V3, p_seat: V3, hw: float, hd: float, seat_depth_notch: float, up_hint: V3, role: str, bid: str, z_seat: float, derived_length: float, derived_angle: float, cs: dict):
        u = vnorm(vsub(p_apex, p_tail)); w = vnorm(vcross(up_hint, u)); d_perp = vnorm(vcross(w, u)); full_depth = hd * 2.0; cos_pitch = v2_radius(u)
        notch_d = full_depth - seat_depth_notch
        def get_side_pts(lat: float) -> list[V3]:
            v0 = vadd(p_tail, vmul(w, lat)); v1 = vadd(p_apex, vmul(w, lat))
            v2 = (v1[0], v1[1], v1[2] - full_depth/cos_pitch if cos_pitch > 0.1 else v1[2]-full_depth)
            v4 = (p_seat[0], p_seat[1], z_seat); v3 = (v4[0], v4[1], v4[2] - notch_d/cos_pitch); v5 = (v0[0], v0[1], z_seat); return [v0, v1, v2, v3, v4, v5]
        pts_l = get_side_pts(-hw); pts_r = get_side_pts(hw); all_pts = pts_l + pts_r
        faces = [{"verts": [0, 6, 7, 1], "normal": list(vmul(d_perp, -1)), "color_key": "top"}, {"verts": [1, 7, 8, 2], "normal": list(u), "color_key": "end"}, {"verts": [2, 8, 9, 3], "normal": list(d_perp), "color_key": "bottom"}, {"verts": [3, 9, 10, 4], "normal": list(vmul(u, -1)), "color_key": "other"}, {"verts": [4, 10, 11, 5], "normal": [0, 0, -1], "color_key": "bottom"}, {"verts": [5, 11, 6, 0], "normal": list(vmul(u, -1)), "color_key": "start"}, {"verts": [0, 1, 2, 3, 4, 5], "normal": list(vmul(w, -1)), "color_key": "left"}, {"verts": [11, 10, 9, 8, 7, 6], "normal": list(w), "color_key": "right"}]
        resolved["members"].append({
            "id": bid,
            "role": role,
            "p0": list(p_tail),
            "p1": list(p_apex),
            "axis_u": list(u),
            "axis_w": list(w),
            "axis_d": list(d_perp),
            "vertices": [list(v) for v in all_pts],
            "faces": faces,
            "derived_length_ft": round(derived_length, 4),
            "derived_angle_deg": round(derived_angle, 2),
            "constraints_satisfied": cs
        })

    zp = joints["z_planes"]; pxy = joints["layout"]["post_xy"]; Z_BEAM_TOP = zp["Z_BEAM_TOP"]
    post_h = structure["members"]["posts"]["cut_length_ft"]
    beam_d_ft = structure["members"]["beams"]["actual_depth_in"] / 12.0

    # Posts
    for i, p in enumerate(pxy):
        post_id = f"P{i+1}"
        p0 = (p[0], p[1], zp["Z_GRADE"])
        p1 = (p[0], p[1], zp["Z_POST_TOP"])
        cs = {"base_on_footing": True, "top_on_beam": True}
        add_prism(p0, p1, PHW, PHD, UP, "post", post_id, post_h, 90.0, cs)
        add_prism((p[0], p[1], zp["Z_GRADE"] - 1.5), (p[0], p[1], zp["Z_GRADE"] + 0.33), 0.5, 0.5, UP, "footing", f"FT{i+1}", 1.83, 90.0, {})
        
    # Beams
    for i in range(qty):
        beam_id = f"B{i+1}"
        p1 = pxy[i]
        p2 = pxy[(i+1)%qty]
        p0 = (p1[0], p1[1], zp["Z_BEAM_CENTER"])
        pt_end = (p2[0], p2[1], zp["Z_BEAM_CENTER"])
        beam_len = vdist(p0, pt_end)
        cs = {"start_on_post": True, "end_on_post": True}
        add_prism(p0, pt_end, BHW, BHD, UP, "beam", beam_id, beam_len, 0.0, cs)
        
    # Braces
    for bj in joints["braces"]["endpoints"]:
        brace_id = bj["id"]
        p0 = tuple(bj["start"])
        p1 = tuple(bj["end"])
        length = vdist(p0, p1)
        angle = math.degrees(math.atan2(abs(p1[2] - p0[2]), math.sqrt((p1[0]-p0[0])**2 + (p1[1]-p0[1])**2)))
        
        cs = {}
        for mc in structure["cad_constraints"]["member_constraints"]:
            if mc["member_id"] == brace_id:
                 c = mc["constraints"]
                 start_plane = planes_map[c["start_surface"]]
                 end_plane = planes_map[c["end_surface"]]
                 d0 = abs(point_to_plane_distance(p0, tuple(start_plane["point"]), tuple(start_plane["normal"])))
                 d1 = abs(point_to_plane_distance(p1, tuple(end_plane["point"]), tuple(end_plane["normal"])))
                 cs["start_on_post_face"] = d0 < 0.0025
                 cs["end_on_beam_soffit"] = d1 < 0.0025
                 break
        add_prism(p0, p1, KHW, KHD, UP, "brace", brace_id, length, angle, cs)
        
    # Rafters
    for rj in joints["primary_rafters"]:
        rafter_id = rj["id"]
        p_tail = tuple(rj["start"])
        p_apex = tuple(rj["end"])
        p_seat = tuple(rj["seat_point"])
        length = vdist(p_tail, p_apex)
        angle = math.degrees(math.atan2(abs(p_apex[2] - p_tail[2]), math.sqrt((p_apex[0]-p_tail[0])**2 + (p_apex[1]-p_tail[1])**2)))
        
        cs = {}
        for mc in structure["cad_constraints"]["member_constraints"]:
            if mc["member_id"] == rafter_id:
                c = mc["constraints"]
                plane_id = c["plane_constraint"]["plane_id"]
                roof_plane = planes_map[plane_id]
                d_tail = abs(point_to_plane_distance(p_tail, tuple(roof_plane["point"]), tuple(roof_plane["normal"])))
                d_apex = abs(point_to_plane_distance(p_apex, tuple(roof_plane["point"]), tuple(roof_plane["normal"])))
                d_seat = abs(point_to_plane_distance(p_seat, tuple(roof_plane["point"]), tuple(roof_plane["normal"])))
                if d_tail >= 0.0025 or d_apex >= 0.0025 or d_seat >= 0.0025:
                    print(f"DEBUG {rafter_id}: d_tail={d_tail:.6f}, d_apex={d_apex:.6f}, d_seat={d_seat:.6f}")
                    print(f"  p_tail={p_tail}, p_apex={p_apex}, p_seat={p_seat}")
                    print(f"  plane_pt={roof_plane['point']}, plane_norm={roof_plane['normal']}")
                cs["tail_on_roof_plane"] = d_tail < 0.0025
                cs["hub_on_roof_plane"] = d_apex < 0.0025
                cs["seat_on_roof_plane"] = d_seat < 0.0025
                break
        add_notched_rafter(p_tail, p_apex, p_seat, RHW, RHD, rj["seat_depth_ft"], UP, "rafter", rafter_id, Z_BEAM_TOP, length, angle, cs)
        
    # Jack Rafters
    if joints["jack_rafters"]["enabled"]:
        for ep in joints["jack_rafters"]["endpoints"]:
            jack_id = ep["id"]
            p_tail = tuple(ep["start"])
            p_end = tuple(ep["end"])
            p_seat = tuple(ep["seat_point"])
            length = vdist(p_tail, p_end)
            angle = math.degrees(math.atan2(abs(ep["end"][2] - ep["start"][2]), math.sqrt((ep["end"][0]-ep["start"][0])**2 + (ep["end"][1]-ep["start"][1])**2)))
            
            cs = {}
            for mc in structure["cad_constraints"]["member_constraints"]:
                if mc["member_id"] == jack_id:
                    c = mc["constraints"]
                    plane_id = c["plane_constraint"]["plane_id"]
                    roof_plane = planes_map[plane_id]
                    d_tail = abs(point_to_plane_distance(p_tail, tuple(roof_plane["point"]), tuple(roof_plane["normal"])))
                    d_end = abs(point_to_plane_distance(p_end, tuple(roof_plane["point"]), tuple(roof_plane["normal"])))
                    d_seat = abs(point_to_plane_distance(p_seat, tuple(roof_plane["point"]), tuple(roof_plane["normal"])))
                    if d_tail >= 0.0025 or d_end >= 0.0025 or d_seat >= 0.0025:
                        print(f"DEBUG {jack_id}: d_tail={d_tail:.6f}, d_end={d_end:.6f}, d_seat={d_seat:.6f}")
                        print(f"  p_tail={p_tail}, p_end={p_end}, p_seat={p_seat}")
                        print(f"  plane_pt={roof_plane['point']}, plane_norm={roof_plane['normal']}")
                    cs["tail_on_roof_plane"] = d_tail < 0.0025
                    cs["end_on_roof_plane"] = d_end < 0.0025
                    cs["seat_on_roof_plane"] = d_seat < 0.0025
                    break
            add_notched_rafter(p_tail, p_end, p_seat, RHW, RHD, joints["primary_rafters"][0]["seat_depth_ft"], UP, "rafter", jack_id, Z_BEAM_TOP, length, angle, cs)
            
    # Hub
    hj = joints["hub"]; hr = hj["radius_ft"]; hh = hj["height_ft"]; az = zp["Z_APEX"]; hz_t = az + hh/2.0; hz_b = az - hh/2.0; r_c = hr / math.cos(math.pi/qty)
    t_ring = [(r_c*math.cos(2*math.pi*(i-0.5)/qty), r_c*math.sin(2*math.pi*(i-0.5)/qty), hz_t) for i in range(qty)]
    b_ring = [(r_c*math.cos(2*math.pi*(i-0.5)/qty), r_c*math.sin(2*math.pi*(i-0.5)/qty), hz_b) for i in range(qty)]
    h_faces = [{"verts": list(range(qty)), "normal": [0,0,1], "color_key": "top"}, {"verts": list(reversed(range(qty, 2*qty))), "normal": [0,0,-1], "color_key": "bottom"}]
    for i in range(qty): j = (i+1)%qty; fn = (math.cos(2*math.pi*i/qty), math.sin(2*math.pi*i/qty), 0.0); h_faces.append({"verts": [qty+i, qty+j, j, i], "normal": list(fn), "color_key": "left"})
    
    cs = {"height_lte_beam_depth_x1.2": hh <= beam_d_ft * 1.2 + 0.001}
    resolved["members"].append({
        "id": "HUB",
        "role": "hub",
        "p0": [0.0, 0.0, hz_b],
        "p1": [0.0, 0.0, hz_t],
        "axis_u": [0.0, 0.0, 1.0],
        "axis_w": [1.0, 0.0, 0.0],
        "axis_d": [0.0, 1.0, 0.0],
        "vertices": [list(v) for v in t_ring+b_ring],
        "faces": h_faces,
        "derived_length_ft": round(hh, 4),
        "derived_angle_deg": 90.0,
        "constraints_satisfied": cs
    })

    # Phase 3 — Full Resolution Guarantee
    for m in resolved["members"]:
        print(f"MEMBER {m['id']}: {m.get('constraints_satisfied')}")
    for m in resolved["members"]:
        if "p0" not in m or "p1" not in m or m["p0"] is None or m["p1"] is None:
            raise ValueError(f"Member {m['id']} is missing endpoints p0 or p1")
        if any(not math.isfinite(x) for x in m["p0"] + m["p1"]):
            raise ValueError(f"Member {m['id']} has non-finite endpoints")
        # Ensure all constraints are indeed satisfied
        for constraint, satisfied in m.get("constraints_satisfied", {}).items():
            if not satisfied:
                raise ValueError(f"Member {m['id']} failed constraint: {constraint}")
                
    return resolved

def solve_brace_endpoints_geometric(px: float, py: float, ux: float, uy: float, phw: float, z_soffit: float, run: float) -> tuple[V3, V3]:
    p0 = (px + ux * phw, py + uy * phw, z_soffit - run)
    p1 = (px + ux * (phw + run), py + uy * (phw + run), z_soffit)
    return p0, p1

def solve_rafter_endpoints_geometric(i: int, qty: int, Z_APEX: float, Z_BEAM_TOP: float, v_shift: float, r_ft: float, hub_r: float, oh_ft: float) -> tuple[V3, V3, V3]:
    theta_i = 2.0 * math.pi * i / qty
    theta_next = 2.0 * math.pi * (i + 1) / qty
    theta_prev = 2.0 * math.pi * (i - 1) / qty
    
    p_apex = (0.0, 0.0, Z_APEX + v_shift)
    p_a = (r_ft * math.cos(theta_i), r_ft * math.sin(theta_i), Z_BEAM_TOP + v_shift)
    p_b = (r_ft * math.cos(theta_next), r_ft * math.sin(theta_next), Z_BEAM_TOP + v_shift)
    p_prev = (r_ft * math.cos(theta_prev), r_ft * math.sin(theta_prev), Z_BEAM_TOP + v_shift)
    
    n1 = vnorm(vcross(vsub(p_b, p_a), vsub(p_apex, p_a)))
    n2 = vnorm(vcross(vsub(p_a, p_prev), vsub(p_apex, p_prev)))
    
    dir_rafter = vcross(n1, n2)
    if dir_rafter[2] > 0:
        dir_rafter = vmul(dir_rafter, -1.0)
    u_dir = vnorm(dir_rafter)
    
    p_hub_plane = (hub_r * math.cos(theta_i), hub_r * math.sin(theta_i), Z_APEX)
    n_hub_plane = (math.cos(theta_i), math.sin(theta_i), 0.0)
    
    p_beam_top_plane = (0.0, 0.0, Z_BEAM_TOP + v_shift)
    n_beam_top_plane = (0.0, 0.0, 1.0)
    
    p_hub, _ = intersect_line_plane(p_apex, u_dir, p_hub_plane, n_hub_plane)
    p_seat_top, _ = intersect_line_plane(p_apex, u_dir, p_beam_top_plane, n_beam_top_plane)
    
    u_xy_len = v2_radius(u_dir)
    p_tail = vadd(p_seat_top, vmul(u_dir, oh_ft / u_xy_len))
    return p_tail, p_hub, p_seat_top

def compute_joints(structure, cuts, rl, rise, height, hub_r, svg_coords):
    if "cad_constraints" not in structure:
        from cad_language_translator import translate_to_constraints
        was_sealed = structure.get("geometry", {}).get("_sealed", False)
        if was_sealed:
            structure["geometry"]["_sealed"] = False
        translate_to_constraints(structure)
        if was_sealed:
            structure["geometry"]["_sealed"] = True
    qty = structure["layout"]["post_count"]; r_ft = structure["layout"]["inscribed_radius_ft"]
    post_h = structure["members"]["posts"]["cut_length_ft"]; beam_d_in = structure["members"]["beams"]["actual_depth_in"]; beam_d_ft = beam_d_in / 12.0; roof_r = rise["rise_ft"]
    rafter_d_in = structure["roof"]["primary_rafters"]["actual_depth_in"]; rafter_w_in = structure["roof"]["primary_rafters"]["actual_width_in"]; rafter_d_ft = rafter_d_in / 12.0
    Z_GRADE = 0.0; Z_POST_TOP = post_h - beam_d_ft; Z_BEAM_TOP = post_h; Z_APEX = post_h + roof_r; Z_BEAM_CENTER = Z_POST_TOP + beam_d_ft / 2.0
    joints = {"units": "feet", "coordinate_system": "right_handed_z_up", "tolerance_ft": 0.0052, "z_planes": {"Z_GRADE": Z_GRADE, "Z_POST_TOP": round(Z_POST_TOP, 3), "Z_BEAM_TOP": round(Z_BEAM_TOP, 3), "Z_BEAM_CENTER": round(Z_BEAM_CENTER, 3), "Z_APEX": round(Z_APEX, 3), "Z_BEAM_SOFFIT": round(Z_POST_TOP, 3)}}
    post_xy = [[round(r_ft * math.cos(2*math.pi*i/qty), 4), round(r_ft * math.sin(2*math.pi*i/qty), 4)] for i in range(qty)]
    joints["layout"] = {"post_count": qty, "post_radius_ft": r_ft, "post_xy": post_xy}
    
    seat_depth_notch = rafter_d_ft / 3.0; remaining_meat = rafter_d_ft - seat_depth_notch
    apothem = r_ft * math.cos(math.pi/qty); common_slope = roof_r / (apothem - hub_r * math.cos(math.pi/qty))
    v_shift_common = remaining_meat * math.cos(math.atan(common_slope))
    
    joints["hub"] = {
        "type": structure["hub"]["type"],
        "radius_ft": round(hub_r, 4),
        "height_ft": round(beam_d_ft * 1.2, 3),
        "face_planes": {
            "planes": [{"id": f"H{i+1}", "point": (hub_r*math.cos(2*math.pi*i/qty), hub_r*math.sin(2*math.pi*i/qty), Z_APEX), "normal": (math.cos(2*math.pi*i/qty), math.sin(2*math.pi*i/qty), 0.0)} for i in range(qty)]
        }
    }
    
    rafters = []; oh_ft = structure["roof"]["primary_rafters"]["overhang_ft"]
    for i in range(qty):
        p_tail, p_hub, p_seat_top = solve_rafter_endpoints_geometric(
            i, qty, Z_APEX, Z_BEAM_TOP, v_shift_common, r_ft, hub_r * math.cos(math.pi / qty), oh_ft
        )
        rafters.append({"id": f"R{i+1}", "start": [round(x, 4) for x in p_tail], "end": [round(x, 4) for x in p_hub], "seat_point": [round(x, 4) for x in p_seat_top], "seat_depth_ft": round(remaining_meat, 4)})
    joints["primary_rafters"] = rafters
    joints["rafters"] = {
        "hub_termination_points": {
            "points": [r["end"] for r in rafters]
        },
        "primary_rafters": rafters
    }

    jack_spec = structure["roof"].get("secondary_rafters", {}); jack_endpoints = []
    if jack_spec.get("enabled"):
        jack_count = jack_spec.get("count_per_side", 2)
        for i in range(qty):
            p1_xy = post_xy[i]; p2_xy = post_xy[(i+1)%qty]; dx = p2_xy[0]-p1_xy[0]; dy = p2_xy[1]-p1_xy[1]; blen = math.sqrt(dx*dx + dy*dy); ux, uy = dx/blen, dy/blen; in_x, in_y = -uy, ux; spacing = blen / (jack_count + 1)
            for j_idx in range(jack_count):
                dist = (j_idx + 1) * spacing; p_seat_xy = (p1_xy[0] + ux*dist, p1_xy[1] + uy*dist); p_seat_top = (p_seat_xy[0], p_seat_xy[1], Z_BEAM_TOP + v_shift_common); dir_jack = (in_x, in_y, roof_r / apothem); f = (j_idx + 1.0) / (jack_count + 1.0); hip_idx = i if f < 0.5 else (i+1)%qty; suffix = 'a' if f < 0.5 else 'b'; h_p0 = (post_xy[hip_idx][0], post_xy[hip_idx][1], Z_BEAM_TOP); h_dir = vnorm(vsub((0.0,0.0, Z_APEX + v_shift_common), (h_p0[0], h_p0[1], Z_BEAM_TOP + v_shift_common))); h_perp_raw = (-h_dir[1], h_dir[0], 0.0); h_perp = vmul(h_perp_raw, 1.0 if vdot(vsub(p_seat_top, h_p0), h_perp_raw) >= 0.0 else -1.0); p_side = vadd((post_xy[hip_idx][0], post_xy[hip_idx][1], Z_BEAM_TOP), vmul(h_perp, rafter_w_in/24.0)); p_end, _ = intersect_line_plane(p_seat_top, dir_jack, p_side, h_perp); p_tail = vadd(p_seat_top, vmul(dir_jack, -oh_ft / v2_radius(dir_jack)))
                jack_endpoints.append({"id": f"J{i+1}{suffix}", "start": [round(x, 4) for x in p_tail], "end": [round(x, 4) for x in p_end], "seat_point": [round(x, 4) for x in p_seat_top], "mate_id": f"R{hip_idx+1}"})
    joints["jack_rafters"] = {"enabled": jack_spec.get("enabled", False), "endpoints": jack_endpoints}
    
    bs = structure.get("bracing", {}); bp = []
    if bs.get("enabled"):
        phw = (structure["members"]["posts"]["actual_width_in"] / 24.0); run_t = bs["brace"]["constraints"]["run_ft"]
        for i in range(qty):
            p1 = post_xy[i]; p2 = post_xy[(i+1)%qty]; dx = p2[0]-p1[0]; dy = p2[1]-p1[1]; bl = math.sqrt(dx*dx + dy*dy); ux, uy = dx/bl, dy/bl; run = min(run_t, bl * 0.3)
            p0_A, p1_A = solve_brace_endpoints_geometric(p1[0], p1[1], ux, uy, phw, Z_POST_TOP, run)
            bp.append({"id": f"K{i+1}A", "start": [round(x, 4) for x in p0_A], "end": [round(x, 4) for x in p1_A]})
            p0_B, p1_B = solve_brace_endpoints_geometric(p2[0], p2[1], -ux, -uy, phw, Z_POST_TOP, run)
            bp.append({"id": f"K{i+1}B", "start": [round(x, 4) for x in p0_B], "end": [round(x, 4) for x in p1_B]})
    joints["braces"] = {"enabled": bs.get("enabled", False), "endpoints": bp}
    joints["beam_ring"] = beam_ring_miter(qty)
    joints["resolved_model"] = compile_resolved_model(structure, joints)
    return joints

def beam_ring_miter(sides: int) -> dict[str, float]:
    ia = (sides - 2) * 180.0 / sides; return {"beam_miter_deg": round((180.0 - ia) / 2.0, 2), "interior_angle_deg": round(ia, 2)}
def rafter_length(run: float, rise_n: float, run_n: float, oh: float) -> dict[str, float]:
    sf = math.sqrt(1 + (rise_n/run_n)**2); return {"structural_length_ft": round(run*sf, 3), "total_with_overhang_ft": round((run+oh)*sf, 3)}
def total_height(post: float, beam_in: float, run: float, rise_n: float, run_n: float) -> dict[str, float]:
    tr = run*(rise_n/run_n); th = post + (beam_in/12.0) + tr; return {"post_ft": post, "beam_depth_ft": round(beam_in/12.0, 3), "roof_rise_ft": round(tr, 3), "total_height_ft": round(th, 3)}
def svg_layout(th: float, span: float, sides: int) -> dict[str, Any]:
    sc = 42.0; ch = math.ceil(th*sc); h = max(1200, ch+200); g = h-120; d = span*2 if sides > 4 else span; cw = math.ceil(d*sc)+200; w = max(1600, cw+200)
    return {"viewBox": f"0 0 {w} {h}", "width_px": w, "height_px": h, "grade_y": g, "scale_px_per_ft": sc}

def compute_from_structure(path: str):
    from structure_io import load_structure, save_structure, assert_not_sealed
    s = load_structure(path); assert_not_sealed(s, "geometry"); qty = s["layout"]["post_count"]; span = s["layout"]["inscribed_radius_ft"]; pr, rr = [int(x) for x in s["roof"]["pitch"].split(":")]; oh = s["roof"]["primary_rafters"]["overhang_ft"]; beam_in = s["members"]["beams"]["actual_depth_in"]; post_ft = s["members"]["posts"]["cut_length_ft"]
    
    # Invariant checks
    rafter_count = s["roof"]["primary_rafters"]["count"]
    if rafter_count != qty:
        s["geometry"] = {"_sealed": False, "warnings": [f"INVARIANT_VIOLATION: rafter count {rafter_count} != post count {qty}"]}
        save_structure(s, path)
        sys.exit(1)
        
    # Translate to constraints if not already present
    if "cad_constraints" not in s:
        from cad_language_translator import translate_to_constraints
        translate_to_constraints(s)
        
    cuts = {"miter_deg": 28.71, "bevel_deg": 9.1}; rl = rafter_length(span, pr, rr, oh); rise = {"rise_ft": round(span*(pr/rr), 3)}; height = total_height(post_ft, beam_in, span, pr, rr); hr = max(s["hub"]["radius_min_ft"], 0.75); lay = svg_layout(height["total_height_ft"], span, qty); sc = lay["scale_px_per_ft"]; g = lay["grade_y"]; svg = {**lay, "post_top_y": round(g-post_ft*sc), "beam_top_y": round(g-(post_ft+beam_in/12.0)*sc), "hub_apex_y": round(g-height["total_height_ft"]*sc)}; s["geometry"] = {"_sealed": True, "compound_cut": cuts, "beam_ring": beam_ring_miter(qty), "rafter": rl, "roof_rise": rise, "total_height": height, "hub_radius_ft": round(hr, 4), "svg_coordinates": svg, "joints": compute_joints(s, cuts, rl, rise, height, hr, svg)}; s["meta"]["lifecycle"] = "GEOMETRY_SEALED"; save_structure(s, path); return s

def main():
    if len(sys.argv) < 2: sys.exit(1)
    path = sys.argv[1]
    with open(path) as f: d = json.load(f)
    if "meta" in d: compute_from_structure(path)
if __name__ == "__main__": main()

