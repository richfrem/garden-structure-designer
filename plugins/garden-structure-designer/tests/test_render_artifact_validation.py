"""Tests for Option C render artifact validation across vector blueprints and raster presentation sheets."""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import render_drawings as rd  # type: ignore[import]  # noqa: E402
import svg_validator as sv  # type: ignore[import]  # noqa: E402

FIXTURE_PATH = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "rendering"
    / "hex_10ft_yellow_cedar.structure.json"
)


def test_all_eight_sheets_pass_svg_validator(tmp_path: Path):
    """Verify all 8 sheets produced by Option C pass svg_validator completely with 0 errors."""
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        structure_data = json.load(f)

    rd.render_all_sheets(structure_data, tmp_path)

    for sheet_name in rd.SVG_SHEET_FILENAMES:
        sheet_path = tmp_path / sheet_name
        assert sheet_path.exists()
        errors = sv.validate(str(sheet_path), str(FIXTURE_PATH))
        assert errors == [], f"Validation errors on {sheet_name}: {errors}"


def test_all_eight_sheets_pass_content_validator(tmp_path: Path):
    """Verify all 8 Option C sheets pass drawing_content_validator (raster sheets via canvas + labels)."""
    import drawing_content_validator as dcv  # type: ignore[import]

    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        structure_data = json.load(f)

    rd.render_all_sheets(structure_data, tmp_path)

    for sheet_name in rd.SVG_SHEET_FILENAMES:
        errors, _ = dcv.validate(str(tmp_path / sheet_name), str(FIXTURE_PATH))
        assert errors == [], f"Content errors on {sheet_name}: {errors}"
