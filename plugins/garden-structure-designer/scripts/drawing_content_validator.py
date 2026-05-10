#!/usr/bin/env python3
"""
drawing_content_validator.py
=====================================

Purpose:
    Content-quality validator for generated SVG drawing sheets.
    Goes beyond XML well-formedness (svg_validator.py) to assess whether
    drawings are builder-meaningful: dimensions, member IDs, title blocks,
    semantic role counts, sheet coverage, and component isolation panels.

Layer: Execution

Usage Examples:
    python3 drawing_content_validator.py outputs/blueprint-elevation.svg \
        plugins/garden-structure-designer/context/staging/structural-model.json

    # Batch mode — validate all SVGs in outputs/:
    for f in outputs/*.svg; do
        python3 drawing_content_validator.py "$f" \
            plugins/garden-structure-designer/context/staging/structural-model.json
    done

Failure Codes Emitted:
    SVG_PLACEHOLDER_GEOMETRY
    SVG_CONTENT_TOO_SMALL
    SVG_CONTENT_TOP_LEFT_CLUSTER
    SVG_TOO_FEW_DRAWING_ELEMENTS
    SVG_MISSING_DIMENSIONS
    SVG_MISSING_TITLE_BLOCK
    SVG_MISSING_MEMBER_IDS
    SVG_MISSING_BRACES
    SVG_MISSING_FOOTINGS
    SVG_MISSING_COMPONENT_DETAILS
    SVG_NOT_BUILDER_MEANINGFUL

Script Dependencies:
    Standard library: json, os, re, sys, xml.etree.ElementTree

Consumed by:
    adversarial-drawing-reviewer skill, drawing-red-team-agent
"""
from __future__ import annotations

import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Minimum number of semantic data-role elements to be considered non-placeholder
MIN_SEMANTIC_ELEMENTS = 3

# Minimum text label count to be considered non-placeholder
MIN_TEXT_LABELS = 2

# SVG sheets that must contain dimension annotations
DIMENSION_REQUIRED_SHEETS = [
    "blueprint-plan",
    "blueprint-elevation",
    "blueprint-isometric",
    "blueprint-component-isolation",
]

# SVG sheets that must contain a title block
TITLE_BLOCK_REQUIRED_SHEETS = [
    "blueprint-plan",
    "blueprint-elevation",
    "blueprint-isometric",
    "blueprint-component-isolation",
]

# SVG sheets that must contain member ID labels (P1, B1, R1, etc.)
MEMBER_ID_REQUIRED_SHEETS = [
    "blueprint-plan",
    "blueprint-elevation",
    "blueprint-isometric",
]

# SVG sheets that must show braces and footings
STRUCTURAL_ELEMENT_REQUIRED_SHEETS = [
    "drawing-elevation-view",
    "drawing-isometric-view",
    "blueprint-elevation",
    "blueprint-isometric",
]

# Component isolation sheet
COMPONENT_ISOLATION_SHEET = "blueprint-component-isolation"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sheet_name(svg_path: str) -> str:
    """Extract the base sheet name (no extension) from an SVG path."""
    return os.path.splitext(os.path.basename(svg_path))[0]


def _count_semantic_roles(raw: str) -> dict[str, int]:
    """Count occurrences of each data-role attribute value."""
    roles = ["post", "beam", "rafter", "brace", "footing", "dimension", "component", "title-block"]
    return {role: len(re.findall(rf'data-role="{role}"', raw)) for role in roles}


def _count_text_labels(raw: str) -> int:
    """Count non-empty SVG text elements."""
    # Match <text ...>content</text> with non-whitespace content
    matches = re.findall(r"<text[^>]*>([^<]+)</text>", raw)
    return sum(1 for m in matches if m.strip())


def _has_dimension_annotations(raw: str) -> bool:
    """Check for dimension annotations: arrows, callouts, or data-role=dimension."""
    has_role = 'data-role="dimension"' in raw
    # Also accept common dimension patterns: feet/inches markers or ← → arrows
    has_dim_text = bool(re.search(r"""(\d+['"\s]*(ft|in|mm|cm)|←|→|⟵|⟶|↔|<-[^-]|->)""", raw))
    has_dim_line = bool(re.search(r'class="[^"]*dim[^"]*"', raw, re.IGNORECASE))
    return has_role or has_dim_text or has_dim_line


def _has_title_block(raw: str) -> bool:
    """Check for a title block element."""
    has_role = 'data-role="title-block"' in raw
    has_class = bool(re.search(r'class="[^"]*title[^"-]*block[^"]*"', raw, re.IGNORECASE))
    # Common title block text patterns
    has_text = bool(re.search(r"(Sheet\s*\d|Scale:|Drawn\s*by:|Date:|Rev\.|Project\s*No\.)", raw, re.IGNORECASE))
    return has_role or has_class or has_text


def _has_member_ids(raw: str) -> bool:
    """Check for member ID labels like P1, P2, B1, R1, etc."""
    # Post IDs: P1-P12, Beam IDs: B1-B12 or BM-1, Rafter IDs: R1-R12
    return bool(re.search(r"\b[PBRpbr]\d{1,2}\b", raw))


def _has_braces(raw: str) -> bool:
    """Check for knee brace elements."""
    has_role = 'data-role="brace"' in raw
    has_text = bool(re.search(r"(knee\s*brace|brace|kicker)", raw, re.IGNORECASE))
    return has_role or has_text


def _has_footings(raw: str) -> bool:
    """Check for footing/caisson elements."""
    has_role = 'data-role="footing"' in raw
    has_text = bool(re.search(r"(footing|caisson|pad|pier)", raw, re.IGNORECASE))
    return has_role or has_text


def _has_component_panels(raw: str, model: dict) -> bool:
    """
    Check that blueprint-component-isolation actually isolates components.

    Looks for at least 3 distinct component groups / panels.
    """
    component_count = len(re.findall(r'data-role="component"', raw))
    # Also look for <g> groups with component-like class names
    group_count = len(re.findall(r'class="[^"]*component[^"]*"', raw, re.IGNORECASE))
    panel_count = max(component_count, group_count)
    return panel_count >= 3


def _is_top_left_clustered(raw: str) -> bool:
    """
    Heuristic: detect if all geometry is crammed into the top-left corner.

    Parses transform/x/y attributes to check if most elements use very small
    coordinate values relative to the viewBox.
    """
    viewbox_match = re.search(r'viewBox="([^"]+)"', raw)
    if not viewbox_match:
        return False
    parts = viewbox_match.group(1).split()
    if len(parts) < 4:
        return False
    try:
        vb_width = float(parts[2])
        vb_height = float(parts[3])
    except ValueError:
        return False

    # Gather x/y/cx/cy coordinates
    coords_x = [float(v) for v in re.findall(r'\bx="([\d.]+)"', raw)]
    coords_y = [float(v) for v in re.findall(r'\by="([\d.]+)"', raw)]
    coords_x += [float(v) for v in re.findall(r'\bcx="([\d.]+)"', raw)]
    coords_y += [float(v) for v in re.findall(r'\bcy="([\d.]+)"', raw)]

    if not coords_x or not coords_y:
        return False

    max_x = max(coords_x, default=0)
    max_y = max(coords_y, default=0)

    # If all elements fit within the top-left 20% of the viewBox, flag it
    return max_x < vb_width * 0.20 and max_y < vb_height * 0.20


def _count_total_drawing_elements(raw: str) -> int:
    """Count total geometric elements: rect, circle, line, path, polygon, polyline."""
    elements = ["rect", "circle", "line", "path", "polygon", "polyline", "ellipse"]
    total = 0
    for el in elements:
        total += len(re.findall(rf"<{el}[\s/>]", raw))
    return total


# ---------------------------------------------------------------------------
# Per-sheet checks
# ---------------------------------------------------------------------------

def _check_content_quality(svg_path: str, raw: str, model: dict) -> list[str]:
    """
    Run content-quality checks on a single SVG.

    Returns a list of failure code strings (empty = PASS).
    """
    errors: list[str] = []
    sheet = _sheet_name(svg_path)
    roles = _count_semantic_roles(raw)
    text_count = _count_text_labels(raw)
    total_elements = _count_total_drawing_elements(raw)
    semantic_total = sum(roles.values())

    # --- Placeholder / empty drawing ---
    if total_elements < 5:
        errors.append(
            f"SVG_PLACEHOLDER_GEOMETRY: Only {total_elements} geometric elements found. "
            "Drawing is essentially blank."
        )

    if total_elements < 15:
        errors.append(
            f"SVG_CONTENT_TOO_SMALL: Only {total_elements} geometric elements. "
            "Expected at least 15 for a builder-meaningful sheet."
        )

    # --- Semantic role density ---
    if semantic_total < MIN_SEMANTIC_ELEMENTS:
        errors.append(
            f"SVG_TOO_FEW_DRAWING_ELEMENTS: Only {semantic_total} semantic data-role elements. "
            f"Minimum {MIN_SEMANTIC_ELEMENTS} required."
        )

    # --- Text labels ---
    if text_count < MIN_TEXT_LABELS:
        errors.append(
            f"SVG_NOT_BUILDER_MEANINGFUL: Only {text_count} text label(s) found. "
            "A builder-meaningful drawing must have at least 2 labels."
        )

    # --- Top-left clustering ---
    if _is_top_left_clustered(raw):
        errors.append(
            "SVG_CONTENT_TOP_LEFT_CLUSTER: All geometry appears clustered in the top-left "
            "corner of the viewBox. Drawing is likely mis-scaled or uses wrong coordinate space."
        )

    # --- Dimension annotations ---
    if any(kw in sheet for kw in DIMENSION_REQUIRED_SHEETS):
        if not _has_dimension_annotations(raw):
            errors.append(
                "SVG_MISSING_DIMENSIONS: No dimension annotations found. "
                "Blueprint sheets must include dimensional callouts."
            )

    # --- Title block ---
    if any(kw in sheet for kw in TITLE_BLOCK_REQUIRED_SHEETS):
        if not _has_title_block(raw):
            errors.append(
                "SVG_MISSING_TITLE_BLOCK: No title block found. "
                "Blueprint sheets must include a title block with project metadata."
            )

    # --- Member IDs ---
    if any(kw in sheet for kw in MEMBER_ID_REQUIRED_SHEETS):
        if not _has_member_ids(raw):
            errors.append(
                "SVG_MISSING_MEMBER_IDS: No member ID labels found (e.g., P1, B1, R1). "
                "Blueprint sheets must label all structural members."
            )

    # --- Braces and footings ---
    if any(kw in sheet for kw in STRUCTURAL_ELEMENT_REQUIRED_SHEETS):
        if not _has_braces(raw):
            errors.append(
                "SVG_MISSING_BRACES: No knee brace elements found on a sheet that requires them. "
                "Elevation and isometric views must show lateral bracing."
            )
        if not _has_footings(raw):
            errors.append(
                "SVG_MISSING_FOOTINGS: No footing/caisson elements found on a sheet that requires them. "
                "Elevation and isometric views must show footings at grade."
            )

    # --- Component isolation panels ---
    if COMPONENT_ISOLATION_SHEET in sheet:
        if not _has_component_panels(raw, model):
            errors.append(
                "SVG_MISSING_COMPONENT_DETAILS: Component isolation sheet does not contain "
                "at least 3 distinct component panels. Each structural component must be isolated "
                "with its own panel, labels, and callouts."
            )

    return errors


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate(svg_path: str, model_path: str) -> list[str]:
    """
    Run content-quality validation on a single SVG against structural-model.json.

    Args:
        svg_path: Path to the SVG file to validate.
        model_path: Path to context/staging/structural-model.json.

    Returns:
        List of failure code strings. Empty list means content PASS.
    """
    if not os.path.exists(svg_path):
        return [f"SVG_PLACEHOLDER_GEOMETRY: File not found: {svg_path}"]

    if not os.path.exists(model_path):
        return [f"SVG_NOT_BUILDER_MEANINGFUL: structural-model.json not found: {model_path}"]

    with open(svg_path, encoding="utf-8") as f:
        raw = f.read()

    with open(model_path, encoding="utf-8") as f:
        model = json.load(f)

    return _check_content_quality(svg_path, raw, model)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Parse CLI arguments and run content validation, printing results to stdout."""
    if len(sys.argv) < 3:
        print(
            "Usage: python3 scripts/drawing_content_validator.py "
            "<svg_file> <path-to-structural-model.json>",
            file=sys.stderr,
        )
        sys.exit(1)

    svg_path, model_path = sys.argv[1], sys.argv[2]
    errors = validate(svg_path, model_path)

    if errors:
        print(f"CONTENT VALIDATION FAILED: {os.path.basename(svg_path)}")
        for err in errors:
            print(f"  ✗ {err}")
        sys.exit(1)
    else:
        print(f"CONTENT VALIDATION PASSED ✓  ({svg_path})")
        sys.exit(0)


if __name__ == "__main__":
    main()
