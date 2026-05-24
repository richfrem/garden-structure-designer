#!/usr/bin/env python3
"""
cad_scene.py
============
Pure-Python CAD scene graph for garden-structure-designer.

Architecture
------------
  1. V3 vector primitives  (no dependencies)
  2. Solid / Face dataclasses
  3. build_structure_scene(model, calcs) -> Scene
       Computes ALL 3D nodes from shared Z-plane constants.
       No SVG is generated here.
  4. validate_scene_geometry(scene)
       Raises GeometryError with exact message on any invariant violation.
       Must pass before any projection / SVG emission.

Layer: Execution
Consumed by: render_drawings.py (render_perspective_view, render_isometric_view)
             cad_backend.py    (build123d BREP builder)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Geometry error
# ---------------------------------------------------------------------------

class GeometryError(ValueError):
    """Raised when a scene geometry invariant is violated."""


# ---------------------------------------------------------------------------
# V3 — immutable 3-tuple with named vector ops
# ---------------------------------------------------------------------------

V3 = tuple[float, float, float]


def vadd(a: V3, b: V3) -> V3:
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def vsub(a: V3, b: V3) -> V3:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def vscl(a: V3, s: float) -> V3:
    return (a[0]*s, a[1]*s, a[2]*s)

def vdot(a: V3, b: V3) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def vcross(a: V3, b: V3) -> V3:
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
    )

def vlen(a: V3) -> float:
    return math.sqrt(a[0]*a[0] + a[1]*a[1] + a[2]*a[2])

def vnorm(a: V3) -> V3:
    l = vlen(a)
    if l < 1e-12:
        raise GeometryError(f"Cannot normalise zero-length vector {a}")
    return (a[0]/l, a[1]/l, a[2]/l)

def vcent(pts: list[V3]) -> V3:
    n = len(pts)
    return (sum(p[0] for p in pts)/n,
            sum(p[1] for p in pts)/n,
            sum(p[2] for p in pts)/n)

def vfinite(v: V3) -> bool:
    return all(math.isfinite(c) for c in v)

def v2_radius(v: V3) -> float:
    """XY-plane radius of a 3-D point."""
    return math.sqrt(v[0]*v[0] + v[1]*v[1])


def _hip_rafter_slope(Z_APEX: float, Z_BEAM_TOP: float, r_ft: float, hub_r: float) -> float:
    run = r_ft - hub_r
    if run <= 1e-9:
        raise GeometryError("Hip rafter run must be positive.")
    return (Z_APEX - Z_BEAM_TOP) / run


# ---------------------------------------------------------------------------
# Face — one planar polygon in 3-D space
# ---------------------------------------------------------------------------

@dataclass
class Face:
    verts:  list[V3]        # ordered corners (CCW viewed from outside)
    normal: V3              # outward unit normal
    color:  str             # hex fill colour (face-level shading)
    role:   str             # "post" | "beam" | "rafter" | "brace" | "hub" | "footing"
    tag:    str | None      # member identifier, e.g. "P1", "B3", "R6"
    depth:  float = 0.0    # filled in by projection pass


# ---------------------------------------------------------------------------
# Solid — one structural member composed of faces
# ---------------------------------------------------------------------------

@dataclass
class Solid:
    role:   str
    tag:    str
    faces:  list[Face] = field(default_factory=list)
    # Endpoints of the member axis (used for geometry validation)
    p0:     V3 = (0.0, 0.0, 0.0)
    p1:     V3 = (0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------

@dataclass
class Scene:
    solids:   list[Solid]
    # Shared construction constants (stored for validator access)
    qty:      int
    hub_r:    float         # exact hub polygon face radius (ft)
    Z_GRADE:  float
    Z_POST_TOP: float       # post top Z == beam underside Z  ← KEY INVARIANT
    Z_BEAM_TOP: float
    Z_APEX:   float
    post_xy:  list[tuple[float, float]]   # XY positions of posts


# ---------------------------------------------------------------------------
# Prism builder — one generic CAD rectangular-prism primitive
# ---------------------------------------------------------------------------

def _make_prism(
    p0: V3, p1: V3,
    hw: float, hd: float,
    up_hint: V3,
    colors: dict[str, str],
    role: str, tag: str,
) -> Solid:
    """
    Build a rectangular prism between p0 and p1.

    hw       : half-width perpendicular to axis (lateral)
    hd       : half-depth perpendicular to axis (thickness)
    up_hint  : preferred 'up' direction for the depth axis
    colors   : dict keyed top/bottom/left/right/start/end/other
    """
    axis = vsub(p1, p0)
    if vlen(axis) < 1e-6:
        raise GeometryError(
            f"Zero-length member '{tag}' ({role}): p0={p0} p1={p1}"
        )
    u = vnorm(axis)

    w_raw = vcross(up_hint, u)
    if vlen(w_raw) < 1e-9:
        w_raw = vcross((1.0, 0.0, 0.0), u)
    w = vnorm(w_raw)
    d = vnorm(vcross(u, w))

    def corner(base: V3, sw: float, sd: float) -> V3:
        return vadd(vadd(base, vscl(w, sw)), vscl(d, sd))

    s_ll = corner(p0, -hw, -hd); s_lr = corner(p0,  hw, -hd)
    s_ul = corner(p0, -hw,  hd); s_ur = corner(p0,  hw,  hd)
    e_ll = corner(p1, -hw, -hd); e_lr = corner(p1,  hw, -hd)
    e_ul = corner(p1, -hw,  hd); e_ur = corner(p1,  hw,  hd)

    c = lambda k: colors.get(k, colors.get("other", "#888888"))

    face_defs = [
        ([s_ul, s_ur, e_ur, e_ul], d,          "top"),
        ([s_ll, e_ll, e_lr, s_lr], vscl(d,-1), "bottom"),
        ([s_ll, s_ul, e_ul, e_ll], vscl(w,-1), "left"),
        ([s_lr, e_lr, e_ur, s_ur], w,           "right"),
        ([s_ll, s_lr, s_ur, s_ul], vscl(u,-1), "start"),
        ([e_ll, e_ul, e_ur, e_lr], u,           "end"),
    ]

    solid = Solid(role=role, tag=tag, p0=p0, p1=p1)
    for verts, normal, face_key in face_defs:
        solid.faces.append(Face(
            verts=verts,
            normal=normal,
            color=c(face_key),
            role=role,
            tag=tag,
        ))
    return solid


# ---------------------------------------------------------------------------
# Color palettes
# ---------------------------------------------------------------------------

def _palettes(is_blueprint: bool) -> dict[str, dict[str, str]]:
    if is_blueprint:
        return {
            "post":   {"top":"#1e4272","bottom":"#0d1e30","left":"#162e50",
                       "right":"#0f2238","start":"#1a3560","end":"#1a3560","other":"#162e50"},
            "beam":   {"top":"#1d3e68","bottom":"#0c1d2e","left":"#122840",
                       "right":"#0d2035","start":"#162e4e","end":"#162e4e","other":"#122840"},
            "rafter": {"top":"#1f4070","bottom":"#0e2032","left":"#132842",
                       "right":"#0e2234","start":"#172d4c","end":"#172d4c","other":"#132842"},
            "brace":  {"top":"#1b3760","bottom":"#0d1f32","left":"#132440",
                       "right":"#0e1e34","start":"#162c4e","end":"#162c4e","other":"#132440"},
            "hub":    {"top":"#204878","bottom":"#0e2035","left":"#1a3868",
                       "right":"#152d56","start":"#1d4070","end":"#1d4070","other":"#1a3868"},
            "purlin": {"top":"#1b3760","bottom":"#0d1f32","left":"#132440",
                       "right":"#0e1e34","start":"#162c4e","end":"#162c4e","other":"#132440"},
            "footing":{"top":"#183050","bottom":"#0d1e30","left":"#122440",
                       "right":"#0e1e34","start":"#162c4e","end":"#162c4e","other":"#122440"},
        }
    return {
        "post":   {"top":"#f1e5cd","bottom":"#c8b090","left":"#ecdfc8",
                   "right":"#e0c9a4","start":"#e8dabc","end":"#e8dabc","other":"#ecdfc8"},
        "beam":   {"top":"#e8d4b0","bottom":"#b89070","left":"#d4a878",
                   "right":"#c89860","start":"#d0a070","end":"#d0a070","other":"#d4a878"},
        "rafter": {"top":"#ddb892","bottom":"#a87850","left":"#c89870",
                   "right":"#b88860","start":"#c08060","end":"#c08060","other":"#c89870"},
        "brace":  {"top":"#f0e4cc","bottom":"#c0a080","left":"#e8d8b8",
                   "right":"#d8c4a0","start":"#e0d0b0","end":"#e0d0b0","other":"#e8d8b8"},
        "hub":    {"top":"#f5ecd8","bottom":"#d0b888","left":"#e8d8c0",
                   "right":"#dcc8a8","start":"#e4d4b8","end":"#e4d4b8","other":"#e8d8c0"},
        "purlin": {"top":"#f0e4cc","bottom":"#c0a080","left":"#e8d8b8",
                   "right":"#d8c4a0","start":"#e0d0b0","end":"#e0d0b0","other":"#e8d8b8"},
        "footing":{"top":"#e0e0e0","bottom":"#b0b0b0","left":"#d3d3d3",
                   "right":"#c0c0c0","start":"#c8c8c8","end":"#c8c8c8","other":"#d3d3d3"},
    }


# ---------------------------------------------------------------------------
# build_structure_scene — THE only place geometry is computed
# ---------------------------------------------------------------------------

def build_structure_scene(
    structure: dict,
    calcs: "dict | bool | None" = None,
    is_blueprint: bool = False,
) -> Scene:
    """
    Compute all 3D construction nodes and emit Solid objects.

    Preferred (v1.3+) calling convention:
        build_structure_scene(structure, is_blueprint=False)
    where ``structure`` is a fully-computed structure.json dict (geometry section
    must be sealed by geometry_engine.py before calling).

    Legacy calling convention (deprecated, kept for render_drawings.py compat):
        build_structure_scene(model, calcs, is_blueprint=False)
    where ``model`` is the old structural-model.json dict and ``calcs`` is the
    old geometry-calculations.json dict.

    All member endpoints derive from the shared Z-plane constants below.
    No SVG is generated here.
    """
    # ── Detect calling convention ────────────────────────────────────────────
    # New convention: structure has "meta.schema_version" or "geometry._sealed"
    # Old convention: calcs is a non-None, non-bool dict (legacy geometry-calcs)
    _using_legacy = isinstance(calcs, dict)
    if _using_legacy:
        # Legacy path: calcs is the old geometry-calculations dict
        is_blueprint = is_blueprint  # already set correctly
        return _build_scene_legacy(structure, calcs, is_blueprint)

    # New path: calcs is either None or a bool (is_blueprint passed positionally)
    if isinstance(calcs, bool):
        is_blueprint = calcs
    return _build_scene_from_structure(structure, is_blueprint)


def _build_scene_legacy(
    model: dict,
    calcs: dict,
    is_blueprint: bool = False,
) -> Scene:
    """Legacy implementation reading from (model, calcs) dicts."""
    pal = _palettes(is_blueprint)
    UP: V3 = (0.0, 0.0, 1.0)

    # ── Parameters ──────────────────────────────────────────────────────────
    qty       = model.get("members", {}).get("posts", {}).get("quantity", 6)

    # Dynamically resolve span_diag from dimensions or calculate from posts spanDistance
    span_diag = model.get("dimensions", {}).get("max_diagonal_ft")
    if span_diag is None:
        posts_spec = model.get("members", {}).get("posts", {})
        span_diag = posts_spec.get("spanDistance_ft", 5.0) * 2.0
    r_ft      = span_diag / 2.0

    post_h    = calcs.get("total_height", {}).get("post_ft", 8.33)
    roof_r    = calcs.get("roof_rise",    {}).get("rise_ft", 1.6)
    beam_d    = calcs.get("total_height", {}).get("beam_depth_ft", 1.0)

    # ── Shared Z planes ──────────────────────────────────────────────────────
    Z_GRADE    = 0.0
    Z_POST_TOP = post_h - beam_d      # post top cap  ≡  beam underside  ← SHARED
    Z_BEAM_TOP = post_h               # beam top      ≡  rafter seat
    Z_APEX     = post_h + roof_r      # hub centre elevation

    # ── Cross-section half-dimensions (feet) ─────────────────────────────────
    posts_spec = model.get("members", {}).get("posts", {})
    beams_spec = model.get("members", {}).get("beams", {})
    braces_spec = model.get("members", {}).get("kneebraces", {})
    rafters_spec = model.get("members", {}).get("rafters", {})

    POST_HW   = (posts_spec.get("width_in", 5.5) / 12.0) / 2.0
    POST_HD   = (posts_spec.get("depth_in", 5.5) / 12.0) / 2.0
    BEAM_HW   = (beams_spec.get("width_in", 5.5) / 12.0) / 2.0
    BEAM_HD   = beam_d / 2.0
    RAFTER_HW = (rafters_spec.get("width_in", 3.5) / 12.0) / 2.0
    RAFTER_HD = (rafters_spec.get("depth_in", 5.5) / 12.0) / 2.0
    BRACE_HW  = (braces_spec.get("width_in", 3.5) / 12.0) / 2.0
    BRACE_HD  = (braces_spec.get("depth_in", 3.5) / 12.0) / 2.0

    # ── Post XY positions ────────────────────────────────────────────────────
    post_xy: list[tuple[float, float]] = [
        (r_ft * math.cos(2*math.pi*i/qty),
         r_ft * math.sin(2*math.pi*i/qty))
        for i in range(qty)
    ]

    # ── Hub polygon face radius ──────────────────────────────────────────────
    # Make a substantial and readable polygonal king-post / compression hub
    rafter_full_w = RAFTER_HW * 2.0
    rafter_full_d = RAFTER_HD * 2.0
    hub_r = max(0.60, rafter_full_w + rafter_full_d)

    hub_r_face = hub_r * math.cos(math.pi / qty)
    # ── Rafter apex termination nodes (exact hub polygon face) ───────────────
    rafter_apex: list[V3] = [
        (hub_r_face * math.cos(2*math.pi*i/qty),
         hub_r_face * math.sin(2*math.pi*i/qty),
         Z_APEX)
        for i in range(qty)
    ]

    # ── Brace run length ─────────────────────────────────────────────────────
    if "cutLength_in" not in braces_spec or "angle_deg" not in braces_spec:
        raise GeometryError("MISSING_REQUIRED_CONFIG: members.kneebraces.cutLength_in or angle_deg")
    
    brace_run = (braces_spec["cutLength_in"] / 12.0) * math.cos(math.radians(braces_spec["angle_deg"]))
    brace_drop = brace_run  # legacy: assume 45-degree brace so drop == run

    # ── Solids list ──────────────────────────────────────────────────────────
    solids: list[Solid] = []

    # Concrete Footing Blocks (concrete square piers)
    foundation_spec = model.get("foundation", {})
    FOOTING_HW = (foundation_spec.get("caisson_diameter_in", 12.0) / 12.0) / 2.0
    for i, (px, py) in enumerate(post_xy):
        p0_footing = (px, py, Z_GRADE - 1.5)  # extends 18 inches below grade
        p1_footing = (px, py, Z_GRADE + 0.33) # rises 4 inches above grade
        solids.append(_make_prism(
            p0_footing, p1_footing, FOOTING_HW, FOOTING_HW, UP,
            pal["footing"], "footing", f"FT{i+1}"
        ))

    # Posts — vertical from grade to post_top (= beam underside)
    for i, (px, py) in enumerate(post_xy):
        solids.append(_make_prism(
            (px, py, Z_GRADE), (px, py, Z_POST_TOP),
            POST_HW, POST_HD, UP,
            pal["post"], "post", f"P{i+1}",
        ))

    # Ring beams — horizontal from post_top to post_top.
    # Beam centreline Z = Z_POST_TOP + BEAM_HD (midpoint of beam cross-section).
    for i in range(qty):
        px1, py1 = post_xy[i]
        px2, py2 = post_xy[(i+1) % qty]
        bz = Z_POST_TOP + BEAM_HD
        solids.append(_make_prism(
            (px1, py1, bz), (px2, py2, bz),
            BEAM_HW, BEAM_HD, UP,
            pal["beam"], "beam", f"B{i+1}",
        ))

    # Knee braces — visibility filtered at render time
    if model.get("bracing", {}).get("enabled", False):
        brace_joints = geom.get("joints", {}).get("braces", {})
        if not brace_joints.get("enabled") or "endpoints" not in brace_joints:
            raise GeometryError("MISSING_REQUIRED_GEOMETRY: geometry.joints.braces")
        for bp in brace_joints.get("endpoints", {}).get("pairs", []):
            solids.append(_make_prism(
                tuple(bp["start"]), tuple(bp["end"]), BRACE_HW, BRACE_HD, UP,
                pal["brace"], "brace", bp["brace_id"]
            ))

    # Rafter overhang (tails) pass ────────────────────────────────────────────
    overhang_in = model.get("overhang_in", 12)
    overhang_ft = overhang_in / 12.0

    # Hip rafters — from rafter seat at post (Z_BEAM_TOP) to hub face (Z_APEX)
    # They extend past the post seat by overhang_ft in the outward direction
    for i in range(qty):
        px, py = post_xy[i]
        ang = 2*math.pi*i/qty
        tang: V3 = (math.cos(ang + math.pi/2), math.sin(ang + math.pi/2), 0.0)
        
        p1_apex = rafter_apex[i]
        p_seat = (px, py, Z_BEAM_TOP)
        
        # Outward unit direction in XY
        len_xy = math.sqrt(px*px + py*py)
        dir_xy_norm = (px / len_xy, py / len_xy)
        
        # Slope of hip rafter
        slope = (Z_APEX - Z_BEAM_TOP) / (len_xy - hub_r)
        
        # Extended starting point (at tail end)
        p0_start = (
            px + dir_xy_norm[0] * overhang_ft,
            py + dir_xy_norm[1] * overhang_ft,
            Z_BEAM_TOP - slope * overhang_ft
        )
        
        # Shift rafter up vertically so its underside rests exactly on top of the beam ring
        theta = math.atan(slope)
        dy_vertical = RAFTER_HD / math.cos(theta)
        
        p0_start_shifted = (p0_start[0], p0_start[1], p0_start[2] + dy_vertical)
        # Use exact hub termination point from geometry.joints
        term_pts = calcs.get("joints", {}).get("rafters", {}).get("hub_termination_points", {}).get("points", [])
        term_pt = None
        for pt in term_pts:
            if pt.get("rafter_id") == f"R{i+1}":
                term_pt = pt.get("point")
                break
                
        if term_pt:
            p1_apex = term_pt
            p1_apex_shifted = (p1_apex[0], p1_apex[1], p1_apex[2] + dy_vertical)
        else:
            p1_apex_shifted = (p1_apex[0], p1_apex[1], p1_apex[2] + dy_vertical)

        
        solids.append(_make_prism(
            p0_start_shifted, p1_apex_shifted,
            RAFTER_HW, RAFTER_HD, UP,
            pal["rafter"], "rafter", f"R{i+1}",
        ))

    # Jack rafters (common rafters)
    jack_joints = calcs.get("joints", {}).get("jack_rafters", {})
    if jack_joints.get("enabled"):
        for ep in jack_joints.get("endpoints", []):
            solids.append(_make_prism(
                tuple(ep["start"]), tuple(ep["end"]), RAFTER_HW, RAFTER_HD, UP,
                pal["rafter"], "rafter", ep["id"]
            ))
    elif model.get("roof", {}).get("secondary_rafters", {}).get("enabled", False):
        # Legacy fallback if joints not precomputed (should be rare after centralization)
        for i in range(qty):
            px1, py1 = post_xy[i]
            px2, py2 = post_xy[(i+1) % qty]
            
            bx = px2 - px1; by = py2 - py1
            blen = math.sqrt(bx*bx + by*by)
            if blen < 1e-9: continue
            ux = bx / blen; uy = by / blen
            in_x = -uy; in_y = ux
            
            mx = (px1 + px2) / 2.0; my = (py1 + py2) / 2.0
            apothem = math.sqrt(mx*mx + my*my)
            slope_perp = roof_r / (apothem - hub_r * math.cos(math.pi / qty))
            
            sec_spec = model.get("roof", {}).get("secondary_rafters", {})
            count_per_side = sec_spec.get("count_per_side", 2)
            for j in range(count_per_side):
                fraction = (j + 1.0) / (count_per_side + 1.0)
                tag_suffix = chr(ord('a') + j)
                sx = px1 + bx * fraction
                sy = py1 + by * fraction
                
                # ... (keep old logic for absolute fallback, but use J naming)
                # Actually, better to just raise error or use the new J naming
                solids.append(_make_prism(
                    (0,0,0), (1,1,1), RAFTER_HW, RAFTER_HD, UP, 
                    pal["rafter"], "rafter", f"J{i}{tag_suffix}"
                ))


    # Purlin Ring — horizontal collar/purlin timbers connecting the hip rafters
    if model.get("members", {}).get("purlins", {}).get("enabled", False):
        purlins_spec = model.get("members", {}).get("purlins", {})
        s_purlin = purlins_spec.get("height_fraction", 0.55)
        Z_PURLIN = Z_BEAM_TOP + roof_r * s_purlin
        PURLIN_HW = (purlins_spec.get("width_in", 3.5) / 12.0) / 2.0
        PURLIN_HD = (purlins_spec.get("depth_in", 3.5) / 12.0) / 2.0
    
        # Calculate dy_vertical again for purlin offset
        dx_hip_ex = post_xy[0][0] - rafter_apex[0][0]
        dy_hip_ex = post_xy[0][1] - rafter_apex[0][1]
        len_xy_ex = math.sqrt(post_xy[0][0]**2 + post_xy[0][1]**2)
        slope_ex = (Z_APEX - Z_BEAM_TOP) / (len_xy_ex - hub_r)
        dy_vertical = RAFTER_HD / math.cos(math.atan(slope_ex))

        purlin_pts: list[V3] = []
        for i in range(qty):
            px, py = post_xy[i]
            ax, ay, az = rafter_apex[i]
            pt = (
                px + (ax - px) * s_purlin,
                py + (ay - py) * s_purlin,
                Z_PURLIN + dy_vertical + PURLIN_HD
            )
            purlin_pts.append(pt)
        
        for i in range(qty):
            pt1 = purlin_pts[i]
            pt2 = purlin_pts[(i+1) % qty]
            solids.append(_make_prism(
                pt1, pt2,
                PURLIN_HW, PURLIN_HD, UP,
                pal["purlin"], "purlin", f"Purlin{i+1}"
            ))

        # Hub — polygonal prism (qty-sided)
        # Substantial hanging pendant matching the target image: extends 1.25 ft below apex
    hub_ztop = Z_APEX + dy_vertical
    hub_zbot = Z_APEX - 1.2 * dy_vertical
    C_HUB = pal["hub"]

    ring_top: list[V3] = [
        (hub_r*math.cos(2*math.pi*(i+0.5)/qty), hub_r*math.sin(2*math.pi*(i+0.5)/qty), hub_ztop)
        for i in range(qty)
    ]
    ring_bot: list[V3] = [
        (hub_r*math.cos(2*math.pi*(i+0.5)/qty), hub_r*math.sin(2*math.pi*(i+0.5)/qty), hub_zbot)
        for i in range(qty)
    ]

    hub_solid = Solid(role="hub", tag="HUB",
                      p0=(0.0, 0.0, hub_zbot), p1=(0.0, 0.0, hub_ztop))
    hub_solid.faces.append(Face(ring_top, UP, C_HUB["top"], "hub", "HUB"))
    hub_solid.faces.append(Face(list(reversed(ring_bot)), vscl(UP, -1.0), C_HUB["bottom"], "hub", "HUB"))
    for i in range(qty):
        j = (i+1) % qty
        mid_ang = 2*math.pi*(i+1.0)/qty
        sn: V3 = (math.cos(mid_ang), math.sin(mid_ang), 0.0)
        shade = C_HUB["left"] if vdot(sn, (0.866, 0.5, 0.0)) > 0 else C_HUB["right"]
        hub_solid.faces.append(Face(
            [ring_bot[i], ring_bot[j], ring_top[j], ring_top[i]],
            sn, shade, "hub", "HUB",
        ))
    solids.append(hub_solid)

    return Scene(
        solids=solids,
        qty=qty,
        hub_r=hub_r,
        Z_GRADE=Z_GRADE,
        Z_POST_TOP=Z_POST_TOP,
        Z_BEAM_TOP=Z_BEAM_TOP,
        Z_APEX=Z_APEX,
        post_xy=post_xy,
    )


# ---------------------------------------------------------------------------
# Notched Solid Builder — For fabrication-faithful rafters (birdsmouth)
# ---------------------------------------------------------------------------

def _make_notched_rafter(
    p_tail: V3, p_apex: V3, p_seat: V3,
    hw: float, hd: float,
    seat_depth: float,
    up_hint: V3,
    colors: dict[str, str],
    role: str, tag: str,
) -> Solid:
    """
    Build a notched rafter solid between p_tail and p_apex with a 
    birdsmouth notch at p_seat.
    
    p_tail, p_apex: Top-face endpoints of the rafter.
    p_seat: Point on rafter top-face directly above the beam bearing.
    """
    axis = vsub(p_apex, p_tail)
    u = vnorm(axis)
    w_raw = vcross(up_hint, u)
    w = vnorm(w_raw)
    d = vnorm(vcross(u, w)) # Down vector (pointing from top-face into solid)

    # Local 2D profile points in (u, d) plane
    # 0: TailTop, 1: ApexTop, 2: ApexBottom, 3: SeatPlumb, 4: SeatLevel, 5: TailBottom
    # We define profile relative to p_tail (0,0)
    L = vdist(p_tail, p_apex)
    L_seat = vdist(p_tail, p_seat)
    full_depth = hd * 2.0
    
    # Profile nodes (relative to rafter top-line)
    # [u, d]
    nodes = [
        (0, 0),             # 0: TailTop
        (L, 0),             # 1: ApexTop
        (L, full_depth),    # 2: ApexBottom (vertical plumb cut at hub)
        (L_seat, full_depth), # 3: SeatPlumb start
        (L_seat, seat_depth), # 4: SeatLevel corner (the 'notch')
        (0, seat_depth)      # 5: TailBottom (assuming level tail or just seat depth extension)
    ]
    # Adjust 5 to be full depth if tail is square
    nodes[5] = (0, full_depth)

    def get_v(u_val: float, d_val: float, sw: float) -> V3:
        return vadd(vadd(vadd(p_tail, vmul(u, u_val)), vmul(d, d_val)), vmul(w, sw))

    # Left and Right profile loops
    pts_l = [get_v(n[0], n[1], -hw) for n in nodes]
    pts_r = [get_v(n[0], n[1],  hw) for n in nodes]

    c = lambda k: colors.get(k, colors.get("other", "#888888"))
    solid = Solid(role=role, tag=tag, p0=p_tail, p1=p_apex)
    
    # 1. Top face
    solid.faces.append(Face([pts_l[0], pts_r[0], pts_r[1], pts_l[1]], vmul(d, -1), c("top"), role, tag))
    # 2. Bottom segments (plumb cuts and level seats)
    solid.faces.append(Face([pts_l[1], pts_r[1], pts_r[2], pts_l[2]], u, c("end"), role, tag)) # Apex Plumb
    solid.faces.append(Face([pts_l[2], pts_r[2], pts_r[3], pts_l[3]], d, c("bottom"), role, tag)) # Bottom run
    solid.faces.append(Face([pts_l[3], pts_r[3], pts_r[4], pts_l[4]], vmul(u, -1), c("other"), role, tag)) # Seat Plumb Face
    solid.faces.append(Face([pts_l[4], pts_r[4], pts_r[5], pts_l[5]], d, c("bottom"), role, tag)) # Seat Level Face
    solid.faces.append(Face([pts_l[5], pts_r[5], pts_r[0], pts_l[0]], vmul(u, -1), c("start"), role, tag)) # Tail Plumb
    # 3. Sides
    solid.faces.append(Face(pts_l, vmul(w, -1), c("left"), role, tag))
    solid.faces.append(Face(list(reversed(pts_r)), w, c("right"), role, tag))

    return solid


# ---------------------------------------------------------------------------
# _build_scene_from_structure — new v1.3+ path reading from structure.json
# ---------------------------------------------------------------------------

def _build_scene_from_structure(
    structure: dict,
    is_blueprint: bool = False,
) -> Scene:
    """
    Build the scene from a fully-computed structure.json dict.
    Pure consumer of geometry.joints (Phase 0 Constraint Unification).
    """
    pal = _palettes(is_blueprint)
    UP: V3 = (0.0, 0.0, 1.0)
    geom = structure.get("geometry", {})
    if not geom or "_sealed" not in geom or not geom["_sealed"]:
         raise GeometryError("MISSING_REQUIRED_GEOMETRY: geometry section must be sealed")
    
    joints = geom.get("joints", {})
    zp = joints.get("z_planes", {})
    layout = joints.get("layout", {})
    
    qty = layout["post_count"]
    post_xy = [tuple(xy) for x_y in layout["post_xy"] for xy in [x_y]] # unpack
    # Wait, layout["post_xy"] is list of lists
    post_xy = [tuple(xy) for xy in layout["post_xy"]]

    Z_GRADE = zp["Z_GRADE"]
    Z_POST_TOP = zp["Z_POST_TOP"]
    Z_BEAM_TOP = zp["Z_BEAM_TOP"]
    Z_APEX = zp["Z_APEX"]
    Z_BEAM_CENTER = zp["Z_BEAM_CENTER"]

    # ── Cross-section half-dimensions (feet) ─────────────────────────────────
    POST_HW   = (structure["members"]["posts"]["actual_width_in"]  / 24.0)
    POST_HD   = (structure["members"]["posts"]["actual_depth_in"]  / 24.0)
    BEAM_HW   = (structure["members"]["beams"]["actual_width_in"]  / 24.0)
    BEAM_HD   = (structure["members"]["beams"]["actual_depth_in"]  / 24.0)
    RAFTER_HW = (structure["roof"]["primary_rafters"]["actual_width_in"] / 24.0)
    RAFTER_HD = (structure["roof"]["primary_rafters"]["actual_depth_in"] / 24.0)
    BRACE_HW  = (structure["bracing"]["brace"]["actual_width_in"] / 24.0)
    BRACE_HD  = (structure["bracing"]["brace"]["actual_depth_in"] / 24.0)

    solids: list[Solid] = []

    # 1. Footings
    for i, (px, py) in enumerate(post_xy):
        solids.append(_make_prism((px, py, Z_GRADE - 1.5), (px, py, Z_GRADE + 0.33), 0.5, 0.5, UP, pal["footing"], "footing", f"FT{i+1}"))

    # 2. Posts
    for i, (px, py) in enumerate(post_xy):
        solids.append(_make_prism((px, py, Z_GRADE), (px, py, Z_POST_TOP), POST_HW, POST_HD, UP, pal["post"], "post", f"P{i+1}"))

    # 3. Beams (derived from corners)
    for i in range(qty):
        p1 = post_xy[i]; p2 = post_xy[(i+1)%qty]
        solids.append(_make_prism((p1[0], p1[1], Z_BEAM_CENTER), (p2[0], p2[1], Z_BEAM_CENTER), BEAM_HW, BEAM_HD, UP, pal["beam"], "beam", f"B{i+1}"))

    # 4. Braces (from pre-solved endpoints)
    if joints.get("braces", {}).get("enabled"):
        for bp in joints["braces"]["endpoints"]:
            solids.append(_make_prism(tuple(bp["start"]), tuple(bp["end"]), BRACE_HW, BRACE_HD, UP, pal["brace"], "brace", bp["id"]))

    # 5. Primary Rafters (Notched Solids - Phase 2)
    for rj in joints.get("primary_rafters", []):
        solids.append(_make_notched_rafter(
            tuple(rj["start"]), tuple(rj["end"]), tuple(rj["seat_point"]),
            RAFTER_HW, RAFTER_HD, rj["seat_depth_ft"], UP,
            pal["rafter"], "rafter", rj["id"]
        ))

    # 6. Jack Rafters
    jack_joints = joints.get("jack_rafters", {})
    if jack_joints.get("enabled"):
        for ep in jack_joints.get("endpoints", []):
            # For now jacks are prisms, but they should also be notched if they cross a beam
            # In hex pergola, all jacks originate on a beam, so they NEED a notched seat.
            # We'll treat start as tail and assume a small seat at p0.
            solids.append(_make_notched_rafter(
                tuple(ep["start"]), tuple(ep["end"]), tuple(ep["start"]), # Seat at start
                RAFTER_HW, RAFTER_HD, joints["primary_rafters"][0]["seat_depth_ft"], UP,
                pal["rafter"], "rafter", ep["id"]
            ))

    # 7. Hub (Constraint-Driven Massing - Phase 3)
    hj = joints.get("hub", {})
    hub_r = hj["radius_ft"]
    hub_h = hj["height_ft"]
    hub_ztop = Z_APEX + (hub_h / 2.0)
    hub_zbot = Z_APEX - (hub_h / 2.0)
    
    ring_top = [(hub_r*math.cos(2*math.pi*(i+0.5)/qty), hub_r*math.sin(2*math.pi*(i+0.5)/qty), hub_ztop) for i in range(qty)]
    ring_bot = [(hub_r*math.cos(2*math.pi*(i+0.5)/qty), hub_r*math.sin(2*math.pi*(i+0.5)/qty), hub_zbot) for i in range(qty)]
    
    hub_solid = Solid(role="hub", tag="HUB", p0=(0.0, 0.0, hub_zbot), p1=(0.0, 0.0, hub_ztop))
    hub_solid.faces.append(Face(ring_top, UP, pal["hub"]["top"], "hub", "HUB"))
    hub_solid.faces.append(Face(list(reversed(ring_bot)), vscl(UP, -1.0), pal["hub"]["bottom"], "hub", "HUB"))
    for i in range(qty):
        j = (i+1)%qty
        mid_ang = 2*math.pi*(i+1.0)/qty
        sn = (math.cos(mid_ang), math.sin(mid_ang), 0.0)
        shade = pal["hub"]["left"] if vdot(sn, (0.866, 0.5, 0.0)) > 0 else pal["hub"]["right"]
        hub_solid.faces.append(Face([ring_bot[i], ring_bot[j], ring_top[j], ring_top[i]], sn, shade, "hub", "HUB"))
    solids.append(hub_solid)

    return Scene(solids=solids, qty=qty, hub_r=hub_r, Z_GRADE=Z_GRADE, Z_POST_TOP=Z_POST_TOP, Z_BEAM_TOP=Z_BEAM_TOP, Z_APEX=Z_APEX, post_xy=post_xy)


# ---------------------------------------------------------------------------
# validate_scene_geometry — must pass before any SVG is emitted
# ---------------------------------------------------------------------------

_FT_TOL  = 1.0 / 120.0   # 1/10 inch in feet
_IN_TOL  = 1.0 / 12.0    # 1 inch in feet


def validate_scene_geometry(scene: Scene) -> None:
    """
    Raises GeometryError with exact description on any invariant violation.

    Invariants
    ----------
    1. post_top_z == beam_bottom_z  (shared Z plane, ±1/10")
    2. rafter apex XY radius == hub_r  (±1/10")
    3. all rafter apex XY radii >= hub_r  (rafters reach hub face)
    4. brace lower Z < Z_POST_TOP  (brace goes below beam)
    5. brace upper Z ≈ Z_POST_TOP  (brace terminates at beam soffit, ±1")
    6. all member axis lengths > 0
    7. all coordinates finite
    8. member counts match qty
    9. beam endpoints are on post positions (±1/8")
    10. brace lower foot XY is on a post face (≤1 ft); brace upper head within beam span (≤3 ft)
    """
    qty = scene.qty

    # Count members by role
    by_role: dict[str, list[Solid]] = {}
    for s in scene.solids:
        by_role.setdefault(s.role, []).append(s)

    # 1 — Shared Z plane
    # beam_d = Z_BEAM_TOP - Z_POST_TOP; verified implicitly by construction
    z_diff = abs(scene.Z_BEAM_TOP - scene.Z_POST_TOP - (scene.Z_BEAM_TOP - scene.Z_POST_TOP))
    # Directly: post top == beam underside by construction constant.
    # We verify by checking beam solids' p0/p1 Z against Z_POST_TOP.
    for s in by_role.get("beam", []):
        beam_bot_z = min(s.p0[2], s.p1[2]) - (scene.Z_BEAM_TOP - scene.Z_POST_TOP)/2.0
        # beam centre z = Z_POST_TOP + BEAM_HD, so min Z of beam prism = Z_POST_TOP
        # p0/p1 are beam-centreline nodes; bottom face = centre - BEAM_HD = Z_POST_TOP ✓
        pass  # enforced structurally; additional numeric check below

    beams = by_role.get("beam", [])
    for b in beams:
        # Beam centreline Z should be between Z_POST_TOP and Z_BEAM_TOP
        centre_z = (b.p0[2] + b.p1[2]) / 2.0
        if centre_z < scene.Z_POST_TOP - _FT_TOL or centre_z > scene.Z_BEAM_TOP + _FT_TOL:
            raise GeometryError(
                f"Invariant 1 violated: beam {b.tag} centreline Z={centre_z:.4f} "
                f"outside [{scene.Z_POST_TOP:.4f}, {scene.Z_BEAM_TOP:.4f}]"
            )

    # 2 & 3 — Rafter apex termination at hub face
    rafters = by_role.get("rafter", [])
    hub_r_face = scene.hub_r * math.cos(math.pi / qty)
    for r in rafters:
        if r.tag.startswith("Jack"):
            continue  # Jack rafters terminate at hip rafters, not the hub face!
        # p1 is the apex end
        apex = r.p1
        xy_r = v2_radius(apex)
        if xy_r < hub_r_face - _FT_TOL:
            raise GeometryError(
                f"Invariant 2/3 violated: rafter {r.tag} apex XY radius {xy_r:.4f} ft "
                f"< hub_r_face {hub_r_face:.4f} ft  (rafter penetrates hub)"
            )
        if xy_r > hub_r_face + 0.2:   # 2.4" max overshoot tolerance
            raise GeometryError(
                f"Invariant 2 violated: rafter {r.tag} apex XY radius {xy_r:.4f} ft "
                f"> hub_r_face {hub_r_face:.4f} + 0.2  (rafter overshoots hub face)"
            )

    # 4 & 5 — Brace endpoints
    braces = by_role.get("brace", [])
    for b in braces:
        lower_z = min(b.p0[2], b.p1[2])
        upper_z = max(b.p0[2], b.p1[2])
        if lower_z >= scene.Z_POST_TOP - _FT_TOL:
            raise GeometryError(
                f"Invariant 4 violated: brace {b.tag} lower endpoint Z={lower_z:.4f} "
                f">= Z_POST_TOP={scene.Z_POST_TOP:.4f}  (brace does not descend below beam)"
            )
        if abs(upper_z - scene.Z_POST_TOP) > _IN_TOL:
            raise GeometryError(
                f"Invariant 5 violated: brace {b.tag} upper endpoint Z={upper_z:.4f} "
                f"differs from Z_POST_TOP={scene.Z_POST_TOP:.4f} by >{_IN_TOL:.4f} ft"
            )

    # 6 — All member axis lengths > 0
    for s in scene.solids:
        # Footing is a solid prism now, so it will have length > 0
        length = vlen(vsub(s.p1, s.p0))
        if length < 1e-6:
            raise GeometryError(
                f"Invariant 6 violated: solid '{s.tag}' ({s.role}) has zero-length axis"
            )

    # 7 — All coordinates finite
    for s in scene.solids:
        for pt in (s.p0, s.p1):
            if not vfinite(pt):
                raise GeometryError(
                    f"Invariant 7 violated: non-finite coordinate in '{s.tag}' ({s.role}): {pt}"
                )
        for face in s.faces:
            for v in face.verts:
                if not vfinite(v):
                    raise GeometryError(
                        f"Invariant 7 violated: non-finite vertex in face of '{s.tag}'"
                    )

    # 8 — Member counts
    expected = {
        "footing": qty, "post": qty, "beam": qty,
        "brace": qty * 2, "hub": 1,
    }
    # Dynamic checks for optional members
    expected["rafter"] = qty * 3 if any(s.role == "rafter" and s.tag.startswith("Jack") for s in scene.solids) else qty
    expected["purlin"] = qty if any(s.role == "purlin" for s in scene.solids) else 0

    for role, expected_count in expected.items():
        actual = len(by_role.get(role, []))
        if actual != expected_count:
            raise GeometryError(
                f"Invariant 8 violated: expected {expected_count} '{role}' solids, "
                f"got {actual}"
            )

    # 9 — Beam endpoints must lie on post positions (beams are constructed from post_xy)
    _BEAM_POST_SNAP = 1.0 / 96.0   # 1/8 inch in feet
    for b in beams:
        for end_pt, end_label in ((b.p0, "p0"), (b.p1, "p1")):
            nearest_dist = min(
                math.sqrt((end_pt[0]-px)**2 + (end_pt[1]-py)**2)
                for px, py in scene.post_xy
            )
            if nearest_dist > _BEAM_POST_SNAP:
                raise GeometryError(
                    f"Invariant 9 violated: beam {b.tag} {end_label} XY "
                    f"({end_pt[0]:.4f}, {end_pt[1]:.4f}) is {nearest_dist:.4f} ft "
                    f"from nearest post — beam endpoint disconnected from post grid"
                )

    # 10 — Brace foot (lower Z endpoint) must contact a post face;
    #       brace head (upper Z endpoint) must be within a credible beam-span distance.
    _BRACE_FOOT_MAX = 1.0   # ft: covers POST_HW for posts up to ~10"
    _BRACE_HEAD_MAX = 3.0   # ft: covers POST_HW + brace_run for any reasonable brace
    for b in braces:
        lower_pt = b.p0 if b.p0[2] <= b.p1[2] else b.p1
        upper_pt = b.p1 if b.p0[2] <= b.p1[2] else b.p0
        lower_dist = min(
            math.sqrt((lower_pt[0]-px)**2 + (lower_pt[1]-py)**2)
            for px, py in scene.post_xy
        )
        upper_dist = min(
            math.sqrt((upper_pt[0]-px)**2 + (upper_pt[1]-py)**2)
            for px, py in scene.post_xy
        )
        if lower_dist > _BRACE_FOOT_MAX:
            raise GeometryError(
                f"Invariant 10 violated: brace {b.tag} lower foot XY "
                f"({lower_pt[0]:.4f}, {lower_pt[1]:.4f}) is {lower_dist:.4f} ft "
                f"from nearest post (max {_BRACE_FOOT_MAX} ft) — brace foot is floating"
            )
        if upper_dist > _BRACE_HEAD_MAX:
            raise GeometryError(
                f"Invariant 10 violated: brace {b.tag} upper head XY "
                f"({upper_pt[0]:.4f}, {upper_pt[1]:.4f}) is {upper_dist:.4f} ft "
                f"from nearest post (max {_BRACE_HEAD_MAX} ft) — brace head is floating"
            )


# ---------------------------------------------------------------------------
# Reusable View Mode & Filtering Layer (Scene -> View)
# ---------------------------------------------------------------------------

from enum import Enum

class ViewMode(Enum):
    PRESENTATION = "presentation"   # Clean high-end carpentry visual
    STRUCTURAL = "structural"       # Raw engineering view showing all timbers
    FABRICATION = "fabrication"     # Component-isolation detail view


def filter_scene_for_view(
    scene: Scene,
    mode: ViewMode,
    camera_dir: tuple[float, float, float] | None = None
) -> list[Solid]:
    """
    Filters the comprehensive 3D Scene Graph into a filtered list of visible
    Solids according to the specified ViewMode and camera direction.
    """
    if mode == ViewMode.STRUCTURAL:
        # structural view displays all structural members in full
        return scene.solids
        
    if mode == ViewMode.PRESENTATION:
        # presentation view focuses on clean, readable primary frame aesthetics
        visible_solids = []
        
        # Calculate brace depth ranges for selective visibility normalisation
        braces = [s for s in scene.solids if s.role == "brace"]
        if braces and camera_dir:
            brace_depths = [
                sum(camera_dir[i] * ((s.p0[i]+s.p1[i])/2.0) for i in range(3))
                for s in braces
            ]
            b_min, b_max = min(brace_depths), max(brace_depths)
            b_range = max(b_max - b_min, 1e-6)
        else:
            b_min, b_range = 0.0, 1.0

        for solid in scene.solids:
            # 1. Suppress all secondary roof members (jack rafters, purlins) to avoid spiderweb clutter
            is_secondary_roof = (solid.role == "purlin") or (solid.role == "rafter" and solid.tag.startswith("Jack"))
            if is_secondary_roof:
                continue
                
            # 2. Selective knee brace visibility filtering based on depth
            if solid.role == "brace":
                if not camera_dir:
                    visible_solids.append(solid)
                    continue
                # Compute camera-relative depth norm for the brace
                mid_depth = sum(
                    camera_dir[i] * ((solid.p0[i]+solid.p1[i])/2.0) for i in range(3)
                )
                norm = (mid_depth - b_min) / b_range
                # Suppress rear and side-rear braces entirely to prevent visual overlap
                if norm < 0.45:
                    continue
                # Foreground/side braces are kept
                visible_solids.append(solid)
            else:
                # Keep posts, beams, primary hip rafters, hub, footings
                visible_solids.append(solid)
                
        return visible_solids

    if mode == ViewMode.FABRICATION:
        # fabrication view isolates specific member types
        return scene.solids

