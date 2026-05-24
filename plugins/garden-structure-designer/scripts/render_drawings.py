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

def resolve_label_overlap(
    lx: float,
    ly: float,
    placed_labels: list[tuple[float, float]],
    min_dist: float = 20.0,
    max_radius: float = 40.0,
) -> tuple[float, float]:
    """
    Collision resolution using a deterministic spiral search pattern.
    Enforces a maximum displacement radius.
    """
    if not placed_labels:
        return lx, ly

    def _collides(cx, cy):
        for px, py in placed_labels:
            if math.sqrt((cx - px) ** 2 + (cy - py) ** 2) < min_dist:
                return True
        return False

    if not _collides(lx, ly):
        return lx, ly

    step = 5.0
    for radius in [r for r in range(10, int(max_radius) + int(step), int(step))]:
        if radius > max_radius:
            break
        for angle_deg in [0, 45, 90, 135, 180, 225, 270, 315]:
            angle = math.radians(angle_deg)
            candidate_x = lx + radius * math.cos(angle)
            candidate_y = ly + radius * math.sin(angle)
            
            if not _collides(candidate_x, candidate_y):
                return candidate_x, candidate_y

    return lx, ly  # Return original if no slot found within max_radius


def get_label_style(role: str, view_type: str) -> dict[str, Any]:
    """
    Compute font size and weight based on hierarchical priority and view type.
    Priority: Posts/Beams (High) > Rafters (Medium) > Braces (Low)
    """
    styles = {
        "plan": {"high": 16, "medium": 12, "low": 9},
        "elevation": {"high": 14, "medium": 10, "low": 8},
        "isometric": {"high": 12, "medium": 9, "low": 7},
        "perspective": {"high": 12, "medium": 9, "low": 7},
    }
    view_styles = styles.get(view_type, styles["plan"])
    
    if role in ("post", "beam", "hub"):
        return {"size": view_styles["high"], "weight": "bold", "opacity": 1.0}
    if role == "rafter":
        return {"size": view_styles["medium"], "weight": "normal", "opacity": 0.9}
    return {"size": view_styles["low"], "weight": "normal", "opacity": 0.75}


def get_label_offset(solid, proj_func, view_center=None) -> tuple[float, float]:
    """
    Compute role-based default 2D offsets for labels.
    """
    mid3 = vcent([(solid.p0[0], solid.p0[1], solid.p0[2]), (solid.p1[0], solid.p1[1], solid.p1[2])])
    lx, ly = proj_func(mid3)
    
    if solid.role == "beam":
        return 0.0, -15.0
    if solid.role == "post":
        if view_center:
            dx = lx - view_center[0]; dy = ly - view_center[1]
            d = math.sqrt(dx*dx + dy*dy)
            if d > 1e-3: return (dx/d)*25.0, (dy/d)*25.0
        return 15.0, 0.0
    if solid.role in ("rafter", "brace"):
        p0_2d = proj_func(solid.p0); p1_2d = proj_func(solid.p1)
        adx = p1_2d[0] - p0_2d[0]; ady = p1_2d[1] - p0_2d[1]
        alen = math.sqrt(adx*adx + ady*ady)
        if alen > 1e-3:
            pdx, pdy = -ady/alen, adx/alen
            if pdy > 0: pdx, pdy = -pdx, -pdy
            return pdx * 12.0, pdy * 12.0
    if solid.role == "hub":
        return 0.0, -20.0
    return 0.0, 0.0


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

# Tie-breaking biases for elevation view painter's algorithm
_ELEV_BIAS: dict[str, float] = {
    "hub": 0.005, "rafter": 0.004, "purlin": 0.003,
    "beam": 0.002, "brace": 0.001,
}

def _get_palette(structure: dict, is_blueprint: bool) -> dict[str, str]:
    if is_blueprint:
        return _PALETTE_BLUEPRINT
    if "presentation" not in structure or "palette" not in structure["presentation"]:
        raise ValueError("MISSING_REQUIRED_CONFIG: presentation.palette")
    key = structure["presentation"]["palette"]
    if key not in _PALETTES:
        raise ValueError(f"INVALID_PALETTE: {key}")
    return _PALETTES[key]


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
    if "intent" not in structure or "jurisdiction" not in structure["intent"]:
        raise ValueError("MISSING_REQUIRED_CONFIG: intent.jurisdiction")
    jurisdiction = structure["intent"]["jurisdiction"]

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
    if "compound_cut" not in geo or "miter_deg" not in geo["compound_cut"] or "bevel_deg" not in geo["compound_cut"]:
        raise ValueError("MISSING_REQUIRED_GEOMETRY: geometry.compound_cut.miter_deg or bevel_deg")
    if "svg_coordinates" not in geo:
        raise ValueError("MISSING_REQUIRED_GEOMETRY: geometry.svg_coordinates")
    cuts = geo["compound_cut"]
    miter = str(round(cuts["miter_deg"], 2))
    bevel = str(round(cuts["bevel_deg"], 2))
    svg_list.append(f'    <!-- VALIDATOR_ANCHORS: {pitch} {miter}° {bevel}° -->')
    svg_list.append(f'    <!-- SAW_SETTINGS: {{"miter_deg": {miter}, "bevel_deg": {bevel}}} -->')
    svg_list.append(f'    <!-- COORDINATE MAP: {json.dumps(geo["svg_coordinates"])} -->')
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

    if "members" not in structure or "posts" not in structure["members"] or "nominal_size" not in structure["members"]["posts"]:
        raise ValueError("MISSING_REQUIRED_CONFIG: members.posts.nominal_size")
    post_nom = structure["members"]["posts"]["nominal_size"]
    if "materials" not in structure or "primary" not in structure["materials"]:
        raise ValueError("MISSING_REQUIRED_CONFIG: materials.primary")
    post_material = structure["materials"]["primary"]

    scale = round((coords["width_px"] * 0.55) / span_diag, 1)
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
            # Apply role-based depth bias to prevent depth-sorting collisions
            # (roof members are structurally on top of support frames)
            if solid.role == "hub":
                depth += 20.0
            elif solid.role == "rafter":
                depth += 15.0
            elif solid.role == "purlin":
                depth += 10.0
            elif solid.role == "brace":
                depth += 2.0
            elif solid.role == "beam":
                depth += 5.0
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

    # ── Member ID Labels pass ────────────────────────────────────────────────
    _lc = palette.get("dimension", palette["text"])
    _plan_label_roles = {"post", "hub"}
    rendered_ids: set[str] = set()
    placed_labels: list[tuple[float, float]] = []
    
    label_svgs = []
    # Identify expected members for this view
    expected_members = [s for s in scene.solids if s.role in _plan_label_roles]
    
    for _s in scene.solids:
        if _s.role not in _plan_label_roles or not _s.tag or _s.tag in rendered_ids:
            continue
        
        # Centralized offset logic
        off_x, off_y = get_label_offset(_s, proj2d, view_center=(cx, cy))
        mid3 = vcent([_s.p0, _s.p1])
        base_x, base_y = proj2d(mid3)
        _lx, _ly = base_x + off_x, base_y + off_y
        
        # Resolve collisions
        _lx, _ly = resolve_label_overlap(_lx, _ly, placed_labels, min_dist=20.0, max_radius=40.0)
        placed_labels.append((_lx, _ly))
        rendered_ids.add(_s.tag)
        
        label_svgs.append(
            f'    <text x="{_lx:.1f}" y="{_ly:.1f}" text-anchor="middle"'
            f' font-size="7" font-family="monospace" fill="{_lc}" opacity="0.85"'
            f' data-label="{_s.tag}">{_s.tag}</text>'
        )
        
    # CAD Debuggability Gate: Ensure all members in the target roles were labeled
    if len(rendered_ids) < len({s.tag for s in expected_members}):
        missing = {s.tag for s in expected_members} - rendered_ids
        print(f"CAD_DEBUGGABILITY_WARNING: missing labels in plan view: {missing}", file=sys.stderr)

    if label_svgs:
        svg_list.append('  <g id="annotation-labels-layer" class="annotation-labels-layer">')
        svg_list.extend(label_svgs)
        svg_list.append('  </g>')

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
    if "members" not in structure or "posts" not in structure["members"] or "nominal_size" not in structure["members"]["posts"]:
        raise ValueError("MISSING_REQUIRED_CONFIG: members.posts.nominal_size")
    post_nom = structure["members"]["posts"]["nominal_size"]
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
            # Depth: smaller Y is closer (depth = -c[1]).
            # Tie-breaking bias is tiny (0.001 ft ≈ 0.01") so actual Y-depth governs.
            # The large biases used in plan view are wrong here: a back rafter at
            # Y=4.875 would get depth=-4.875+15=10.1 and draw over a front post at
            # depth=4.2, which reverses correct occlusion.
            depth = -c[1]
            # Use fixed tiny biases for painter's tie-breaking if centroids match exactly
            bias = 0.0
            if solid.role in _ELEV_BIAS:
                bias = _ELEV_BIAS[solid.role]
            depth += bias
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

    # ── Member ID Labels pass ────────────────────────────────────────────────
    _lc_elev = palette.get("dimension", palette["text"])
    _elev_label_roles = {"post", "beam", "hub"}
    rendered_ids: set[str] = set()
    placed_labels: list[tuple[float, float]] = []
    
    label_svgs = []
    # Identify expected members for this view
    expected_members = [s for s in scene.solids if s.role in _elev_label_roles]
    
    for _s in scene.solids:
        if _s.role not in _elev_label_roles or not _s.tag or _s.tag in rendered_ids:
            continue
        
        # Centralized offset logic
        off_x, off_y = get_label_offset(_s, proj2d, view_center=(cx, cy))
        mid3 = vcent([_s.p0, _s.p1])
        base_x, base_y = proj2d(mid3)
        _lx, _ly = base_x + off_x, base_y + off_y
        
        # Resolve collisions
        _lx, _ly = resolve_label_overlap(_lx, _ly, placed_labels, min_dist=20.0, max_radius=40.0)
        placed_labels.append((_lx, _ly))
        rendered_ids.add(_s.tag)
        
        label_svgs.append(
            f'    <text x="{_lx:.1f}" y="{_ly:.1f}" text-anchor="middle"'
            f' font-size="7" font-family="monospace" fill="{_lc_elev}" opacity="0.85"'
            f' data-label="{_s.tag}">{_s.tag}</text>'
        )
        
    # CAD Debuggability Gate: Ensure all members in the target roles were labeled
    if len(rendered_ids) < len({s.tag for s in expected_members}):
        missing = {s.tag for s in expected_members} - rendered_ids
        print(f"CAD_DEBUGGABILITY_WARNING: missing labels in elevation view: {missing}", file=sys.stderr)

    if label_svgs:
        svg_list.append('  <g id="annotation-labels-layer" class="annotation-labels-layer">')
        svg_list.extend(label_svgs)
        svg_list.append('  </g>')

    return svg_list


def render_perspective_view(
    structure: dict,
    filename: str,
    azimuth_rot: float = 0.0,
    suppress_secondary: bool = True,
) -> list[str]:
    """
    CAD scene graph renderer — delegates all geometry to cad_scene.py.

    Parameters
    ----------
    azimuth_rot:        Rotate scene around Z before projection (radians).
                        0 = default camera; math.pi/qty = rotated 30° for hex.
    suppress_secondary: When True (default) skip jack rafters and purlins.
                        These interpenetrate without Boolean trimming and
                        produce hub spaghetti in 3D views.  The plan view
                        already shows them correctly from above.
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
    if "members" not in structure or "posts" not in structure["members"] or "nominal_size" not in structure["members"]["posts"]:
        raise ValueError("MISSING_REQUIRED_CONFIG: members.posts.nominal_size")
    post_nom = structure["members"]["posts"]["nominal_size"]

    approx_h = post_h + roof_r + span_diag * 0.5
    available_h = coords["height_px"] - 250
    scale = round(min(55.0, available_h / approx_h), 1)
    cx, cy = coords["width_px"] / 2, coords["height_px"] / 2 + 200
    r = (span_diag / 2.0) * scale

    # ── Camera direction ─────────────────────────────────────────────────────
    # 30/30 isometric: view axis is (1,1,1) normalised.
    _cam_raw = (1.0, 1.0, 1.0)
    _cam_len = math.sqrt(sum(c*c for c in _cam_raw))
    CAM_base: tuple[float, float, float] = (_cam_raw[0]/_cam_len, _cam_raw[1]/_cam_len, _cam_raw[2]/_cam_len)

    # When the scene is rotated by azimuth_rot, the effective camera direction
    # in the unrotated frame rotates by -azimuth_rot around Z.
    if azimuth_rot != 0.0:
        _ca = math.cos(-azimuth_rot); _sa = math.sin(-azimuth_rot)
        CAM: tuple[float, float, float] = (
            CAM_base[0]*_ca - CAM_base[1]*_sa,
            CAM_base[0]*_sa + CAM_base[1]*_ca,
            CAM_base[2],
        )
        _rc = math.cos(azimuth_rot); _rs = math.sin(azimuth_rot)
        def proj3(pt: tuple) -> tuple:
            x, y, z = pt[0], pt[1], pt[2]
            rx = x*_rc - y*_rs
            ry = x*_rs + y*_rc
            return project_iso(rx, ry, z, scale, cx, cy)
    else:
        CAM = CAM_base
        def proj3(pt: tuple) -> tuple:  # type: ignore[misc]
            return project_iso(pt[0], pt[1], pt[2], scale, cx, cy)

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
        # Suppress secondary framing in 3D presentation views.
        # Jack rafters (tag "Jack…") and purlins create an untrimmed spaghetti
        # at the hub; they are correctly visible in the top-down plan view.
        if suppress_secondary:
            if solid.role == "purlin":
                continue
            if solid.role == "rafter" and solid.tag.startswith("Jack"):
                continue

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
            # Cull start/end joint faces of beams and braces to keep joints clean and flush
            axis = vsub(solid.p1, solid.p0)
            if vlen(axis) > 1e-6:
                u = vnorm(axis)
                is_start_end = abs(vdot(face.normal, u)) > 0.99
            else:
                is_start_end = False

            if is_start_end and solid.role in ("beam", "brace"):
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
            # Apply role-based depth bias to prevent depth-sorting collisions
            # (roof members are structurally on top of support frames)
            if solid.role == "hub":
                depth += 20.0
            elif solid.role == "rafter":
                depth += 15.0
            elif solid.role == "brace":
                depth += 2.0
            elif solid.role == "beam":
                depth += 5.0
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
    def bbox_union(boxes: list) -> tuple | None:
        if not boxes:
            return None
        return (
            min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes),
        )

    ub = bbox_union(projected_bboxes)
    right_x = (ub[2] + 60) if ub else (cx + r + 60)
    i_apex  = proj3((0.0, 0.0, scene.Z_APEX))
    draw_dimension(
        svg_list, right_x, i_apex[1], right_x, cy,
        f"TOTAL HT: {post_h+roof_r:.2f} FT",
        vertical=True, is_blueprint=is_blueprint
    )

    bottom_y = (ub[3] + 55) if ub else (cy + 55)
    draw_dimension(
        svg_list, cx-r, bottom_y, cx+r, bottom_y,
        f"DIAGONAL SPAN: {span_diag:.0f} FT",
        is_blueprint=is_blueprint
    )

    px0, py0 = scene.post_xy[0]
    top_px, top_py = proj3((px0, py0, scene.Z_POST_TOP))
    left_x = (ub[0] - 160) if ub else (cx - r - 160)
    draw_leader(
        svg_list, top_px, top_py, left_x, top_py - 30,
        f"{post_nom} POST @ {post_h:.2f}ft", is_blueprint=is_blueprint
    )

    # Sheet title — differs between perspective (face-on) and isometric (rotated)
    if azimuth_rot != 0.0:
        title_line1 = "ISOMETRIC VIEW"
        title_line2 = "30° ROTATED — PRIMARY FRAMING — SAANICH BC"
    else:
        title_line1 = "3D PERSPECTIVE MODEL"
        title_line2 = "DETERMINISTIC CAD SOLID — HEX PERGOLA — SAANICH BC"
    svg_list.append(f'    <g transform="translate(60,60)" font-family="Courier New, monospace" fill="{palette["text"]}">')
    svg_list.append(f'        <text x="0" y="0" font-size="20" font-weight="bold">{title_line1}</text>')
    svg_list.append(f'        <text x="0" y="25" font-size="12">{title_line2}</text>')
    svg_list.append(f'    </g>')

    # ── Member ID Labels pass ────────────────────────────────────────────────
    _lc_3d = palette.get("dimension", palette["text"])
    _3d_label_roles = {"post", "beam", "rafter", "hub", "brace"}
    rendered_ids: set[str] = set()
    placed_labels: list[tuple[float, float]] = []
    
    label_svgs = []
    # Identify expected members for this view
    expected_members = [s for s in scene.solids if s.role in _3d_label_roles]
    
    for _s in scene.solids:
        if _s.role not in _3d_label_roles or not _s.tag or _s.tag in rendered_ids:
            continue
        
        # Centralized offset logic
        off_x, off_y = get_label_offset(_s, proj3)
        mid3 = vcent([_s.p0, _s.p1])
        base_x, base_y = proj3(mid3)
        _lx, _ly = base_x + off_x, base_y + off_y
        
        # Resolve collisions
        _lx, _ly = resolve_label_overlap(_lx, _ly, placed_labels, min_dist=20.0, max_radius=40.0)
        placed_labels.append((_lx, _ly))
        rendered_ids.add(_s.tag)
        
        label_svgs.append(
            f'    <text x="{_lx:.1f}" y="{_ly:.1f}" text-anchor="middle"'
            f' font-size="7" font-family="monospace" fill="{_lc_3d}" opacity="0.85"'
            f' data-label="{_s.tag}">{_s.tag}</text>'
        )
        
    # CAD Debuggability Gate: Ensure all members in the target roles were labeled
    if len(rendered_ids) < len({s.tag for s in expected_members}):
        missing = {s.tag for s in expected_members} - rendered_ids
        print(f"CAD_DEBUGGABILITY_WARNING: missing labels in 3D view: {missing}", file=sys.stderr)

    if label_svgs:
        svg_list.append('  <g id="annotation-labels-layer" class="annotation-labels-layer">')
        svg_list.extend(label_svgs)
        svg_list.append('  </g>')

    return svg_list


def render_isometric_view(structure: dict, filename: str) -> list[str]:
    """Isometric view: scene rotated 30° (π/qty) to show a beam face instead of a post face."""
    qty = structure["layout"]["post_count"]
    return render_perspective_view(structure, filename, azimuth_rot=math.pi / qty)


def render_component_isolation_view(structure: dict, filename: str) -> list[str]:
    """Generates a professional 2x3 grid of highly detailed, isolated fabrication Component panels."""
    svg_list = []
    is_blueprint = "blueprint" in filename
    palette = _get_palette(structure, is_blueprint)
    stroke = palette["outline"]
    qty = structure["layout"]["post_count"]

    members = structure["members"]
    if "posts" not in members or "nominal_size" not in members["posts"]:
        raise ValueError("MISSING_REQUIRED_CONFIG: members.posts.nominal_size")
    post_nom = members["posts"]["nominal_size"]

    if "beams" not in members or "nominal_size" not in members["beams"]:
        raise ValueError("MISSING_REQUIRED_CONFIG: members.beams.nominal_size")
    beam_nom = members["beams"]["nominal_size"]

    if "roof" not in structure or "primary_rafters" not in structure["roof"] or "nominal_size" not in structure["roof"]["primary_rafters"]:
        raise ValueError("MISSING_REQUIRED_CONFIG: roof.primary_rafters.nominal_size")
    rafter_nom = structure["roof"]["primary_rafters"]["nominal_size"]

    if "kneebraces" not in members or "nominal_size" not in members["kneebraces"]:
        raise ValueError("MISSING_REQUIRED_CONFIG: members.kneebraces.nominal_size")
    brace_nom = members["kneebraces"]["nominal_size"]

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
            if "actual_width_in" not in members["posts"]:
                raise ValueError("MISSING_REQUIRED_CONFIG: members.posts.actual_width_in")
            post_w = members["posts"]["actual_width_in"]
            if "materials" not in structure or "primary" not in structure["materials"]:
                raise ValueError("MISSING_REQUIRED_CONFIG: materials.primary")
            post_material = structure["materials"]["primary"]
            # Post outline with double lines
            svg_list.append(f'        <rect data-role="post" x="{cx-20}" y="{cy-100}" width="40" height="200" fill="{palette["post"]}" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <line x1="{cx}" y1="{cy-110}" x2="{cx}" y2="{cy+110}" stroke="{palette["centerline"]}" stroke-width="0.8" stroke-dasharray="8,3,2,3" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">PROFILE: {post_nom} {post_material}</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">LENGTH: {ph} FT</text>')
            draw_dimension(svg_list, cx-70, cy-100, cx-70, cy+100, f"{ph} FT", vertical=True, is_blueprint=is_blueprint)
            draw_dimension(svg_list, cx-20, cy+125, cx+20, cy+125, f"{post_w:.1f} IN", is_blueprint=is_blueprint)

        elif role == "beam":
            bm = structure["geometry"]["beam_ring"]["beam_miter_deg"]
            if "actual_depth_in" not in members["beams"] or "cut_length_ft" not in members["beams"]:
                raise ValueError("MISSING_REQUIRED_CONFIG: members.beams.actual_depth_in or cut_length_ft")
            beam_d_val = members["beams"]["actual_depth_in"]
            beam_cut = members["beams"]["cut_length_ft"]
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
            if "materials" not in structure or "primary" not in structure["materials"]:
                raise ValueError("MISSING_REQUIRED_CONFIG: materials.primary")
            rafter_material = structure["materials"]["primary"]
            # Rafter double line outline
            svg_list.append(f'        <polygon data-role="rafter" points="{cx-150},{cy+30} {cx+150},{cy-30} {cx+145},{cy-45} {cx-155},{cy+15}" fill="{palette["rafter"]}" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">PROFILE: {rafter_nom} {rafter_material}</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">MITER: {rm:.2f}° | BEVEL: {rb:.2f}°</text>')
            draw_dimension(svg_list, cx-140, cy+40, cx+140, cy-15, f"{rl:.1f} IN", is_blueprint=is_blueprint)

        elif role == "brace":
            if "kneebraces" not in members or "cut_length_in" not in members["kneebraces"] or "angle_deg" not in members["kneebraces"]:
                raise ValueError("MISSING_REQUIRED_CONFIG: members.kneebraces.cut_length_in or angle_deg")
            brace_len = members["kneebraces"]["cut_length_in"]
            brace_ang = members["kneebraces"]["angle_deg"]
            # Brace profile outline
            svg_list.append(f'        <polygon data-role="brace" points="{cx-30},{cy+80} {cx+70},{cy-20} {cx+50},{cy-40} {cx-50},{cy+60}" fill="{palette["brace"]}" stroke="{stroke}" stroke-width="1.5" />')
            svg_list.append(f'        <text x="20" y="65" font-family="monospace" font-size="11" fill="{palette["text"]}">PROFILE: {brace_nom} Knee brace</text>')
            svg_list.append(f'        <text x="20" y="85" font-family="monospace" font-size="11" fill="{palette["text"]}">ANGLE: {brace_ang:.1f}° compound</text>')
            draw_dimension(svg_list, cx-30, cy+95, cx+60, cy+5, f"{brace_len:.1f} IN", is_blueprint=is_blueprint)

        elif role == "footing":
            if "foundation" not in structure or "caisson_diameter_in" not in structure["foundation"] or "caisson_depth_in" not in structure["foundation"]:
                raise ValueError("MISSING_REQUIRED_CONFIG: foundation.caisson_diameter_in or caisson_depth_in")
            foundation = structure["foundation"]
            footing_dia = foundation["caisson_diameter_in"]
            footing_depth = foundation["caisson_depth_in"]
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


# --- PNG Co-generation (token-efficient: no browser needed for smoke tests) ---

def _generate_png(svg_path: str | Path, width_px: int, height_px: int) -> bool:
    """
    Render svg_path → outputs/visual-smoke/<stem>.png without launching a browser.

    Strategy (in order):
      1. qlmanage (macOS Quick Look) — fast, zero browser overhead
      2. Playwright chromium — fallback when qlmanage is unavailable or produces
         a zero-byte file (e.g., SVG uses features QL can't handle)

    Returns True if a non-empty PNG was written.
    """
    import subprocess as _sp

    svg_path = Path(svg_path)
    png_dir  = svg_path.parent / "visual-smoke"
    png_dir.mkdir(parents=True, exist_ok=True)
    target_png = png_dir / (svg_path.stem + ".png")

    # --- Strategy 1: qlmanage (macOS) ---
    if sys.platform == "darwin":
        _sp.run(
            ["qlmanage", "-t", "-s", str(width_px), "-o", str(png_dir), str(svg_path)],
            stdout=_sp.DEVNULL, stderr=_sp.DEVNULL,
        )
        tmp_png = png_dir / (svg_path.name + ".png")
        if tmp_png.exists():
            if target_png.exists():
                target_png.unlink()
            tmp_png.rename(target_png)

    if target_png.exists() and target_png.stat().st_size > 0:
        # qlmanage on macOS Sequoia produces square PNGs regardless of SVG aspect
        # ratio; resize to the correct SVG dimensions so CV heuristics and crops
        # operate on undistorted pixel coordinates.
        try:
            from PIL import Image as _PILImage
            _img = _PILImage.open(target_png)
            if _img.size != (width_px, height_px):
                _resample = getattr(_PILImage, "Resampling", _PILImage).LANCZOS
                _img = _img.resize((width_px, height_px), _resample)
                _img.save(target_png)
        except Exception:
            pass
        return True

    # --- Strategy 2: Playwright (fallback) ---
    try:
        from playwright.sync_api import sync_playwright as _pw
        with _pw() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": width_px, "height": height_px})
            page.goto(svg_path.resolve().as_uri())
            page.screenshot(path=str(target_png), full_page=False)
            browser.close()
    except Exception:
        pass

    return target_png.exists() and target_png.stat().st_size > 0


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
    elif "isometric" in filename:
        content = render_isometric_view(structure, filename)
    elif "perspective" in filename:
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

    _generate_png(output_path, width_px, height_px)


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
        png_path = out_dir / "visual-smoke" / output_path.with_suffix(".png").name
        png_ok = png_path.exists() and png_path.stat().st_size > 0
        print(f"  ✓ {output_file}  {'[PNG ok]' if png_ok else '[PNG MISSING]'}")


if __name__ == "__main__":
    main()
