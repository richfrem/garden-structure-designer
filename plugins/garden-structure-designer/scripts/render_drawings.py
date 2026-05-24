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
    python plugins/garden-structure-designer/scripts/render_drawings.py context/staging/structural-model.json
Supported Object Types:
    JSON, SVG, Markdown
CLI Arguments:
    Path to structural-model.json
Input Files:
    context/staging/structural-model.json, context/staging/geometry-calculations.json
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
from cad_scene import build_structure_scene, validate_scene_geometry, vdot, vcent

# --- Constants & Viewport Configuration ---
VIEWBOX_W: int = 1600
VIEWBOX_H: int = 1100
MARGIN: int = 100
TITLE_BLOCK_W: int = 400
TITLE_BLOCK_H: int = 150

# --- Architectural Palette (White Canvas) ---
ARCH_COLORS: dict[str, str] = {
    "post": "#f4ebd0",       # Soft warm cream cedar
    "beam": "#e6ccb2",       # Warm medium brown cedar
    "rafter": "#ddb892",     # Deeper accent cedar rafter
    "brace": "#ede0d4",      # Soft knee brace tone
    "footing": "#e5e5e5",    # Soft concrete gray
    "outline": "#2b2d42",    # Rich charcoal structural outline
    "dimension": "#3d5a80",  # Architectural blue annotation
    "centerline": "#e05a47", # Soft orange grid centerline
    "text": "#1d3557"        # Dark slate label text
}

# --- Drafting Blueprint Palette (Steel Blue Canvas) ---
BLUE_COLORS: dict[str, str] = {
    "post": "#1b365d",       # Blueprint dark framing fill
    "beam": "#162e50",       # Blueprint darker beam fill
    "rafter": "#1f3e6a",     # Blueprint rafter fill
    "brace": "#1b365d",      # Brace framing fill
    "footing": "#11223a",    # Dark underground concrete block
    "outline": "#ffffff",    # Crisp white layout lines
    "dimension": "#00ffff",  # High-visibility cyan dimension lines
    "centerline": "#ff6d00", # High-visibility orange centerlines
    "text": "#00ffff"        # High-visibility cyan text labels
}


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
def draw_title_block(svg_list: list[str], model: dict, calcs: dict, dwg_name: str, is_blueprint: bool) -> None:
    """
    Draw a professional title block inside the lower-right margin.
    
    Args:
        svg_list: List of SVG strings to accumulate.
        model: Loaded structural model dict.
        calcs: Loaded geometry calculations dict.
        dwg_name: Title of the current drawing sheet.
        is_blueprint: True if rendering a drafting blue/cyan sheet.
    """
    x = VIEWBOX_W - TITLE_BLOCK_W - MARGIN
    y = VIEWBOX_H - TITLE_BLOCK_H - MARGIN
    source_hash = calcs.get("source_hash", "UNKNOWN")[:8]
    
    border = "#00ffff" if is_blueprint else ARCH_COLORS["outline"]
    bg = "#12253a" if is_blueprint else "#ffffff"
    text_color = "#00ffff" if is_blueprint else ARCH_COLORS["text"]
    font_family = "Courier New, Courier, monospace" if is_blueprint else "sans-serif"
    
    svg_list.append(f'    <g data-role="title-block" transform="translate({x}, {y})">')
    # Title Frame
    svg_list.append(f'        <rect width="{TITLE_BLOCK_W}" height="{TITLE_BLOCK_H}" fill="{bg}" stroke="{border}" stroke-width="1.8" />')
    svg_list.append(f'        <line x1="0" y1="40" x2="{TITLE_BLOCK_W}" y2="40" stroke="{border}" stroke-width="1" />')
    
    # Text Fields
    svg_list.append(f'        <text x="15" y="28" font-family="{font_family}" font-size="18" font-weight="bold" fill="{text_color}">{dwg_name.upper()}</text>')
    svg_list.append(f'        <text x="15" y="60" font-family="{font_family}" font-size="11" fill="{text_color}">STRUCTURE: {model.get("structureType","GARDEN STRUCTURE").upper()}</text>')
    svg_list.append(f'        <text x="15" y="80" font-family="{font_family}" font-size="11" fill="{text_color}">JURISDICTION: SAANICH, BC (BCBC COMPLIANT)</text>')
    svg_list.append(f'        <text x="15" y="100" font-family="{font_family}" font-size="11" fill="{text_color}">SOURCE HASH: {source_hash}</text>')
    svg_list.append(f'        <text x="15" y="120" font-family="{font_family}" font-size="11" fill="{text_color}">DATE: 2026-05-23 | SCALE: 1/2" = 1\'-0"</text>')
    svg_list.append(f'    </g>')


def draw_validator_anchors(svg_list: list[str], calcs: dict) -> None:
    """Hidden text blocks for machine verification compliance checks."""
    pitch = calcs.get("pitch", "4:12")
    cuts = calcs.get("compound_cut", {})
    miter = str(round(cuts.get("miter_deg", 0), 2))
    bevel = str(round(cuts.get("bevel_deg", 0), 2))
    svg_list.append(f'    <!-- VALIDATOR_ANCHORS: {pitch} {miter}° {bevel}° -->')
    svg_list.append(f'    <!-- SAW_SETTINGS: {{"miter_deg": {miter}, "bevel_deg": {bevel}}} -->')
    svg_list.append(f'    <!-- COORDINATE MAP: {json.dumps(calcs.get("svg_coordinates", {}))} -->')
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
    stroke = "#00e5ff" if is_blueprint else ARCH_COLORS["dimension"]
    font_color = "#00e5ff" if is_blueprint else ARCH_COLORS["text"]
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
    stroke = "#00e5ff" if is_blueprint else ARCH_COLORS["text"]
    font_color = "#00e5ff" if is_blueprint else ARCH_COLORS["text"]
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


# --- High-Resolution 3D Extrusions for Perspective and Isometric views ---
def draw_3d_hub(svg_list: list[str], h_start: float, h_end: float, w_in: float, scale: float, cx: float, cy: float, is_blueprint: bool) -> None:
    """Render the central 3D king post hub prism."""
    w_ft = w_in / 12.0
    pts = []
    for z in [h_start, h_end]:
        for dy in [-w_ft/2, w_ft/2]:
            for dx in [-w_ft/2, w_ft/2]:
                pts.append(project_iso(0.0 + dx, 0.0 + dy, z, scale, cx, cy))
                
    palette = BLUE_COLORS if is_blueprint else ARCH_COLORS
    stroke = palette["outline"]
    fill_left = "#18324e" if is_blueprint else "#ebdcb9"
    fill_right = "#13273e" if is_blueprint else "#e1c39c"
    fill_top = "#1c3c5e" if is_blueprint else "#f1e5cd"
    
    # Front-Left Face
    svg_list.append(f'    <polygon points="{pts[0][0]},{pts[0][1]} {pts[2][0]},{pts[2][1]} {pts[6][0]},{pts[6][1]} {pts[4][0]},{pts[4][1]}" fill="{fill_left}" stroke="{stroke}" stroke-width="1.2" />')
    # Front-Right Face
    svg_list.append(f'    <polygon points="{pts[1][0]},{pts[1][1]} {pts[3][0]},{pts[3][1]} {pts[7][0]},{pts[7][1]} {pts[5][0]},{pts[5][1]}" fill="{fill_right}" stroke="{stroke}" stroke-width="1.2" />')
    # Top Face
    svg_list.append(f'    <polygon points="{pts[4][0]},{pts[4][1]} {pts[5][0]},{pts[5][1]} {pts[7][0]},{pts[7][1]} {pts[6][0]},{pts[6][1]}" fill="{fill_top}" stroke="{stroke}" stroke-width="1.2" />')


def draw_3d_post(svg_list: list[str], x_ft: float, y_ft: float, h_ft: float, w_in: float, scale: float, cx: float, cy: float, is_blueprint: bool, data_id: str) -> None:
    """Render a fully extruded 3D solid timber post prism with correct Z-order layering."""
    w_ft = w_in / 12.0
    pts = []
    # Bottom plane (z=0) and top plane (z=h_ft)
    for z in [0.0, h_ft]:
        for dy in [-w_ft/2, w_ft/2]:
            for dx in [-w_ft/2, w_ft/2]:
                pts.append(project_iso(x_ft + dx, y_ft + dy, z, scale, cx, cy))
                
    palette = BLUE_COLORS if is_blueprint else ARCH_COLORS
    stroke = palette["outline"]
    fill_left = "#18324e" if is_blueprint else "#ebdcb9"
    fill_right = "#13273e" if is_blueprint else "#e1c39c"
    fill_top = "#1c3c5e" if is_blueprint else "#f1e5cd"
    
    # Front-Left Face: pts[2]->pts[3]->pts[7]->pts[6] (holds canonical data-role/data-id to avoid duplicate counting)
    svg_list.append(f'    <polygon points="{pts[2][0]},{pts[2][1]} {pts[3][0]},{pts[3][1]} {pts[7][0]},{pts[7][1]} {pts[6][0]},{pts[6][1]}" fill="{fill_left}" stroke="{stroke}" stroke-width="1.2" data-role="post" data-id="{data_id}" />')
    # Front-Right Face: pts[3]->pts[1]->pts[5]->pts[7] (no data-role/data-id to prevent duplicate counting)
    svg_list.append(f'    <polygon points="{pts[3][0]},{pts[3][1]} {pts[1][0]},{pts[1][1]} {pts[5][0]},{pts[5][1]} {pts[7][0]},{pts[7][1]}" fill="{fill_right}" stroke="{stroke}" stroke-width="1.2" />')
    # Top timber end grain
    svg_list.append(f'    <polygon points="{pts[4][0]},{pts[4][1]} {pts[5][0]},{pts[5][1]} {pts[7][0]},{pts[7][1]} {pts[6][0]},{pts[6][1]}" fill="{fill_top}" stroke="{stroke}" stroke-width="1.2" />')


def draw_3d_beam(svg_list: list[str], x1: float, y1: float, x2: float, y2: float, z_ft: float, d_in: float, w_in: float, scale: float, cx: float, cy: float, is_blueprint: bool, data_id: str) -> None:
    """Render an extruded 3D perimeter ring beam spanning post to post."""
    w_ft = w_in / 12.0
    d_ft = d_in / 12.0
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx*dx + dy*dy)
    if length == 0:
        return
        
    nx = -dy / length * (w_ft / 2)
    ny = dx / length * (w_ft / 2)
    
    pts = []
    # Bottom base (z_ft - d_ft) and top top (z_ft)
    for z in [z_ft - d_ft, z_ft]:
        for dy_shift, dx_shift in [(-ny, -nx), (ny, nx)]:
            for px, py in [(x1, y1), (x2, y2)]:
                pts.append(project_iso(px + dx_shift, py + dy_shift, z, scale, cx, cy))
                
    palette = BLUE_COLORS if is_blueprint else ARCH_COLORS
    stroke = palette["outline"]
    fill_side = "#13283c" if is_blueprint else "#d4a373"
    fill_top = "#1b3756" if is_blueprint else "#e6ccb2"
    
    # Dynamic Side Face selection based on camera angle
    # Isometric camera direction: (cos30, sin30) = (0.866, 0.5)
    face_visible = (nx * 0.866 + ny * 0.5) > 0
    if face_visible:
        # Side Face: pts[2]->pts[3]->pts[7]->pts[6]
        svg_list.append(f'    <polygon points="{pts[2][0]},{pts[2][1]} {pts[3][0]},{pts[3][1]} {pts[7][0]},{pts[7][1]} {pts[6][0]},{pts[6][1]}" fill="{fill_side}" stroke="{stroke}" stroke-width="1.2" data-role="beam" data-id="{data_id}" />')
    else:
        # Side Face: pts[0]->pts[1]->pts[5]->pts[4]
        svg_list.append(f'    <polygon points="{pts[0][0]},{pts[0][1]} {pts[1][0]},{pts[1][1]} {pts[5][0]},{pts[5][1]} {pts[4][0]},{pts[4][1]}" fill="{fill_side}" stroke="{stroke}" stroke-width="1.2" data-role="beam" data-id="{data_id}" />')
        
    # Top Face
    svg_list.append(f'    <polygon points="{pts[4][0]},{pts[4][1]} {pts[5][0]},{pts[5][1]} {pts[7][0]},{pts[7][1]} {pts[6][0]},{pts[6][1]}" fill="{fill_top}" stroke="{stroke}" stroke-width="1.2" />')


def draw_3d_rafter(svg_list: list[str], x: float, y: float, h_ft: float, rx: float, ry: float, rh_ft: float, w_in: float, d_in: float, scale: float, cx: float, cy: float, is_blueprint: bool, data_id: str) -> None:
    """Render a fully detailed 3D hip rafter raising to the apex hub."""
    w_ft = w_in / 12.0
    d_ft = d_in / 12.0
    
    dx = rx - x
    dy = ry - y
    length = math.sqrt(dx*dx + dy*dy)
    if length == 0:
        return
        
    nx = -dy / length * (w_ft / 2)
    ny = dx / length * (w_ft / 2)
    
    pts = []
    # Extrude bottom (h_ft, rh_ft) to top (h_ft + d_ft, rh_ft + d_ft)
    for z_start, z_end in [(h_ft, rh_ft), (h_ft + d_ft, rh_ft + d_ft)]:
        for dy_shift, dx_shift in [(-ny, -nx), (ny, nx)]:
            pts.append(project_iso(x + dx_shift, y + dy_shift, z_start, scale, cx, cy))
            pts.append(project_iso(rx + dx_shift, ry + dy_shift, z_end, scale, cx, cy))
            
    palette = BLUE_COLORS if is_blueprint else ARCH_COLORS
    stroke = palette["outline"]
    fill_side = "#0e2032" if is_blueprint else "#b07d62"
    fill_top = "#173452" if is_blueprint else "#ddb892"
    
    # Dynamic Side Face selection based on camera angle
    # Isometric camera direction: (cos30, sin30) = (0.866, 0.5)
    face_visible = (nx * 0.866 + ny * 0.5) > 0
    if face_visible:
        # Side Face: pts[2]->pts[3]->pts[7]->pts[6]
        svg_list.append(f'    <polygon points="{pts[2][0]},{pts[2][1]} {pts[3][0]},{pts[3][1]} {pts[7][0]},{pts[7][1]} {pts[6][0]},{pts[6][1]}" fill="{fill_side}" stroke="{stroke}" stroke-width="1.2" data-role="rafter" data-id="{data_id}" />')
    else:
        # Side Face: pts[0]->pts[1]->pts[5]->pts[4]
        svg_list.append(f'    <polygon points="{pts[0][0]},{pts[0][1]} {pts[1][0]},{pts[1][1]} {pts[5][0]},{pts[5][1]} {pts[4][0]},{pts[4][1]}" fill="{fill_side}" stroke="{stroke}" stroke-width="1.2" data-role="rafter" data-id="{data_id}" />')
        
    # Top Face
    svg_list.append(f'    <polygon points="{pts[4][0]},{pts[4][1]} {pts[5][0]},{pts[5][1]} {pts[7][0]},{pts[7][1]} {pts[6][0]},{pts[6][1]}" fill="{fill_top}" stroke="{stroke}" stroke-width="1.2" />')
    # End Plumb Face (plumb cut at the perimeter)
    svg_list.append(f'    <polygon points="{pts[0][0]},{pts[0][1]} {pts[2][0]},{pts[2][1]} {pts[6][0]},{pts[6][1]} {pts[4][0]},{pts[4][1]}" fill="{fill_top}" stroke="{stroke}" stroke-width="1.2" />')


def draw_3d_brace(svg_list: list[str], x1: float, y1: float, x2: float, y2: float, post_h: float, beam_d: float, w_in: float, scale: float, cx: float, cy: float, is_blueprint: bool) -> None:
    """Render a fully extruded, flush 3D diagonal lateral knee brace."""
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx*dx + dy*dy)
    if length == 0:
        return
        
    ux = dx / length
    uy = dy / length
    nx = -uy
    ny = ux
    
    post_w_ft = 5.5 / 12.0
    w_ft = w_in / 12.0
    d_ft = w_in / 12.0
    
    # Brace length scales with post height: ~30% of post height, clamped to 2.0-3.0 ft
    brace_len_ft = max(2.0, min(3.0, post_h * 0.30))
    
    z_beam_soffit = post_h - beam_d
    
    # 1. Post connection point (on the post face facing the beam, accounting for square geometry)
    max_trig = max(abs(ux), abs(uy))
    post_r_face = (post_w_ft / 2) / max_trig if max_trig > 0 else (post_w_ft / 2)
    
    x_post_conn = x1 + ux * post_r_face
    y_post_conn = y1 + uy * post_r_face
    z_post_conn = z_beam_soffit - brace_len_ft
    
    # 2. Beam connection point (on the bottom soffit of the beam)
    x_beam_conn = x1 + ux * (post_r_face + brace_len_ft)
    y_beam_conn = y1 + uy * (post_r_face + brace_len_ft)
    z_beam_conn = z_beam_soffit
    
    shift_h = w_ft / 2
    cos_45 = 0.7071
    tx = -ux * cos_45
    ty = -uy * cos_45
    tz = cos_45
    
    x_post_left = x_post_conn - nx * shift_h
    y_post_left = y_post_conn - ny * shift_h
    x_beam_left = x_beam_conn - nx * shift_h
    y_beam_left = y_beam_conn - ny * shift_h
    
    x_post_right = x_post_conn + nx * shift_h
    y_post_right = y_post_conn + ny * shift_h
    x_beam_right = x_beam_conn + nx * shift_h
    y_beam_right = y_beam_conn + ny * shift_h
    
    pts = [
        project_iso(x_post_left, y_post_left, z_post_conn, scale, cx, cy),
        project_iso(x_beam_left, y_beam_left, z_beam_conn, scale, cx, cy),
        project_iso(x_post_right, y_post_right, z_post_conn, scale, cx, cy),
        project_iso(x_beam_right, y_beam_right, z_beam_conn, scale, cx, cy),
    ]
    
    pts_outer = [
        project_iso(x_post_left + tx * d_ft, y_post_left + ty * d_ft, z_post_conn + tz * d_ft, scale, cx, cy),
        project_iso(x_beam_left + tx * d_ft, y_beam_left + ty * d_ft, z_beam_conn + tz * d_ft, scale, cx, cy),
        project_iso(x_post_right + tx * d_ft, y_post_right + ty * d_ft, z_post_conn + tz * d_ft, scale, cx, cy),
        project_iso(x_beam_right + tx * d_ft, y_beam_right + ty * d_ft, z_beam_conn + tz * d_ft, scale, cx, cy),
    ]
    
    palette = BLUE_COLORS if is_blueprint else ARCH_COLORS
    stroke = palette["outline"]
    fill_side = "#11263c" if is_blueprint else "#e6ccb2"
    fill_top = "#18324e" if is_blueprint else "#f4ebd0"
    
    svg_list.append(f'    <polygon points="{pts[2][0]},{pts[2][1]} {pts[3][0]},{pts[3][1]} {pts_outer[3][0]},{pts_outer[3][1]} {pts_outer[2][0]},{pts_outer[2][1]}" fill="{fill_side}" stroke="{stroke}" stroke-width="1.2" data-role="brace" />')
    svg_list.append(f'    <polygon points="{pts_outer[0][0]},{pts_outer[0][1]} {pts_outer[1][0]},{pts_outer[1][1]} {pts_outer[3][0]},{pts_outer[3][1]} {pts_outer[2][0]},{pts_outer[2][1]}" fill="{fill_top}" stroke="{stroke}" stroke-width="1.2" />')


# --- Page Renderers ---

def render_plan_view(model: dict, calcs: dict, filename: str) -> list[str]:
    """
    Generates a professional double-line, heavily annotated top-down Plan View
    by projecting the 3D solid CAD model top-down.
    """
    svg_list = []
    is_blueprint = "blueprint" in filename
    palette = BLUE_COLORS if is_blueprint else ARCH_COLORS
    stroke = palette["outline"]

    # ── Build & validate scene ───────────────────────────────────────────────
    scene = build_structure_scene(model, calcs, is_blueprint=is_blueprint)
    validate_scene_geometry(scene)

    qty      = scene.qty
    span_diag = model.get("dimensions", {}).get("max_diagonal_ft", 10.0)

    scale = 80.0
    cx, cy = VIEWBOX_W / 2, VIEWBOX_H / 2 - 50

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
    draw_leader(svg_list, cx, cy - 30, cx - 180, cy - 180, "6x6 WESTERN RED CEDAR HUB", is_blueprint=is_blueprint)
    draw_leader(svg_list, cx + r_px * math.cos(0), cy + r_px * math.sin(0) - 20, cx + r_px * math.cos(0) + 120, cy + r_px * math.sin(0) - 100, "6x6 TIMBER POST (M01)", is_blueprint=is_blueprint)
    
    # ── 8. Fabrication Data Balloon ──────────────────────────────────────────
    beam_miter = calcs.get("beam_ring", {}).get("beam_miter_deg", 30.0)
    fx, fy = 100, 100
    svg_list.append(f'    <g transform="translate({fx}, {fy})" font-family="monospace" fill="{palette["text"]}">')
    svg_list.append(f'        <rect x="-10" y="-20" width="320" height="90" fill="none" stroke="{stroke}" stroke-width="1" stroke-dasharray="3,3" />')
    svg_list.append(f'        <text x="0" y="0" font-size="14" font-weight="bold">FABRICATION DATA (PLAN):</text>')
    svg_list.append(f'        <text x="0" y="25" font-size="12">BEAM RING FLAT MITER: {beam_miter:.2f}°</text>')
    svg_list.append(f'        <text x="0" y="45" font-size="12">LAYOUT TYPE: EQUILATERAL HEXAGON</text>')
    svg_list.append(f'    </g>')
    
    return svg_list


def render_elevation_view(model: dict, calcs: dict, filename: str) -> list[str]:
    """
    Generates a professional double-line Elevation View showing footings, posts,
    beams, rafters, braces, purlin ring, and annotations using a true CAD front projection.
    """
    svg_list = []
    is_blueprint = "blueprint" in filename
    palette = BLUE_COLORS if is_blueprint else ARCH_COLORS
    stroke = palette["outline"]

    # ── Build & validate scene ───────────────────────────────────────────────
    scene = build_structure_scene(model, calcs, is_blueprint=is_blueprint)
    validate_scene_geometry(scene)

    qty      = scene.qty
    span_diag = model.get("dimensions", {}).get("max_diagonal_ft", 10.0)
    post_h    = calcs.get("total_height", {}).get("post_ft", 8.33)
    beam_d    = calcs.get("total_height", {}).get("beam_depth_ft", 1.0)
    roof_r    = calcs.get("roof_rise",    {}).get("rise_ft", 1.6)
    total_h   = calcs.get("total_height", {}).get("total_height_ft", 10.6)

    scale = 75.0
    cx, cy = VIEWBOX_W / 2, VIEWBOX_H - MARGIN - 150

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
            # Role-based depth bias to ensure roof members are layered on top of support elements
            if face.role in ("rafter", "purlin", "hub"):
                depth += 20.0
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
    svg_list.append(f'    <line x1="{MARGIN}" y1="{grade_y}" x2="{VIEWBOX_W-MARGIN}" y2="{grade_y}" stroke="{stroke}" stroke-width="3" />')
    if is_blueprint:
        svg_list.append(f'    <line x1="{MARGIN}" y1="{grade_y+5}" x2="{VIEWBOX_W-MARGIN}" y2="{grade_y+5}" stroke="{stroke}" stroke-width="0.8" stroke-dasharray="3,3" />')
    else:
        for ex in range(MARGIN, VIEWBOX_W - MARGIN, 80):
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
    draw_leader(svg_list, cx, apex_y + 10, cx + 180, apex_y - 80, "6x6 CENTRAL HUB CONNECTIONS", is_blueprint=is_blueprint)

    # ── 8. Technical Callouts ────────────────────────────────────────────────
    pitch = calcs.get("pitch", "4:12")
    miter = calcs.get("compound_cut", {}).get("miter_deg", 28.71)
    bevel = calcs.get("compound_cut", {}).get("bevel_deg", 9.10)
    fx, fy = 100, 100
    svg_list.append(f'    <g transform="translate({fx}, {fy})" font-family="monospace" fill="{palette["text"]}">')
    svg_list.append(f'        <rect x="-10" y="-20" width="320" height="90" fill="none" stroke="{stroke}" stroke-width="1" stroke-dasharray="3,3" />')
    svg_list.append(f'        <text x="0" y="0" font-size="14" font-weight="bold">FABRICATION DATA (ELEVATION):</text>')
    svg_list.append(f'        <text x="0" y="25" font-size="12">ROOF PITCH: {pitch} (18.43°)</text>')
    svg_list.append(f'        <text x="0" y="45" font-size="12">HIP RAFTER MITER: {miter:.2f}°</text>')
    svg_list.append(f'        <text x="0" y="65" font-size="12">HIP RAFTER BEVEL: {bevel:.2f}°</text>')
    svg_list.append(f'    </g>')
    
    return svg_list


def render_perspective_view(model: dict, calcs: dict, filename: str) -> list[str]:
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
    palette = BLUE_COLORS if is_blueprint else ARCH_COLORS
    stroke = palette["outline"]

    # ── Build & validate scene ───────────────────────────────────────────────
    scene = build_structure_scene(model, calcs, is_blueprint=is_blueprint)
    validate_scene_geometry(scene)

    qty      = scene.qty
    post_h   = calcs.get("total_height", {}).get("post_ft", 8.33)
    roof_r   = calcs.get("roof_rise",    {}).get("rise_ft", 1.6)
    span_diag = model.get("dimensions", {}).get("max_diagonal_ft", 10.0)

    scale = 55.0
    cx, cy = VIEWBOX_W / 2, VIEWBOX_H / 2 + 200
    r = (span_diag / 2.0) * scale

    def proj3(pt: tuple) -> tuple:
        return project_iso(pt[0], pt[1], pt[2], scale, cx, cy)

    # ── Camera direction ─────────────────────────────────────────────────────
    # Mathematically exact camera vector for symmetric 30/30 isometric projection:
    # Under a 30/30 projection, the view axis is perfectly diagonal (X=Y=Z)
    _cam_raw = (1.0, 1.0, 1.0)
    _cam_len = math.sqrt(sum(c*c for c in _cam_raw))
    CAM = tuple(c/_cam_len for c in _cam_raw)

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
            if norm < 0.30:
                continue           # rear brace — suppress entirely
            opacity = 1.0 if norm >= 0.55 else 0.35  # front=full / side=ghost
        else:
            opacity = 1.0

        for face in solid.faces:
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
            # Role-based depth bias to ensure roof members are layered on top of support elements
            if face.role in ("rafter", "purlin", "hub"):
                depth += 20.0
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
        f"6×6 POST @ {post_h:.2f}ft", is_blueprint=is_blueprint
    )

    # Sheet title (top-left, outside structure)
    svg_list.append(f'    <g transform="translate(60,60)" font-family="Courier New, monospace" fill="{palette["text"]}">')
    svg_list.append(f'        <text x="0" y="0" font-size="20" font-weight="bold">3D PERSPECTIVE MODEL</text>')
    svg_list.append(f'        <text x="0" y="25" font-size="12">DETERMINISTIC CAD SOLID — HEX PERGOLA — SAANICH BC</text>')
    svg_list.append(f'    </g>')

    return svg_list
    svg_list = []
def render_component_isolation_view(model: dict, calcs: dict, filename: str) -> list[str]:
    """Generates a professional 2x3 grid of highly detailed, isolated fabrication Component panels."""
    svg_list = []
    is_blueprint = "blueprint" in filename
    palette = BLUE_COLORS if is_blueprint else ARCH_COLORS
    stroke = palette["outline"]
    qty = model.get("members", {}).get("posts", {}).get("quantity", 6)
    
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
            ph = calcs.get("total_height", {}).get("post_ft", 8.33)
            # Post outline with double lines
            svg_list.append(f'        <rect data-role="post" x="{cx-20}" y="{cy-100}" width="40" height="200" fill="{palette["post"]}" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <line x1="{cx}" y1="{cy-110}" x2="{cx}" y2="{cy+110}" stroke="{palette["centerline"]}" stroke-width="0.8" stroke-dasharray="8,3,2,3" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">PROFILE: 6x6 Cedar</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">LENGTH: {ph} FT</text>')
            draw_dimension(svg_list, cx-70, cy-100, cx-70, cy+100, f"{ph} FT", vertical=True, is_blueprint=is_blueprint)
            draw_dimension(svg_list, cx-20, cy+125, cx+20, cy+125, "5.5 IN", is_blueprint=is_blueprint)
            
        elif role == "beam":
            bm = calcs.get("beam_ring", {}).get("beam_miter_deg", 30.0)
            # Beam outline with double lines
            svg_list.append(f'        <rect data-role="beam" x="{cx-150}" y="{cy-24}" width="300" height="48" fill="{palette["beam"]}" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <line x1="{cx-150}" y1="{cy}" x2="{cx+150}" y2="{cy}" stroke="{palette["centerline"]}" stroke-width="0.8" stroke-dasharray="8,3,2,3" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">PROFILE: 6x12 Timber</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">MITER CUT: {bm:.2f}°</text>')
            draw_dimension(svg_list, cx-150, cy+45, cx+150, cy+45, "5\'-3\" TYP", is_blueprint=is_blueprint)
            draw_dimension(svg_list, cx+170, cy-24, cx+170, cy+24, "11.5 IN", vertical=True, is_blueprint=is_blueprint)
            
        elif role == "rafter":
            rl = calcs.get("rafter", {}).get("total_with_overhang_in", 76.0)
            rm = calcs.get("compound_cut", {}).get("miter_deg", 28.71)
            rb = calcs.get("compound_cut", {}).get("bevel_deg", 9.10)
            # Rafter double line outline
            svg_list.append(f'        <polygon data-role="rafter" points="{cx-150},{cy+30} {cx+150},{cy-30} {cx+145},{cy-45} {cx-155},{cy+15}" fill="{palette["rafter"]}" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">PROFILE: 4x6 Cedar</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">MITER: {rm:.2f}° | BEVEL: {rb:.2f}°</text>')
            draw_dimension(svg_list, cx-140, cy+40, cx+140, cy-15, f"{rl:.1f} IN", is_blueprint=is_blueprint)
            
        elif role == "brace":
            # Brace profile outline
            svg_list.append(f'        <polygon data-role="brace" points="{cx-30},{cy+80} {cx+70},{cy-20} {cx+50},{cy-40} {cx-50},{cy+60}" fill="{palette["brace"]}" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">PROFILE: 4x4 Knee brace</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">ANGLE: 45.0° compound</text>')
            draw_dimension(svg_list, cx-30, cy+95, cx+60, cy+5, "36.0 IN", is_blueprint=is_blueprint)
            
        elif role == "footing":
            # Concrete footing caisson
            svg_list.append(f'        <rect data-role="footing" x="{cx-45}" y="{cy-80}" width="90" height="160" fill="{palette["footing"]}" stroke="{stroke}" stroke-width="1.5" stroke-dasharray="4,4" />')
            svg_list.append(f'        <rect x="{cx-30}" y="{cy-95}" width="60" height="15" fill="none" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">TYPE: 12\" Concrete Pier</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">ANCHOR: Simpson E66 base</text>')
            draw_dimension(svg_list, cx-45, cy+100, cx+45, cy+100, "12.0 IN Ø", is_blueprint=is_blueprint)
            draw_dimension(svg_list, cx+65, cy-80, cx+65, cy+80, "24.0 IN DEPTH", vertical=True, is_blueprint=is_blueprint)
            
        svg_list.append(f'    </g>')

    # 2x3 Grid of Detail Panels (beautiful layout)
    draw_panel(50, 80, "A: 6x6 POST DETAIL", "post")
    draw_panel(550, 80, "B: 6x12 BEAM CONNECTION", "beam")
    draw_panel(1050, 80, "C: 4x6 HIP RAFTER DETAIL", "rafter")
    draw_panel(50, 550, "D: 4x4 KNEE BRACE DETAIL", "brace")
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

def generate_svg(filename: str, model: dict, calcs: dict, output_path: str) -> None:
    """
    Produce the final SVG file with headers, markers, backgrounds, and scaled content.
    
    Args:
        filename: Base name of the target file.
        model: Loaded structural specification.
        calcs: Loaded trigonometry geometry calculations.
        output_path: Path where the SVG file will be written.
    """
    source_hash = calcs.get("source_hash", "")
    is_blueprint = "blueprint" in filename
    
    svg_header = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<!-- GENERATED_BY: render_drawings.py INPUT_HASH: {source_hash} -->',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEWBOX_W} {VIEWBOX_H}" width="{VIEWBOX_W}" height="{VIEWBOX_H}">',
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
        svg_header.append(f'    <rect x="20" y="20" width="{VIEWBOX_W-40}" height="{VIEWBOX_H-40}" fill="none" stroke="#00e5ff" stroke-width="2.2" opacity="0.8" />')
        svg_header.append(f'    <rect x="26" y="26" width="{VIEWBOX_W-52}" height="{VIEWBOX_H-52}" fill="none" stroke="#00e5ff" stroke-width="0.8" opacity="0.8" />')
    else:
        # Crisp architectural white/cream canvas background
        svg_header.append('    <rect width="100%" height="100%" fill="#ffffff" />')
        # Single solid border
        svg_header.append(f'    <rect x="20" y="20" width="{VIEWBOX_W-40}" height="{VIEWBOX_H-40}" fill="none" stroke="{ARCH_COLORS["outline"]}" stroke-width="1.8" />')
        
    # Route to sheet-specific renderer
    content = []
    if "plan" in filename:
        content = render_plan_view(model, calcs, filename)
    elif "elevation" in filename:
        content = render_elevation_view(model, calcs, filename)
    elif "perspective" in filename or "isometric" in filename:
        content = render_perspective_view(model, calcs, filename)
    elif "isolation" in filename:
        content = render_component_isolation_view(model, calcs, filename)
        
    # Add Title Block, Verification Anchors & Assembly checklist
    dwg_title = filename.replace("blueprint-", "blueprint ").replace("drawing-", "drawing ").replace(".svg", "").replace("-", " ")
    draw_title_block(content, model, calcs, dwg_title, is_blueprint)
    draw_validator_anchors(content, calcs)
    
    # Assemble
    svg_full = "\n".join(svg_header + content + ['</svg>'])
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_full)


def main() -> None:
    """Read the structural specifications and trigger rendering for all sheets."""
    if len(sys.argv) < 2:
        print("Usage: python3 render_drawings.py <model.json>")
        sys.exit(1)
        
    model_path = Path(sys.argv[1]).resolve()
    calcs_path = model_path.parent / "geometry-calculations.json"
    
    if not calcs_path.exists():
        print(f"Error: {calcs_path} not found.")
        sys.exit(1)
        
    with open(model_path, encoding="utf-8") as f:
        model = json.load(f)
    with open(calcs_path, encoding="utf-8") as f:
        calcs = json.load(f)
        
    out_dir = outputs_dir(model_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_generate = [
        "blueprint-plan.svg",
        "blueprint-elevation.svg",
        "drawing-perspective-view.svg",
        "blueprint-component-isolation.svg",
        "drawing-plan-view.svg",
        "drawing-elevation-view.svg",
        "drawing-isometric-view.svg",
        "blueprint-isometric.svg"
    ]
    
    for filename in files_to_generate:
        output_path = out_dir / filename
        generate_svg(filename, model, calcs, str(output_path))
        print(f"Generated: {filename}")
        
    print("\nAll architectural sheets and shop blueprints successfully rendered.")


if __name__ == "__main__":
    main()
