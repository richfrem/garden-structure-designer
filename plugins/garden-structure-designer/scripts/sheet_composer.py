#!/usr/bin/env python3
"""
sheet_composer.py
=================

Purpose:
    Unified sheet composer assembling both vector blueprint sheets (OpenCASCADE HLR)
    and shaded presentation sheets (Three.js WebGL renders). Overlays semantic midpoint
    labels, dimension leaders, title block, and validator anchors.

Layer: Presentation / Sheet Composition
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from cad_camera import CameraSpec, SheetTransform, project_anchor, project_world, to_sheet
from cad_projection_hlr import HLRProjectionResult, deduplicate_coincident_edges
from cad_render_contracts import SolidAssembly
from constants import (
    LW_TITLE_BORDER,
    LW_TITLE_RULE,
    LW_LEADER,
    LW_DIMENSION,
    LW_MEMBER_DRAWING,
    LW_MEMBER_BLUEPRINT,
)


@dataclass(frozen=True)
class SheetSpec:
    sheet_id: str
    dwg_name: str
    is_blueprint: bool = False
    width_px: int = 1600
    height_px: int = 1200


def _draw_title_block(
    dwg_name: str,
    structure: dict,
    width_px: int,
    height_px: int,
    is_blueprint: bool,
) -> str:
    title_w = 340
    title_h = 140
    x = width_px - title_w - 20
    y = height_px - title_h - 20

    meta = structure.get("meta", {})
    sh = meta.get("source_hash", "UNSTAMPED")[:8]
    rev = meta.get("revision_id", "UNSTAMPED")[:8]
    st = structure.get("structure", {}).get("type", "STRUCTURE").upper()
    jur = structure.get("intent", {}).get("jurisdiction", "BC")

    border = "#00ffff" if is_blueprint else "#2b2d42"
    bg = "#12253a" if is_blueprint else "#ffffff"
    tc = "#00ffff" if is_blueprint else "#1d3557"

    return f"""
    <g data-role="title-block" transform="translate({x}, {y})">
        <rect width="{title_w}" height="{title_h}" fill="{bg}" stroke="{border}" stroke-width="{LW_TITLE_BORDER}" />
        <line x1="0" y1="40" x2="{title_w}" y2="40" stroke="{border}" stroke-width="{LW_TITLE_RULE}" />
        <text x="15" y="28" font-family="monospace" font-size="18" font-weight="bold" fill="{tc}">{dwg_name.upper()}</text>
        <text x="15" y="60" font-family="monospace" font-size="11" fill="{tc}">STRUCTURE: {st}</text>
        <text x="15" y="80" font-family="monospace" font-size="11" fill="{tc}">JURISDICTION: {jur}</text>
        <text x="15" y="100" font-family="monospace" font-size="11" fill="{tc}">SOURCE HASH: {sh}</text>
        <text x="15" y="120" font-family="monospace" font-size="11" fill="{tc}">REVISION: {rev} | SCALE: AUTO</text>
    </g>
    """


def _draw_validator_anchors(structure: dict) -> str:
    geo = structure.get("geometry", {})
    pitch = structure.get("roof", {}).get("pitch", "2/12")
    cuts = geo.get("compound_cut", {})
    miter = str(round(cuts.get("miter_deg", 0.0), 2))
    bevel = str(round(cuts.get("bevel_deg", 0.0), 2))
    svg_coords = geo.get("svg_coordinates", {})
    return f"""
    <!-- VALIDATOR_ANCHORS: {pitch} {miter}° {bevel}° -->
    <!-- SAW_SETTINGS: {{"miter_deg": {miter}, "bevel_deg": {bevel}}} -->
    <!-- COORDINATE MAP: {json.dumps(svg_coords)} -->
    <g style="visibility:hidden; display:none;"><text>{pitch}</text><text>{miter}</text><text>{bevel}</text></g>
    """


def _draw_dimensions(
    assembly: SolidAssembly,
    camera: CameraSpec,
    sheet_tf: SheetTransform,
    is_blueprint: bool,
) -> List[str]:
    """Draws overall X/Y/Z extent dimensions from assembly bounds, projected via the shared camera."""
    (lo, hi) = assembly.bounds_mm
    color = "#00e5ff" if is_blueprint else "#3d5a80"
    parts: List[str] = []
    for axis, name in enumerate(("X", "Y", "Z")):
        end = list(lo)
        end[axis] = hi[axis]
        p0 = project_world(lo, camera)
        p1 = project_world(tuple(end), camera)
        (x0, y0) = to_sheet((p0[0], p0[1]), sheet_tf)
        (x1, y1) = to_sheet((p1[0], p1[1]), sheet_tf)
        if math.hypot(x1 - x0, y1 - y0) < 20.0:
            continue  # axis is edge-on in this view
        extent_mm = hi[axis] - lo[axis]
        label = f"{name}: {extent_mm:.0f} MM ({extent_mm / 304.8:.2f} FT)"
        parts.append(
            f'  <g data-role="dimension" data-tag="sheet:dim-{name}">'
            f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{color}" stroke-width="{LW_DIMENSION}" />'
            f'<text x="{(x0 + x1) / 2:.1f}" y="{(y0 + y1) / 2 - 8:.1f}" text-anchor="middle" '
            f'font-family="monospace" font-size="13" font-weight="bold" fill="{color}">{label}</text></g>'
        )
    return parts


def compose_sheet(
    assembly: SolidAssembly,
    camera: CameraSpec,
    sheet_spec: SheetSpec,
    background: Union[HLRProjectionResult, Path],
    structure: dict,
) -> str:
    """
    Composes a complete semantic SVG sheet:
    1. Background (vector paths from HLR or embedded PNG from WebGL)
    2. Midpoint labels near member anchors
    3. Title block and metadata anchors
    """
    w = sheet_spec.width_px
    h = sheet_spec.height_px
    bg_color = "#0a192f" if sheet_spec.is_blueprint else "#ffffff"

    # Compute bounding viewport scale
    (min_b, max_b) = assembly.bounds_mm
    dx = max_b[0] - min_b[0]
    dy = max_b[1] - min_b[1]
    dz = max_b[2] - min_b[2]
    span = max(dx, dy, dz)

    # Reserve margins (leave 360px for title block on right/bottom)
    view_w = w - 100
    view_h = h - 100
    scale = min(view_w, view_h) / (span * 1.5)

    sheet_tf = SheetTransform(
        viewport_x=50.0,
        viewport_y=50.0,
        viewport_w=float(view_w),
        viewport_h=float(view_h),
        center_x=0.0,
        center_y=0.0,
        scale=scale,
    )

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
        f'  <rect width="100%" height="100%" fill="{bg_color}" />',
    ]

    # --- Background ---
    if isinstance(background, Path):
        # Raster presentation PNG
        png_bytes = background.read_bytes()
        b64_data = base64.b64encode(png_bytes).decode("ascii")
        svg_parts.append(
            f'  <image x="0" y="0" width="{w}" height="{h}" href="data:image/png;base64,{b64_data}" data-role="presentation-canvas" />'
        )
    elif isinstance(background, HLRProjectionResult):
        # Vector HLR
        stroke_color = "#00e5ff" if sheet_spec.is_blueprint else "#2b2d42"
        stroke_w = LW_MEMBER_BLUEPRINT if sheet_spec.is_blueprint else LW_MEMBER_DRAWING

        # Gather all visible edges and deduplicate coincident ones
        all_vis_edges = []
        for m_res in background.members.values():
            all_vis_edges.extend(m_res.visible_edges)

        deduped = deduplicate_coincident_edges(all_vis_edges, tol_mm=0.05)

        for edge in deduped:
            path_d = edge.to_svg_path(sheet_tf)
            svg_parts.append(
                f'  <path data-projection="hlr" data-role="{edge.role}" data-id="{edge.member_id}" data-tag="{edge.member_id}" data-visibility="visible" '
                f'd="{path_d}" stroke="{stroke_color}" stroke-width="{stroke_w}" fill="none" stroke-linecap="round" stroke-linejoin="round" />'
            )

    svg_parts.extend(_draw_dimensions(assembly, camera, sheet_tf, sheet_spec.is_blueprint))

    # --- Midpoint Labels ---
    label_color = "#00ffff" if sheet_spec.is_blueprint else "#1d3557"
    for member in assembly.members:
        if not member.anchors:
            continue
        mid_anchor = member.anchors[0]
        # Project 3D anchor to 2D sheet coordinates
        sheet_pt = project_anchor(mid_anchor, camera, sheet_tf)

        # Emit visible label
        svg_parts.append(
            f'  <g data-role="{member.role}" data-id="{member.member_id}" data-tag="{member.member_id}" data-label="{member.member_id}" data-member-role="{member.role}">'
            f'    <text data-role="label" x="{sheet_pt[0]:.1f}" y="{sheet_pt[1]:.1f}" font-family="monospace" font-size="12" '
            f'font-weight="bold" fill="{label_color}" text-anchor="middle" dominant-baseline="central">{member.member_id}</text>'
            f'  </g>'
        )

    # --- Title Block ---
    svg_parts.append(_draw_title_block(sheet_spec.dwg_name, structure, w, h, sheet_spec.is_blueprint))

    # --- Validator Anchors ---
    svg_parts.append(_draw_validator_anchors(structure))

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)
