from __future__ import annotations
import math
#!/usr/bin/env python3
"""
geometry_engine.py (CLI)
=====================================

Purpose:
    geometry_engine.py (CLI) =====================================

Layer: Execution

Usage Examples:
    python geometry_engine.py [args]

Supported Object Types:
    JSON, SVG, Markdown

CLI Arguments:
    Varies per script, typically input file paths.

Input Files:
    context/staging/ *.json outputs/ *.svg

Output:
    Validation codes (0 or 1), generated JSON or SVG files.

Key Functions:
    Refer to module docstring or inner functions.

Script Dependencies:
    Standard library json, os, sys, math, hashlib, etc.

Consumed by:
    design-orchestrator, various skills in the pipeline.
"""

import json
import math
import os
import sys
import hashlib
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCALE_PX_PER_FT: float = 42.0  # standard plugin coordinate scale
GRADE_Y: int = 640              # canonical SVG grade baseline (pixels)
DEFAULT_BEAM_DEPTH_IN: float = 7.25
DEFAULT_POST_CUT_FT: float = 8.33
DEFAULT_SPAN_FT: float = 5.0
DEFAULT_OVERHANG_IN: float = 12.0
DEFAULT_PITCH: str = "4:12"
DEFAULT_SIDES: int = 6

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _deg(radians: float) -> float:
    """Convert radians to degrees."""
    return math.degrees(radians)


def _rad(degrees: float) -> float:
    """Convert degrees to radians."""
    return math.radians(degrees)


# ---------------------------------------------------------------------------
# Structural Math
# ---------------------------------------------------------------------------


def compound_cut(pitch_rise: float, pitch_run: float, sides: int) -> dict[str, float]:
    """
    Compute compound miter and bevel angles for a hip rafter at a regular polygon hub.

    Uses the canonical timber-framing formula:
        Miter = arctan(cos(pitch_angle) × tan(plan_half_angle))
        Bevel = arcsin(sin(pitch_angle) × sin(plan_half_angle))

    Source: Gross, M. "Roof Framing" (Tab Books, 1984); validated against
    Granlund & Bartholomew "Compound Angle Calculator for Regular Polygons."

    CRITICAL: For a hexagonal (sides=6) structure at 4:12 pitch:
        - pitch_angle  = 18.43°
        - plan_half    = 30°
        - Miter        = 28.71°  ← NOT 18.43° (common hallucination)
        - Bevel        = 9.10°   ← NOT 15.6°  (common hallucination)

    Args:
        pitch_rise: Numerator of the pitch ratio (e.g. 4 for 4:12).
        pitch_run: Denominator of the pitch ratio (e.g. 12 for 4:12).
        sides: Number of sides of the polygon (e.g. 6 for hexagon).

    Returns:
        Dictionary with miter_deg, bevel_deg, pitch_angle_deg, plan_half_angle_deg.
    """
    pitch_angle = math.atan(pitch_rise / pitch_run)
    plan_half = _rad(360.0 / (2.0 * sides))
    miter = math.atan(math.cos(pitch_angle) * math.tan(plan_half))
    bevel = math.asin(math.sin(pitch_angle) * math.sin(plan_half))
    return {
        "miter_deg": round(_deg(miter), 2),
        "bevel_deg": round(_deg(bevel), 2),
        "pitch_angle_deg": round(_deg(pitch_angle), 2),
        "plan_half_angle_deg": round(_deg(plan_half), 2),
    }


def beam_ring_miter(sides: int) -> dict[str, float]:
    """
    Compute beam ring plan-angle miter for a regular polygon.
    This is a FLAT cut (no pitch component). Do not confuse with
    the hip rafter compound miter which includes pitch.

    For hexagon: interior = 120°, beam_miter = 30.0°
    For square:  interior = 90°,  beam_miter = 45.0°
    For octagon: interior = 135°, beam_miter = 22.5°
    """
    interior_angle = (sides - 2) * 180.0 / sides
    beam_miter = (180.0 - interior_angle) / 2.0
    return {
        "beam_miter_deg": round(beam_miter, 2),
        "interior_angle_deg": round(interior_angle, 2),
    }


def rafter_length(
    run_ft: float,
    pitch_rise: float,
    pitch_run: float,
    overhang_ft: float = 0.0,
) -> dict[str, float]:
    """
    Compute actual rafter length from beam-bearing to tail (including overhang).

    Args:
        run_ft: Horizontal run from post centre-line to hub centre (feet).
        pitch_rise: Pitch rise numerator (e.g. 4).
        pitch_run: Pitch run denominator (e.g. 12).
        overhang_ft: Horizontal overhang beyond post CL (feet).

    Returns:
        Dictionary with structural_length_ft, total_with_overhang_ft,
        total_with_overhang_in.
    """
    slope_factor = math.sqrt(1 + (pitch_rise / pitch_run) ** 2)
    structural_ft = run_ft * slope_factor
    total_ft = (run_ft + overhang_ft) * slope_factor
    return {
        "structural_length_ft": round(structural_ft, 3),
        "total_with_overhang_ft": round(total_ft, 3),
        "total_with_overhang_in": round(total_ft * 12, 2),
    }


def roof_rise(
    run_ft: float,
    pitch_rise: float,
    pitch_run: float,
) -> dict[str, float]:
    """
    Compute vertical rise of the roof over a given horizontal run.

    Args:
        run_ft: Horizontal run from post CL to hub (feet).
        pitch_rise: Pitch rise numerator.
        pitch_run: Pitch run denominator.

    Returns:
        Dictionary with rise_ft and rise_in.
    """
    rise_ft = run_ft * (pitch_rise / pitch_run)
    return {
        "rise_ft": round(rise_ft, 3),
        "rise_in": round(rise_ft * 12, 2),
    }


def total_height(
    post_length_ft: float,
    beam_depth_in: float,
    roof_run_ft: float,
    pitch_rise: float,
    pitch_run: float,
) -> dict[str, float]:
    """
    Compute grade-to-apex total building height.

    Args:
        post_length_ft: Post cut length in feet.
        beam_depth_in: Beam depth in inches.
        roof_run_ft: Horizontal run from post to hub (feet).
        pitch_rise: Pitch rise numerator.
        pitch_run: Pitch run denominator.

    Returns:
        Dictionary with post_ft, beam_depth_ft, roof_rise_ft, total_height_ft,
        total_height_in.
    """
    beam_ft = beam_depth_in / 12.0
    rise_ft = roof_run_ft * (pitch_rise / pitch_run)
    total_ft = post_length_ft + beam_ft + rise_ft
    return {
        "post_ft": round(post_length_ft, 3),
        "beam_depth_ft": round(beam_ft, 3),
        "roof_rise_ft": round(rise_ft, 3),
        "total_height_ft": round(total_ft, 3),
        "total_height_in": round(total_ft * 12, 2),
    }


def svg_layout(
    total_height_ft: float,
    span_ft: float,
    sides: int,
    scale_px_per_ft: float = 42.0,
    margin_top_px: int = 80,
    margin_bottom_px: int = 120,
    min_height_px: int = 1200,
    min_width_px: int = 1600,
) -> dict[str, Any]:
    """
    Compute dynamic SVG viewport dimensions and coordinate datums.
    Replaces the fixed GRADE_Y=640 constant.

    All drawing-generator and shop-blueprint-generator agents MUST read
    their viewBox and grade_y from this output.
    """
    content_height_px = math.ceil(total_height_ft * scale_px_per_ft)
    height_px = max(min_height_px, content_height_px + margin_top_px + margin_bottom_px)
    grade_y = height_px - margin_bottom_px

    # For plan views, compute width from polygon diameter
    diameter_ft = span_ft * 2 if sides > 4 else span_ft
    content_width_px = math.ceil(diameter_ft * scale_px_per_ft) + 200  # label margins
    width_px = max(min_width_px, content_width_px + 200)

    return {
        "viewBox": f"0 0 {width_px} {height_px}",
        "width_px": width_px,
        "height_px": height_px,
        "margin_top_px": margin_top_px,
        "margin_bottom_px": margin_bottom_px,
        "grade_y": grade_y,
        "scale_px_per_ft": scale_px_per_ft,
        "content_height_px": content_height_px,
        "content_width_px": content_width_px,
    }


def svg_scale_map(
    structural_model: dict[str, Any],
    scale_px_per_ft: float = SCALE_PX_PER_FT,
) -> dict[str, Any]:
    """
    Derive canonical SVG pixel Y-coordinates from structural model values.

    All drawing-generator and shop-blueprint-generator agents must read their
    pixel coordinates from this output — never compute them independently.

    Args:
        structural_model: Parsed structural-model.json content.
        scale_px_per_ft: Pixels per foot (default 42.0).

    Returns:
        Dictionary mapping datum names to pixel coordinates.
    """
    # Support both 'members' (canonical schema) and 'structuralElements' (legacy)
    members = structural_model.get("members") or structural_model.get("structuralElements", {})
    posts = members.get("posts", {})
    beams = members.get("beams") or members.get("ringBeams", {})
    roof = members.get("roofStructure") or structural_model.get("roofStructure", {})

    post_ft = posts.get("cutLength_ft", DEFAULT_POST_CUT_FT)
    beam_in = beams.get("depth_in", DEFAULT_BEAM_DEPTH_IN)
    pitch_str = roof.get("pitch", DEFAULT_PITCH)
    rise_n, run_n = [int(x) for x in pitch_str.split(":")]
    span_ft = posts.get("spanDistance_ft", DEFAULT_SPAN_FT)
    sides = posts.get("quantity", DEFAULT_SIDES)

    post_px = post_ft * scale_px_per_ft
    beam_px = (beam_in / 12.0) * scale_px_per_ft
    rise_px = span_ft * (rise_n / run_n) * scale_px_per_ft
    
    total_ft = post_ft + (beam_in / 12.0) + (span_ft * (rise_n / run_n))
    layout = svg_layout(total_ft, span_ft, sides, scale_px_per_ft)
    grade_y = layout["grade_y"]

    result = {
        **layout,
        "post_top_y": round(grade_y - post_px),
        "beam_soffit_y": round(grade_y - post_px),
        "beam_top_y": round(grade_y - post_px - beam_px),
        "hub_apex_y": round(grade_y - post_px - beam_px - rise_px),
        "rise_px": round(rise_px),
        "beam_px": round(beam_px),
        "post_px": round(post_px),
    }
    return result


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------


def compute(model_path: str) -> dict[str, Any]:
    """
    Load structural-model.json and compute the full geometry calculation set.

    Args:
        model_path: Absolute or relative path to structural-model.json.

    Returns:
        Complete geometry-calculations dict ready for JSON serialisation.
    """
    with open(model_path, 'rb') as f:
        raw_bytes = f.read()
    model = json.loads(raw_bytes.decode('utf-8'))
    model_hash = hashlib.sha256(raw_bytes).hexdigest()

    # Support both 'members' (canonical) and 'structuralElements' (legacy)
    members = model.get("members") or model.get("structuralElements", {})
    posts = members.get("posts", {})
    beams = members.get("beams") or members.get("ringBeams", {})
    roof = members.get("roofStructure") or model.get("roofStructure", {})

    sides = posts.get("quantity", DEFAULT_SIDES)
    pitch = roof.get("pitch", DEFAULT_PITCH)
    pr, rr = [int(x) for x in pitch.split(":")]
    span_ft = posts.get("spanDistance_ft", DEFAULT_SPAN_FT)
    overhang_in = model.get("overhang_in", DEFAULT_OVERHANG_IN)
    beam_depth_in = beams.get("depth_in", DEFAULT_BEAM_DEPTH_IN)
    post_cut_ft = posts.get("cutLength_ft", DEFAULT_POST_CUT_FT)

    cuts = compound_cut(pr, rr, sides)
    rl = rafter_length(span_ft, pr, rr, overhang_in / 12.0)
    rise = roof_rise(span_ft, pr, rr)
    height = total_height(post_cut_ft, beam_depth_in, span_ft, pr, rr)
    svg = svg_scale_map(model)

    result: dict[str, Any] = {
        "schema": "geometry-calculations/1.0",
        "source": model_path,
        "pitch": pitch,
        "sides": sides,
        "compound_cut": cuts,
        "beam_ring": beam_ring_miter(sides),
        "rafter": rl,
        "roof_rise": rise,
        "total_height": height,
        "svg_coordinates": svg,
        "warnings": [],
        "source_hash": model_hash,
    }

    # Height limit guard — reads from sibling design-spec.json if present
    design_spec_path = os.path.join(os.path.dirname(model_path), "design-spec.json")
    if os.path.exists(design_spec_path):
        with open(design_spec_path) as f:
            spec = json.load(f)
        limit = spec.get("heightConstraints", {}).get("totalHeightLimit_ft")
        if limit and height["total_height_ft"] > limit:
            result["warnings"].append(
                f"FAIL: total_height_ft={height['total_height_ft']:.3f} "
                f"exceeds design-spec limit of {limit} ft."
            )

    return result


# ---------------------------------------------------------------------------
# M1+ entry point: structure.json in-place geometry computation
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Vector Math Primitives
# ---------------------------------------------------------------------------

V3 = tuple[float, float, float]

def vdot(a: V3, b: V3) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def vcross(a: V3, b: V3) -> V3:
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])

def vsub(a: V3, b: V3) -> V3:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def vadd(a: V3, b: V3) -> V3:
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def vmul(a: V3, s: float) -> V3:
    return (a[0]*s, a[1]*s, a[2]*s)

def vlen(a: V3) -> float:
    return math.sqrt(vdot(a, a))

def vnorm(a: V3) -> V3:
    length = vlen(a)
    return vmul(a, 1.0/length) if length > 1e-9 else (0.0, 0.0, 0.0)

def vdist(a: V3, b: V3) -> float:
    return vlen(vsub(a, b))

def intersect_line_plane(p0: V3, d: V3, p_plane: V3, n: V3, eps: float = 1e-8) -> tuple[V3, float]:
    """Return p = p0 + t*d where p lies on plane defined by (p_plane, n)."""
    denom = vdot(d, n)
    if abs(denom) < eps:
        raise ValueError("Line parallel to plane")
    t = vdot(vsub(p_plane, p0), n) / denom
    return vadd(p0, vmul(d, t)), t


def compute_joints(structure, cuts, rl, rise, height, hub_r, svg_coords):
    joints = {
        "units": "feet",
        "coordinate_system": "right_handed_z_up",
        "tolerance_ft": 0.0052,
        "notes": [
            "Derived by geometry_engine.py (v4 Professional-Grade). Do not manually edit.",
            "All rafters derived from dual-constraint roof planes (z=f(x,y) + apex convergence).",
            "Single source of truth for all downstream CAD and fabrication."
        ]
    }
    
    qty = structure["layout"]["post_count"]
    r_ft = structure["layout"]["inscribed_radius_ft"]
    post_h = structure["members"]["posts"]["cut_length_ft"]
    beam_d_in = structure["members"]["beams"]["actual_depth_in"]
    beam_d_ft = beam_d_in / 12.0
    roof_r = rise["rise_ft"]
    
    # Phase 4: Proportional Hard Constraints
    rafter_d_in = structure["roof"]["primary_rafters"]["actual_depth_in"]
    rafter_w_in = structure["roof"]["primary_rafters"]["actual_width_in"]
    rafter_d_ft = rafter_d_in / 12.0
    if beam_d_in <= rafter_d_in:
        print(f"WARNING: Proportional inconsistency detected (Beam Depth {beam_d_in}\" <= Rafter Depth {rafter_d_in}\")", file=sys.stderr)
    
    Z_GRADE = 0.0
    Z_POST_TOP = post_h - beam_d_ft
    Z_BEAM_CENTER = Z_POST_TOP + beam_d_ft / 2.0
    Z_BEAM_TOP = post_h
    Z_APEX = post_h + roof_r
    
    joints["z_planes"] = {
        "Z_GRADE": Z_GRADE,
        "Z_POST_TOP": round(Z_POST_TOP, 3),
        "Z_BEAM_TOP": round(Z_BEAM_TOP, 3),
        "Z_BEAM_CENTER": round(Z_BEAM_CENTER, 3),
        "Z_APEX": round(Z_APEX, 3),
        "Z_BEAM_SOFFIT": round(Z_POST_TOP, 3)
    }
    
    post_xy = []
    for i in range(qty):
        x = r_ft * math.cos(2*math.pi*i/qty)
        y = r_ft * math.sin(2*math.pi*i/qty)
        post_xy.append([round(x, 4), round(y, 4)])
        
    joints["layout"] = {
        "post_count": qty,
        "post_radius_ft": r_ft,
        "post_xy": post_xy,
    }
    
    # ── Phase 1: Dual-Constraint Roof Planes ────────────────────────────────
    # Apex node
    APEX = (0.0, 0.0, Z_APEX)
    
    # Define N roof planes (triangular segments)
    # Each plane i covers the sector between Post i and Post i+1
    roof_planes = []
    for i in range(qty):
        p1 = (post_xy[i][0], post_xy[i][1], Z_BEAM_TOP)
        p2 = (post_xy[(i+1)%qty][0], post_xy[(i+1)%qty][1], Z_BEAM_TOP)
        # Normal of plane formed by (Apex, Post i, Post i+1)
        v1 = vsub(p1, APEX)
        v2 = vsub(p2, APEX)
        normal = vnorm(vcross(v1, v2))
        roof_planes.append({
            "sector": i,
            "anchor": APEX,
            "normal": normal
        })

    # ── Phase 3: Hub as Joint System ─────────────────────────────────────────
    # Hub defines termination planes and shoulder offsets
    hub_radius = hub_r
    hub_face_planes = []
    hub_term_points = []
    
    for i in range(qty):
        theta = 2*math.pi*i/qty
        nx = math.cos(theta); ny = math.sin(theta)
        # Vertical termination plane
        p_hub = (hub_radius * nx, hub_radius * ny, Z_APEX)
        n_hub = (nx, ny, 0.0)
        hub_face_planes.append({"id": f"H{i+1}", "point": p_hub, "normal": n_hub})

    joints["hub"] = {
        "type": structure["hub"]["type"],
        "radius_ft": round(hub_radius, 4),
        "height_ft": round(beam_d_ft * 1.2, 3), # Phase 4 massing rule
        "face_planes": hub_face_planes
    }

    # ── Primary Rafters (Hips) ──────────────────────────────────────────────
    # Hips follow the Post-to-Apex line.
    rafters = []
    overhang_ft = structure["roof"]["primary_rafters"]["overhang_ft"]
    
    for i in range(qty):
        # 1. Theoretical Axis (Post CL to Apex)
        p_post = (post_xy[i][0], post_xy[i][1], Z_BEAM_TOP)
        dir_hip = vnorm(vsub(APEX, p_post))
        
        # 2. Intersect with Hub Face Plane
        p_hub_face, _ = intersect_line_plane(p_post, dir_hip, hub_face_planes[i]["point"], hub_face_planes[i]["normal"])
        
        # 3. Apply Birdsmouth Seating Logic (Phase 2)
        # The rafter bottom face must rest on Z_BEAM_TOP.
        # Theoretical axis is currently at Z_BEAM_TOP at the post.
        # We need to shift it up so the NOTCH is at Z_BEAM_TOP.
        # Notch depth is 1/3 of rafter depth.
        seat_depth = rafter_d_ft / 3.0
        pitch_rad = math.acos(vdot(dir_hip, (dir_hip[0], dir_hip[1], 0.0)) / vlen((dir_hip[0], dir_hip[1], 1e-9)))
        # Vertical shift = (depth - seat_depth) / cos(pitch)
        v_shift = (rafter_d_ft - seat_depth) / math.cos(math.atan(rise["rise_ft"] / r_ft)) # Simplified pitch for hip
        
        p0 = (p_post[0] - dir_hip[0]*overhang_ft, p_post[1] - dir_hip[1]*overhang_ft, p_post[2] - dir_hip[2]*overhang_ft + v_shift)
        p1 = (p_hub_face[0], p_hub_face[1], p_hub_face[2] + v_shift)
        
        rafters.append({
            "id": f"R{i+1}",
            "start": [round(x, 4) for x in p0],
            "end": [round(x, 4) for x in p1],
            "seat_point": [round(x, 4) for x in vadd(p_post, (0,0,v_shift))],
            "seat_depth_ft": round(seat_depth, 4)
        })
    joints["primary_rafters"] = rafters

    # ── Secondary Rafters (Jacks) ───────────────────────────────────────────
    jack_spec = structure["roof"].get("secondary_rafters", {})
    jack_endpoints = []
    if jack_spec.get("enabled"):
        jack_count = jack_spec.get("count_per_side", 2)
        for i in range(qty):
            p1_xy = post_xy[i]; p2_xy = post_xy[(i+1)%qty]
            dx, dy = p2_xy[0]-p1_xy[0], p2_xy[1]-p1_xy[1]
            blen = math.sqrt(dx*dx + dy*dy)
            ux, uy = dx/blen, dy/blen
            spacing = blen / (jack_count + 1)
            
            for j_idx in range(jack_count):
                dist = (j_idx + 1) * spacing
                p_seat_xy = (p1_xy[0] + ux*dist, p1_xy[1] + uy*dist)
                
                # Jack Direction: Inward Normal of Beam
                in_x, in_y = -uy, ux
                
                # 1. Planar Constraint: z = f(x,y) on roof_planes[i]
                # P = P_seat + t * (in_x, in_y, tan(pitch))
                # Solve for t to hit Apex Convergence or Hip Plane.
                # Actually, all jacks in sector i MUST lie on roof_planes[i].
                plane = roof_planes[i]
                
                # Seat point on beam top
                p_seat = (p_seat_xy[0], p_seat_xy[1], Z_BEAM_TOP)
                # Vertical shift for birdsmouth (Phase 2)
                # Pitch of common rafter is different from hip!
                apothem = r_ft * math.cos(math.pi/qty)
                common_slope = roof_r / (apothem - hub_radius * math.cos(math.pi/qty))
                c_v_shift = (rafter_d_ft - seat_depth) / math.cos(math.atan(common_slope))
                
                p_start = (p_seat[0] - in_x*overhang_ft, p_seat[1] - in_y*overhang_ft, p_seat[2] - common_slope*overhang_ft + c_v_shift)
                dir_jack = (in_x, in_y, common_slope)
                
                # 2. Convergence Constraint: Intersect with Hip Rafter Side Plane
                # Near post i -> Hip i. Near post i+1 -> Hip i+1.
                fraction = (j_idx + 1.0) / (jack_count + 1.0)
                hip_idx = i if fraction < 0.5 else (i+1)%qty
                suffix = 'a' if fraction < 0.5 else 'b'
                
                # Hip Plane for Jack: Vertical plane through hip axis, shifted by rafter half-width
                h_p1 = (post_xy[hip_idx][0], post_xy[hip_idx][1], Z_BEAM_TOP)
                h_dir = vnorm(vsub(APEX, h_p1))
                h_perp_xy = (-h_dir[1], h_dir[0], 0.0) # Normal to hip in XY
                
                # Decide side based on sector
                # Vector from hip to jack start
                v_to_jack = vsub(p_start, h_p1)
                side_sign = 1.0 if vdot(v_to_jack, h_perp_xy) >= 0 else -1.0
                n_hip_side = vmul(h_perp_xy, side_sign)
                p_hip_side = vadd(h_p1, vmul(n_hip_side, rafter_w_in/24.0))
                
                p_end, _ = intersect_line_plane(p_start, dir_jack, p_hip_side, n_hip_side)
                
                jack_endpoints.append({
                    "id": f"J{i+1}{suffix}",
                    "start": [round(x, 4) for x in p_start],
                    "end": [round(x, 4) for x in p_end],
                    "mate_id": f"R{hip_idx+1}"
                })
    joints["jack_rafters"] = {"enabled": jack_spec.get("enabled", False), "endpoints": jack_endpoints}

    # ── Braces (Normalized) ──────────────────────────────────────────────────
    bracing_spec = structure.get("bracing", {})
    brace_pairs = []
    if bracing_spec.get("enabled"):
        b_len = bracing_spec["brace"]["length_ft"]
        b_ang = math.radians(bracing_spec["brace"]["angle_deg"])
        b_run = b_len * math.cos(b_ang)
        b_drop = b_len * math.sin(b_ang)
        post_hw = (structure["members"]["posts"]["actual_width_in"] / 24.0)
        
        for i in range(qty):
            vi = (post_xy[i][0], post_xy[i][1]); vj = (post_xy[(i+1)%qty][0], post_xy[(i+1)%qty][1])
            dx, dy = vnorm((vj[0]-vi[0], vj[1]-vi[1], 0.0))[:2]
            # Brace A (toward next)
            p0a = (vi[0]+dx*post_hw, vi[1]+dy*post_hw, Z_POST_TOP - b_drop)
            p1a = (vi[0]+dx*(post_hw+b_run), vi[1]+dy*(post_hw+b_run), Z_POST_TOP)
            brace_pairs.append({"id": f"K{i+1}A", "start": p0a, "end": p1a})
            # Brace B (toward prev)
            vk = (post_xy[(i-1)%qty][0], post_xy[(i-1)%qty][1])
            dkx, dky = vnorm((vk[0]-vi[0], vk[1]-vi[1], 0.0))[:2]
            p0b = (vi[0]+dkx*post_hw, vi[1]+dky*post_hw, Z_POST_TOP - b_drop)
            p1b = (vi[0]+dkx*(post_hw+b_run), vi[1]+dky*(post_hw+b_run), Z_POST_TOP)
            brace_pairs.append({"id": f"K{i+1}B", "start": p0b, "end": p1b})
            
    joints["braces"] = {"enabled": bracing_spec.get("enabled", False), "endpoints": brace_pairs}
    
    return joints
    return joints
def compute_from_structure(structure_path: str) -> dict:
    """
    Read structure.json, compute all geometry, seal geometry section, write back.
    This is the new M1+ entry point. The old compute() is kept for compat.
    """
    import os as _os
    import sys as _sys
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from structure_io import load_structure, save_structure, assert_not_sealed

    structure = load_structure(structure_path)

    # Coordinate system contract
    cad_meta = structure.get("cad", {})
    assert cad_meta.get("units", "feet") == "feet", "cad.units must be 'feet'"
    assert cad_meta.get("coordinate_system", "right_handed_z_up") == "right_handed_z_up", \
        "cad.coordinate_system must be 'right_handed_z_up'"

    assert_not_sealed(structure, "geometry")

    layout   = structure["layout"]
    members  = structure["members"]
    roof     = structure["roof"]
    hub_spec = structure["hub"]
    inv      = structure.get("invariants", {})
    if "precision" not in cad_meta:
        raise ValueError(
            "cad.precision is required — add it to structure.json before running geometry_engine"
        )
    precision = cad_meta["precision"]

    sides      = layout["post_count"]
    span_ft    = layout["inscribed_radius_ft"]
    pitch      = roof["pitch"]
    pr, rr     = [int(x) for x in pitch.split(":")]
    overhang_ft = roof["primary_rafters"]["overhang_ft"]
    beam_depth_in = members["beams"]["actual_depth_in"]
    post_cut_ft   = members["posts"]["cut_length_ft"]
    rafter_w_in   = roof["primary_rafters"]["actual_width_in"]
    rafter_d_in   = roof["primary_rafters"]["actual_depth_in"]

    # Compute geometry (unchanged math functions)
    cuts   = compound_cut(pr, rr, sides)
    rl     = rafter_length(span_ft, pr, rr, overhang_ft)
    rise   = roof_rise(span_ft, pr, rr)
    height = total_height(post_cut_ft, beam_depth_in, span_ft, pr, rr)

    # Hub radius: geometry_engine owns the formula.
    # Contract: hub_r >= radius_min_ft AND satisfies no_rafter_inside_hub_radius.
    if "radius_min_ft" not in hub_spec:
        raise ValueError(
            "hub.radius_min_ft is required — add it to structure.json before running geometry_engine"
        )
    radius_min = hub_spec["radius_min_ft"]
    hub_r = max(radius_min, (rafter_w_in + rafter_d_in) / 12.0)

    warnings: list = []

    # Invariant: rafter_count_equals_post_count
    if inv.get("rafter_count_equals_post_count"):
        rafter_count = roof["primary_rafters"]["count"]
        if rafter_count != sides:
            warnings.append(
                f"INVARIANT FAIL: rafter_count={rafter_count} != post_count={sides}"
            )

    # Invariant: no_zero_length_members
    if inv.get("no_zero_length_members") and rl["structural_length_ft"] < precision:
        warnings.append(
            f"INVARIANT FAIL: rafter structural_length_ft={rl['structural_length_ft']}"
            f" < precision={precision}"
        )

    # Height limit check from code section
    height_limit = structure.get("code", {}).get("height_limit_ft")
    if height_limit and height["total_height_ft"] > height_limit:
        warnings.append(
            f"FAIL: total_height_ft={height['total_height_ft']:.3f} "
            f"exceeds code limit of {height_limit} ft."
        )

    layout_result = svg_layout(height["total_height_ft"], span_ft, sides)
    scale   = layout_result["scale_px_per_ft"]
    grade_y = layout_result["grade_y"]
    post_px = post_cut_ft * scale
    beam_px = (beam_depth_in / 12.0) * scale
    rise_px = span_ft * (pr / rr) * scale

    svg_coords = {
        **layout_result,
        "post_top_y":    round(grade_y - post_px),
        "beam_soffit_y": round(grade_y - post_px),
        "beam_top_y":    round(grade_y - post_px - beam_px),
        "hub_apex_y":    round(grade_y - post_px - beam_px - rise_px),
        "rise_px":       round(rise_px),
        "beam_px":       round(beam_px),
        "post_px":       round(post_px),
    }

    # --- Fabrication-Grade Joint Computation ---
    joints = compute_joints(structure, cuts, rl, rise, height, hub_r, svg_coords)
    
    structure["geometry"] = {
        "_comment": "DERIVED — written by geometry_engine.py. Do not manually edit.",
        "_sealed":     True,
        "compound_cut": cuts,
        "beam_ring":    beam_ring_miter(sides),
        "rafter":       rl,
        "roof_rise":    rise,
        "total_height": height,
        "hub_radius_ft": round(hub_r, 4),
        "svg_coordinates": svg_coords,
        "warnings":     warnings,
        "joints": joints,
    }
    structure["meta"]["lifecycle"] = "GEOMETRY_SEALED"

    save_structure(structure, structure_path)

    if warnings:
        for w in warnings:
            print(f"WARNING: {w}", file=sys.stderr)
        sys.exit(1)

    return structure


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python3 geometry_engine.py <structure.json | structural-model.json>",
            file=sys.stderr,
        )
        sys.exit(1)

    path = sys.argv[1]

    # Detect new vs legacy invocation by checking file content
    import json as _json
    with open(path) as _f:
        _data = _json.load(_f)

    if "meta" in _data and "schema_version" in _data.get("meta", {}):
        # New: structure.json
        compute_from_structure(path)
        return

    # Legacy: structural-model.json → write geometry-calculations.json
    result = compute(path)
    out_path = os.path.join(os.path.dirname(path), "geometry-calculations.json")
    with open(out_path, "w") as f:
        import json as _json2
        _json2.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    if result.get("warnings"):
        print("\nWARNINGS:", file=sys.stderr)
        for w in result["warnings"]:
            print(f"  {w}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
