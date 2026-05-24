#!/usr/bin/env python3
"""
geometry_engine.py (CLI)
=====================================
Purpose:
    Complete Geometry Compiler for garden-structure-designer.
    Resolves every 3D vertex and face into a 'DEAD' geometry contract.
"""
from __future__ import annotations
import json
import math
import os
import sys
import hashlib
from datetime import datetime, timezone
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCALE_PX_PER_FT: float = 42.0
GRADE_Y: int = 640
DEFAULT_BEAM_DEPTH_IN: float = 7.25
DEFAULT_POST_CUT_FT: float = 8.33
DEFAULT_SPAN_FT: float = 5.0
DEFAULT_OVERHANG_IN: float = 12.0
DEFAULT_PITCH: str = "4:12"
DEFAULT_SIDES: int = 6

# ---------------------------------------------------------------------------
# Vector Math Primitives (v5 Geometry Compiler)
# ---------------------------------------------------------------------------
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

def intersect_line_plane(p0: V3, d: V3, p_plane: V3, n: V3, eps: float = 1e-8) -> tuple[V3, float]:
    denom = vdot(d, n)
    if abs(denom) < eps: raise ValueError("Line parallel to plane")
    t = vdot(vsub(p_plane, p0), n) / denom
    return vadd(p0, vmul(d, t)), t

# ---------------------------------------------------------------------------
# Compiler Functions
# ---------------------------------------------------------------------------

def get_compound_cuts(target_normal: V3, x_axis: V3, y_axis: V3, z_axis: V3) -> tuple[float, float]:
    """Calculate miter and bevel angles for a target plane normal in a local frame."""
    local_n = (vdot(target_normal, x_axis), vdot(target_normal, y_axis), vdot(target_normal, z_axis))
    # miter is rotation around z (in xy plane)
    miter = math.degrees(math.atan2(local_n[1], abs(local_n[0])))
    # bevel is tilt from vertical (z axis)
    # n.z = cos(bevel)
    bevel = math.degrees(math.acos(vnorm(local_n)[2])) - 90.0
    return miter, bevel

def compile_resolved_model(structure: dict, joints: dict) -> dict:
    resolved = {"constraints_resolved": True, "members": []}
    qty = structure["layout"]["post_count"]
    POST_HW = (structure["members"]["posts"]["actual_width_in"] / 24.0)
    POST_HD = (structure["members"]["posts"]["actual_depth_in"] / 24.0)
    BEAM_HW = (structure["members"]["beams"]["actual_width_in"] / 24.0)
    BEAM_HD = (structure["members"]["beams"]["actual_depth_in"] / 24.0)
    RAFTER_HW = (structure["roof"]["primary_rafters"]["actual_width_in"] / 24.0)
    RAFTER_HD = (structure["roof"]["primary_rafters"]["actual_depth_in"] / 24.0)
    BRACE_HW = (structure["bracing"]["brace"]["actual_width_in"] / 24.0)
    BRACE_HD = (structure["bracing"]["brace"]["actual_depth_in"] / 24.0)
    UP = (0.0, 0.0, 1.0)
    
    def add_prism(p0: V3, p1: V3, hw: float, hd: float, up_hint: V3, role: str, bid: str):
        axis = vsub(p1, p0); u = vnorm(axis); w = vnorm(vcross(up_hint, u)); d = vnorm(vcross(w, u))
        pts = [
            vadd(vadd(p0, vmul(d, -hd)), vmul(w, -hw)), vadd(vadd(p0, vmul(d, -hd)), vmul(w,  hw)),
            vadd(vadd(p0, vmul(d,  hd)), vmul(w,  hw)), vadd(vadd(p0, vmul(d,  hd)), vmul(w, -hw)),
            vadd(vadd(p1, vmul(d, -hd)), vmul(w, -hw)), vadd(vadd(p1, vmul(d, -hd)), vmul(w,  hw)),
            vadd(vadd(p1, vmul(d,  hd)), vmul(w,  hw)), vadd(vadd(p1, vmul(d,  hd)), vmul(w, -hw)),
        ]
        faces = [
            {"verts": [0, 3, 2, 1], "normal": list(vmul(u, -1)), "color_key": "start"},
            {"verts": [4, 5, 6, 7], "normal": list(u),          "color_key": "end"},
            {"verts": [0, 1, 5, 4], "normal": list(vmul(d, -1)), "color_key": "top"},
            {"verts": [3, 7, 6, 2], "normal": list(d),          "color_key": "bottom"},
            {"verts": [0, 4, 7, 3], "normal": list(vmul(w, -1)), "color_key": "left"},
            {"verts": [1, 2, 6, 5], "normal": list(w),          "color_key": "right"}
        ]
        resolved["members"].append({
            "id": bid, "role": role, "p0": list(p0), "p1": list(p1),
            "axis_u": list(u), "axis_w": list(w), "axis_d": list(d),
            "vertices": [list(v) for v in pts], "faces": faces,
            "saw_angles": {
                "start": {"miter_deg": 0.0, "bevel_deg": 0.0},
                "end": {"miter_deg": 0.0, "bevel_deg": 0.0}
            }
        })


    def add_notched_rafter(p_tail: V3, p_apex: V3, p_seat: V3, hw: float, hd: float, seat_depth_notch: float, up_hint: V3, role: str, bid: str):
        u = vnorm(vsub(p_apex, p_tail)); w = vnorm(vcross(up_hint, u)); d_perp = vnorm(vcross(w, u))
        full_depth = hd * 2.0; cos_pitch = v2_radius(u); z_seat = p_seat[2] - (full_depth - seat_depth_notch) * cos_pitch
        def get_side_pts(lateral: float) -> list[V3]:
            v0 = vadd(vadd(p_tail, vmul(d_perp, 0)), vmul(w, lateral)); v1 = vadd(vadd(p_apex, vmul(d_perp, 0)), vmul(w, lateral))
            v2 = (v1[0], v1[1], v1[2] - full_depth/cos_pitch if cos_pitch > 0.1 else v1[2]-full_depth)
            v4 = (v0[0] + (p_seat[0]-p_tail[0]), v0[1] + (p_seat[1]-p_tail[1]), z_seat)
            v3 = (v4[0], v4[1], v4[2] - seat_depth_notch/cos_pitch if cos_pitch > 0.1 else v4[2]-seat_depth_notch)
            v5 = (v0[0], v0[1], z_seat); return [v0, v1, v2, v3, v4, v5]
        pts_l = get_side_pts(-hw); pts_r = get_side_pts(hw); all_pts = pts_l + pts_r
        faces = [
            {"verts": [0, 6, 7, 1], "normal": list(vmul(d_perp, -1)), "color_key": "top"},
            {"verts": [1, 7, 8, 2], "normal": list(u), "color_key": "end"},
            {"verts": [2, 8, 9, 3], "normal": list(d_perp), "color_key": "bottom"},
            {"verts": [3, 9, 10, 4], "normal": list(vmul(u, -1)), "color_key": "other"},
            {"verts": [4, 10, 11, 5], "normal": [0, 0, -1], "color_key": "bottom"},
            {"verts": [5, 11, 6, 0], "normal": list(vmul(u, -1)), "color_key": "start"},
            {"verts": [0, 1, 2, 3, 4, 5], "normal": list(vmul(w, -1)), "color_key": "left"},
            {"verts": [11, 10, 9, 8, 7, 6], "normal": list(w), "color_key": "right"}
        ]
        resolved["members"].append({
            "id": bid, "role": role, "p0": list(p_tail), "p1": list(p_apex),
            "axis_u": list(u), "axis_w": list(w), "axis_d": list(d_perp),
            "vertices": [list(v) for v in all_pts], "faces": faces
        })


    zp = joints["z_planes"]; pxy = joints["layout"]["post_xy"]
    for i, p in enumerate(pxy): add_prism((p[0], p[1], zp["Z_GRADE"]), (p[0], p[1], zp["Z_POST_TOP"]), POST_HW, POST_HD, UP, "post", f"P{i+1}")
    for i in range(qty): add_prism((pxy[i][0], pxy[i][1], zp["Z_BEAM_CENTER"]), (pxy[(i+1)%qty][0], pxy[(i+1)%qty][1], zp["Z_BEAM_CENTER"]), BEAM_HW, BEAM_HD, UP, "beam", f"B{i+1}")
    for bj in joints.get("braces", {}).get("endpoints", []): add_prism(tuple(bj["start"]), tuple(bj["end"]), BRACE_HW, BRACE_HD, UP, "brace", bj["id"])
    for rj in joints["primary_rafters"]: add_notched_rafter(tuple(rj["start"]), tuple(rj["end"]), tuple(rj["seat_point"]), RAFTER_HW, RAFTER_HD, rj["seat_depth_ft"], UP, "rafter", rj["id"])
    if joints["jack_rafters"]["enabled"]:
        for ep in joints["jack_rafters"]["endpoints"]: add_notched_rafter(tuple(ep["start"]), tuple(ep["end"]), tuple(ep["seat_point"]), RAFTER_HW, RAFTER_HD, joints["primary_rafters"][0]["seat_depth_ft"], UP, "rafter", ep["id"])
    
    hj = joints["hub"]; hr = hj["radius_ft"]; hh = hj["height_ft"]; az = zp["Z_APEX"]; hz_t = az + hh/2.0; hz_b = az - hh/2.0; r_c = hr / math.cos(math.pi/qty)
    t_ring = [(r_c*math.cos(2*math.pi*(i-0.5)/qty), r_c*math.sin(2*math.pi*(i-0.5)/qty), hz_t) for i in range(qty)]
    b_ring = [(r_c*math.cos(2*math.pi*(i-0.5)/qty), r_c*math.sin(2*math.pi*(i-0.5)/qty), hz_b) for i in range(qty)]
    h_faces = [{"verts": list(range(qty)), "normal": [0,0,1], "color_key": "top"}, {"verts": list(reversed(range(qty, 2*qty))), "normal": [0,0,-1], "color_key": "bottom"}]
    for i in range(qty): j = (i+1)%qty; fn = (math.cos(2*math.pi*i/qty), math.sin(2*math.pi*i/qty), 0.0); h_faces.append({"verts": [qty+i, qty+j, j, i], "normal": list(fn), "color_key": "left"})
    resolved["members"].append({
        "id": "HUB", "role": "hub", "p0": [0,0,hz_b], "p1": [0,0,hz_t],
        "axis_u": [0,0,1], "axis_w": [1,0,0], "axis_d": [0,1,0],
        "vertices": [list(v) for v in t_ring+b_ring], "faces": h_faces
    })

    return resolved

def compute_joints(structure, cuts, rl, rise, height, hub_r, svg_coords):
    joints = {"units": "feet", "coordinate_system": "right_handed_z_up", "tolerance_ft": 0.0052, "notes": ["Derived by geometry_engine.py (v5 Geometry Compiler)."]}
    qty = structure["layout"]["post_count"]; r_ft = structure["layout"]["inscribed_radius_ft"]
    post_h = structure["members"]["posts"]["cut_length_ft"]; beam_d_in = structure["members"]["beams"]["actual_depth_in"]; beam_d_ft = beam_d_in / 12.0; roof_r = rise["rise_ft"]
    rafter_d_in = structure["roof"]["primary_rafters"]["actual_depth_in"]; rafter_w_in = structure["roof"]["primary_rafters"]["actual_width_in"]; rafter_d_ft = rafter_d_in / 12.0
    Z_GRADE = 0.0; Z_POST_TOP = post_h - beam_d_ft; Z_BEAM_CENTER = Z_POST_TOP + beam_d_ft / 2.0; Z_BEAM_TOP = post_h; Z_APEX = post_h + roof_r
    joints["z_planes"] = {"Z_GRADE": Z_GRADE, "Z_POST_TOP": round(Z_POST_TOP, 3), "Z_BEAM_TOP": round(Z_BEAM_TOP, 3), "Z_BEAM_CENTER": round(Z_BEAM_CENTER, 3), "Z_APEX": round(Z_APEX, 3), "Z_BEAM_SOFFIT": round(Z_POST_TOP, 3)}
    post_xy = [[round(r_ft * math.cos(2*math.pi*i/qty), 4), round(r_ft * math.sin(2*math.pi*i/qty), 4)] for i in range(qty)]
    joints["layout"] = {"post_count": qty, "post_radius_ft": r_ft, "post_xy": post_xy}
    APEX = (0.0, 0.0, Z_APEX); hub_radius = hub_r; hub_face_planes = []
    for i in range(qty): theta = 2*math.pi*i/qty; nx = math.cos(theta); ny = math.sin(theta); hub_face_planes.append({"id": f"H{i+1}", "point": (hub_radius * nx, hub_radius * ny, Z_APEX), "normal": (nx, ny, 0.0)})
    joints["hub"] = {"type": structure["hub"]["type"], "radius_ft": round(hub_radius, 4), "height_ft": round(beam_d_ft * 1.2, 3), "face_planes": hub_face_planes}
    rafters = []; overhang_ft = structure["roof"]["primary_rafters"]["overhang_ft"]
    for i in range(qty):
        p_post = (post_xy[i][0], post_xy[i][1], Z_BEAM_TOP); dir_hip = vnorm(vsub(APEX, p_post))
        p_hub_face, _ = intersect_line_plane(p_post, dir_hip, hub_face_planes[i]["point"], hub_face_planes[i]["normal"])
        seat_depth = rafter_d_ft / 3.0; pitch_rad = math.atan(rise["rise_ft"] / r_ft); v_shift = (rafter_d_ft - seat_depth) * math.cos(pitch_rad)
        p0 = (p_post[0] - dir_hip[0]*overhang_ft, p_post[1] - dir_hip[1]*overhang_ft, p_post[2] - dir_hip[2]*overhang_ft + v_shift); p1 = (p_hub_face[0], p_hub_face[1], p_hub_face[2] + v_shift)
        rafters.append({"id": f"R{i+1}", "start": [round(x, 4) for x in p0], "end": [round(x, 4) for x in p1], "seat_point": [round(x, 4) for x in vadd(p_post, (0,0,v_shift))], "seat_depth_ft": round(seat_depth, 4)})
    joints["primary_rafters"] = rafters
    jack_spec = structure["roof"].get("secondary_rafters", {}); jack_endpoints = []
    if jack_spec.get("enabled"):
        jack_count = jack_spec.get("count_per_side", 2)
        for i in range(qty):
            p1_xy = post_xy[i]; p2_xy = post_xy[(i+1)%qty]; dx, dy = p2_xy[0]-p1_xy[0], p2_xy[1]-p1_xy[1]; blen = math.sqrt(dx*dx + dy*dy); ux, uy = dx/blen, dy/blen; spacing = blen / (jack_count + 1); in_x, in_y = -uy, ux; apothem = r_ft * math.cos(math.pi/qty); common_slope = roof_r / (apothem - hub_radius * math.cos(math.pi/qty)); c_v_shift = (rafter_d_ft - (rafter_d_ft/3.0)) * math.cos(math.atan(common_slope))
            for j_idx in range(jack_count):
                dist = (j_idx + 1) * spacing; p_seat = (p1_xy[0] + ux*dist, p1_xy[1] + uy*dist, Z_BEAM_TOP); p_start = (p_seat[0] - in_x*overhang_ft, p_seat[1] - in_y*overhang_ft, p_seat[2] - common_slope*overhang_ft + c_v_shift); dir_jack = (in_x, in_y, common_slope); f = (j_idx + 1.0) / (jack_count + 1.0); hip_idx = i if f < 0.5 else (i+1)%qty; suffix = 'a' if f < 0.5 else 'b'; h_p1 = (post_xy[hip_idx][0], post_xy[hip_idx][1], Z_BEAM_TOP); h_dir = vnorm(vsub(APEX, h_p1)); h_perp_xy = (-h_dir[1], h_dir[0], 0.0); n_hip_side = vmul(h_perp_xy, 1.0 if vdot(vsub(p_start, h_p1), h_perp_xy) >= 0 else -1.0); p_hip_side = vadd(h_p1, vmul(n_hip_side, rafter_w_in/24.0)); p_end, _ = intersect_line_plane(p_start, dir_jack, p_hip_side, n_hip_side)
                jack_endpoints.append({"id": f"J{i+1}{suffix}", "start": [round(x, 4) for x in p_start], "end": [round(x, 4) for x in p_end], "seat_point": [round(p_seat[0], 4), round(p_seat[1], 4), round(p_seat[2] + c_v_shift, 4)], "mate_id": f"R{hip_idx+1}"})
    joints["jack_rafters"] = {"enabled": jack_spec.get("enabled", False), "endpoints": jack_endpoints}
    bracing_spec = structure.get("bracing", {}); brace_pairs = []
    if bracing_spec.get("enabled"):
        b_len = bracing_spec["brace"]["length_ft"]; b_ang = math.radians(bracing_spec["brace"]["angle_deg"]); b_run = b_len * math.cos(b_ang); b_drop = b_len * math.sin(b_ang); post_hw = (structure["members"]["posts"]["actual_width_in"] / 24.0)
        for i in range(qty):
            vi = (post_xy[i][0], post_xy[i][1]); vj = (post_xy[(i+1)%qty][0], post_xy[(i+1)%qty][1]); dx, dy = vnorm((vj[0]-vi[0], vj[1]-vi[1], 0.0))[:2]
            brace_pairs.append({"id": f"K{i+1}A", "start": [vi[0]+dx*post_hw, vi[1]+dy*post_hw, Z_POST_TOP - b_drop], "end": [vi[0]+dx*(post_hw+b_run), vi[1]+dy*(post_hw+b_run), Z_POST_TOP]})
            vk = (post_xy[(i-1)%qty][0], post_xy[(i-1)%qty][1]); dkx, dky = vnorm((vk[0]-vi[0], vk[1]-vi[1], 0.0))[:2]
            brace_pairs.append({"id": f"K{i+1}B", "start": [vi[0]+dkx*post_hw, vi[1]+dky*post_hw, Z_POST_TOP - b_drop], "end": [vi[0]+dkx*(post_hw+b_run), vi[1]+dky*(post_hw+b_run), Z_POST_TOP]})
    joints["braces"] = {"enabled": bracing_spec.get("enabled", False), "endpoints": brace_pairs}
    joints["resolved_model"] = compile_resolved_model(structure, joints)
    return joints

def beam_ring_miter(sides: int) -> dict[str, float]:
    interior_angle = (sides - 2) * 180.0 / sides
    return {"beam_miter_deg": round((180.0 - interior_angle) / 2.0, 2), "interior_angle_deg": round(interior_angle, 2)}

def compound_cut(rise_n: float, run_n: float, sides: int) -> dict[str, float]:
    pa = math.atan(rise_n / run_n); ph = math.radians(360.0 / (2.0 * sides))
    return {"miter_deg": round(math.degrees(math.atan(math.cos(pa) * math.tan(ph))), 2), "bevel_deg": round(math.degrees(math.asin(math.sin(pa) * math.sin(ph))), 2)}

def rafter_length(run: float, rise_n: float, run_n: float, oh: float) -> dict[str, float]:
    sf = math.sqrt(1 + (rise_n/run_n)**2)
    return {"structural_length_ft": round(run*sf, 3), "total_with_overhang_ft": round((run+oh)*sf, 3)}

def roof_rise(run: float, rise_n: float, run_n: float) -> dict[str, float]:
    return {"rise_ft": round(run*(rise_n/run_n), 3)}

def total_height(post: float, beam_in: float, run: float, rise_n: float, run_n: float) -> dict[str, float]:
    tr = run*(rise_n/run_n); th = post + (beam_in/12.0) + tr
    return {"post_ft": post, "beam_depth_ft": round(beam_in/12.0, 3), "roof_rise_ft": round(tr, 3), "total_height_ft": round(th, 3)}

def svg_layout(th: float, span: float, sides: int) -> dict[str, Any]:
    ch = math.ceil(th*42.0); h = max(1200, ch+200); g = h-120
    d = span*2 if sides > 4 else span; cw = math.ceil(d*42.0)+200; w = max(1600, cw+200)
    return {"viewBox": f"0 0 {w} {h}", "width_px": w, "height_px": h, "grade_y": g, "scale_px_per_ft": 42.0}

def compute_from_structure(path: str):
    from structure_io import load_structure, save_structure, assert_not_sealed
    s = load_structure(path); assert_not_sealed(s, "geometry")
    qty = s["layout"]["post_count"]; span = s["layout"]["inscribed_radius_ft"]
    pr, rr = [int(x) for x in s["roof"]["pitch"].split(":")]; oh = s["roof"]["primary_rafters"]["overhang_ft"]
    beam_in = s["members"]["beams"]["actual_depth_in"]; post_ft = s["members"]["posts"]["cut_length_ft"]
    cuts = compound_cut(pr, rr, qty); rl = rafter_length(span, pr, rr, oh); rise = roof_rise(span, pr, rr); height = total_height(post_ft, beam_in, span, pr, rr)
    hr = max(s["hub"]["radius_min_ft"], (s["roof"]["primary_rafters"]["actual_width_in"] + s["roof"]["primary_rafters"]["actual_depth_in"])/12.0)
    lay = svg_layout(height["total_height_ft"], span, qty); sc = lay["scale_px_per_ft"]; g = lay["grade_y"]
    svg = {**lay, "post_top_y": round(g-post_ft*sc), "beam_top_y": round(g-(post_ft+beam_in/12.0)*sc), "hub_apex_y": round(g-height["total_height_ft"]*sc)}
    s["geometry"] = {"_sealed": True, "compound_cut": cuts, "beam_ring": beam_ring_miter(qty), "rafter": rl, "roof_rise": rise, "total_height": height, "hub_radius_ft": round(hr, 4), "svg_coordinates": svg, "joints": compute_joints(s, cuts, rl, rise, height, hr, svg)}
    s["meta"]["lifecycle"] = "GEOMETRY_SEALED"; save_structure(s, path)
    return s

def main():
    if len(sys.argv) < 2: sys.exit(1)
    path = sys.argv[1]
    with open(path) as f: d = json.load(f)
    if "meta" in d: compute_from_structure(path)
    else: pass # Legacy removed for brevity
if __name__ == "__main__": main()
