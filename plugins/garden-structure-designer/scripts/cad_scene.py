#!/usr/bin/env python3
"""
cad_scene.py
============
Pure-Python CAD scene graph for garden-structure-designer.
Refactored for v5: Pure Translator of the JSON Geometry Compiler output.

Layer: Execution (Pure Translation)
"""
from __future__ import annotations
import math
import warnings
from dataclasses import dataclass, field
from enum import Enum

class GeometryError(ValueError):
    """Raised when a scene geometry invariant is violated."""

# ---------------------------------------------------------------------------
# V3 Vector Primitives (Mirroring Compiler)
# ---------------------------------------------------------------------------
V3 = tuple[float, float, float]

def vadd(a: V3, b: V3) -> V3: return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def vsub(a: V3, b: V3) -> V3: return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def vscl(a: V3, s: float) -> V3: return (a[0]*s, a[1]*s, a[2]*s)
def vmul(a: V3, s: float) -> V3: return (a[0]*s, a[1]*s, a[2]*s)
def vdot(a: V3, b: V3) -> float: return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def vcross(a: V3, b: V3) -> V3: return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def vlen(a: V3) -> float: return math.sqrt(vdot(a, a))
def vnorm(a: V3) -> V3: l = vlen(a); return vmul(a, 1.0/l) if l > 1e-12 else (0.0, 0.0, 0.0)
def vdist(a: V3, b: V3) -> float: return vlen(vsub(a, b))
def vcent(pts: list[V3]) -> V3:
    n = len(pts); return (sum(p[0] for p in pts)/n, sum(p[1] for p in pts)/n, sum(p[2] for p in pts)/n)
def vfinite(v: V3) -> bool: return all(math.isfinite(c) for c in v)
def v2_radius(v: V3) -> float: return math.sqrt(v[0]*v[0] + v[1]*v[1])

@dataclass
class Face:
    verts:  list[V3]
    normal: V3
    color:  str
    role:   str
    tag:    str | None
    depth:  float = 0.0

@dataclass
class Solid:
    role:   str
    tag:    str
    faces:  list[Face] = field(default_factory=list)
    p0:     V3 = (0.0, 0.0, 0.0)
    p1:     V3 = (0.0, 0.0, 0.0)

@dataclass
class Scene:
    solids:   list[Solid]
    qty:      int
    hub_r:    float
    Z_GRADE:  float
    Z_POST_TOP: float
    Z_BEAM_TOP: float
    Z_APEX:   float
    post_xy:  list[tuple[float, float]]

# ---------------------------------------------------------------------------
# Scene Builder — The Pure Translator
# ---------------------------------------------------------------------------

def _build_scene_legacy(model: dict, calcs: dict) -> tuple[dict, dict]:
    """DEPRECATED: Builds (resolved_model, joints) from old dual-dict (model, calcs) format.

    Called only when build_structure_scene() receives a dict as second argument.
    Use compute_from_structure() + build_structure_scene(structure) instead.
    """
    warnings.warn(
        "build_structure_scene(model, calcs) is DEPRECATED. "
        "Pass a single structure.json dict that contains resolved_model. "
        "Call compute_from_structure() first to populate it.",
        DeprecationWarning,
        stacklevel=3,
    )
    qty = model.get("members", {}).get("posts", {}).get("quantity", 6)
    r_ft = model.get("dimensions", {}).get("max_diagonal_ft", 10.0) / 2.0
    post_h = calcs.get("total_height", {}).get("post_ft", 8.33)
    beam_d = calcs.get("total_height", {}).get("beam_depth_ft", 0.604)
    roof_r = calcs.get("roof_rise", {}).get("rise_ft", 1.667)

    structure_dict = {
        "layout": {
            "post_count": qty,
            "inscribed_radius_ft": r_ft
        },
        "members": {
            "posts": {
                "nominal_size": "6x6",
                "actual_width_in": 5.5,
                "actual_depth_in": 5.5,
                "cut_length_ft": post_h
            },
            "beams": {
                "nominal_size": "6x12",
                "actual_width_in": 6.0,
                "actual_depth_in": beam_d * 12.0
            }
        },
        "roof": {
            "pitch": f"{roof_r * 12.0 / r_ft:.6f}:12",
            "primary_rafters": {
                "count": qty,
                "nominal_size": "4x6",
                "actual_width_in": 3.5,
                "actual_depth_in": 5.5,
                "overhang_ft": 0.75
            }
        },
        "hub": {
            "type": "polygonal",
            "radius_min_ft": 0.6
        },
        "bracing": {
            "enabled": model.get("bracing", {}).get("enabled", True),
            "brace": {
                "nominal_size": "4x4",
                "actual_width_in": 3.5,
                "actual_depth_in": 3.5,
                "count_per_post": 2,
                "constraints": {"start_surface": "post_face", "end_surface": "beam_soffit", "run_ft": 1.5}
            }
        }
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


def build_structure_scene(structure: dict, is_blueprint: bool = False) -> Scene:
    """
    Build the scene by strictly translating the resolved_model from Step 2.
    NO MATH ALLOWED. (Phase 1 Purge)
    """
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

    solids: list[Solid] = []
    for m in resolved["members"]:
        role = m["role"]; bid = m["id"]
        role_pal = pal.get(role, pal.get("other", "#888888"))
        solid = Solid(role=role, tag=bid, p0=tuple(m["p0"]), p1=tuple(m["p1"]))
        for f in m["faces"]:
            verts = [tuple(m["vertices"][idx]) for idx in f["verts"]]
            color = role_pal if isinstance(role_pal, str) else role_pal.get(f["color_key"], role_pal.get("other", "#888888"))
            solid.faces.append(Face(verts=verts, normal=tuple(f["normal"]), color=color, role=role, tag=bid))
        solids.append(solid)

    zp = joints["z_planes"]; layout = joints["layout"]
    return Scene(solids=solids, qty=layout["post_count"], hub_r=joints["hub"]["radius_ft"], Z_GRADE=zp["Z_GRADE"], Z_POST_TOP=zp["Z_POST_TOP"], Z_BEAM_TOP=zp["Z_BEAM_TOP"], Z_APEX=zp["Z_APEX"], post_xy=[tuple(xy) for xy in layout["post_xy"]])

def validate_scene_geometry(scene: Scene) -> None:
    """v5 Compiler-Only Invariants: ensure the translation produced a finite, non-zero model."""
    for s in scene.solids:
        if vdist(s.p0, s.p1) < 1e-6: raise GeometryError(f"zero-length member {s.tag}")
        if not all(vfinite(f.normal) for f in s.faces): raise GeometryError(f"Non-finite normal in {s.tag}")
        
        if s.role == "beam":
            _BEAM_POST_SNAP = 0.125 / 12.0
            for end_pt, label in ((s.p0, "p0"), (s.p1, "p1")):
                nearest_dist = min(
                    math.sqrt((end_pt[0] - px) ** 2 + (end_pt[1] - py) ** 2)
                    for px, py in scene.post_xy
                )
                if nearest_dist > _BEAM_POST_SNAP:
                    raise GeometryError(
                        f"Invariant 9: Beam {s.tag} {label} XY is displaced from post grid"
                    )
        elif s.role == "brace":
            _BRACE_FOOT_MAX = 1.0
            lower_pt = s.p0 if s.p0[2] <= s.p1[2] else s.p1
            nearest_dist = min(
                math.sqrt((lower_pt[0] - px) ** 2 + (lower_pt[1] - py) ** 2)
                for px, py in scene.post_xy
            )
            if nearest_dist > _BRACE_FOOT_MAX:
                raise GeometryError(
                    f"Invariant 10: Brace {s.tag} lower foot is floating"
                )
                
            upper_pt = s.p0 if s.p0[2] > s.p1[2] else s.p1
            dist_to_soffit = abs(upper_pt[2] - scene.Z_POST_TOP)
            if dist_to_soffit > 1.0 / 12.0:
                raise GeometryError(
                    f"Invariant 10: Brace {s.tag} upper head is floating"
                )

            # Find closest beam centerline in XY to ensure brace head is on the beam span
            min_beam_dist = float('inf')
            for b in scene.solids:
                if b.role == "beam":
                    ax, ay = b.p0[0], b.p0[1]
                    bx, by = b.p1[0], b.p1[1]
                    px, py = upper_pt[0], upper_pt[1]
                    dx = bx - ax
                    dy = by - ay
                    ab2 = dx*dx + dy*dy
                    if ab2 > 1e-6:
                        t = ((px - ax) * dx + (py - ay) * dy) / ab2
                        t = max(0.0, min(1.0, t))
                        cx = ax + t * dx
                        cy = ay + t * dy
                        dist = math.sqrt((px - cx)**2 + (py - cy)**2)
                        if dist < min_beam_dist:
                            min_beam_dist = dist
            if min_beam_dist > 0.5:
                raise GeometryError(
                    f"Invariant 10: Brace {s.tag} upper head is floating"
                )

class ViewMode(Enum):
    PRESENTATION = "presentation"; STRUCTURAL = "structural"; FABRICATION = "fabrication"

def filter_scene_for_view(scene: Scene, mode: ViewMode, camera_dir: tuple[float, float, float] | None = None) -> list[Solid]:
    if mode == ViewMode.STRUCTURAL or mode == ViewMode.FABRICATION: return scene.solids
    if mode == ViewMode.PRESENTATION:
        visible = []
        braces = [s for s in scene.solids if s.role == "brace"]
        if braces and camera_dir:
            depths = [vdot(camera_dir, vcent([s.p0, s.p1])) for s in braces]
            b_min = min(depths); b_range = max(max(depths)-b_min, 1e-6)
        else: b_min = 0.0; b_range = 1.0
        for s in scene.solids:
            if s.role == "purlin" or (s.role == "rafter" and (s.tag.startswith("Jack") or s.tag.startswith("J"))): continue
            if s.role == "brace" and camera_dir:
                if (vdot(camera_dir, vcent([s.p0, s.p1])) - b_min) / b_range < 0.45: continue
            visible.append(s)
        return visible

def _palettes(is_bp: bool) -> dict:
    if is_bp: return {"post":{"top":"#1e4272","bottom":"#0d1e30","left":"#162e50","right":"#0f2238","start":"#1a3560","end":"#1a3560","other":"#162e50"},"beam":{"top":"#1d3e68","bottom":"#0c1d2e","left":"#122840","right":"#0d2035","start":"#162e4e","end":"#162e4e","other":"#122840"},"rafter":{"top":"#1f4070","bottom":"#0e2032","left":"#132842","right":"#0e2234","start":"#172d4c","end":"#172d4c","other":"#132842"},"brace":{"top":"#1b3760","bottom":"#0d1f32","left":"#132440","right":"#0e1e34","start":"#162c4e","end":"#162c4e","other":"#132440"},"hub":{"top":"#204878","bottom":"#0e2035","left":"#1a3868","right":"#152d56","start":"#1d4070","end":"#1d4070","other":"#1a3868"},"purlin":{"top":"#1b3760","bottom":"#0d1f32","left":"#132440","right":"#0e1e34","start":"#162c4e","end":"#162c4e","other":"#132440"},"footing":{"top":"#183050","bottom":"#0d1e30","left":"#122440","right":"#0e1e34","start":"#162c4e","end":"#162c4e","other":"#122440"}}
    return {"post":{"top":"#f1e5cd","bottom":"#c8b090","left":"#ecdfc8","right":"#e0c9a4","start":"#e8dabc","end":"#e8dabc","other":"#ecdfc8"},"beam":{"top":"#e8d4b0","bottom":"#b89070","left":"#d4a878","right":"#c89860","start":"#d0a070","end":"#d0a070","other":"#d4a878"},"rafter":{"top":"#ddb892","bottom":"#a87850","left":"#c89870","right":"#b88860","start":"#c08060","end":"#c08060","other":"#c89870"},"brace":{"top":"#f0e4cc","bottom":"#c0a080","left":"#e8d8b8","right":"#d8c4a0","start":"#e0d0b0","end":"#e0d0b0","other":"#e8d8b8"},"hub":{"top":"#f5ecd8","bottom":"#d0b888","left":"#e8d8c0","right":"#dcc8a8","start":"#e4d4b8","end":"#e4d4b8","other":"#e8d8c0"},"purlin":{"top":"#f0e4cc","bottom":"#c0a080","left":"#e8d8b8","right":"#d8c4a0","start":"#e0d0b0","end":"#e0d0b0","other":"#e8d8b8"},"footing":{"top":"#e0e0e0","bottom":"#b0b0b0","left":"#d3d3d3","right":"#c0c0c0","start":"#c8c8c8","end":"#c8c8c8","other":"#d3d3d3"}}
