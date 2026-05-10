#!/usr/bin/env python3
"""
drawing_content_validator.py
=====================================

Purpose:
    Content-quality validator for generated SVG drawing sheets.
    Goes beyond XML well-formedness (svg_validator.py) to assess whether
    drawings are builder-meaningful: dimensions, member IDs, title blocks,
    semantic role counts, sheet coverage, and component isolation panels.

    Uses PER-SHEET minimum thresholds. Global low thresholds (e.g. MIN=3)
    are intentionally avoided — they allowed garbage drawings to pass.

Layer: Execution

Usage Examples:
    # Single file:
    python3 drawing_content_validator.py outputs/blueprint-elevation.svg \\
        plugins/garden-structure-designer/context/staging/structural-model.json

    # Single file with JSON output:
    python3 drawing_content_validator.py outputs/blueprint-elevation.svg \\
        plugins/garden-structure-designer/context/staging/structural-model.json \\
        --json-output context/staging/drawing-content-report.json

    # Batch mode (from shell loop):
    for f in outputs/*.svg; do
        python3 drawing_content_validator.py "$f" \\
            plugins/garden-structure-designer/context/staging/structural-model.json \\
            --json-output context/staging/drawing-content-report.json --append
    done

Failure Codes Emitted:
    SVG_PLACEHOLDER_GEOMETRY         — fewer than 5 geometric elements total
    SVG_CONTENT_TOO_SMALL            — below sheet-specific min_elements threshold
    SVG_CONTENT_TOP_LEFT_CLUSTER     — all geometry in top-left 20% of viewBox
    SVG_TOO_FEW_SEMANTIC_ELEMENTS    — below sheet-specific min_semantic threshold
    SVG_TOO_FEW_TEXT_LABELS          — below sheet-specific min_text threshold
    SVG_MISSING_REQUIRED_ROLE        — a required data-role is absent for this sheet
    SVG_MISSING_DIMENSIONS           — no dimension annotations on a blueprint sheet
    SVG_MISSING_TITLE_BLOCK          — no title block on a blueprint sheet
    SVG_MISSING_MEMBER_IDS           — no member ID labels (P1, B1, R1) on blueprint
    SVG_MISSING_BRACES               — no brace elements on elevation/isometric
    SVG_MISSING_FOOTINGS             — no footing elements on elevation/isometric
    SVG_MISSING_COMPONENT_DETAILS    — fewer than required component panels
    SVG_NOT_BUILDER_MEANINGFUL       — general builder-usefulness failure

Script Dependencies:
    Standard library: argparse, json, os, re, sys

Consumed by:
    adversarial-drawing-reviewer skill, drawing-red-team-agent,
    run_drawing_red_team.py, generate_quality_dashboard.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from typing import Optional

# ---------------------------------------------------------------------------
# Per-sheet requirement matrix
# ---------------------------------------------------------------------------

# Each entry defines thresholds for that sheet basename (no extension).
# "required_roles" are data-role values that MUST be present.
# "min_components" applies only to component-isolation sheets.
SHEET_REQUIREMENTS: dict[str, dict] = {
    "drawing-plan-view": {
        "min_elements": 20,
        "min_semantic": 8,
        "min_text": 4,
        "required_roles": ["post", "beam", "rafter"],
        "min_components": 0,
    },
    "drawing-elevation-view": {
        "min_elements": 25,
        "min_semantic": 10,
        "min_text": 5,
        "required_roles": ["post", "beam", "rafter"],
        "needs_braces": True,
        "needs_footings": True,
        "min_components": 0,
    },
    "drawing-isometric-view": {
        "min_elements": 25,
        "min_semantic": 10,
        "min_text": 5,
        "required_roles": ["post", "beam", "rafter"],
        "needs_braces": True,
        "needs_footings": True,
        "min_components": 0,
    },
    "drawing-perspective-view": {
        "min_elements": 15,
        "min_semantic": 6,
        "min_text": 3,
        "required_roles": ["post", "beam"],
        "min_components": 0,
    },
    "blueprint-plan": {
        "min_elements": 30,
        "min_semantic": 20,
        "min_text": 8,
        "required_roles": ["post", "beam", "rafter", "dimension", "title-block"],
        "needs_dimensions": True,
        "needs_title_block": True,
        "needs_member_ids": True,
        "min_components": 0,
    },
    "blueprint-elevation": {
        "min_elements": 35,
        "min_semantic": 25,
        "min_text": 10,
        "required_roles": ["post", "beam", "rafter", "brace", "footing", "dimension", "title-block"],
        "needs_dimensions": True,
        "needs_title_block": True,
        "needs_member_ids": True,
        "needs_braces": True,
        "needs_footings": True,
        "min_components": 0,
    },
    "blueprint-isometric": {
        "min_elements": 35,
        "min_semantic": 25,
        "min_text": 8,
        "required_roles": ["post", "beam", "rafter", "brace", "footing", "title-block"],
        "needs_dimensions": True,
        "needs_title_block": True,
        "needs_member_ids": True,
        "needs_braces": True,
        "needs_footings": True,
        "min_components": 0,
    },
    "blueprint-component-isolation": {
        "min_elements": 40,
        "min_semantic": 30,
        "min_text": 12,
        "required_roles": ["component", "post", "beam", "rafter", "brace", "dimension", "title-block"],
        "needs_dimensions": True,
        "needs_title_block": True,
        "min_components": 4,  # post, beam, rafter, brace (hub is +1 if present)
    },
}

# Fallback for any sheet not in the matrix
DEFAULT_REQUIREMENTS: dict = {
    "min_elements": 10,
    "min_semantic": 3,
    "min_text": 2,
    "required_roles": [],
    "min_components": 0,
}

ALL_SEMANTIC_ROLES = [
    "post", "beam", "rafter", "brace", "footing",
    "dimension", "component", "title-block",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sheet_name(svg_path: str) -> str:
    return os.path.splitext(os.path.basename(svg_path))[0]


def _get_requirements(sheet: str) -> dict:
    for key in SHEET_REQUIREMENTS:
        if key in sheet:
            return SHEET_REQUIREMENTS[key]
    return DEFAULT_REQUIREMENTS


def _count_semantic_roles(raw: str) -> dict[str, int]:
    return {role: len(re.findall(rf'data-role="{role}"', raw)) for role in ALL_SEMANTIC_ROLES}


def _count_text_labels(raw: str) -> int:
    matches = re.findall(r"<text[^>]*>([^<]+)</text>", raw)
    return sum(1 for m in matches if m.strip())


def _count_total_elements(raw: str) -> int:
    elements = ["rect", "circle", "line", "path", "polygon", "polyline", "ellipse"]
    return sum(len(re.findall(rf"<{el}[\s/>]", raw)) for el in elements)


def _has_dimension_annotations(raw: str) -> bool:
    has_role = 'data-role="dimension"' in raw
    has_dim_text = bool(re.search(r"(\d+['\"]\s*(ft|in|mm|cm)|←|→|⟵|⟶|↔)", raw))
    has_dim_class = bool(re.search(r'class="[^"]*dim[^"]*"', raw, re.IGNORECASE))
    return has_role or has_dim_text or has_dim_class


def _has_title_block(raw: str) -> bool:
    has_role = 'data-role="title-block"' in raw
    has_class = bool(re.search(r'class="[^"]*title[^"-]*block[^"]*"', raw, re.IGNORECASE))
    has_text = bool(re.search(r"(Sheet\s*\d|Scale:|Drawn\s*by:|Date:|Rev\.|Project\s*No\.)", raw, re.IGNORECASE))
    return has_role or has_class or has_text


def _has_member_ids(raw: str) -> bool:
    return bool(re.search(r"\b[PBRpbr]\d{1,2}\b", raw))


def _has_braces(raw: str) -> bool:
    return 'data-role="brace"' in raw or bool(re.search(r"(knee\s*brace|brace|kicker)", raw, re.IGNORECASE))


def _has_footings(raw: str) -> bool:
    return 'data-role="footing"' in raw or bool(re.search(r"(footing|caisson|pad|pier)", raw, re.IGNORECASE))


def _count_component_panels(raw: str, model: dict) -> int:
    """Count distinct isolated component panels."""
    role_count = len(re.findall(r'data-role="component"', raw))
    class_count = len(re.findall(r'class="[^"]*component[^"]*"', raw, re.IGNORECASE))
    return max(role_count, class_count)


def _has_hub_reference(raw: str, model: dict) -> bool:
    """Detect if the model/drawing references a central hub."""
    if "hub" in raw.lower():
        return True
    roof = model.get("roofStructure", model.get("members", {}).get("roofStructure", {}))
    return bool(roof.get("hubDiameter") or roof.get("hub"))


def _is_top_left_clustered(raw: str) -> bool:
    vb = re.search(r'viewBox="([^"]+)"', raw)
    if not vb:
        return False
    parts = vb.group(1).split()
    if len(parts) < 4:
        return False
    try:
        vb_w, vb_h = float(parts[2]), float(parts[3])
    except ValueError:
        return False
    xs = [float(v) for v in re.findall(r'\b(?:x|cx)="([\d.]+)"', raw)]
    ys = [float(v) for v in re.findall(r'\b(?:y|cy)="([\d.]+)"', raw)]
    if not xs or not ys:
        return False
    return max(xs) < vb_w * 0.20 and max(ys) < vb_h * 0.20


# ---------------------------------------------------------------------------
# Core check
# ---------------------------------------------------------------------------

def _check_sheet(svg_path: str, raw: str, model: dict) -> tuple[list[str], dict]:
    """
    Run all content checks for one SVG sheet.

    Returns:
        (failure_codes, counts_dict)
    """
    errors: list[str] = []
    sheet = _sheet_name(svg_path)
    req = _get_requirements(sheet)

    roles = _count_semantic_roles(raw)
    text_count = _count_text_labels(raw)
    total_elements = _count_total_elements(raw)
    semantic_total = sum(roles.values())

    counts = {
        "total_elements": total_elements,
        "semantic_total": semantic_total,
        "text_label_count": text_count,
        "semantic_counts": roles,
    }

    # Absolute blank / placeholder
    if total_elements < 5:
        errors.append(
            f"SVG_PLACEHOLDER_GEOMETRY: Only {total_elements} geometric elements — essentially blank."
        )
        return errors, counts  # No point running further checks

    # Sheet-specific element floor
    if total_elements < req["min_elements"]:
        errors.append(
            f"SVG_CONTENT_TOO_SMALL: {total_elements} elements found, "
            f"need {req['min_elements']} for sheet '{sheet}'."
        )

    # Sheet-specific semantic floor
    if semantic_total < req["min_semantic"]:
        errors.append(
            f"SVG_TOO_FEW_SEMANTIC_ELEMENTS: {semantic_total} data-role elements, "
            f"need {req['min_semantic']} for sheet '{sheet}'."
        )

    # Sheet-specific text floor
    if text_count < req["min_text"]:
        errors.append(
            f"SVG_TOO_FEW_TEXT_LABELS: {text_count} text labels, "
            f"need {req['min_text']} for sheet '{sheet}'."
        )

    # Required roles
    for role in req.get("required_roles", []):
        if roles.get(role, 0) == 0:
            errors.append(
                f"SVG_MISSING_REQUIRED_ROLE: data-role=\"{role}\" not found on sheet '{sheet}'."
            )

    # Top-left clustering
    if _is_top_left_clustered(raw):
        errors.append(
            "SVG_CONTENT_TOP_LEFT_CLUSTER: All geometry in top-left 20% of viewBox — "
            "mis-scaled or wrong coordinate space."
        )

    # Dimension annotations
    if req.get("needs_dimensions") and not _has_dimension_annotations(raw):
        errors.append("SVG_MISSING_DIMENSIONS: No dimension annotations found.")

    # Title block
    if req.get("needs_title_block") and not _has_title_block(raw):
        errors.append("SVG_MISSING_TITLE_BLOCK: No title block found.")

    # Member IDs
    if req.get("needs_member_ids") and not _has_member_ids(raw):
        errors.append("SVG_MISSING_MEMBER_IDS: No member ID labels (P1, B1, R1) found.")

    # Braces
    if req.get("needs_braces") and not _has_braces(raw):
        errors.append("SVG_MISSING_BRACES: No knee brace elements found.")

    # Footings
    if req.get("needs_footings") and not _has_footings(raw):
        errors.append("SVG_MISSING_FOOTINGS: No footing/caisson elements found.")

    # Component isolation panels
    min_components = req.get("min_components", 0)
    if min_components > 0:
        panel_count = _count_component_panels(raw, model)
        # Add 1 required component if hub is present
        required = min_components
        if _has_hub_reference(raw, model):
            required = min_components + 1
        if panel_count < required:
            errors.append(
                f"SVG_MISSING_COMPONENT_DETAILS: {panel_count} component panels found, "
                f"need {required} (post, beam, rafter, brace"
                + (", hub" if required > min_components else "")
                + ")."
            )

    return errors, counts


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate(svg_path: str, model_path: str) -> tuple[list[str], dict]:
    """
    Run content-quality validation on a single SVG.

    Returns:
        (failure_codes, counts_dict)
    """
    if not os.path.exists(svg_path):
        return ([f"SVG_PLACEHOLDER_GEOMETRY: File not found: {svg_path}"], {})

    model: dict = {}
    if model_path and os.path.exists(model_path):
        try:
            with open(model_path, encoding="utf-8") as f:
                model = json.load(f)
        except json.JSONDecodeError:
            pass  # Proceed without model — still run heuristic checks

    with open(svg_path, encoding="utf-8") as f:
        raw = f.read()

    return _check_sheet(svg_path, raw, model)


# ---------------------------------------------------------------------------
# JSON report helpers
# ---------------------------------------------------------------------------

def _load_or_init_report(report_path: str) -> dict:
    if os.path.exists(report_path):
        try:
            with open(report_path, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {
        "schema": "garden-structure-designer/drawing-content-report/1.0",
        "generated": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "files": [],
    }


def _write_report(report: dict, report_path: str) -> None:
    os.makedirs(os.path.dirname(report_path) or ".", exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


def _update_report(
    report: dict,
    svg_path: str,
    failure_codes: list[str],
    counts: dict,
) -> None:
    sheet_status = "FAIL" if failure_codes else "PASS"
    if sheet_status == "FAIL":
        report["status"] = "FAIL"

    # Remove any existing entry for this file (idempotent re-runs)
    report["files"] = [f for f in report["files"] if f.get("file") != svg_path]

    report["files"].append({
        "file": svg_path,
        "status": sheet_status,
        "failure_codes": failure_codes,
        "total_elements": counts.get("total_elements", 0),
        "semantic_total": counts.get("semantic_total", 0),
        "semantic_counts": counts.get("semantic_counts", {}),
        "text_label_count": counts.get("text_label_count", 0),
    })


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Content-quality validator for garden-structure-designer SVG sheets."
    )
    parser.add_argument("svg_file", help="Path to the SVG file to validate.")
    parser.add_argument(
        "model_path",
        nargs="?",
        default="",
        help="Path to context/staging/structural-model.json (optional).",
    )
    parser.add_argument(
        "--json-output",
        metavar="REPORT_PATH",
        default="",
        help="Write results to this JSON report file.",
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append/merge into existing JSON report instead of overwriting.",
    )
    args = parser.parse_args()

    failure_codes, counts = validate(args.svg_file, args.model_path)

    # JSON output handling
    if args.json_output:
        if args.append:
            report = _load_or_init_report(args.json_output)
        else:
            report = {
                "schema": "garden-structure-designer/drawing-content-report/1.0",
                "generated": datetime.now(timezone.utc).isoformat(),
                "status": "PASS",
                "files": [],
            }
        _update_report(report, args.svg_file, failure_codes, counts)
        _write_report(report, args.json_output)

    if failure_codes:
        print(f"CONTENT VALIDATION FAILED: {os.path.basename(args.svg_file)}")
        for err in failure_codes:
            print(f"  ✗ {err}")
        sys.exit(1)
    else:
        print(f"CONTENT VALIDATION PASSED ✓  ({args.svg_file})")
        sys.exit(0)


if __name__ == "__main__":
    main()
