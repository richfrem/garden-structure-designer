#!/usr/bin/env python3
"""
drawing_content_validator.py
===========================

Purpose:
    Per-sheet content-quality gate for the eight SVG sheets: element, semantic-role and text floors
    from the SHEET_REQUIREMENTS matrix, required roles, dimensions, title block, member ids, knee braces
    (not demanded when the structure explicitly disables bracing), footings, component panels, and
    top-left clustering / blank-sheet detection. Findings are SVG_* failure codes. The optional JSON
    report (--json-output/--append) is bound to the checked structure's source_hash and revision.
    Run per sheet by run_drawing_red_team.py. (Member tagging against structure.json lives in svg_validator.py.)

Layer: Execution / Stage 5 QA Gate

Key Input Dependencies:
    - the SVG file; optional context/staging/structure.json (hub, bracing flags, revision identity)

Key Functions:
    validate(svg_path, model_path) -> tuple[list[str], dict]
    main() -> None
    _check_sheet(svg_path, raw, model) -> tuple[list[str], dict]
    _density_errors / _feature_errors / _component_errors / _bracing_disabled
    _sheet_name / _get_requirements / _count_semantic_roles / _count_text_labels / _count_total_elements
    _has_dimension_annotations / _has_title_block / _has_member_ids / _has_braces / _has_footings
    _count_component_panels / _has_hub_reference / _is_top_left_clustered
    _report_identity(model_path) / _load_or_init_report(path) / _write_report(report, path) / _update_report(...)

Usage Examples:
    python3 drawing_content_validator.py outputs/blueprint-plan.svg context/staging/structure.json --json-output report.json [--append]
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
    """Sheet basename without extension."""
    return os.path.splitext(os.path.basename(svg_path))[0]


def _get_requirements(sheet: str) -> dict:
    """Requirement entry for the sheet (substring match on SHEET_REQUIREMENTS), else the defaults."""
    for key in SHEET_REQUIREMENTS:
        if key in sheet:
            return SHEET_REQUIREMENTS[key]
    return DEFAULT_REQUIREMENTS


def _count_semantic_roles(raw: str) -> dict[str, int]:
    """Occurrences of each data-role value (regex count)."""
    return {role: len(re.findall(rf'data-role="{role}"', raw)) for role in ALL_SEMANTIC_ROLES}


def _count_text_labels(raw: str) -> int:
    """Number of non-empty <text> elements."""
    matches = re.findall(r"<text[^>]*>([^<]+)</text>", raw)
    return sum(1 for m in matches if m.strip())


def _count_total_elements(raw: str) -> int:
    """Number of geometric elements (rect, circle, line, path, polygon, polyline, ellipse)."""
    elements = ["rect", "circle", "line", "path", "polygon", "polyline", "ellipse"]
    return sum(len(re.findall(rf"<{el}[\s/>]", raw)) for el in elements)


def _has_dimension_annotations(raw: str) -> bool:
    """True when the sheet has a dimension role/class or dimension-looking text."""
    has_role = 'data-role="dimension"' in raw
    has_dim_text = bool(re.search(r"(\d+['\"]\s*(ft|in|mm|cm)|←|→|⟵|⟶|↔)", raw))
    has_dim_class = bool(re.search(r'class="[^"]*dim[^"]*"', raw, re.IGNORECASE))
    return has_role or has_dim_text or has_dim_class


def _has_title_block(raw: str) -> bool:
    """True when the sheet has a title-block role/class or title-block text."""
    has_role = 'data-role="title-block"' in raw
    has_class = bool(re.search(r'class="[^"]*title[^"-]*block[^"]*"', raw, re.IGNORECASE))
    has_text = bool(re.search(r"(Sheet\s*\d|Scale:|Drawn\s*by:|Date:|Rev\.|Project\s*No\.)", raw, re.IGNORECASE))
    return has_role or has_class or has_text


def _has_member_ids(raw: str) -> bool:
    """True when member id labels (P/B/R numbers) appear."""
    return bool(re.search(r"\b[PBRpbr]\d{1,2}\b", raw))


def _has_braces(raw: str) -> bool:
    """True when brace elements or brace text appear."""
    return 'data-role="brace"' in raw or bool(re.search(r"(knee\s*brace|brace|kicker)", raw, re.IGNORECASE))


def _has_footings(raw: str) -> bool:
    """True when footing elements or footing text appear."""
    return 'data-role="footing"' in raw or bool(re.search(r"(footing|caisson|pad|pier)", raw, re.IGNORECASE))


def _count_component_panels(raw: str, model: dict) -> int:
    """Count distinct isolated component panels."""
    role_count = len(re.findall(r'data-role="component"', raw))
    class_count = len(re.findall(r'class="[^"]*component[^"]*"', raw, re.IGNORECASE))
    return max(role_count, class_count)


def _has_hub_reference(raw: str, model: dict) -> bool:
    """Detect if the model/drawing references a central hub."""
    if "hub" in model and isinstance(model["hub"], dict):
        hub_type = model["hub"].get("type")
        if hub_type in ("none", "", None):
            return False
        return True
    roof = model.get("roofStructure", model.get("members", {}).get("roofStructure", {}))
    return bool(roof.get("hubDiameter") or roof.get("hub"))


def _is_top_left_clustered(raw: str) -> bool:
    """True when all coordinates sit in the top-left 20% of the viewBox (mis-scaled drawing)."""
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

def _bracing_disabled(model: dict) -> bool:
    """True only when the structure explicitly disables bracing (C2: disabled bracing requires zero braces)."""
    return (model.get("bracing") or {}).get("enabled") is False


def _density_errors(sheet: str, req: dict, counts: dict, raw: str, model: dict) -> list[str]:
    """Element / semantic / text floors for the sheet."""
    errors: list[str] = []
    min_elem, min_sem = req["min_elements"], req["min_semantic"]
    if sheet == "blueprint-component-isolation" and not _has_hub_reference(raw, model):
        min_elem, min_sem = 30, 22
    if counts["total_elements"] < min_elem:
        errors.append(f"SVG_CONTENT_TOO_SMALL: {counts['total_elements']} elements found, need {min_elem} for sheet '{sheet}'.")
    if counts["semantic_total"] < min_sem:
        errors.append(f"SVG_TOO_FEW_SEMANTIC_ELEMENTS: {counts['semantic_total']} data-role elements, need {min_sem} for sheet '{sheet}'.")
    if counts["text_label_count"] < req["min_text"]:
        errors.append(f"SVG_TOO_FEW_TEXT_LABELS: {counts['text_label_count']} text labels, need {req['min_text']} for sheet '{sheet}'.")
    return errors


def _feature_errors(raw: str, req: dict, model: dict) -> list[str]:
    """Dimensions, title block, member ids, braces (unless bracing is disabled) and footings."""
    checks = [
        ("needs_dimensions", _has_dimension_annotations(raw), "SVG_MISSING_DIMENSIONS: No dimension annotations found."),
        ("needs_title_block", _has_title_block(raw), "SVG_MISSING_TITLE_BLOCK: No title block found."),
        ("needs_member_ids", _has_member_ids(raw), "SVG_MISSING_MEMBER_IDS: No member ID labels (P1, B1, R1) found."),
        ("needs_braces", _has_braces(raw) or _bracing_disabled(model), "SVG_MISSING_BRACES: No knee brace elements found."),
        ("needs_footings", _has_footings(raw), "SVG_MISSING_FOOTINGS: No footing/caisson elements found."),
    ]
    return [message for flag, present, message in checks if req.get(flag) and not present]


def _component_errors(raw: str, req: dict, model: dict) -> list[str]:
    """Isolated component panels: post, beam, rafter, brace (+ hub when the structure has one)."""
    min_components = req.get("min_components") or 0
    if min_components <= 0:
        return []
    required = min_components + 1 if _has_hub_reference(raw, model) else min_components
    panel_count = _count_component_panels(raw, model)
    if panel_count >= required:
        return []
    return [
        f"SVG_MISSING_COMPONENT_DETAILS: {panel_count} component panels found, "
        f"need {required} (post, beam, rafter, brace" + (", hub" if required > min_components else "") + ")."
    ]


def _check_sheet(svg_path: str, raw: str, model: dict) -> tuple[list[str], dict]:
    """
    Run all content checks for one SVG sheet.

    Returns:
        (failure_codes, counts_dict)
    """
    sheet = _sheet_name(svg_path)
    req = _get_requirements(sheet)
    roles = _count_semantic_roles(raw)
    total_elements = _count_total_elements(raw)
    counts = {
        "total_elements": total_elements,
        "semantic_total": sum(roles.values()),
        "text_label_count": _count_text_labels(raw),
        "semantic_counts": roles,
    }

    # Absolute blank / placeholder: no point running further checks
    if total_elements < 5:
        return [f"SVG_PLACEHOLDER_GEOMETRY: Only {total_elements} geometric elements — essentially blank."], counts

    errors = _density_errors(sheet, req, counts, raw, model)
    errors += [
        f"SVG_MISSING_REQUIRED_ROLE: data-role=\"{role}\" not found on sheet '{sheet}'."
        for role in req.get("required_roles", []) if (roles.get(role) or 0) == 0
    ]
    if _is_top_left_clustered(raw):
        errors.append(
            "SVG_CONTENT_TOP_LEFT_CLUSTER: All geometry in top-left 20% of viewBox — "
            "mis-scaled or wrong coordinate space."
        )
    errors += _feature_errors(raw, req, model)
    errors += _component_errors(raw, req, model)
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

def _report_identity(model_path: str) -> dict:
    """source_hash / revision_id / revision_hash of the structure the sheets were checked against (None when unavailable)."""
    meta: dict = {}
    if model_path and os.path.exists(model_path):
        try:
            with open(model_path, encoding="utf-8") as f:
                meta = json.load(f).get("meta") or {}
        except json.JSONDecodeError:
            pass
    return {key: meta.get(key) for key in ("source_hash", "revision_id", "revision_hash")}


def _load_or_init_report(report_path: str) -> dict:
    """Loads an existing JSON report (for --append) or creates a fresh one."""
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
    """Writes the JSON report, creating parent directories."""
    os.makedirs(os.path.dirname(report_path) or ".", exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


def _update_report(
    report: dict,
    svg_path: str,
    failure_codes: list[str],
    counts: dict,
) -> None:
    """Idempotently records one sheet and recomputes the overall status."""
    sheet_status = "FAIL" if failure_codes else "PASS"

    # Remove any existing entry for this file (idempotent re-runs)
    report["files"] = [f for f in report["files"] if f.get("file") != svg_path]

    report["files"].append({
        "file": svg_path,
        "status": sheet_status,
        "failure_codes": failure_codes,
        "total_elements": counts.get("total_elements") or 0,
        "semantic_total": counts.get("semantic_total") or 0,
        "semantic_counts": counts.get("semantic_counts", {}),
        "text_label_count": counts.get("text_label_count") or 0,
    })

    # Always recompute overall status from all entries — never leave stale state
    report["status"] = (
        "FAIL" if any(f.get("status") == "FAIL" for f in report["files"]) else "PASS"
    )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI: validate one SVG, optionally write/merge the JSON report, exit 1 on failure codes."""
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
        report.update(_report_identity(args.model_path))
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
