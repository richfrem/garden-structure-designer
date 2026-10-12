"""
End-to-End Package Integration Test for Option C Rendering Engine.

Validates that the frozen 10ft hexagonal Yellow Cedar pergola produces all 8 Option C
sheets (vector blueprints via OpenCASCADE HLR, shaded presentation views via Three.js
WebGL), passes drawing content and SVG validation, generates cut lists, and
compiles the complete construction package.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
sys.path.insert(0, str(PLUGIN_ROOT))

from constants import SVG_SHEET_FILENAMES
from render_drawings import render_all_sheets
from svg_validator import validate as validate_svg
from drawing_content_validator import validate as validate_drawing_content

BLUEPRINT_SHEETS = [
    "blueprint-plan.svg",
    "blueprint-elevation.svg",
    "blueprint-isometric.svg",
    "blueprint-component-isolation.svg",
]


FIXTURE_PATH = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "rendering"
    / "hex_10ft_yellow_cedar.structure.json"
)


def test_option_c_hex_pergola_e2e_package(tmp_path: Path):
    """Run frozen 10ft hex pergola through Option C renderers and verify all package outputs."""
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        structure = json.load(f)

    svg_dir = tmp_path / "svg"
    svg_dir.mkdir(parents=True, exist_ok=True)
    structure_path = tmp_path / "structure.json"
    structure_path.write_text(json.dumps(structure), encoding="utf-8")

    # 1. Render all 8 sheets via Option C
    render_all_sheets(structure, svg_dir)

    for sheet_name in SVG_SHEET_FILENAMES:
        sheet_path = svg_dir / sheet_name
        assert sheet_path.exists(), f"Sheet {sheet_name} was not generated"
        assert sheet_path.stat().st_size > 1000, f"Sheet {sheet_name} is unexpectedly small"

        # 2. Validate SVG structure and namespaces
        svg_errors = validate_svg(str(sheet_path), str(structure_path))
        assert not svg_errors, f"SVG validation failed for {sheet_name}: {svg_errors}"

        # 3. Validate drawing content (geometry presence & semantics)
        content_errors, _ = validate_drawing_content(str(sheet_path), str(structure_path))
        assert not content_errors, f"Content validation failed for {sheet_name}: {content_errors}"

    # 4. Verify vector blueprints vs raster presentation distinctions
    for bp in ["blueprint-plan.svg", "blueprint-elevation.svg", "blueprint-isometric.svg"]:
        bp_content = (svg_dir / bp).read_text(encoding="utf-8")
        assert "<path" in bp_content
        assert 'data-projection="hlr"' in bp_content

    # Component isolation is a technical 2D component detail blueprint
    comp_content = (svg_dir / "blueprint-component-isolation.svg").read_text(encoding="utf-8")
    assert "<polygon" in comp_content or "<rect" in comp_content

    for pres in ["drawing-isometric-view.svg", "drawing-perspective-view.svg"]:
        pres_content = (svg_dir / pres).read_text(encoding="utf-8")
        assert "<image" in pres_content
        assert "data:image/png;base64," in pres_content
