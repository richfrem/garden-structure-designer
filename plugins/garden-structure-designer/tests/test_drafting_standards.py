"""Invariant tests for scripts/constants.py and parity across the drafting tools."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import constants as C  # type: ignore[import]  # noqa: E402
import exchange_writer  # type: ignore[import]  # noqa: E402
import export_cad  # type: ignore[import]  # noqa: E402
import render_drawings  # type: ignore[import]  # noqa: E402


def test_unit_conversions_are_consistent():
    assert C.MM_PER_FOOT == pytest.approx(C.MM_PER_INCH * C.INCHES_PER_FOOT)
    assert C.MM_PER_UNIT["feet"] == C.MM_PER_UNIT["ft"] == C.MM_PER_FOOT
    assert C.MM_PER_UNIT["mm"] == 1.0


def test_layer_table_covers_every_role_and_dimensions():
    assert set(C.ROLE_LAYERS.values()) | {C.DIMENSION_LAYER} == set(C.LAYER_COLORS)
    assert len(set(C.LAYER_COLORS.values())) == len(C.LAYER_COLORS)


def test_sheet_ids_and_filenames_align():
    assert set(C.SHEET_FILENAMES) == set(C.SHEET_IDS)
    assert all(name.startswith(sheet) and name.endswith(".dxf") for sheet, name in C.SHEET_FILENAMES.items())


def test_lineweights_positive_and_blueprint_heavier():
    weights = [v for k, v in vars(C).items() if k.startswith("LW_")]
    assert weights and all(w > 0 for w in weights)
    assert C.LW_MEMBER_BLUEPRINT > C.LW_MEMBER_DRAWING


def test_dimension_standards_positive():
    assert C.DIM_OFFSET_MM > 0 and C.DIM_TEXT_HEIGHT_MM > 0 and C.DIM_TICK_OFFSET_MM > 0


def test_tolerances_ordered():
    assert 0 < C.DXF_PLANAR_TOL_MM < C.DXF_BOUNDS_TOL_MM <= C.DIM_CROSSCHECK_TOL_MM


@pytest.mark.parametrize("name", [
    "APPID", "DIM_OFFSET_MM", "DIM_TEXT_HEIGHT_MM", "DIMENSION_LAYER", "INSUNITS_MM",
    "LAYER_COLORS", "MM_PER_UNIT", "ROLE_LAYERS", "SHEET_IDS",
])
def test_exchange_writer_reuses_constants(name):
    assert getattr(exchange_writer, name) is getattr(C, name)


def test_export_cad_reuses_sheet_filenames():
    assert export_cad.SHEET_FILENAMES is C.SHEET_FILENAMES


@pytest.mark.parametrize("name", [k for k in vars(C) if k.startswith("LW_")])
def test_render_drawings_lineweights_match_constants(name):
    assert getattr(render_drawings, name) == getattr(C, name)


def test_render_drawings_has_no_hardcoded_lineweight_literals():
    source = (Path(render_drawings.__file__)).read_text()
    helpers = source[source.index("def draw_title_block"):source.index("def draw_validator_anchors")]
    helpers += source[source.index("def draw_dimension"):source.index("# --- Page Renderers ---")]
    assert not re.search(r'stroke-width="[\d.]+"', helpers)
