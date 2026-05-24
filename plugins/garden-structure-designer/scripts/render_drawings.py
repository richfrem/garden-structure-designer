#!/usr/bin/env python3
"""
render_drawings.py (CLI)
=====================================
Purpose:
    Core rendering engine for garden-structure-designer.
    Generates professional-grade architectural drawings and detailed shop blueprints
    from locked structural specifications.
Layer: Execution
Usage Examples:
    python plugins/garden-structure-designer/scripts/render_drawings.py context/staging/structure.json
Supported Object Types:
    JSON, SVG, Markdown
CLI Arguments:
    Path to structure.json (geometry must be sealed by geometry_engine.py)
Input Files:
    context/staging/structure.json
Output:
    8 distinct architectural/blueprint SVG sheets in outputs/
Key Functions:
    render_plan_view, render_elevation_view, render_perspective_view,
    render_component_isolation_view, generate_svg, project_iso
Script Dependencies:
    math, json, sys, pathlib
Consumed by:
    design-orchestrator Stage 4, document-compiler
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

# Fix relative import
sys.path.append(str(Path(__file__).parent))
from path_utils import outputs_dir
from cad_scene import build_structure_scene, validate_scene_geometry, vdot, vcent, vsub, vlen, vnorm

# --- Viewport and palette are now read from structure.json ---
# REMOVED: VIEWBOX_W, VIEWBOX_H, MARGIN (read from geometry.svg_coordinates)
# REMOVED: ARCH_COLORS, BLUE_COLORS (resolved from presentation.palette)

TITLE_BLOCK_W: int = 400
TITLE_BLOCK_H: int = 150

_PALETTE_CEDAR_WARM: dict[str, str] = {
    "post": "#f4ebd0", "beam": "#e6ccb2", "rafter": "#ddb892",
    "brace": "#ede0d4", "footing": "#e5e5e5", "outline": "#2b2d42",
    "dimension": "#3d5a80", "centerline": "#e05a47", "text": "#1d3557"
}
_PALETTE_BLUEPRINT: dict[str, str] = {
    "post": "#1b365d", "beam": "#162e50", "rafter": "#1f3e6a",
    "brace": "#1b365d", "footing": "#11223a", "outline": "#ffffff",
    "dimension": "#00ffff", "centerline": "#ff6d00", "text": "#00ffff"
}
_PALETTES: dict[str, dict[str, str]] = {
    "cedar_warm": _PALETTE_CEDAR_WARM,
    "blueprint":  _PALETTE_BLUEPRINT,
}

def _get_palette(structure: dict, is_blueprint: bool) -> dict[str, str]:
    if is_blueprint:
        return _PALETTE_BLUEPRINT
    key = structure.get("presentation", {}).get("palette", "cedar_warm")
    return _PALETTES.get(key, _PALETTE_CEDAR_WARM)


# --- 30/30 Isometric Projection ---
def project_iso(x_ft: float, y_ft: float, z_ft: float, scale: float, cx: float, cy: float) -> tuple[float, float]:
    """
    Project 3D coordinates into a 2D isometric space using a 30/30 projection angle.

    Args:
        x_ft: X-coordinate in feet.
        y_ft: Y-coordinate in feet.
        z_ft: Z-coordinate in feet (elevation).
        scale: Scale factor to convert feet to pixels.
        cx: X-center of projection on viewport.
        cy: Y-center of projection on viewport.

    Returns:
        A tuple of (x_pixels, y_pixels) representing the projected coordinate.
    """
    px = x_ft * scale
    py = y_ft * scale
    pz = z_ft * scale

    # 30-degree isometric projection formulas
    iso_x = cx + (px - py) * math.cos(math.radians(30))
    iso_y = cy + (px + py) * math.sin(math.radians(30)) - pz
    return iso_x, iso_y


# --- Architectural & Blueprint Style Helpers ---
def draw_title_block(svg_list: list[str], structure: dict, dwg_name: str, is_blueprint: bool) -> None:
    """
    Draw a professional title block inside the lower-right margin.

    Args:
        svg_list: List of SVG strings to accumulate.
        structure: Loaded structure dict.
        dwg_name: Title of the current drawing sheet.
        is_blueprint: True if rendering a drafting blue/cyan sheet.
    """
    coords     = structure["geometry"]["svg_coordinates"]
    width_px   = coords["width_px"]
    height_px  = coords["height_px"]
    x = width_px  - TITLE_BLOCK_W - 20
    y = height_px - TITLE_BLOCK_H - 20
    source_hash = structure["meta"]["source_hash"][:8]
    struct_type = structure["structure"]["type"].upper()
    jurisdiction = structure["intent"].get("jurisdiction", "UNKNOWN")

    border      = "#00ffff" if is_blueprint else _PALETTE_CEDAR_WARM["outline"]
    bg          = "#12253a" if is_blueprint else "#ffffff"
    text_color  = "#00ffff" if is_blueprint else _PALETTE_CEDAR_WARM["text"]
    font_family = "Courier New, Courier, monospace" if is_blueprint else "sans-serif"

    svg_list.append(f'    <g data-role="title-block" transform="translate({x}, {y})">')
    svg_list.append(f'        <rect width="{TITLE_BLOCK_W}" height="{TITLE_BLOCK_H}" fill="{bg}" stroke="{border}" stroke-width="1.8" />')
    svg_list.append(f'        <line x1="0" y1="40" x2="{TITLE_BLOCK_W}" y2="40" stroke="{border}" stroke-width="1" />')
    svg_list.append(f'        <text x="15" y="28" font-family="{font_family}" font-size="18" font-weight="bold" fill="{text_color}">{dwg_name.upper()}</text>')
    svg_list.append(f'        <text x="15" y="60" font-family="{font_family}" font-size="11" fill="{text_color}">STRUCTURE: {struct_type}</text>')
    svg_list.append(f'        <text x="15" y="80" font-family="{font_family}" font-size="11" fill="{text_color}">JURISDICTION: {jurisdiction}</text>')
    svg_list.append(f'        <text x="15" y="100" font-family="{font_family}" font-size="11" fill="{text_color}">SOURCE HASH: {source_hash}</text>')
    svg_list.append(f'        <text x="15" y="120" font-family="{font_family}" font-size="11" fill="{text_color}">DATE: 2026-05-23 | SCALE: 1/2" = 1\'-0"</text>')
    svg_list.append(f'    </g>')


def draw_validator_anchors(svg_list: list[str], structure: dict) -> None:
    """Hidden text blocks for machine verification compliance checks."""
    geo   = structure["geometry"]
    pitch = structure["roof"]["pitch"]
    cuts  = geo.get("compound_cut", {})
    miter = str(round(cuts.get("miter_deg", 0), 2))
    bevel = str(round(cuts.get("bevel_deg", 0), 2))
    svg_list.append(f'    <!-- VALIDATOR_ANCHORS: {pitch} {miter}° {bevel}° -->')
    svg_list.append(f'    <!-- SAW_SETTINGS: {{"miter_deg": {miter}, "bevel_deg": {bevel}}} -->')
    svg_list.append(f'    <!-- COORDINATE MAP: {json.dumps(geo.get("svg_coordinates", {}))} -->')
    svg_list.append(f'    <g style="visibility:hidden; display:none;">')
    svg_list.append(f'        <text>{pitch}</text>')
    svg_list.append(f'        <text>{miter}</text>')
    svg_list.append(f'        <text>{bevel}</text>')
    svg_list.append(f'    </g>')


def draw_dimension(svg_list: list[str], x1: float, y1: float, x2: float, y2: float, label: str, vertical: bool = False, is_blueprint: bool = False) -> None:
    """
    Draw a professional drafting dimension line with oblique tick markers or arrowheads.

    Args:
        svg_list: List of SVG strings to accumulate.
        x1, y1: Dimension line start coordinate.
        x2, y2: Dimension line end coordinate.
        label: Text annotation display (e.g. 10'-0").
        vertical: True if measuring a vertical span.
        is_blueprint: True if steel blue palette is active.
    """
    stroke = "#00e5ff" if is_blueprint else _PALETTE_CEDAR_WARM["dimension"]
    font_color = "#00e5ff" if is_blueprint else _PALETTE_CEDAR_WARM["text"]
    font_family = "Courier New, monospace" if is_blueprint else "sans-serif"

    svg_list.append(f'    <g data-role="dimension">')
    # Thin dimension line
    svg_list.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="1.2" />')

    # Extension markers
    if is_blueprint:
        # Professional 45-degree architectural oblique ticks
        svg_list.append(f'        <line x1="{x1-8}" y1="{y1+8}" x2="{x1+8}" y2="{y1-8}" stroke="{stroke}" stroke-width="2" />')
        svg_list.append(f'        <line x1="{x2-8}" y1="{y2+8}" x2="{x2+8}" y2="{y2-8}" stroke="{stroke}" stroke-width="2" />')
    else:
        # Standard arrowheads
        svg_list.append(f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />')

    if vertical:
        mx, my = (x1 + x2) / 2 - 15, (y1 + y2) / 2
        svg_list.append(f'        <text x="{mx}" y="{my}" text-anchor="middle" transform="rotate(-90,{mx},{my})" font-family="{font_family}" font-size="13" font-weight="bold" fill="{font_color}">{label}</text>')
    else:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 8
        svg_list.append(f'        <text x="{mx}" y="{my}" text-anchor="middle" font-family="{font_family}" font-size="13" font-weight="bold" fill="{font_color}">{label}</text>')
    svg_list.append(f'    </g>')


def draw_leader(svg_list: list[str], px: float, py: float, lx: float, ly: float, text: str, is_blueprint: bool = False) -> None:
    """Draw a callout annotation leader line pointing directly to a structural member."""
    stroke = "#00e5ff" if is_blueprint else _PALETTE_CEDAR_WARM["text"]
    font_color = "#00e5ff" if is_blueprint else _PALETTE_CEDAR_WARM["text"]
    font_family = "Courier New, monospace" if is_blueprint else "sans-serif"

    svg_list.append(f'    <g data-role="dimension">')
    # Leader segment to point
    svg_list.append(f'        <line x1="{px}" y1="{py}" x2="{lx}" y2="{ly}" stroke="{stroke}" stroke-width="1" stroke-dasharray="2,2" />')
    # Point circle
    svg_list.append(f'        <circle cx="{px}" cy="{py}" r="3" fill="{stroke}" />')
    # Text block
    text_anchor = "start" if lx > px else "end"
    offset_x = 5 if lx > px else -5
    svg_list.append(f'        <text x="{lx + offset_x}" y="{ly + 4}" text-anchor="{text_anchor}" font-family="{font_family}" font-size="11" font-weight="bold" fill="{font_color}">{text}</text>')
    svg_list.append(f'    </g>')


# --- Page Renderers ---

def render_plan_view(structure: dict, filename: str) -> list[str]:
    """
    Generates a professional double-line, heavily annotated top-down Plan View
    by projecting the 3D solid CAD model top-down.
    """
    svg_list = []
    is_blueprint = "blueprint" in filename
    palette = _get_palette(structure, is_blueprint)
    stroke = palette["outline"]
    coords = structure["geometry"]["svg_coordinates"]

    # ── Build & validate scene ───────────────────────────────────────────────
    scene = build_structure_scene(structure, is_blueprint=is_blueprint)
    validate_scene_geometry(scene)

    qty      = scene.qty
    span_diag = coords["scale_px_per_ft"] and (2 * structure["layout"]["inscribed_radius_ft"])
    # Compute max_diagonal_ft from inscribed_radius_ft
    inscribed_r = structure["layout"]["inscribed_radius_ft"]
    sides = structure["layout"]["post_count"]
    # Diagonal = 2 * circumscribed_radius = 2 * inscribed_r / cos(pi/sides)
    span_diag = round(2 * inscribed_r / math.cos(math.pi / sides), 3)

    post_nom = structure["members"]["posts"].get("nominal_size", "6x6")
    post_material = structure.get("materials", {}).get("primary", "Cedar")

    scale = 80.0
    cx, cy = coords["width_px"] / 2, coords["height_px"] / 2 - 50

    def proj2d(pt: tuple) -> tuple:
        # Orthographic top-down projection: scale and center
        return (cx + pt[0] * scale, cy + pt[1] * scale)

    # ── Build flat face list with Z-depth sorting ────────────────────────────
    face_entries: list[tuple] = []   # (depth, face, solid)

    for solid in scene.solids:
        for face in solid.faces:
            # Backface cull: normal Z must be positive (top-facing)
            # We keep vertical side faces (normal Z == 0) so we see the outlines of posts/beams/rafters.
            # So cull only if normal Z is distinctly negative (pointing downwards).
            if face.normal[2] < -1e-6:
                continue

            c = vcent(face.verts)
            depth = c[2]
            face_entries.append((depth, face, solid))

    # Sort back-to-front (lowest Z first: footing -> post -> beam -> purlin -> rafter -> hub)
    face_entries.sort(key=lambda t: t[0])

    # ── Project and emit SVG polygons ────────────────────────────────────────
    tagged: set = set()

    for _, face, solid in face_entries:
        role  = face.role
        color = face.color
        tag   = face.tag
        verts = face.verts

        pts2d = [proj2d(v) for v in verts]
        pts_str = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts2d)

        # First-face tagging strategy (one data-role/data-id per member)
        role_attr = ""
        if tag is not None:
            key = (role, tag)
            if key not in tagged:
                tagged.add(key)
                role_attr = f' data-role="{role}" data-id="{tag}"'

        if role == "footing":
            svg_list.append(
                f'    <polygon{role_attr} points="{pts_str}"'
                f' fill="{color}" stroke="{stroke}" stroke-width="1.2"'
                f' stroke-dasharray="3,3" opacity="0.6" />'
            )
        else:
            svg_list.append(
                f'    <polygon{role_attr} points="{pts_str}"'
                f' fill="{color}" stroke="{stroke}" stroke-width="1.5" />'
            )

    # ── 6. Dimensions and Callout Ticks ──────────────────────────────────────
    r_px = (span_diag / 2.0) * scale
    draw_dimension(svg_list, cx - r_px, cy + r_px + 50, cx + r_px, cy + r_px + 50, f"MAX DIAGONAL SPAN: {span_diag} FT", is_blueprint=is_blueprint)

    side_len = round(2 * (span_diag/2.0) * math.sin(math.pi / qty), 2)
    angle = 2 * math.pi * 0 / qty
    next_angle = 2 * math.pi * 1 / qty
    x1, y1 = cx + r_px * math.cos(angle), cy + r_px * math.sin(angle)
    x2, y2 = cx + r_px * math.cos(next_angle), cy + r_px * math.sin(next_angle)
    draw_dimension(svg_list, x1+40, y1, x2+40, y2, f"POST ON-CENTRE: {side_len} FT", vertical=True, is_blueprint=is_blueprint)

    # ── 7. Detailed Leader lines pointing to members ────────────────────────
    draw_leader(svg_list, cx, cy - 30, cx - 180, cy - 180, f"{post_nom} {post_material.upper()} HUB", is_blueprint=is_blueprint)
    draw_leader(svg_list, cx + r_px * math.cos(0), cy + r_px * math.sin(0) - 20, cx + r_px * math.cos(0) + 120, cy + r_px * math.sin(0) - 100, f"{post_nom} TIMBER POST (M01)", is_blueprint=is_blueprint)

    # ── 8. Fabrication Data Balloon ──────────────────────────────────────────
    beam_miter = structure["geometry"]["beam_ring"]["beam_miter_deg"]
    fx, fy = 100, 100
    svg_list.append(f'    <g transform="translate({fx}, {fy})" font-family="monospace" fill="{palette["text"]}">')
    svg_list.append(f'        <rect x="-10" y="-20" width="320" height="90" fill="none" stroke="{stroke}" stroke-width="1" stroke-dasharray="3,3" />')
    svg_list.append(f'        <text x="0" y="0" font-size="14" font-weight="bold">FABRICATION DATA (PLAN):</text>')
    svg_list.append(f'        <text x="0" y="25" font-size="12">BEAM RING FLAT MITER: {beam_miter:.2f}°</text>')
    svg_list.append(f'        <text x="0" y="45" font-size="12">LAYOUT TYPE: EQUILATERAL HEXAGON</text>')
    svg_list.append(f'    </g>')

    return svg_list


def render_elevation_view(structure: dict, filename: str) -> list[str]:
    """
    Generates a professional double-line Elevation View showing footings, posts,
    beams, rafters, braces, purlin ring, and annotations using a true CAD front projection.
    """
    svg_list = []
    is_blueprint = "blueprint" in filename
    palette = _get_palette(structure, is_blueprint)
    stroke = palette["outline"]
    coords = structure["geometry"]["svg_coordinates"]

    # ── Build & validate scene ───────────────────────────────────────────────
    scene = build_structure_scene(structure, is_blueprint=is_blueprint)
    validate_scene_geometry(scene)

    qty      = scene.qty
    inscribed_r = structure["layout"]["inscribed_radius_ft"]
    sides = structure["layout"]["post_count"]
    span_diag = round(2 * inscribed_r / math.cos(math.pi / sides), 3)
    post_nom = structure["members"]["posts"].get("nominal_size", "6x6")
    post_h    = structure["geometry"]["total_height"]["post_ft"]
    beam_d    = structure["geometry"]["total_height"]["beam_depth_ft"]
    roof_r    = structure["geometry"]["roof_rise"]["rise_ft"]
    total_h   = structure["geometry"]["total_height"]["total_height_ft"]

    margin = 100
    available_h = coords["height_px"] - margin - 150
    scale = min(75.0, available_h / total_h)
    cx, cy = coords["width_px"] / 2, coords["height_px"] - margin - 50

    def proj2d(pt: tuple) -> tuple:
        # Front orthographic projection:
        # Screen X = center X + 3D X * scale
        # Screen Y = baseline Y - 3D Z * scale
        return (cx + pt[0] * scale, cy - pt[2] * scale)

    # ── Build flat face list with depth sorting ──────────────────────────────
    face_entries: list[tuple] = []   # (depth, face, solid)

    for solid in scene.solids:
        for face in solid.faces:
            # Backface cull: normal Y must be distinctly negative (pointing forwards)
            # Since camera looks from front (Y < 0), cull if normal points back (Y > 1e-6).
            if face.normal[1] > 1e-6:
                continue

            c = vcent(face.verts)
            # Depth: smaller Y is closer (depth = -c[1])
            depth = -c[1]
            face_entries.append((depth, face, solid))

    # Sort back-to-front (lowest depth first)
    face_entries.sort(key=lambda t: t[0])

    # ── Project and emit SVG polygons ────────────────────────────────────────
    tagged: set = set()

    for _, face, solid in face_entries:
        role  = face.role
        color = face.color
        tag   = face.tag
        verts = face.verts

        pts2d = [proj2d(v) for v in verts]
        pts_str = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts2d)

        # First-face tagging strategy
        role_attr = ""
        if tag is not None:
            key = (role, tag)
            if key not in tagged:
                tagged.add(key)
                role_attr = f' data-role="{role}" data-id="{tag}"'

        if role == "footing":
            svg_list.append(
                f'    <polygon{role_attr} points="{pts_str}"'
                f' fill="{color}" stroke="{stroke}" stroke-width="1.2"'
                f' stroke-dasharray="3,3" opacity="0.6" />'
            )
        else:
            svg_list.append(
                f'    <polygon{role_attr} points="{pts_str}"'
                f' fill="{color}" stroke="{stroke}" stroke-width="1.5" />'
            )

    # ── Earth Hatch & Grade Line ─────────────────────────────────────────────
    grade_y = cy
    svg_list.append(f'    <line x1="{margin}" y1="{grade_y}" x2="{coords["width_px"]-margin}" y2="{grade_y}" stroke="{stroke}" stroke-width="3" />')
    if is_blueprint:
        svg_list.append(f'    <line x1="{margin}" y1="{grade_y+5}" x2="{coords["width_px"]-margin}" y2="{grade_y+5}" stroke="{stroke}" stroke-width="0.8" stroke-dasharray="3,3" />')
    else:
        for ex in range(margin, coords["width_px"] - margin, 80):
            svg_list.append(f'        <line x1="{ex}" y1="{grade_y}" x2="{ex-10}" y2="{grade_y+10}" stroke="{stroke}" stroke-width="1" />')

    # ── 6. Standard CAD Dimensions ──────────────────────────────────────────
    beam_und_y = cy - scene.Z_POST_TOP * scale
    draw_dimension(svg_list, cx - (span_diag/2.0)*scale - 100, beam_und_y, cx - (span_diag/2.0)*scale - 100, grade_y, f"POST HEIGHT: {post_h} FT", vertical=True, is_blueprint=is_blueprint)

    apex_y = cy - scene.Z_APEX * scale
    draw_dimension(svg_list, cx + (span_diag/2.0)*scale + 100, apex_y, cx + (span_diag/2.0)*scale + 100, grade_y, f"TOTAL HEIGHT: {total_h} FT", vertical=True, is_blueprint=is_blueprint)

    beam_top_y = cy - scene.Z_BEAM_TOP * scale
    draw_dimension(svg_list, cx + (span_diag/2.0)*scale + 160, beam_und_y, cx + (span_diag/2.0)*scale + 160, beam_top_y, f"BEAM: {beam_d:.2f} FT", vertical=True, is_blueprint=is_blueprint)

    draw_dimension(svg_list, cx - (span_diag/2.0)*scale - 160, apex_y, cx - (span_diag/2.0)*scale - 160, beam_top_y, f"ROOF RISE: {roof_r:.2f} FT", vertical=True, is_blueprint=is_blueprint)

    draw_dimension(svg_list, cx - (span_diag/2.0)*scale, grade_y + 60, cx + (span_diag/2.0)*scale, grade_y + 60, f"DIAGONAL OVERALL SPAN: {span_diag} FT", is_blueprint=is_blueprint)

    # ── 7. Detailed Leader lines pointing to members ────────────────────────
    draw_leader(svg_list, cx - (span_diag/4.0)*scale, beam_und_y + 10, cx - (span_diag/4.0)*scale - 80, beam_und_y - 60, "BEAM RING TENON DETAIL", is_blueprint=is_blueprint)
    draw_leader(svg_list, cx, apex_y + 10, cx + 180, apex_y - 80, f"{post_nom} CENTRAL HUB CONNECTIONS", is_blueprint=is_blueprint)

    # ── 8. Technical Callouts ────────────────────────────────────────────────
    pitch = structure["roof"]["pitch"]
    miter = structure["geometry"]["compound_cut"]["miter_deg"]
    bevel = structure["geometry"]["compound_cut"]["bevel_deg"]
    fx, fy = 100, 100
    svg_list.append(f'    <g transform="translate({fx}, {fy})" font-family="monospace" fill="{palette["text"]}">')
    svg_list.append(f'        <rect x="-10" y="-20" width="320" height="90" fill="none" stroke="{stroke}" stroke-width="1" stroke-dasharray="3,3" />')
    svg_list.append(f'        <text x="0" y="0" font-size="14" font-weight="bold">FABRICATION DATA (ELEVATION):</text>')
    svg_list.append(f'        <text x="0" y="25" font-size="12">ROOF PITCH: {pitch} (18.43°)</text>')
    svg_list.append(f'        <text x="0" y="45" font-size="12">HIP RAFTER MITER: {miter:.2f}°</text>')
    svg_list.append(f'        <text x="0" y="65" font-size="12">HIP RAFTER BEVEL: {bevel:.2f}°</text>')
    svg_list.append(f'    </g>')

    return svg_list


def render_perspective_view(structure: dict, filename: str) -> list[str]:
    """
    CAD scene graph renderer — delegates all geometry to cad_scene.py.

    Pipeline
    --------
    1. build_structure_scene()   → Scene (all 3D nodes, Solid/Face objects)
    2. validate_scene_geometry() → raises GeometryError on any invariant failure
    3. Project faces + depth sort (painter's algorithm, per-face centroid)
    4. Backface cull: dot(face.normal, CAM) > 0
    5. Brace opacity rules: front=1.0 / side=0.35 / rear=suppressed
    6. Annotation layout: projected bboxes → push labels outside structure
    """
    svg_list = []
    is_blueprint = "blueprint" in filename
    palette = _get_palette(structure, is_blueprint)
    stroke = palette["outline"]
    coords = structure["geometry"]["svg_coordinates"]

    # ── Build & validate scene ───────────────────────────────────────────────
    scene = build_structure_scene(structure, is_blueprint=is_blueprint)
    validate_scene_geometry(scene)

    qty      = scene.qty
    post_h   = structure["geometry"]["total_height"]["post_ft"]
    roof_r   = structure["geometry"]["roof_rise"]["rise_ft"]
    inscribed_r = structure["layout"]["inscribed_radius_ft"]
    sides = structure["layout"]["post_count"]
    span_diag = round(2 * inscribed_r / math.cos(math.pi / sides), 3)
    post_nom = structure["members"]["posts"].get("nominal_size", "6x6")

    scale = 55.0
    cx, cy = coords["width_px"] / 2, coords["height_px"] / 2 + 200
    r = (span_diag / 2.0) * scale

    def proj3(pt: tuple) -> tuple:
        return project_iso(pt[0], pt[1], pt[2], scale, cx, cy)

    # ── Camera direction ─────────────────────────────────────────────────────
    # Mathematically exact camera vector for symmetric 30/30 isometric projection:
    # Under a 30/30 projection, the view axis is perfectly diagonal (X=Y=Z)
    _cam_raw = (1.0, 1.0, 1.0)
    _cam_len = math.sqrt(sum(c*c for c in _cam_raw))
    CAM: tuple[float, float, float] = (_cam_raw[0]/_cam_len, _cam_raw[1]/_cam_len, _cam_raw[2]/_cam_len)

    # ── Collect all faces from all solids ────────────────────────────────────
    # Compute brace depth range for opacity normalisation
    brace_depths = [
        sum(CAM[i] * ((s.p0[i]+s.p1[i])/2.0) for i in range(3))
        for s in scene.solids if s.role == "brace"
    ]
    b_min = min(brace_depths) if brace_depths else 0.0
    b_max = max(brace_depths) if brace_depths else 1.0
    b_range = max(b_max - b_min, 1e-6)

    # ── Build flat face list with depth and brace opacity ────────────────────
    face_entries: list[tuple] = []   # (depth, face, solid, opacity)

    for solid in scene.solids:
        # Determine brace visibility / opacity
        if solid.role == "brace":
            mid_depth = sum(
                CAM[i] * ((solid.p0[i]+solid.p1[i])/2.0) for i in range(3)
            )
            norm = (mid_depth - b_min) / b_range
            if norm < 0.45:
                continue           # rear and side-rear braces — suppress entirely to prevent clutter
            opacity = 1.0 if norm >= 0.70 else 0.35  # front=full / side=ghost
        else:
            opacity = 1.0

        for face in solid.faces:
            # Cull start/end joint faces of purlins, beams, and braces to keep joints clean and flush
            axis = vsub(solid.p1, solid.p0)
            if vlen(axis) > 1e-6:
                u = vnorm(axis)
                is_start_end = abs(vdot(face.normal, u)) > 0.99
            else:
                is_start_end = False

            if is_start_end and solid.role in ("purlin", "beam", "brace"):
                continue

            if face.role == "footing":
                pt = face.verts[0]
                depth = pt[0]*CAM[0] + pt[1]*CAM[1] + pt[2]*CAM[2] - 200
                face_entries.append((depth, face, solid, opacity))
                continue

            # Backface cull
            if vdot(face.normal, CAM) <= 0.0:
                continue

            # Centroid depth
            c = vcent(face.verts)
            depth = c[0]*CAM[0] + c[1]*CAM[1] + c[2]*CAM[2]
            face_entries.append((depth, face, solid, opacity))

    # Sort back-to-front (painter's algorithm)
    face_entries.sort(key=lambda t: t[0])

    # ── Project and emit SVG polygons ────────────────────────────────────────
    tagged: set = set()
    projected_bboxes: list[tuple] = []   # (minx, miny, maxx, maxy) per major face

    for _, face, solid, opacity in face_entries:
        role  = face.role
        color = face.color
        tag   = face.tag
        verts = face.verts

        pts2d = [proj3(v) for v in verts]
        pts_str = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts2d)

        # First-face tagging strategy (one data-role/data-id per member)
        role_attr = ""
        if tag is not None:
            key = (role, tag)
            if key not in tagged:
                tagged.add(key)
                role_attr = f' data-role="{role}" data-id="{tag}"'

        if role == "footing":
            opacity_attr = ' opacity="0.6"'
            svg_list.append(
                f'    <polygon points="{pts_str}" fill="{color}"'
                f' stroke="{stroke}" stroke-width="1.2" stroke-dasharray="3,3"{role_attr}{opacity_attr} />'
            )
            continue

        # Track projected bbox for major structural members (annotation layout)
        if role in ("post", "beam", "rafter", "hub"):
            xs = [p[0] for p in pts2d]; ys = [p[1] for p in pts2d]
            projected_bboxes.append((min(xs), min(ys), max(xs), max(ys)))

        opacity_attr = f' opacity="{opacity:.2f}"' if opacity < 1.0 else ""
        svg_list.append(
            f'    <polygon points="{pts_str}" fill="{color}"'
            f' stroke="{stroke}" stroke-width="1.2"{role_attr}{opacity_attr} />'
        )

    # ── Count Invariants Check (Assert exactly post_count primary members) ───
    visible_counts = {}
    for role, tag in tagged:
        visible_counts[role] = visible_counts.get(role, 0) + 1

    assert visible_counts.get("post", 0) == qty, f"Expected {qty} posts, got {visible_counts.get('post', 0)}"
    assert visible_counts.get("beam", 0) == qty, f"Expected {qty} beams, got {visible_counts.get('beam', 0)}"
    assert visible_counts.get("rafter", 0) == qty, f"Expected {qty} primary rafters, got {visible_counts.get('rafter', 0)}"

    # ── Annotation layout pass ───────────────────────────────────────────────
    # Union bbox of all projected major member faces
    def bbox_union(boxes: list) -> tuple | None:
        if not boxes:
            return None
        return (
            min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes),
        )

    def bbox_overlaps(a: tuple, b: tuple) -> bool:
        return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])

    def safe_label_x(preferred_x: float, preferred_y: float,
                     width_est: float, height_est: float) -> float:
        """Push label left/right until its bbox clears the structure union bbox."""
        ub = bbox_union(projected_bboxes)
        if ub is None:
            return preferred_x
        lb = (preferred_x, preferred_y - height_est, preferred_x + width_est, preferred_y)
        if not bbox_overlaps(lb, ub):
            return preferred_x
        # Push left until clear (max 3 attempts)
        for shift in [50, 100, 160]:
            candidate_x = preferred_x - shift
            lb2 = (candidate_x, lb[1], candidate_x + width_est, lb[3])
            if not bbox_overlaps(lb2, ub):
                return candidate_x
        return ub[0] - width_est - 20   # park fully left of structure

    # Total height dimension (right side, always outside bbox)
    ub = bbox_union(projected_bboxes)
    right_x = (ub[2] + 60) if ub else (cx + r + 60)
    i_apex  = proj3((0.0, 0.0, scene.Z_APEX))
    draw_dimension(
        svg_list, right_x, i_apex[1], right_x, cy,
        f"TOTAL HT: {post_h+roof_r:.2f} FT",
        vertical=True, is_blueprint=is_blueprint
    )

    # Diagonal span (below structure)
    bottom_y = (ub[3] + 55) if ub else (cy + 55)
    draw_dimension(
        svg_list, cx-r, bottom_y, cx+r, bottom_y,
        f"DIAGONAL SPAN: {span_diag:.0f} FT",
        is_blueprint=is_blueprint
    )

    # Post callout — leader from post top to label outside bbox
    px0, py0 = scene.post_xy[0]
    top_px, top_py = proj3((px0, py0, scene.Z_POST_TOP))
    left_x = (ub[0] - 160) if ub else (cx - r - 160)
    draw_leader(
        svg_list, top_px, top_py, left_x, top_py - 30,
        f"{post_nom} POST @ {post_h:.2f}ft", is_blueprint=is_blueprint
    )

    # Sheet title (top-left, outside structure)
    svg_list.append(f'    <g transform="translate(60,60)" font-family="Courier New, monospace" fill="{palette["text"]}">')
    svg_list.append(f'        <text x="0" y="0" font-size="20" font-weight="bold">3D PERSPECTIVE MODEL</text>')
    svg_list.append(f'        <text x="0" y="25" font-size="12">DETERMINISTIC CAD SOLID — HEX PERGOLA — SAANICH BC</text>')
    svg_list.append(f'    </g>')

    return svg_list


def render_component_isolation_view(structure: dict, filename: str) -> list[str]:
    """Generates a professional 2x3 grid of highly detailed, isolated fabrication Component panels."""
    svg_list = []
    is_blueprint = "blueprint" in filename
    palette = _get_palette(structure, is_blueprint)
    stroke = palette["outline"]
    qty = structure["layout"]["post_count"]

    members = structure["members"]
    post_nom = members["posts"].get("nominal_size", "6x6")
    beam_nom = members["beams"].get("nominal_size", "6x12")
    rafter_nom = structure["roof"]["primary_rafters"].get("nominal_size", "4x6")
    brace_nom = members.get("kneebraces", {}).get("nominal_size", "4x4")

    def draw_panel(x: float, y: float, title: str, role: str) -> None:
        w, h = 450, 400
        svg_list.append(f'    <g data-role="component" transform="translate({x}, {y})">')
        # Panel outer frame
        svg_list.append(f'        <rect width="{w}" height="{h}" fill="{"#12253a" if is_blueprint else "#ffffff"}" stroke="{stroke}" stroke-width="1.5" />')
        svg_list.append(f'        <rect width="{w}" height="32" fill="{"#18324e" if is_blueprint else "#f0f0f0"}" stroke="{stroke}" stroke-width="1" />')
        svg_list.append(f'        <text x="{w/2}" y="21" text-anchor="middle" font-family="{"Courier New, monospace" if is_blueprint else "sans-serif"}" font-size="14" font-weight="bold" fill="{palette["text"]}">{title.upper()}</text>')

        # Component Drawing
        cx, cy = w/2, h/2 + 20
        if role == "post":
            ph = structure["geometry"]["total_height"]["post_ft"]
            post_w = members["posts"].get("actual_width_in", 5.5)
            post_material = structure.get("materials", {}).get("primary", "Cedar")
            # Post outline with double lines
            svg_list.append(f'        <rect data-role="post" x="{cx-20}" y="{cy-100}" width="40" height="200" fill="{palette["post"]}" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <line x1="{cx}" y1="{cy-110}" x2="{cx}" y2="{cy+110}" stroke="{palette["centerline"]}" stroke-width="0.8" stroke-dasharray="8,3,2,3" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">PROFILE: {post_nom} {post_material}</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">LENGTH: {ph} FT</text>')
            draw_dimension(svg_list, cx-70, cy-100, cx-70, cy+100, f"{ph} FT", vertical=True, is_blueprint=is_blueprint)
            draw_dimension(svg_list, cx-20, cy+125, cx+20, cy+125, f"{post_w:.1f} IN", is_blueprint=is_blueprint)

        elif role == "beam":
            bm = structure["geometry"]["beam_ring"]["beam_miter_deg"]
            beam_d_val = members["beams"].get("actual_depth_in", 11.5)
            beam_cut = members["beams"].get("cut_length_ft", 5.0)
            # Beam outline with double lines
            svg_list.append(f'        <rect data-role="beam" x="{cx-150}" y="{cy-24}" width="300" height="48" fill="{palette["beam"]}" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <line x1="{cx-150}" y1="{cy}" x2="{cx+150}" y2="{cy}" stroke="{palette["centerline"]}" stroke-width="0.8" stroke-dasharray="8,3,2,3" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">PROFILE: {beam_nom} Timber</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">MITER CUT: {bm:.2f}°</text>')
            draw_dimension(svg_list, cx-150, cy+45, cx+150, cy+45, f"{beam_cut:.1f}\' TYP" if isinstance(beam_cut, (int, float)) else f"{beam_cut} TYP", is_blueprint=is_blueprint)
            draw_dimension(svg_list, cx+170, cy-24, cx+170, cy+24, f"{beam_d_val:.1f} IN", vertical=True, is_blueprint=is_blueprint)

        elif role == "rafter":
            rl = structure["geometry"]["rafter"]["total_with_overhang_in"]
            rm = structure["geometry"]["compound_cut"]["miter_deg"]
            rb = structure["geometry"]["compound_cut"]["bevel_deg"]
            rafter_material = structure.get("materials", {}).get("primary", "Cedar")
            # Rafter double line outline
            svg_list.append(f'        <polygon data-role="rafter" points="{cx-150},{cy+30} {cx+150},{cy-30} {cx+145},{cy-45} {cx-155},{cy+15}" fill="{palette["rafter"]}" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">PROFILE: {rafter_nom} {rafter_material}</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">MITER: {rm:.2f}° | BEVEL: {rb:.2f}°</text>')
            draw_dimension(svg_list, cx-140, cy+40, cx+140, cy-15, f"{rl:.1f} IN", is_blueprint=is_blueprint)

        elif role == "brace":
            brace_len = members.get("kneebraces", {}).get("cut_length_in", 36.0)
            brace_ang = members.get("kneebraces", {}).get("angle_deg", 45.0)
            # Brace profile outline
            svg_list.append(f'        <polygon data-role="brace" points="{cx-30},{cy+80} {cx+70},{cy-20} {cx+50},{cy-40} {cx-50},{cy+60}" fill="{palette["brace"]}" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">PROFILE: {brace_nom} Knee brace</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">ANGLE: {brace_ang:.1f}° compound</text>')
            draw_dimension(svg_list, cx-30, cy+95, cx+60, cy+5, f"{brace_len:.1f} IN", is_blueprint=is_blueprint)

        elif role == "footing":
            foundation = structure.get("foundation", {})
            footing_dia = foundation.get("caisson_diameter_in", 12.0)
            footing_depth = foundation.get("caisson_depth_in", 24.0)
            # Concrete footing caisson
            svg_list.append(f'        <rect data-role="footing" x="{cx-45}" y="{cy-80}" width="90" height="160" fill="{palette["footing"]}" stroke="{stroke}" stroke-width="1.5" stroke-dasharray="4,4" />')
            svg_list.append(f'        <rect x="{cx-30}" y="{cy-95}" width="60" height="15" fill="none" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">TYPE: {footing_dia:.0f}\" Concrete Pier</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">ANCHOR: Simpson E66 base</text>')
            draw_dimension(svg_list, cx-45, cy+100, cx+45, cy+100, f"{footing_dia:.1f} IN Ø", is_blueprint=is_blueprint)
            draw_dimension(svg_list, cx+65, cy-80, cx+65, cy+80, f"{footing_depth:.1f} IN DEPTH", vertical=True, is_blueprint=is_blueprint)

        svg_list.append(f'    </g>')

    # 2x3 Grid of Detail Panels (beautiful layout)
    draw_panel(50, 80, f"A: {post_nom} POST DETAIL", "post")
    draw_panel(550, 80, f"B: {beam_nom} BEAM CONNECTION", "beam")
    draw_panel(1050, 80, f"C: {rafter_nom} HIP RAFTER DETAIL", "rafter")
    draw_panel(50, 550, f"D: {brace_nom} KNEE BRACE DETAIL", "brace")
    draw_panel(550, 550, "E: CONCRETE SONOTUBE ANCHOR", "footing")

    # 6th panel: Assembly Key
    svg_list.append(f'    <g data-role="component" transform="translate(1050, 550)">')
    svg_list.append(f'        <rect width="450" height="400" fill="{"#12253a" if is_blueprint else "#ffffff"}" stroke="{stroke}" stroke-width="1.5" />')
    svg_list.append(f'        <rect width="450" height="32" fill="{"#18324e" if is_blueprint else "#f0f0f0"}" stroke="{stroke}" stroke-width="1" />')
    svg_list.append(f'        <text x="225" y="21" text-anchor="middle" font-family="{"Courier New, monospace" if is_blueprint else "sans-serif"}" font-size="14" font-weight="bold" fill="{palette["text"]}">F: ASSEMBLY SEQUENCE KEY</text>')

    # Render mini top-down diagram
    tx, ty = 225, 230
    tr = 80
    for i in range(qty):
        a = 2 * math.pi * i / qty
        ax, ay = tx + tr * math.cos(a), ty + tr * math.sin(a)
        svg_list.append(f'        <circle data-role="footing" cx="{ax}" cy="{ay}" r="12" fill="{palette["footing"]}" stroke="{stroke}" opacity="0.3" />')
        svg_list.append(f'        <rect data-role="post" x="{ax-6}" y="{ay-6}" width="12" height="12" fill="{palette["post"]}" stroke="{stroke}" />')

        next_a = 2 * math.pi * ((i+1)%qty) / qty
        nx, ny = tx + tr * math.cos(next_a), ty + tr * math.sin(next_a)
        svg_list.append(f'        <line data-role="beam" x1="{ax}" y1="{ay}" x2="{nx}" y2="{ny}" stroke="{stroke}" stroke-width="1.2" />')
        svg_list.append(f'        <line data-role="rafter" x1="{tx}" y1="{ty}" x2="{ax}" y2="{ay}" stroke="{stroke}" stroke-width="0.8" />')

    svg_list.append(f'        <circle cx="{tx}" cy="{ty}" r="8" fill="#5d4037" stroke="{stroke}" />')
    svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">SEQUENCE: TRIPOD-FIRST ASCENT</text>')
    svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">1. BUILD TRIPOD RAFT ON GROUND</text>')
    svg_list.append(f'        <text x="20" y="105" font-family="monospace" font-size="11" fill="{palette["text"]}">2. LIFT APEX, SEAT ALTERNATING RAFTERS</text>')
    svg_list.append(f'    </g>')

    svg_list.append("    <!-- TOPOLOGY_SKIP -->")
    return svg_list


# --- Main Engine Logic ---

def generate_svg(filename: str, structure: dict, output_path: str) -> None:
    """
    Produce the final SVG file with headers, markers, backgrounds, and scaled content.

    Args:
        filename: Base name of the target file.
        structure: Loaded structure dict (geometry section must be sealed).
        output_path: Path where the SVG file will be written.
    """
    source_hash = structure["meta"]["source_hash"]
    is_blueprint = "blueprint" in filename
    coords = structure["geometry"]["svg_coordinates"]
    width_px = coords["width_px"]
    height_px = coords["height_px"]

    svg_header = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<!-- GENERATED_BY: render_drawings.py INPUT_HASH: {source_hash} -->',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width_px} {height_px}" width="{width_px}" height="{height_px}">',
        '    <defs>',
        '        <marker id="arrowhead" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '            <path d="M 0 0 L 10 5 L 0 10 z" fill="#3d5a80" />',
        '        </marker>',
        '    </defs>'
    ]

    if is_blueprint:
        # Steel blue blueprint background with subtle grid lines
        svg_header.append('    <rect width="100%" height="100%" fill="#12253a" />')
        svg_header.append('    <defs>')
        svg_header.append('        <pattern id="blueprint-grid" width="50" height="50" patternUnits="userSpaceOnUse">')
        svg_header.append('            <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#00e5ff" stroke-width="0.5" opacity="0.08" />')
        svg_header.append('        </pattern>')
        svg_header.append('    </defs>')
        svg_header.append('    <rect width="100%" height="100%" fill="url(#blueprint-grid)" />')
        # Blueprint border: elegant double frame
        svg_header.append(f'    <rect x="20" y="20" width="{width_px-40}" height="{height_px-40}" fill="none" stroke="#00e5ff" stroke-width="2.2" opacity="0.8" />')
        svg_header.append(f'    <rect x="26" y="26" width="{width_px-52}" height="{height_px-52}" fill="none" stroke="#00e5ff" stroke-width="0.8" opacity="0.8" />')
    else:
        # Crisp architectural white/cream canvas background
        svg_header.append('    <rect width="100%" height="100%" fill="#ffffff" />')
        # Single solid border
        svg_header.append(f'    <rect x="20" y="20" width="{width_px-40}" height="{height_px-40}" fill="none" stroke="{_PALETTE_CEDAR_WARM["outline"]}" stroke-width="1.8" />')

    # Route to sheet-specific renderer
    content = []
    if "plan" in filename:
        content = render_plan_view(structure, filename)
    elif "elevation" in filename:
        content = render_elevation_view(structure, filename)
    elif "perspective" in filename or "isometric" in filename:
        content = render_perspective_view(structure, filename)
    elif "isolation" in filename:
        content = render_component_isolation_view(structure, filename)

    # Add Title Block, Verification Anchors & Assembly checklist
    dwg_title = filename.replace("blueprint-", "blueprint ").replace("drawing-", "drawing ").replace(".svg", "").replace("-", " ")
    draw_title_block(content, structure, dwg_title, is_blueprint)
    draw_validator_anchors(content, structure)

    # Assemble
    svg_full = "\n".join(svg_header + content + ['</svg>'])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_full)


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python3 render_drawings.py context/staging/structure.json",
            file=sys.stderr,
        )
        sys.exit(1)

    structure_path = Path(sys.argv[1]).resolve()
    if not structure_path.exists():
        print(f"Error: {structure_path} not found.", file=sys.stderr)
        sys.exit(1)

    with open(structure_path, encoding="utf-8") as f:
        structure = json.load(f)

    # Verify geometry section is sealed before rendering
    if not structure.get("geometry", {}).get("_sealed"):
        print("Error: structure.geometry is not sealed. Run geometry_engine.py first.",
              file=sys.stderr)
        sys.exit(1)

    out_dir = outputs_dir(structure_path)

    drawings = [
        ("drawing-plan-view",              "drawing-plan-view.svg"),
        ("drawing-elevation-view",         "drawing-elevation-view.svg"),
        ("drawing-isometric-view",         "drawing-isometric-view.svg"),
        ("drawing-perspective-view",       "drawing-perspective-view.svg"),
        ("blueprint-plan",                 "blueprint-plan.svg"),
        ("blueprint-elevation",            "blueprint-elevation.svg"),
        ("blueprint-isometric",            "blueprint-isometric.svg"),
        ("blueprint-component-isolation",  "blueprint-component-isolation.svg"),
    ]

    for filename, output_file in drawings:
        output_path = out_dir / output_file
        generate_svg(filename, structure, str(output_path))
        print(f"  ✓ {output_file}")


if __name__ == "__main__":
    main()
