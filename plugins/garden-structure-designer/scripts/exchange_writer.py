#!/usr/bin/env python3
"""
exchange_writer.py
==================

Purpose:
    Defines the ``ExchangeWriter`` port (Protocol) for CAD exchange-file writers
    and the writer-independent contract shared by every adapter: layer table,
    XDATA stamping, per-sheet geometry rules and result metadata.

Layer: Core (port)

Contract (C4 normative):
    - Layers: FRAMING_POSTS(1) FRAMING_BEAMS(3) FRAMING_RAFTERS(4) FRAMING_HUBS(6)
      FRAMING_BRACES(5) FOOTINGS_PIERS(8) DIMENSIONS_ARCH(2)
    - XDATA (APPID ``GSD``) on every member entity: MEMBER_ID, ROLE, REVISION_ID,
      REVISION_HASH, SHEET_ID (as ``KEY=value`` strings).
    - SB01: full-scale 3D WCS wireframe, millimetres. SB02: XY plan projection (Z=0).
    - Output units are millimetres ($INSUNITS=4); ``structure.json`` feet are converted.

Key Input Dependencies:
    structure["geometry"]["joints"]["resolved_model"]["members"] (id, role, vertices,
    p0, p1) and structure["geometry"]["joints"]["units"].

Key Functions:
    build_draw_entities(structure, sheet_id) -> list[DrawEntity]
    xdata_strings(entity, sheet_id, revision_id, revision_hash) -> list[str]
    sha256_of_file(path) -> str
    build_metadata(sheet_id, output_path, writer, entities_count) -> dict
    ExchangeWriter.export_sheet(...)  (Protocol)

Script Dependencies:
    Standard library only.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

APPID = "GSD"
INSUNITS_MM = 4
SHEET_IDS = ("SB01", "SB02")
MM_PER_UNIT = {"feet": 304.8, "ft": 304.8, "mm": 1.0}

# layer name -> AutoCAD color index
LAYER_COLORS: dict[str, int] = {
    "FRAMING_POSTS": 1,
    "FRAMING_BEAMS": 3,
    "FRAMING_RAFTERS": 4,
    "FRAMING_HUBS": 6,
    "FRAMING_BRACES": 5,
    "FOOTINGS_PIERS": 8,
    "DIMENSIONS_ARCH": 2,
}
ROLE_LAYERS: dict[str, str] = {
    "post": "FRAMING_POSTS",
    "beam": "FRAMING_BEAMS",
    "rafter": "FRAMING_RAFTERS",
    "hub": "FRAMING_HUBS",
    "brace": "FRAMING_BRACES",
    "footing": "FOOTINGS_PIERS",
}
DIMENSION_LAYER = "DIMENSIONS_ARCH"
DIM_OFFSET_MM = 600.0
DIM_TEXT_HEIGHT_MM = 150.0

Point = tuple[float, float, float]


class ExchangeWriter(Protocol):
    """Port: writes one drawing sheet of a structure to an exchange file."""

    def export_sheet(
        self,
        sheet_id: str,
        structure: dict,
        output_path: Path,
        *,
        revision_id: str,
        revision_hash: str,
    ) -> dict: ...


@dataclass(frozen=True)
class DrawEntity:
    """Writer-neutral drawing primitive: a 3D polyline or a text label."""

    layer: str
    points: tuple[Point, ...]
    member_id: str | None = None
    role: str | None = None
    text: str | None = None
    text_height: float = DIM_TEXT_HEIGHT_MM


def _unit_scale(structure: dict) -> float:
    """Return the mm-per-unit factor declared by the resolved geometry."""
    units = structure["geometry"]["joints"]["units"]
    if units not in MM_PER_UNIT:
        raise ValueError(f"Unsupported structure units: {units!r}")
    return MM_PER_UNIT[units]


def _project(sheet_id: str, point: Point) -> Point:
    """Apply the per-sheet projection rule (SB02 flattens Z to 0)."""
    return (point[0], point[1], 0.0) if sheet_id == "SB02" else point


def _wireframe_path(vertices: list[Point]) -> list[Point]:
    """Trace every edge of a prism (two equal vertex rings) as one polyline."""
    n = len(vertices) // 2
    bottom, top = vertices[:n], vertices[n:]
    path = bottom + [bottom[0], top[0]]
    for i in range(1, n):
        path += [top[i], bottom[i], top[i]]
    path.append(top[0])
    return path


def _member_path(member: dict, scale: float) -> list[Point]:
    """Return the scaled wireframe path of a member (centerline if not a prism)."""
    vertices = [tuple(c * scale for c in v) for v in member.get("vertices", [])]
    if len(vertices) >= 6 and len(vertices) % 2 == 0:
        return _wireframe_path(vertices)
    return [tuple(c * scale for c in member[key]) for key in ("p0", "p1")]


def _format_feet_inches(mm: float) -> str:
    """Format millimetres as feet-inches, e.g. ``18'-0"``."""
    inches = round(mm / 25.4 * 16) / 16
    feet, rest = divmod(inches, 12)
    return f"{int(feet)}'-{rest:g}\""


def _dimension_entities(posts: list[dict], scale: float) -> list[DrawEntity]:
    """Build overall length/width dimension lines from the post extents."""
    xs = [p["p0"][0] * scale for p in posts]
    ys = [p["p0"][1] * scale for p in posts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    yd, xd = y0 - DIM_OFFSET_MM, x1 + DIM_OFFSET_MM
    spans = [
        ((x0, yd, 0.0), (x1, yd, 0.0), x1 - x0),
        ((xd, y0, 0.0), (xd, y1, 0.0), y1 - y0),
    ]
    entities: list[DrawEntity] = []
    for start, end, length in spans:
        mid = tuple((a + b) / 2 for a, b in zip(start, end))
        entities.append(DrawEntity(DIMENSION_LAYER, (start, end)))
        entities.append(DrawEntity(DIMENSION_LAYER, (mid,), text=_format_feet_inches(length)))
    return entities


def build_draw_entities(structure: dict, sheet_id: str) -> list[DrawEntity]:
    """Map the resolved members of ``structure`` to draw entities for one sheet."""
    if sheet_id not in SHEET_IDS:
        raise ValueError(f"Unknown sheet_id {sheet_id!r}; expected one of {SHEET_IDS}")
    scale = _unit_scale(structure)
    members = structure["geometry"]["joints"]["resolved_model"]["members"]
    entities: list[DrawEntity] = []
    for member in members:
        role = member["role"]
        if role not in ROLE_LAYERS:
            raise ValueError(f"Member {member['id']} has unmapped role {role!r}")
        path = tuple(_project(sheet_id, p) for p in _member_path(member, scale))
        entities.append(DrawEntity(ROLE_LAYERS[role], path, member["id"], role))
    posts = [m for m in members if m["role"] == "post"]
    if posts:
        entities += [
            DrawEntity(e.layer, tuple(_project(sheet_id, p) for p in e.points), text=e.text)
            for e in _dimension_entities(posts, scale)
        ]
    return entities


def xdata_strings(entity: DrawEntity, sheet_id: str, revision_id: str, revision_hash: str) -> list[str]:
    """Return the ``KEY=value`` XDATA strings for a member entity."""
    return [
        f"MEMBER_ID={entity.member_id}",
        f"ROLE={entity.role}",
        f"REVISION_ID={revision_id}",
        f"REVISION_HASH={revision_hash}",
        f"SHEET_ID={sheet_id}",
    ]


def sha256_of_file(path: Path) -> str:
    """Return the hex SHA-256 digest of a file."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_metadata(sheet_id: str, output_path: Path, writer: str, entities_count: int) -> dict:
    """Return the standard export_sheet result metadata."""
    return {
        "sheet_id": sheet_id,
        "output_path": str(output_path),
        "sha256": sha256_of_file(output_path),
        "writer": writer,
        "entities_count": entities_count,
    }
