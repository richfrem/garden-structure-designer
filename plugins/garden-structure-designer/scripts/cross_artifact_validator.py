#!/usr/bin/env python3
"""
cross_artifact_validator.py
===========================

Purpose:
    Cross-checks outputs across markdown docs, SVG blueprints, and CAD DXF deliverables.
    Verifies miter and bevel angle consistency, SAW_SETTINGS tags, parsed DXF layer
    registrations, GSD APPID XDATA stamping, member bounding box parity, and dimension
    cross-checks between SVG text and DXF entities.

Layer: Execution / QA Cross-Artifact Gate

Key Input Dependencies:
    - context/staging/structure.json
    - outputs/**/*.md and outputs/**/*.svg
    - outputs/cad/SB01-structure.dxf and outputs/cad/SB02-plan.dxf

Key Functions:
    check_paths(file_path: str, content: str) -> list[str]
    check_miter_consistency(...) -> list[str]
    check_saw_settings(...) -> list[str]
    validate(staging_dir: str, outputs_dir: str) -> list[str]
    validate_dxf_artifacts(staging_dir: str, outputs_dir: str) -> list[str]
    validate_dimension_crosscheck(...) -> list[str]

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/cross_artifact_validator.py [staging_dir] [outputs_dir]
"""
from __future__ import annotations

import glob
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.append(str(Path(__file__).parent.resolve()))
from constants import (
    APPID,
    CAD_SUBDIR,
    DIM_CROSSCHECK_TOL_MM,
    DIMENSION_LAYER,
    DXF_BOUNDS_TOL_MM,
    DXF_PLANAR_TOL_MM,
    INCHES_PER_FOOT,
    LAYER_COLORS,
    MM_PER_FOOT,
    MM_PER_INCH,
    MM_PER_UNIT,
    ROLE_LAYERS,
    SHEET_FILENAMES,
    SHEET_ID_PLAN,
    SHEET_ID_STRUCTURE,
)
from path_utils import outputs_dir, staging_dir

Bounds = Tuple[Tuple[float, float, float], Tuple[float, float, float]]

PLAN_SVG = "drawing-plan-view.svg"
ELEVATION_SVG = "drawing-elevation-view.svg"
MAX_SPAN_PATTERN = re.compile(r"MAX SPAN:\s*([\d.]+)\s*FT")
POST_HEIGHT_PATTERN = re.compile(r"POST:\s*([\d.]+)\s*FT")
FEET_INCHES_PATTERN = re.compile(r"^(\d+)'-([\d.]+)\"$")


def check_paths(file_path: str, content: str) -> List[str]:
    """Catches common relative path typos (e.g. output/ instead of outputs/)."""
    errors = []
    if "output/" in content and "outputs/" not in content:
        errors.append(f"{file_path}: Found 'output/' path instead of 'outputs/'")
    return errors


def check_miter_consistency(
    fpath: str,
    content: str,
    miter: str,
    beam_miter: str,
) -> List[str]:
    """Ensures beam descriptions do not accidentally use rafter miter angles."""
    errors = []
    if miter != "0" and beam_miter != "0" and miter != beam_miter and "beam" in content.lower():
        beam_miter_matches = re.finditer(r"(?i)beam.{0,30}?miter.{0,10}?(\d+\.?\d*)", content)
        for match in beam_miter_matches:
            found_miter = match.group(1)
            if found_miter == miter and found_miter != beam_miter:
                errors.append(f"{fpath}: Beam miter incorrectly uses rafter miter ({miter}) instead of beam miter ({beam_miter}).")
    return errors


def check_saw_settings(
    fpath: str,
    content: str,
    miter: str,
    bevel: str,
) -> List[str]:
    """Verifies that SAW_SETTINGS embedded HTML comment metadata matches calculated geometry."""
    errors = []
    saw_match = re.search(r"<!--\s*SAW_SETTINGS:\s*({.*?})\s*-->", content, re.DOTALL)
    if saw_match:
        try:
            saw_settings = json.loads(saw_match.group(1))
            if str(saw_settings.get("miter_deg") or "") != miter:
                errors.append(f"{fpath}: SAW_SETTINGS miter mismatch.")
            if str(saw_settings.get("bevel_deg") or "") != bevel:
                errors.append(f"{fpath}: SAW_SETTINGS bevel mismatch.")
        except json.JSONDecodeError:
            errors.append(f"{fpath}: Invalid SAW_SETTINGS JSON.")
    return errors


def validate(staging_dir_path: str, outputs_dir_path: str) -> List[str]:
    """Validates output markdown and SVG files for correct paths, miters, and saw settings."""
    errors: List[str] = []
    model_path = os.path.join(staging_dir_path, "structure.json")
    if not os.path.exists(model_path):
        return ["MISSING_STRUCTURE: structure.json not found."]

    with open(model_path, encoding="utf-8") as f:
        model = json.load(f)
    calcs = model.get("geometry", {})

    miter = str(round(calcs.get("compound_cut", {}).get("miter_deg") or 0, 2))
    bevel = str(round(calcs.get("compound_cut", {}).get("bevel_deg") or 0, 2))
    beam_miter = str(round((calcs.get("beam_ring") or {}).get("beam_miter_deg") or 0, 2))

    files = glob.glob(os.path.join(outputs_dir_path, "**", "*.md"), recursive=True) + glob.glob(
        os.path.join(outputs_dir_path, "**", "*.svg"), recursive=True
    )

    for fpath in files:
        with open(fpath, encoding="utf-8") as f:
            content = f.read()

        errors.extend(check_paths(fpath, content))
        errors.extend(check_miter_consistency(fpath, content, miter, beam_miter))
        errors.extend(check_saw_settings(fpath, content, miter, bevel))

    return errors


def _entity_points(entity: Any) -> List[Tuple[float, float, float]]:
    """Returns the WCS points of a POLYLINE or TEXT entity."""
    if entity.dxftype() == "POLYLINE":
        return [tuple(p) for p in entity.points()]
    return [tuple(entity.dxf.insert)]


def _bounds(points: List[Tuple[float, float, float]]) -> Bounds:
    """Computes minimum and maximum 3D axis-aligned bounding box coordinates."""
    cols = list(zip(*points))
    return tuple(min(c) for c in cols), tuple(max(c) for c in cols)


def _member_xdata(entity: Any) -> Dict[str, str]:
    """Extracts GSD key-value XDATA tags attached to an entity."""
    return dict(tag.value.split("=", 1) for tag in entity.get_xdata(APPID) if "=" in tag.value)


def _resolved_members(model: dict) -> Tuple[List[dict], float]:
    """Returns resolved members list and mm-per-unit scale factor."""
    joints = model.get("geometry", {}).get("joints", {})
    members = joints.get("resolved_model", {}).get("members", [])
    return members, MM_PER_UNIT.get(joints.get("units"), MM_PER_FOOT)


def _expected_member_bounds(member: dict, scale: float) -> Bounds:
    """Calculates expected bounds of a member in WCS mm."""
    points = member.get("vertices") or [member["p0"], member["p1"]]
    return _bounds([tuple(c * scale for c in p) for p in points])


def _max_delta(a: Bounds, b: Bounds) -> float:
    """Calculates maximum absolute coordinate deviation between two bounding boxes."""
    return max(abs(x - y) for lo_hi_a, lo_hi_b in zip(a, b) for x, y in zip(lo_hi_a, lo_hi_b))


def _group_members(label: str, doc: Any, errors: List[str]) -> Dict[str, List[Any]]:
    """Groups GSD-stamped entities by MEMBER_ID, reporting untagged entities."""
    grouped: Dict[str, List[Any]] = {}
    for entity in doc.modelspace():
        if not entity.has_xdata(APPID):
            continue
        member_id = _member_xdata(entity).get("MEMBER_ID")
        if member_id:
            grouped.setdefault(member_id, []).append(entity)
        else:
            errors.append(f"{label}: GSD XDATA entity without MEMBER_ID.")
    return grouped


def _check_dxf_document(
    label: str,
    sheet_id: str,
    doc: Any,
    members: List[dict],
    scale: float,
    errors: List[str],
) -> Dict[str, List[Any]]:
    """Audit, registry, layer, XDATA-parity and sheet-geometry checks for one DXF."""
    auditor = doc.audit()
    if auditor.has_errors:
        errors.extend(f"{label}: DXF audit error: {err.message}" for err in auditor.errors)
    if APPID not in doc.appids:
        errors.append(f"{label}: APPID {APPID} is not registered.")
    layer_names = {layer.dxf.name for layer in doc.layers}
    errors.extend(f"{label}: missing layer {name}." for name in LAYER_COLORS if name not in layer_names)

    grouped = _group_members(label, doc, errors)
    expected = {m["id"]: m for m in members}
    errors.extend(f"{label}: member {mid} missing from DXF XDATA." for mid in expected if mid not in grouped)
    errors.extend(f"{label}: unexpected member {mid} in DXF XDATA." for mid in grouped if mid not in expected)
    errors.extend(f"{label}: duplicate MEMBER_ID {mid} ({len(ents)} entities)." for mid, ents in grouped.items() if len(ents) > 1)

    for mid, entities in grouped.items():
        member = expected.get(mid)
        if member is None:
            continue
        for entity in entities:
            data = _member_xdata(entity)
            if data.get("SHEET_ID") != sheet_id:
                errors.append(f"{label}: member {mid} SHEET_ID is {data.get('SHEET_ID')!r}, expected {sheet_id}.")
            if data.get("ROLE") != member["role"]:
                errors.append(f"{label}: member {mid} ROLE is {data.get('ROLE')!r}, expected {member['role']!r}.")
            if entity.dxf.layer != ROLE_LAYERS.get(member["role"]):
                errors.append(f"{label}: member {mid} on layer {entity.dxf.layer}, expected {ROLE_LAYERS.get(member['role'])}.")

    if sheet_id == SHEET_ID_STRUCTURE:
        _check_structure_bounds(label, grouped, expected, scale, errors)
    else:
        _check_planar(label, doc, errors)
    return grouped


def _check_structure_bounds(
    label: str,
    grouped: Dict[str, List[Any]],
    expected: Dict[str, dict],
    scale: float,
    errors: List[str],
) -> None:
    """SB01: per-member 3D bounds match the resolved model; superstructure sits above Z=0."""
    for mid, entities in grouped.items():
        member = expected.get(mid)
        if member is None or len(entities) != 1:
            continue
        actual = _bounds(_entity_points(entities[0]))
        want = _expected_member_bounds(member, scale)
        delta = _max_delta(actual, want)
        if delta > DXF_BOUNDS_TOL_MM:
            errors.append(f"{label}: member {mid} bounds differ from resolved model by {delta:.3f} mm.")
        if member["role"] != "footing" and actual[1][2] <= 0:
            errors.append(f"{label}: superstructure member {mid} has Z <= 0 (max Z {actual[1][2]:.3f} mm).")


def _check_planar(label: str, doc: Any, errors: List[str]) -> None:
    """SB02: every entity lies in the Z = 0 plane."""
    for entity in doc.modelspace():
        off_plane = [p for p in _entity_points(entity) if abs(p[2]) > DXF_PLANAR_TOL_MM]
        if off_plane:
            errors.append(f"{label}: {entity.dxftype()} on layer {entity.dxf.layer} has non-planar Z={off_plane[0][2]}.")


def _parse_feet_inches(text: str) -> Optional[float]:
    """Parse ``18'-0"`` / ``12'-4.5"`` into millimetres."""
    match = FEET_INCHES_PATTERN.match(text)
    if not match:
        return None
    return (int(match.group(1)) * INCHES_PER_FOOT + float(match.group(2))) * MM_PER_INCH


def _post_extents_mm(grouped: Dict[str, List[Any]], expected: Dict[str, dict]) -> Optional[Tuple[float, float, float]]:
    """Return (x, y) post-centerline extents and max post height in mm."""
    post_bounds = [_bounds(_entity_points(e)) for mid, ents in grouped.items() if expected.get(mid, {}).get("role") == "post" for e in ents]
    if not post_bounds:
        return None
    centers = [tuple((lo + hi) / 2 for lo, hi in zip(*b)) for b in post_bounds]
    xs, ys = [c[0] for c in centers], [c[1] for c in centers]
    return max(xs) - min(xs), max(ys) - min(ys), max(b[1][2] - b[0][2] for b in post_bounds)


def _svg_value_mm(svg_path: str, pattern: re.Pattern) -> Optional[float]:
    """Return feet value matched by pattern in an SVG in mm."""
    if not os.path.exists(svg_path):
        return None
    with open(svg_path, encoding="utf-8") as f:
        match = pattern.search(f.read())
    return float(match.group(1)) * MM_PER_FOOT if match else None


def validate_dimension_crosscheck(
    outputs_dir_path: str,
    sb01_grouped: Dict[str, List[Any]],
    sb02_doc: Any,
    expected: Dict[str, dict],
) -> List[str]:
    """Numerically cross-check SVG dimension labels and DXF dimension text against DXF geometry."""
    errors: List[str] = []
    extents = _post_extents_mm(sb01_grouped, expected)
    if extents is None:
        return errors
    x_extent, y_extent, post_height = extents

    span = _svg_value_mm(os.path.join(outputs_dir_path, PLAN_SVG), MAX_SPAN_PATTERN)
    max_post_extent = max(x_extent, y_extent)
    max_bound = max_post_extent / math.cos(math.pi / 10) + DIM_CROSSCHECK_TOL_MM if max_post_extent > 0 else DIM_CROSSCHECK_TOL_MM
    if span is not None and not (min(x_extent, y_extent) - DIM_CROSSCHECK_TOL_MM <= span <= max_bound):
        errors.append(f"{PLAN_SVG}: MAX SPAN {span:.1f} mm outside DXF post centerline footprint [{min(x_extent, y_extent):.1f}, {max_bound:.1f}] mm.")

    height = _svg_value_mm(os.path.join(outputs_dir_path, ELEVATION_SVG), POST_HEIGHT_PATTERN)
    if height is not None and abs(height - post_height) > DIM_CROSSCHECK_TOL_MM:
        errors.append(f"{ELEVATION_SVG}: POST height {height:.1f} mm differs from DXF post height {post_height:.1f} mm.")

    dim_values = [_parse_feet_inches(e.dxf.text) for e in sb02_doc.modelspace().query("TEXT") if e.dxf.layer == DIMENSION_LAYER]
    allowed = (x_extent, y_extent)
    for text_mm in dim_values:
        if text_mm is None or not any(abs(text_mm - a) <= DIM_CROSSCHECK_TOL_MM for a in allowed):
            errors.append(f"{SHEET_FILENAMES[SHEET_ID_PLAN]}: dimension text {text_mm} mm matches no DXF post extent {allowed}.")
    return errors


def validate_dxf_artifacts(staging_dir_path: str, outputs_dir_path: str) -> List[str]:
    """Validate parsed SB01/SB02 DXF files against structure.json and SVG sheets."""
    import ezdxf

    model_path = os.path.join(staging_dir_path, "structure.json")
    if not os.path.exists(model_path):
        return ["MISSING_STRUCTURE: structure.json not found."]
    with open(model_path, encoding="utf-8") as f:
        model = json.load(f)
    members, scale = _resolved_members(model)
    expected = {m["id"]: m for m in members}

    errors: List[str] = []
    docs, grouped_by_sheet = {}, {}
    for sheet_id in (SHEET_ID_STRUCTURE, SHEET_ID_PLAN):
        path = os.path.join(outputs_dir_path, CAD_SUBDIR, SHEET_FILENAMES[sheet_id])
        if not os.path.exists(path):
            errors.append(f"MISSING_DXF: {path} not found.")
            continue
        try:
            docs[sheet_id] = ezdxf.readfile(path)
        except (OSError, ezdxf.DXFError) as exc:
            errors.append(f"{path}: unreadable DXF: {exc}")
            continue
        grouped_by_sheet[sheet_id] = _check_dxf_document(SHEET_FILENAMES[sheet_id], sheet_id, docs[sheet_id], members, scale, errors)

    if len(docs) == 2:
        errors.extend(validate_dimension_crosscheck(outputs_dir_path, grouped_by_sheet[SHEET_ID_STRUCTURE], docs[SHEET_ID_PLAN], expected))
    return errors


if __name__ == "__main__":
    s_dir = sys.argv[1] if len(sys.argv) > 1 else str(staging_dir())
    o_dir = sys.argv[2] if len(sys.argv) > 2 else str(outputs_dir())

    validation_errors = validate(s_dir, o_dir)
    if os.path.isdir(os.path.join(o_dir, CAD_SUBDIR)):
        validation_errors += validate_dxf_artifacts(s_dir, o_dir)
    if validation_errors:
        print("CROSS-ARTIFACT VALIDATION FAILED:")
        for e in validation_errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("CROSS-ARTIFACT VALIDATION PASSED ✓")
        sys.exit(0)
