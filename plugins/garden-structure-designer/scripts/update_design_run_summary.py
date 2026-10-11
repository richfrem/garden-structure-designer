#!/usr/bin/env python3
"""
update_design_run_summary.py
===========================

Purpose:
    Writes context/staging/design-run-summary.md: the locked parameters of the current design
    (type, shape, jurisdiction, post count, pitch, cut angles, height), the source hash and the
    committed revision (id and hash), and the SVG frame. Values absent from structure.json are
    labelled "Unknown"; nothing is invented.

Layer: Execution / Run Context

Key Input Dependencies:
    - context/staging/structure.json (optional; summary is still written, fully labelled Unknown)
    - path_utils.py

Key Functions:
    summary_parameters(structure) -> dict
    render_summary(parameters) -> str
    safe_load(path) -> dict
    main() -> None
    _dig(source, *keys) -> Any

Usage Examples:
    python3 update_design_run_summary.py
"""
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir

UNKNOWN = "Unknown"


def safe_load(path) -> dict:
    """Loads a JSON file, returning {} when it does not exist."""
    if Path(path).exists():
        with open(path) as f: return json.load(f)
    return {}


def _dig(source: dict, *keys: str):
    """Walks nested dicts and returns the value, or the literal 'Unknown' label when any level is absent/empty."""
    node = source
    for key in keys:
        node = (node or {}).get(key)
    return node or UNKNOWN


def summary_parameters(structure: dict) -> dict:
    """Collects the locked parameters shown in the summary; absent values are labelled 'Unknown', never invented."""
    return {
        "structure_type": _dig(structure, "structure", "type"),
        "plan_shape": _dig(structure, "structure", "shape"),
        "jurisdiction": _dig(structure, "intent", "jurisdiction"),
        "post_count": _dig(structure, "layout", "post_count"),
        "pitch": _dig(structure, "roof", "pitch"),
        "miter": _dig(structure, "geometry", "compound_cut", "miter_deg"),
        "bevel": _dig(structure, "geometry", "compound_cut", "bevel_deg"),
        "beam_miter": _dig(structure, "geometry", "beam_ring", "beam_miter_deg"),
        "total_height": _dig(structure, "geometry", "total_height", "total_height_ft"),
        "source_hash": _dig(structure, "meta", "source_hash"),
        "revision_id": _dig(structure, "meta", "revision_id"),
        "revision_hash": _dig(structure, "meta", "revision_hash"),
        "viewbox": _dig(structure, "geometry", "svg_coordinates", "viewBox"),
        "grade_y": _dig(structure, "geometry", "svg_coordinates", "grade_y"),
    }


def render_summary(p: dict) -> str:
    """Renders the markdown summary from ``summary_parameters`` output."""
    return f"""# Design Run Summary
 
 ## Active Task
 Generate validated garden structure design package.
 
 ## Locked Parameters
 - Structure type: {p['structure_type']}
 - Plan shape: {p['plan_shape']}
 - Jurisdiction: {p['jurisdiction']}
 - Post count: {p['post_count']}
 - Pitch: {p['pitch']}
 - Rafter miter: {p['miter']}
 - Rafter bevel: {p['bevel']}
 - Beam ring miter: {p['beam_miter']}
 - Total height: {p['total_height']}
 
 ## Deterministic Calculations
 - Source: structure.json
 - Source hash: {p['source_hash']}
 - Revision: {p['revision_id']} ({p['revision_hash']})
 - SVG viewBox: {p['viewbox']}
 - Grade Y: {p['grade_y']}
 
 ## Completed Stages
 Generated dynamically as pipeline executes.
 
 ## Validation Findings
 Check repair-report.json and drift_report.json.
 """


def main() -> None:
    """CLI entrypoint: writes staging/design-run-summary.md from structure.json."""
    summary = render_summary(summary_parameters(safe_load(staging_dir() / "structure.json")))
    with open(staging_dir() / "design-run-summary.md", "w") as f:
        f.write(summary)

    print("Design run summary updated.")


if __name__ == "__main__":
    main()
