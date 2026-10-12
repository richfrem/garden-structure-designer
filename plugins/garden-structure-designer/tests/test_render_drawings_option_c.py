"""Tests for Option C routing of all 8 sheets through OpenCASCADE HLR and Three.js WebGL."""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import render_drawings  # type: ignore[import]  # noqa: E402
from constants import SVG_SHEET_FILENAMES  # type: ignore[import]  # noqa: E402

FIXTURE_PATH = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "rendering"
    / "hex_10ft_yellow_cedar.structure.json"
)


def test_render_all_eight_sheets_option_c(tmp_path: Path):
    """Verify render_drawings generates all 8 sheets using Option C routing."""
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        structure_data = json.load(f)

    # Render all sheets to tmp_path
    render_drawings.render_all_sheets(structure_data, tmp_path)

    for filename in SVG_SHEET_FILENAMES:
        sheet_path = tmp_path / filename
        assert sheet_path.exists(), f"Missing sheet: {filename}"
        content = sheet_path.read_text(encoding="utf-8")
        assert "<svg" in content
        assert "</svg>" in content
        assert 'data-role="title-block"' in content
        assert "VALIDATOR_ANCHORS" in content

        if filename.startswith("blueprint-"):
            # Must be vector HLR
            assert "<path" in content
            assert 'data-role=' in content
        elif filename.startswith("drawing-"):
            # Must be raster presentation WebGL
            assert "<image" in content
            assert 'data-role="presentation-canvas"' in content
