#!/usr/bin/env python3
"""
package_consistency_validator.py
================================

Purpose:
    Final-package completeness and consistency gate. Verifies that every Stage 4/6
    deliverable exists (all eight SVG sheets, both DXF sheets SB01/SB02, the fabrication
    cut list, photorealistic renders), that SVG generation dates/titles agree, and that the
    fabrication cut list is bound to the same ``revision_id``/``revision_hash`` as the
    canonical structure.json. The parsed-DXF content checks live in cross_artifact_validator.py.

Layer: Execution / QA Gate

Key Input Dependencies:
    - context/staging/structure.json (meta.revision_id, meta.revision_hash)
    - outputs/*.svg (8 sheets), outputs/cad/SB01-structure.dxf + SB02-plan.dxf
    - outputs/fabrication/cut-list.json (written by fabrication_builder.py)
    - outputs/high-resolution-image/*_render_*.png
    - constants.py (sheet and directory names), path_utils.py (default directories)

Key Functions:
    validate_package(staging_path=None, outputs_path=None) -> list[str]
    _required_files() -> list[str]
    check_revision_binding(structure_path, cut_list_path) -> list[str]
    _check_svg_consistency(outputs_path) -> list[str]

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/package_consistency_validator.py
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

sys.path.append(str(Path(__file__).parent.resolve()))
from constants import CAD_SUBDIR, CUT_LIST_FILENAME, FABRICATION_SUBDIR, SHEET_FILENAMES, SVG_SHEET_FILENAMES
from path_utils import outputs_dir, staging_dir


def _required_files() -> list[str]:
    """Returns the output-relative paths every complete package must contain."""
    return [
        *SVG_SHEET_FILENAMES,
        *(f"{CAD_SUBDIR}/{name}" for name in SHEET_FILENAMES.values()),
        f"{FABRICATION_SUBDIR}/{CUT_LIST_FILENAME}",
    ]


def check_revision_binding(structure_path: Path, cut_list_path: Path) -> list[str]:
    """The cut list must carry the same revision identity as the canonical structure.json."""
    if not (structure_path.is_file() and cut_list_path.is_file()):
        return []  # absence is reported by the required-files check
    meta = json.loads(structure_path.read_text(encoding="utf-8")).get("meta", {})
    cut_list = json.loads(cut_list_path.read_text(encoding="utf-8"))
    mismatched = [
        key for key in ("revision_id", "revision_hash") if cut_list.get(key) != meta.get(key)
    ]
    return [
        f"REVISION_MISMATCH: {FABRICATION_SUBDIR}/{CUT_LIST_FILENAME} {key} {cut_list.get(key)!r} "
        f"!= structure.json meta.{key} {meta.get(key)!r}"
        for key in mismatched
    ]


def _check_svg_consistency(outputs_path: str) -> list[str]:
    """SVG sheets must agree on generation date and project title."""
    dates: set[str] = set()
    titles: set[str] = set()
    for svg in glob.glob(os.path.join(outputs_path, "**", "*.svg"), recursive=True):
        with open(svg, encoding="utf-8") as f:
            content = f.read()
        date_match = re.search(r"data-date=[\"'](.*?)[\"']", content)
        title_match = re.search(r"data-title=[\"'](.*?)[\"']", content)
        if date_match:
            dates.add(date_match.group(1))
        if title_match:
            titles.add(title_match.group(1))
    errors = []
    if len(dates) > 1:
        errors.append(f"INCONSISTENT_DATES: Found multiple generation dates in SVGs: {dates}")
    if len(titles) > 1:
        errors.append(f"INCONSISTENT_TITLES: Found multiple project titles in SVGs: {titles}")
    return errors


def validate_package(staging_path: Optional[Path] = None, outputs_path: Optional[Path] = None) -> list[str]:
    """Validates the assembled package; returns a list of error strings (empty when consistent)."""
    s_dir = Path(staging_path) if staging_path is not None else staging_dir()
    o_dir = Path(outputs_path) if outputs_path is not None else outputs_dir()
    if not o_dir.exists():
        return ["Outputs directory not found"]

    errors = [
        f"MISSING_OUTPUT: {rel} was not generated."
        for rel in _required_files()
        if not (o_dir / rel).exists()
    ]
    if not glob.glob(str(o_dir / "high-resolution-image" / "*_render_*.png")):
        errors.append("MISSING_RENDERS: No photorealistic renders found in outputs/high-resolution-image/")
    errors.extend(_check_svg_consistency(str(o_dir)))
    errors.extend(check_revision_binding(s_dir / "structure.json", o_dir / FABRICATION_SUBDIR / CUT_LIST_FILENAME))
    return errors


if __name__ == "__main__":
    validation_errors = validate_package()
    if validation_errors:
        print("PACKAGE CONSISTENCY VALIDATION FAILED:")
        for e in validation_errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    print("PACKAGE CONSISTENCY VALIDATION PASSED ✓")
    sys.exit(0)
