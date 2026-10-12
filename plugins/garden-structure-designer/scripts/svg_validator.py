#!/usr/bin/env python3
"""
svg_validator.py
================

Purpose:
    Machine validation of one SVG sheet against structure.json: XML well-formedness, dimension
    labels, post topology count, source-hash and coordinate-map anchors, and member tagging
    (every member element carries a data-tag that is a real member id; no unknown ids).
    Used per sheet by run_drawing_red_team.py. Exit 0 = PASS, 1 = errors listed.

Layer: Execution / Stage 4-5 QA Gate

Key Input Dependencies:
    - the SVG file and context/staging/structure.json (geometry.joints.resolved_model for member ids)
    - path_utils.py

Key Functions:
    validate(svg_path, model_path) -> list[str]
    main() -> None
    _load_geometry_calcs(model_path) -> dict | None     _check_xml_validity(svg_path, raw) -> list[str]
    _check_dimension_labels(...) / _check_topology_count(raw, model) / _check_source_hash(model_path, calcs)
    _check_geometry_coordinates(raw, calcs) -> list[str]
    _check_member_tags(raw, model) -> list[str]         _tag_problems(element, ids, roles, in_component) -> list[str]
    _check_stale_sheet(raw, model) -> list[str]

Usage Examples:
    python3 svg_validator.py outputs/drawing-plan-view.svg [context/staging/structure.json]
"""
from __future__ import annotations

import json
import os
import re
import sys
import xml.etree.ElementTree as ET
import hashlib
from typing import Optional


# ---------------------------------------------------------------------------
# Validation logic
# ---------------------------------------------------------------------------


def _load_geometry_calcs(model_path: str) -> Optional[dict]:
    """
    Load geometry calculations from structure.json or geometry-calculations.json.
    """
    if not os.path.exists(model_path):
        return None
    with open(model_path) as f:
        try:
            data = json.load(f)
        except Exception:
            return None
    if "meta" in data and "schema_version" in data.get("meta", {}):
        return data.get("geometry")

    calc_path = os.path.join(os.path.dirname(model_path), "geometry-calculations.json")
    if os.path.exists(calc_path):
        with open(calc_path) as f:
            try:
                return json.load(f)
            except Exception:
                return None
    return None


def _check_xml_validity(svg_path: str, raw: str) -> list[str]:
    """
    Validate SVG XML well-formedness.

    Checks:
    - Parseable by ElementTree (no broken tags, unescaped characters, etc.).
    - No double-hyphen (--) inside XML comment bodies (illegal per XML 1.0).

    Args:
        svg_path: File path for error messages.
        raw: Raw SVG file contents as string.

    Returns:
        List of error message strings (empty if all pass).
    """
    errors: list[str] = []

    try:
        ET.fromstring(raw)
    except ET.ParseError as exc:
        errors.append(f"XML_INVALID: {exc}")
        return errors  # Cannot safely proceed with further checks

    for match in re.finditer(r"<!--(.*?)-->", raw, re.DOTALL):
        body = match.group(1)
        if "--" in body:
            errors.append(
                "XML_COMMENT: Illegal double-hyphen (--) found inside comment body. "
                "XML 1.0 §2.5 forbids this."
            )
    return errors


def _check_dimension_labels(
    raw: str,
    model: dict,
    calcs: Optional[dict],
) -> list[str]:
    """
    Verify that critical dimension labels are present in the SVG text content.

    Args:
        raw: Raw SVG file contents.
        model: Parsed structural-model.json or structure.json.
        calcs: Parsed geometry-calculations.json, or None.

    Returns:
        List of error strings for any missing labels.
    """
    errors: list[str] = []

    # --- Roof pitch label ---
    if "roof" in model and "pitch" in model["roof"]:
        pitch = model["roof"]["pitch"]
    else:
        members = model.get("members") or model.get("structuralElements", {})
        roof = members.get("roofStructure") or model.get("roofStructure", {})
        pitch = roof.get("pitch", "4:12")

    pitch_prefix = pitch.split(":")[0]  # e.g. "4" for "4:12"
    if pitch_prefix + ":12" not in raw:
        errors.append(
            f"MISSING_PITCH_LABEL: '{pitch}' pitch label not found in SVG text nodes."
        )

    # --- Compound angle labels (only when geometry-calculations.json / geometry section is available) ---
    if calcs:
        cuts = calcs.get("compound_cut", {})
        miter = str(round(cuts.get("miter_deg") or 0.0, 2))
        bevel = str(round(cuts.get("bevel_deg") or 0.0, 2))
        
        if miter not in raw:
            errors.append(
                f"MISSING_MITER_ANGLE: miter angle {miter}° not found in SVG. "
                f"Expected from geometry."
            )
        if bevel not in raw:
            errors.append(
                f"MISSING_BEVEL_ANGLE: bevel angle {bevel}° not found in SVG. "
                f"Expected from geometry."
            )

    return errors


def _check_topology_count(raw: str, model: dict) -> list[str]:
    """
    Count structural post elements in the SVG against the JSON quantity.

    Uses the canonical cedar fill colour (#c8a96e) as a proxy for post elements.
    Sheets that are not topology views should include <!-- TOPOLOGY_SKIP -->
    in their XML to suppress this check.

    Args:
        raw: Raw SVG file contents.
        model: Parsed structural-model.json or structure.json.

    Returns:
        List of error strings if count mismatches (empty if skip or pass).
    """
    if "TOPOLOGY_SKIP" in raw:
        # Only allow on component/detail sheets
        if any(kw in raw.lower() for kw in ["plan view", "elevation view", "isometric"]):
            return ["TOPOLOGY_SKIP_ABUSE: Cannot skip topology on full-structure sheets."]
        return []

    if "layout" in model and "post_count" in model["layout"]:
        expected_qty: int = model["layout"]["post_count"]
    else:
        members = model.get("members") or model.get("structuralElements", {})
        posts = members.get("posts", {})
        expected_qty = posts.get("quantity") or posts.get("count") or 6

    # Count posts:
    # 1. Option C / Semantic SVGs: count unique post tags (e.g. data-tag="P1" .. "P6") or post labels
    post_tags = set(re.findall(r'data-role="post"[^>]*\bdata-tag="([^"]+)"', raw))
    label_post_tags = set(re.findall(r'data-role="label"[^>]*\bdata-tag="(P[^"]+)"', raw))
    post_tags = post_tags.union(label_post_tags)

    if post_tags:
        found = len(post_tags)
    else:
        # Legacy: count raw occurrences of data-role="post" or fill="#c8a96e"
        found = len(re.findall(r'data-role="post"', raw))
        if found == 0:
            found = len(re.findall(r'fill="#c8a96e"', raw))

    if found != expected_qty:
        return [
            f"TOPOLOGY_COUNT: Expected exactly {expected_qty} posts, "
            f"found {found}. Extra posts fail just like missing posts."
        ]
    return []

def _check_source_hash(model_path: str, calcs: dict) -> list[str]:
    """Legacy check: structural-model.json bytes must still match the hash recorded in geometry-calculations.json (no-op for structure.json)."""
    errors = []
    with open(model_path, 'rb') as f:
        current_hash = hashlib.sha256(f.read()).hexdigest()
    
    # If the file itself is structure.json, it is self-consistent
    with open(model_path) as f:
        try:
            data = json.load(f)
            if "meta" in data and "schema_version" in data.get("meta", {}):
                return []
        except Exception:
            pass

    recorded_hash = calcs.get("source_hash")
    if recorded_hash and current_hash != recorded_hash:
        errors.append(
            f"SOURCE_HASH_MISMATCH: structural-model.json changed since "
            f"geometry was computed. Re-run geometry_engine.py."
        )
    return errors

def _check_geometry_coordinates(raw: str, calcs: dict) -> list[str]:
    """The COORDINATE MAP comment embedded in the SVG must match geometry.svg_coordinates (drift > 5 px or a different grade_y fails)."""
    errors = []
    map_match = re.search(r"<!--\s*COORDINATE MAP:\s*({.*?})\s*-->", raw, re.DOTALL)
    if not map_match:
        return []
    try:
        coord_map = json.loads(map_match.group(1))
    except json.JSONDecodeError:
        return ["COORDINATE_MAP_INVALID: Could not parse JSON from COORDINATE MAP comment."]
        
    svg_coords = calcs.get("svg_coordinates", {})
    if not svg_coords:
        return []
        
    for key, expected in svg_coords.items():
        if key in coord_map:
            try:
                found = float(coord_map[key])
                if abs(found - float(expected)) > 5.0:
                    errors.append(f"COORDINATE_DRIFT: {key} drifted. Expected {expected}, found {found}")
            except ValueError:
                pass
                
    canonical_grade = svg_coords.get("grade_y")
    if canonical_grade is not None:
        if "grade_y" in coord_map and float(coord_map["grade_y"]) != float(canonical_grade):
            errors.append(f"CANONICAL_GRADE_MISMATCH: SVG uses grade_y={coord_map['grade_y']} but canonical is {canonical_grade}.")
            
    return errors


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def _check_stale_sheet(raw: str, model: dict) -> list[str]:
    """The title block must show the current source hash and (when stamped) revision id, else the sheet is stale.

    SVG_STALE_SOURCE_HASH / SVG_STALE_REVISION. Models without meta, and unstamped models (no revision_id),
    skip the corresponding check.
    """
    meta = model.get("meta") or {}
    errors: list[str] = []
    source_hash, revision_id = meta.get("source_hash"), meta.get("revision_id")
    if source_hash and f"SOURCE HASH: {source_hash[:8]}" not in raw:
        errors.append(f"SVG_STALE_SOURCE_HASH: sheet does not show source hash {source_hash[:8]} of the current structure.json.")
    if revision_id and f"REVISION: {revision_id[:8]}" not in raw:
        errors.append(f"SVG_STALE_REVISION: sheet does not show revision {revision_id[:8]} of the current structure.json.")
    return errors


def _tag_problems(element: ET.Element, ids: set, roles: set, in_component: bool) -> list[str]:
    """Tag errors of a single element (see _check_member_tags for the rules)."""
    role, tag, ident = element.get("data-role"), element.get("data-tag"), element.get("data-id")
    name = element.tag.split('}')[-1]
    problems: list[str] = []
    if ident and not tag:
        problems.append(f"SVG_MEMBER_TAG_MISSING: <{name}> data-id={ident!r} has no data-tag.")
    elif role in roles and not tag and not ident and not in_component:
        problems.append(f"SVG_MEMBER_TAG_MISSING: <{name}> data-role={role!r} has no data-tag.")
    if tag and not tag.startswith("sheet:") and tag not in ids:
        problems.append(f"SVG_UNKNOWN_MEMBER_TAG: data-tag={tag!r} is not a member of structure.json.")
    return problems


def _check_member_tags(raw: str, model: dict) -> list[str]:
    """Member elements must carry data-tag equal to a real structure.json member id (AGENTS ids across layers).

    SVG_MEMBER_TAG_MISSING: an element has data-id or a member data-role but no data-tag
    (decorative member-role elements inside a data-role="component" panel are tolerated).
    SVG_UNKNOWN_MEMBER_TAG: a data-tag that is not a resolved_model member id.
    Models without a resolved_model (legacy) are skipped.
    """
    members = ((model.get("geometry") or {}).get("joints") or {}).get("resolved_model", {}).get("members", [])
    if not members:
        return []
    ids, roles = {m["id"] for m in members}, {m["role"] for m in members}
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return []  # XML problems are reported by _check_xml_validity
    errors: list[str] = []
    stack = [(root, False)]
    while stack:
        element, in_component = stack.pop()
        errors.extend(_tag_problems(element, ids, roles, in_component))
        stack.extend((child, in_component or element.get("data-role") == "component") for child in reversed(list(element)))
    return errors


def validate(svg_path: str, model_path: str) -> list[str]:
    """
    Run all validation checks on a single SVG against structural-model.json.

    Args:
        svg_path: Path to the SVG file to validate.
        model_path: Path to context/staging/structural-model.json.

    Returns:
        List of error strings. Empty list means PASS.
    """
    with open(svg_path) as f:
        raw = f.read()

    with open(model_path) as f:
        model = json.load(f)

    calcs = _load_geometry_calcs(model_path)

    errors: list[str] = []
    errors.extend(_check_xml_validity(svg_path, raw))

    # Abort further checks if XML is broken — other checks will give false results
    if errors:
        return errors

    if calcs:
        errors.extend(_check_source_hash(model_path, calcs))
        errors.extend(_check_geometry_coordinates(raw, calcs))

    errors.extend(_check_dimension_labels(raw, model, calcs))
    errors.extend(_check_topology_count(raw, model))
    errors.extend(_check_member_tags(raw, model))
    errors.extend(_check_stale_sheet(raw, model))
    return errors


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


from path_utils import staging_dir

def main() -> None:
    """Parse CLI arguments and run validation, printing results to stdout."""
    if len(sys.argv) < 2:
        print(
            "Usage: python3 scripts/svg_validator.py "
            "<svg_file> [path-to-structure.json]",
            file=sys.stderr,
        )
        sys.exit(1)

    svg_path = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else str(staging_dir() / "structure.json")
    errors = validate(svg_path, model_path)

    if errors:
        print("VALIDATION FAILED:")
        for err in errors:
            print(f"  ✗ {err}")
        sys.exit(1)
    else:
        print(f"VALIDATION PASSED ✓  ({svg_path})")
        sys.exit(0)


if __name__ == "__main__":
    main()
