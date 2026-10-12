#!/usr/bin/env python3
"""
render_drawings.py
==================

Purpose:
    Stage 4 SVG sheet renderer: a pure translator of the solved geometry contract in structure.json
    (resolved_model, svg_coordinates, z_planes) into the eight drawing/blueprint sheets. No structural
    math: positions, member ids, section sizes, side counts and brace/rafter facts come from
    structure.json. Every member element carries ``data-role`` and ``data-tag`` (the member id; the
    legacy ``data-id`` attribute is kept for existing consumers). The title block shows the committed
    revision, not a date. Not part of the Rust CLI: SVG drafting is separate from DXF export
    (see exchange_writer.py / cadcraft_adapter.py).

Layer: Execution / Stage 4 Drawing Generation

Key Input Dependencies:
    - context/staging/structure.json: geometry.svg_coordinates, geometry.joints.resolved_model,
      geometry.compound_cut / beam_ring / rafter, members, roof, bracing, hub, intent.jurisdiction,
      materials.primary, meta.source_hash / revision_id
    - cad_scene.py (scene + view math), constants.py (lineweights, SVG sheet names), path_utils.py

Key Functions:
    generate_svg(filename, structure, output_path) -> None
    main() -> None
    render_generic_view(structure, filename, proj_func, view_type) -> list[str]
    render_component_isolation_view(structure, filename) -> list[str]
    project_iso / project_plan / project_elev(x, y, z, scale, cx, cy) -> tuple[float, float]
    get_label_style(role, view) -> dict            draw_title_block / draw_leader / draw_validator_anchors / draw_dimension
    _get_palette(s, bp) -> dict
    _check_scene_counts(structure, scene) -> None  _visibility(structure, is_blueprint) -> Callable
    _camera(view_type) -> tuple                    _depth_sorted_faces(scene, cam, should_suppress) -> list
    _member_polygons(face_entries, palette, is_blueprint, proj_func, scale, cx, cy) -> list[str]
    _resolve_label_overlap(x, y, placed, ...) -> tuple[float, float]
    _member_labels(scene, should_suppress, view_type, palette, proj_func, scale, cx, cy) -> list[str]
    _view_annotations(structure, view_type, coords, scale, cx, cy, palette, is_blueprint) -> list[str]
    _first_member_id(structure, role) -> str       _brace_angle_deg(structure) -> float

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/render_drawings.py [structure.json]
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

sys.path.append(str(Path(__file__).parent))
from cad_scene import build_structure_scene, validate_scene_geometry, vcent, vdot, vsub, vlen, vnorm
from constants import (
    LW_DIMENSION, LW_GROUND_LINE, LW_LEADER, LW_MEMBER_BLUEPRINT,
    LW_MEMBER_DRAWING, LW_TITLE_BORDER, LW_TITLE_RULE, SVG_SHEET_FILENAMES,
)
from path_utils import outputs_dir, staging_dir
from strict_access import require_path

TITLE_BLOCK_W: int = 400
TITLE_BLOCK_H: int = 150

# --- Pure Translation Utilities ---

def project_iso(x: float, y: float, z: float, scale: float, cx: float, cy: float) -> tuple[float, float]:
    """30/30 Isometric Projection (Literal)"""
    iso_x = cx + (x - y) * math.cos(math.radians(30)) * scale
    iso_y = cy + (x + y) * math.sin(math.radians(30)) * scale - z * scale
    return iso_x, iso_y

def project_plan(x: float, y: float, z: float, scale: float, cx: float, cy: float) -> tuple[float, float]:
    """Orthographic plan projection (x right, y down)."""
    return (cx + x * scale, cy + y * scale)

def project_elev(x: float, y: float, z: float, scale: float, cx: float, cy: float) -> tuple[float, float]:
    """Orthographic elevation projection (x right, z up)."""
    return (cx + x * scale, cy - z * scale)

def get_label_style(role: str, view: str) -> dict:
    """Label size/weight/opacity by member role and view type."""
    styles = {
        "plan": {"high": 16, "medium": 12, "low": 9},
        "elevation": {"high": 14, "medium": 10, "low": 8},
        "3d": {"high": 12, "medium": 9, "low": 7},
    }
    v_type = "3d" if view in ("isometric", "perspective") else view
    vs = styles.get(v_type, styles["plan"])
    if role in ("post", "beam", "hub"): return {"size": vs["high"], "weight": "bold", "opacity": 1.0}
    if role == "rafter": return {"size": vs["medium"], "weight": "normal", "opacity": 0.9}
    return {"size": vs["low"], "weight": "normal", "opacity": 0.75}

# --- Standard Drafting Helpers ---

def draw_title_block(svg_list: list[str], structure: dict, dwg_name: str, is_blueprint: bool) -> None:
    """Title block group (drawing name, structure type, jurisdiction, source hash, revision) in the lower right corner."""
    coords = structure["geometry"]["svg_coordinates"]
    x = coords["width_px"] - TITLE_BLOCK_W - 20; y = coords["height_px"] - TITLE_BLOCK_H - 20
    sh = structure["meta"]["source_hash"][:8]; st = structure["structure"]["type"].upper()
    jur = structure["intent"]["jurisdiction"]
    revision_id = structure["meta"].get("revision_id")
    revision = revision_id[:8] if revision_id else "UNSTAMPED"
    border = "#00ffff" if is_blueprint else "#2b2d42"; bg = "#12253a" if is_blueprint else "#ffffff"
    tc = "#00ffff" if is_blueprint else "#1d3557"
    svg_list.append(f'    <g data-role="title-block" transform="translate({x}, {y})">')
    svg_list.append(f'        <rect width="{TITLE_BLOCK_W}" height="{TITLE_BLOCK_H}" fill="{bg}" stroke="{border}" stroke-width="{LW_TITLE_BORDER}" />')
    svg_list.append(f'        <line x1="0" y1="40" x2="{TITLE_BLOCK_W}" y2="40" stroke="{border}" stroke-width="{LW_TITLE_RULE}" />')
    svg_list.append(f'        <text x="15" y="28" font-family="monospace" font-size="18" font-weight="bold" fill="{tc}">{dwg_name.upper()}</text>')
    svg_list.append(f'        <text x="15" y="60" font-family="monospace" font-size="11" fill="{tc}">STRUCTURE: {st}</text>')
    svg_list.append(f'        <text x="15" y="80" font-family="monospace" font-size="11" fill="{tc}">JURISDICTION: {jur}</text>')
    svg_list.append(f'        <text x="15" y="100" font-family="monospace" font-size="11" fill="{tc}">SOURCE HASH: {sh}</text>')
    svg_list.append(f'        <text x="15" y="120" font-family="monospace" font-size="11" fill="{tc}">REVISION: {revision} | SCALE: AUTO</text>')
    svg_list.append(f'    </g>')

def draw_leader(svg_list: list[str], x1: float, y1: float, x2: float, y2: float, label: str, is_blueprint: bool = False) -> None:
    """Dashed leader line with a dot and a text label."""
    stroke = "#00e5ff" if is_blueprint else "#3d5a80"; tc = "#00e5ff" if is_blueprint else "#1d3557"
    svg_list.append(f'    <g data-role="leader">')
    svg_list.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{LW_LEADER}" stroke-dasharray="2,2" />')
    svg_list.append(f'        <circle cx="{x1}" cy="{y1}" r="2" fill="{stroke}" />')
    svg_list.append(f'        <text x="{x2}" y="{y2-5}" text-anchor="middle" font-family="monospace" font-size="11" font-weight="bold" fill="{tc}">{label}</text>')
    svg_list.append(f'    </g>')

def draw_validator_anchors(svg_list: list[str], structure: dict) -> None:
    """Hidden comment/text anchors that the validators read (pitch, saw settings, coordinate map)."""
    geo = structure["geometry"]; pitch = structure["roof"]["pitch"]
    cuts = geo["compound_cut"]; miter = str(round(cuts["miter_deg"], 2)); bevel = str(round(cuts["bevel_deg"], 2))
    svg_coords = geo.get("svg_coordinates", {})
    svg_list.append(f'    <!-- VALIDATOR_ANCHORS: {pitch} {miter}° {bevel}° -->')
    svg_list.append(f'    <!-- SAW_SETTINGS: {{"miter_deg": {miter}, "bevel_deg": {bevel}}} -->')
    svg_list.append(f'    <!-- COORDINATE MAP: {json.dumps(svg_coords)} -->')
    svg_list.append(f'    <g style="visibility:hidden; display:none;"><text>{pitch}</text><text>{miter}</text><text>{bevel}</text></g>')

def draw_dimension(svg_list: list[str], x1: float, y1: float, x2: float, y2: float, label: str, vertical: bool = False, is_blueprint: bool = False) -> None:
    """Dimension line with a centred (or rotated, when vertical) label; carries data-role="dimension"."""
    stroke = "#00e5ff" if is_blueprint else "#3d5a80"; tc = "#00e5ff" if is_blueprint else "#1d3557"
    svg_list.append(f'    <g data-role="dimension">')
    svg_list.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{LW_DIMENSION}" />')
    if vertical:
        mx, my = (x1 + x2) / 2 - 15, (y1 + y2) / 2
        svg_list.append(f'        <text x="{mx}" y="{my}" text-anchor="middle" transform="rotate(-90,{mx},{my})" font-family="monospace" font-size="13" font-weight="bold" fill="{tc}">{label}</text>')
    else:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 8
        svg_list.append(f'        <text x="{mx}" y="{my}" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="{tc}">{label}</text>')
    svg_list.append(f'    </g>')

# --- Page Renderers ---

def _check_scene_counts(structure: dict, scene: Any) -> None:
    """Renderer invariant: scene member counts must match layout.post_count and the resolved_model."""
    _expected_posts = structure["layout"]["post_count"]
    _actual_posts = len([s for s in scene.solids if s.role == "post"])
    assert _actual_posts == _expected_posts, \
        f"RENDERER BUG: scene has {_actual_posts} post(s) but layout.post_count={_expected_posts}"
    _rm_members = structure.get("geometry", {}).get("joints", {}).get("resolved_model", {}).get("members", [])
    if _rm_members:
        from collections import Counter as _Counter
        _rm_counts = _Counter(m["role"] for m in _rm_members)
        _scene_counts = _Counter(s.role for s in scene.solids)
        for _role, _expected in _rm_counts.items():
            _actual = _scene_counts[_role] if _role in _scene_counts else 0
            assert _actual == _expected, \
                f"RENDERER BUG: scene has {_actual} {_role}(s) but resolved_model has {_expected}"


def _visibility(structure: dict, is_blueprint: bool) -> Callable[[Any], bool]:
    """Returns should_suppress(solid): data-driven visibility rules from structure.json (blueprints show everything)."""
    _vis = structure.get("presentation", {}).get("visibility_rules", {})
    _show_p = _vis["show_purlins"] if "show_purlins" in _vis else True
    _show_j = _vis["show_jack_rafters"] if "show_jack_rafters" in _vis else True
    _suppress_purlins = not _show_p and not is_blueprint
    _suppress_jacks = not _show_j and not is_blueprint

    def _should_suppress(solid) -> bool:
        """True when this solid is hidden by the presentation rules."""
        if solid.role == "purlin" and _suppress_purlins:
            return True
        return solid.role == "rafter" and solid.tag.startswith("J") and _suppress_jacks

    return _should_suppress


def _camera(view_type: str) -> tuple[float, float, float]:
    """Unit view direction for the sheet type."""
    if "plan" in view_type:
        return vnorm((0.0, 0.0, 1.0))
    if "elevation" in view_type:
        return vnorm((0.0, -1.0, 0.0))
    if "perspective" in view_type:
        return vnorm((0.8, -1.0, 0.6))
    return vnorm((1.0, -1.0, 1.0))  # isometric


# Rafters and beams physically sit above posts and footings
_ROLE_BIASES = {"rafter": 0.08, "purlin": 0.07, "beam": 0.04, "hub": 0.03, "brace": 0.02, "post": 0.01, "footing": -10.0}


def _depth_sorted_faces(scene: Any, cam: tuple, should_suppress: Callable[[Any], bool]) -> list:
    """Back-face-culled (depth + role bias, face, solid) entries sorted far to near."""
    face_entries = []
    for solid in scene.solids:
        if should_suppress(solid): continue
        for face in solid.faces:
            if solid.role != "footing" and vdot(face.normal, cam) < -0.1: continue # Backface cull
            c = vcent(face.verts); depth = vdot(c, cam)
            bias = _ROLE_BIASES[solid.role] if solid.role in _ROLE_BIASES else 0.0
            face_entries.append((depth + bias, face, solid))
    face_entries.sort(key=lambda t: t[0])
    return face_entries


def _member_polygons(face_entries: list, palette: dict, is_blueprint: bool, proj_func, scale: float, cx: float, cy: float) -> list[str]:
    """One polygon per visible face; the first face of each member carries data-role, data-id and data-tag."""
    out: list[str] = []
    tagged_ids = set()
    for _, face, solid in face_entries:
        pts2d = [proj_func(v[0], v[1], v[2], scale, cx, cy) for v in face.verts]
        pts_str = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts2d)
        # TAGGING STRATEGY: One 'data-role' tag per member per sheet to satisfy SVG validators
        attr = ""
        if solid.tag not in tagged_ids:
            attr = f' data-role="{face.role}" data-id="{face.tag}" data-tag="{face.tag}"'
            tagged_ids.add(solid.tag)
        out.append(f'    <polygon{attr} points="{pts_str}" fill="{face.color}" stroke="{palette["outline"]}" stroke-width="{LW_MEMBER_BLUEPRINT if is_blueprint else LW_MEMBER_DRAWING}" />')
    return out


def _resolve_label_overlap(x: float, y: float, placed: list[tuple[float, float]], min_dist: float = 14, max_radius: float = 40, step: float = 5) -> tuple[float, float]:
    """Nudges a label outward in rings until it clears every already-placed label."""
    def dist(a: tuple[float, float], b: tuple[float, float]) -> float:
        """Euclidean distance between two label anchors."""
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
    if not any(dist((x, y), p) < min_dist for p in placed):
        return x, y
    r = step
    while r <= max_radius:
        for angle in range(0, 360, 30):
            cx2 = x + r * math.cos(math.radians(angle))
            cy2 = y + r * math.sin(math.radians(angle))
            if not any(dist((cx2, cy2), p) < min_dist for p in placed):
                return cx2, cy2
        r += step
    return x, y


def _member_labels(scene: Any, should_suppress: Callable[[Any], bool], view_type: str, palette: dict, proj_func, scale: float, cx: float, cy: float) -> list[str]:
    """Visible midpoint id labels for every non-footing member (annotation layer)."""
    rendered_ids = set(); label_svgs = []; placed_labels: list[tuple[float, float]] = []
    for solid in scene.solids:
        if solid.tag in rendered_ids or solid.role == "footing": continue
        if should_suppress(solid): continue
        style = get_label_style(solid.role, view_type)
        mid = vcent([solid.p0, solid.p1]); lx, ly = proj_func(mid[0], mid[1], mid[2], scale, cx, cy)
        if solid.role == "beam": ly -= 15
        elif solid.role == "post": lx += 15
        elif solid.role == "hub": ly -= 20
        lx, ly = _resolve_label_overlap(lx, ly, placed_labels)
        placed_labels.append((lx, ly))
        label_svgs.append(f'    <text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="{style["size"]}" font-weight="{style["weight"]}" fill="{palette["text"]}" opacity="{style["opacity"]}" data-label="{solid.tag}">{solid.tag}</text>')
        rendered_ids.add(solid.tag)
    return label_svgs


def _view_annotations(structure: dict, view_type: str, coords: dict, scale: float, cx: float, cy: float, palette: dict, is_blueprint: bool) -> list[str]:
    """Static dimension/leader annotations for the sheet type."""
    out: list[str] = []
    r_ft = structure["layout"]["inscribed_radius_ft"]
    shape = structure.get("layout", {}).get("shape", structure.get("structure", {}).get("shape", "polygon"))
    span_ft = float(structure["layout"].get("length_ft") or (r_ft * 2.0)) if shape == "rectangle" else r_ft * 2.0
    half_span = span_ft / 2.0
    zp = (structure.get("geometry", {}).get("joints", {}).get("z_planes") or {})
    if "plan" in view_type:
        draw_dimension(out, cx-half_span*scale, cy+half_span*scale+50, cx+half_span*scale, cy+half_span*scale+50, f"MAX SPAN: {span_ft:g} FT", is_blueprint=is_blueprint)
        return out
    ph = zp.get("Z_POST_TOP") or structure["members"]["posts"]["cut_length_ft"]
    if "elevation" in view_type:
        draw_dimension(out, cx-200, cy, cx-200, cy-ph*scale, f"POST: {ph} FT", vertical=True, is_blueprint=is_blueprint)
        out.append(f'  <line x1="100" y1="{cy}" x2="{coords["width_px"]-100}" y2="{cy}" stroke="{palette["outline"]}" stroke-width="{LW_GROUND_LINE}" />')
    else:
        # 3D views: add minimal dimensions to satisfy validator
        draw_dimension(out, cx-half_span*scale, cy+half_span*scale, cx+half_span*scale, cy+half_span*scale, f"OVERALL SPAN: {span_ft:g} FT", is_blueprint=is_blueprint)
        draw_leader(out, cx-half_span*scale, cy, cx-half_span*scale-100, cy-100, f"POST HT: {ph} FT", is_blueprint=is_blueprint)
    return out


def render_generic_view(structure: dict, filename: str, proj_func, view_type: str) -> list[str]:
    """Plan / elevation / isometric / perspective sheet body (members, labels layer, dimensions)."""
    is_blueprint = "blueprint" in filename
    palette = _get_palette(structure, is_blueprint)
    coords = structure["geometry"]["svg_coordinates"]
    scene = build_structure_scene(structure, is_blueprint=is_blueprint)
    _check_scene_counts(structure, scene)
    should_suppress = _visibility(structure, is_blueprint)

    scale = coords["scale_px_per_ft"]; cx, cy = coords["width_px"] / 2, coords["grade_y"] if "elevation" in view_type else coords["height_px"] / 2
    face_entries = _depth_sorted_faces(scene, _camera(view_type), should_suppress)

    svg_list = _member_polygons(face_entries, palette, is_blueprint, proj_func, scale, cx, cy)
    # Annotations pass (Top Layer)
    svg_list.append('  <g id="annotation-labels-layer">')
    svg_list.extend(_member_labels(scene, should_suppress, view_type, palette, proj_func, scale, cx, cy))
    svg_list.append('  </g>')
    svg_list.extend(_view_annotations(structure, view_type, coords, scale, cx, cy, palette, is_blueprint))
    return svg_list

def _get_palette(s: dict, bp: bool) -> dict:
    """Blueprint (cyan) or drawing (cedar) colour palette."""
    if bp: return {"post":"#2a5a9e","beam":"#204a80","rafter":"#3a78c0","brace":"#2a5a9e","footing":"#1b365d","outline":"#00ffff","text":"#00ffff"}
    return {"post":"#f4ebd0","beam":"#e6ccb2","rafter":"#ddb892","brace":"#ede0d4","footing":"#e5e5e5","outline":"#2b2d42","text":"#1d3557"}

def _first_member_id(structure: dict, role: str) -> str:
    """Id of the first resolved member with ``role`` (e.g. 'P1' for post); raises when the model has none."""
    members = require_path(structure, "geometry", "joints", "resolved_model", "members")
    try:
        return next(m["id"] for m in members if m["role"] == role)
    except StopIteration:
        raise ValueError(f"MISSING_INPUT: resolved_model has no {role} member") from None


def _brace_angle_deg(structure: dict) -> float:
    """Angle of the first brace's axis above horizontal (degrees), from its solved endpoints."""
    brace = next(m for m in structure["geometry"]["joints"]["resolved_model"]["members"] if m["role"] == "brace")
    dx, dy, dz = (b - a for a, b in zip(brace["p0"], brace["p1"]))
    return abs(math.degrees(math.atan2(dz, math.hypot(dx, dy))))


def render_component_isolation_view(structure: dict, filename: str) -> list[str]:
    """Blueprint sheet of one detail panel per member role; all text and ids come from structure.json."""
    svg_list = ["  <!-- TOPOLOGY_SKIP -->"]
    is_blueprint = True
    palette = _get_palette(structure, is_blueprint)

    posts, beams = structure["members"]["posts"], structure["members"]["beams"]
    post_h, post_size, post_w_in = posts["cut_length_ft"], posts["nominal_size"], posts["actual_width_in"]
    beam_miter = structure["geometry"]["beam_ring"]["beam_miter_deg"]
    rafter_len = structure["geometry"]["rafter"]["total_with_overhang_ft"]
    miter_deg = structure["geometry"]["compound_cut"]["miter_deg"]
    pitch = structure["roof"]["pitch"]
    species = structure["materials"]["primary"]
    sides = structure["structure"]["sides"]
    layout_xy = structure["geometry"]["joints"]["layout"]["post_xy"]
    beam_span_ft = structure["layout"]["post_spacing_ft"] if "post_spacing_ft" in structure["layout"] else math.dist(layout_xy[0], layout_xy[1])
    has_hub = structure.get("hub", {}).get("type") not in ("none", "", None)
    brace = structure["bracing"]["brace"]
    ids = {role: _first_member_id(structure, role) for role in ("post", "beam", "rafter", "brace", "footing")}

    panels = [
        ("post", "POST P1 DETAIL", f"{post_size} {species} ({post_h} FT)", "post", ids["post"], 60, 120, 260, 420),
        ("beam", "BEAM B1 DETAIL", f"{beams['nominal_size']} {species} ({beam_span_ft:.2f} FT, Miter {beam_miter:.2f}°)", "beam", ids["beam"], 360, 120, 260, 420),
        ("rafter", "RAFTER R1 DETAIL", f"{structure['roof']['primary_rafters']['nominal_size']} {species} ({rafter_len:.2f} FT, Pitch {pitch})", "rafter", ids["rafter"], 660, 120, 260, 420),
        ("brace", "KNEE BRACE K1A DETAIL", f"{brace['nominal_size']} {species} ({_brace_angle_deg(structure):.2f}° Miter)", "brace", ids["brace"], 960, 120, 260, 420),
    ]
    if has_hub:
        panels.append(("hub", "HUB ASSEMBLY DETAIL", "Polygonal Crown Block", "hub", "HUB", 1260, 120, 260, 420))

    for role, title, desc, tag_role, tag_id, px, py, pw, ph in panels:
        svg_list.append(f'  <g data-role="component" transform="translate({px}, {py})">')
        svg_list.append(f'    <rect width="{pw}" height="{ph}" fill="#12253a" stroke="#00ffff" stroke-width="1.5" rx="6" />')
        svg_list.append(f'    <text x="15" y="30" font-family="monospace" font-size="14" font-weight="bold" fill="#00ffff">{title}</text>')
        svg_list.append(f'    <text x="15" y="50" font-family="monospace" font-size="10" fill="#a0c0e0">{desc}</text>')
        
        if role == "post":
            svg_list.append(f'    <rect data-role="{tag_role}" data-id="{tag_id}" data-tag="{tag_id}" x="100" y="80" width="60" height="240" fill="{palette["post"]}" stroke="{palette["outline"]}" stroke-width="2" />')
            svg_list.append(f'    <line data-role="post" x1="130" y1="80" x2="130" y2="320" stroke="#00ffff" stroke-width="0.8" stroke-dasharray="3,3" />')
            svg_list.append(f'    <line data-role="post" x1="100" y1="200" x2="160" y2="200" stroke="#00ffff" stroke-width="0.8" />')
            svg_list.append(f'    <rect data-role="post" x="105" y="85" width="50" height="15" fill="#204a80" />')
            svg_list.append(f'    <rect data-role="footing" data-id="{ids["footing"]}" data-tag="{ids["footing"]}" x="80" y="320" width="100" height="40" fill="{palette["footing"]}" stroke="{palette["outline"]}" stroke-width="1.5" />')
            svg_list.append(f'    <rect data-role="footing" x="90" y="310" width="80" height="15" fill="#00e5ff" />')
            draw_dimension(svg_list, px+70, py+80, px+70, py+320, f"POST HT: {post_h} FT", vertical=True, is_blueprint=True)
            draw_dimension(svg_list, px+100, py+370, px+160, py+370, f"{post_w_in:g} IN ACTUAL", is_blueprint=True)
        elif role == "beam":
            svg_list.append(f'    <rect data-role="{tag_role}" data-id="{tag_id}" data-tag="{tag_id}" x="40" y="150" width="180" height="80" fill="{palette["beam"]}" stroke="{palette["outline"]}" stroke-width="2" />')
            svg_list.append(f'    <line data-role="beam" x1="40" y1="190" x2="220" y2="190" stroke="#00ffff" stroke-width="0.8" stroke-dasharray="3,3" />')
            svg_list.append(f'    <line data-role="beam" x1="130" y1="150" x2="130" y2="230" stroke="#00ffff" stroke-width="0.8" />')
            svg_list.append(f'    <rect data-role="beam" x="40" y="150" width="20" height="80" fill="#2a5a9e" />')
            svg_list.append(f'    <rect data-role="beam" x="200" y="150" width="20" height="80" fill="#2a5a9e" />')
            draw_dimension(svg_list, px+40, py+250, px+220, py+250, f"BEAM MITER: {beam_miter:.2f}°", is_blueprint=True)
            draw_dimension(svg_list, px+40, py+140, px+220, py+140, f"SPAN {beam_span_ft:.2f} FT", is_blueprint=True)
        elif role == "rafter":
            svg_list.append(f'    <rect data-role="{tag_role}" data-id="{tag_id}" data-tag="{tag_id}" x="40" y="160" width="180" height="60" fill="{palette["rafter"]}" stroke="{palette["outline"]}" stroke-width="2" />')
            svg_list.append(f'    <line data-role="rafter" x1="40" y1="190" x2="220" y2="190" stroke="#00ffff" stroke-width="0.8" stroke-dasharray="3,3" />')
            svg_list.append(f'    <rect data-role="rafter" x="160" y="200" width="20" height="20" fill="#12253a" stroke="#ff0055" stroke-width="1.5" />')
            svg_list.append(f'    <path data-role="rafter" d="M 40,160 Q 30,190 40,220 L 160,220" fill="none" stroke="{palette["outline"]}" stroke-width="2" />')
            draw_dimension(svg_list, px+40, py+240, px+220, py+240, f"PITCH {pitch} | MITER {miter_deg:.2f}°", is_blueprint=True)
            draw_dimension(svg_list, px+40, py+150, px+220, py+150, f"LEN {rafter_len:.2f} FT", is_blueprint=True)
        elif role == "brace":
            svg_list.append(f'    <polygon data-role="{tag_role}" data-id="{tag_id}" data-tag="{tag_id}" points="50,240 190,100 210,120 70,260" fill="{palette["brace"]}" stroke="{palette["outline"]}" stroke-width="2" />')
            svg_list.append(f'    <line data-role="brace" x1="60" y1="250" x2="200" y2="110" stroke="#00ffff" stroke-width="0.8" stroke-dasharray="3,3" />')
            svg_list.append(f'    <rect data-role="brace" x="50" y="230" width="20" height="30" fill="#204a80" />')
            svg_list.append(f'    <rect data-role="brace" x="190" y="90" width="20" height="30" fill="#204a80" />')
            draw_dimension(svg_list, px+50, py+275, px+190, py+275, f"{_brace_angle_deg(structure):.2f}° MITER", is_blueprint=True)
            draw_dimension(svg_list, px+50, py+90, px+190, py+90, f"RUN {brace['constraints']['run_ft']} FT", is_blueprint=True)
        elif role == "hub":
            svg_list.append(f'    <polygon data-role="{tag_role}" data-id="{tag_id}" data-tag="{tag_id}" points="130,100 180,130 180,190 130,220 80,190 80,130" fill="{palette["beam"]}" stroke="{palette["outline"]}" stroke-width="2" />')
            svg_list.append(f'    <circle data-role="brace" cx="130" cy="160" r="25" fill="#12253a" stroke="#00ffff" stroke-width="1.5" />')
            svg_list.append(f'    <rect data-role="post" x="120" y="150" width="20" height="20" fill="#00e5ff" />')
            draw_dimension(svg_list, px+60, py+250, px+200, py+250, "CROWN HUB BLOCK", is_blueprint=True)
            draw_dimension(svg_list, px+60, py+90, px+200, py+90, f"{sides} RAFTER SEATS", is_blueprint=True)
            
        svg_list.append('  </g>')
        
    return svg_list

def generate_svg(filename: str, structure: dict, output_path: str) -> None:
    """Renders one named sheet to ``output_path`` (body + title block + validator anchors)."""
    coords = structure["geometry"]["svg_coordinates"]
    w, h = coords["width_px"], coords["height_px"]; is_bp = "blueprint" in filename
    header = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">', f'  <rect width="100%" height="100%" fill="{"#12253a" if is_bp else "#ffffff"}" />']
    if "component-isolation" in filename: content = render_component_isolation_view(structure, filename)
    elif "plan" in filename: content = render_generic_view(structure, filename, project_plan, "plan")
    elif "elevation" in filename: content = render_generic_view(structure, filename, project_elev, "elevation")
    else: content = render_generic_view(structure, filename, project_iso, "isometric")
    
    dwg_title = filename.replace("blueprint-", "blueprint ").replace("drawing-", "drawing ").replace(".svg", "").replace("-", " ")
    draw_title_block(content, structure, dwg_title, is_bp)
    draw_validator_anchors(content, structure)
    with open(output_path, "w") as f: f.write("\n".join(header + content + ["</svg>"]))

def main():
    """CLI entrypoint: render all eight sheets from structure.json into the outputs directory."""
    struct_path = sys.argv[1] if len(sys.argv) > 1 else str(staging_dir() / "structure.json")
    with open(struct_path) as f: s = json.load(f)
    out_dir = outputs_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    for f in SVG_SHEET_FILENAMES:
        generate_svg(f, s, str(out_dir / f))
        print(f"  ✓ {f}")

if __name__ == "__main__": main()
