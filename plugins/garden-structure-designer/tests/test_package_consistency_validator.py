"""Package consistency: all eight SVGs, both DXFs, the fabrication cut list, renders, and one revision."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from constants import CAD_SUBDIR, SHEET_FILENAMES, SVG_SHEET_FILENAMES  # type: ignore[import]  # noqa: E402
from package_consistency_validator import validate_package  # type: ignore[import]  # noqa: E402

REV = {"revision_id": "rev-1", "revision_hash": "hash-1"}


@pytest.fixture
def package(tmp_path):
    staging, outputs = tmp_path / "staging", tmp_path / "outputs"
    (outputs / "fabrication").mkdir(parents=True)
    (outputs / CAD_SUBDIR).mkdir()
    (outputs / "high-resolution-image").mkdir()
    staging.mkdir()
    (staging / "structure.json").write_text(json.dumps({"meta": REV}))
    for name in SVG_SHEET_FILENAMES:
        (outputs / name).write_text('<svg data-date="2026-10-11" data-title="Gazebo"/>')
    for name in SHEET_FILENAMES.values():
        (outputs / CAD_SUBDIR / name).write_text("0\nEOF\n")
    (outputs / "fabrication" / "cut-list.json").write_text(json.dumps(REV))
    (outputs / "high-resolution-image" / "pergola_render_1.png").write_bytes(b"png")
    return staging, outputs


def test_complete_package_passes(package):
    assert validate_package(*package) == []


@pytest.mark.parametrize("rel", [*SVG_SHEET_FILENAMES, f"{CAD_SUBDIR}/SB01-structure.dxf",
                                  f"{CAD_SUBDIR}/SB02-plan.dxf", "fabrication/cut-list.json"])
def test_each_required_deliverable_is_enforced(package, rel):
    staging, outputs = package
    (outputs / rel).unlink()
    assert any(f"MISSING_OUTPUT: {rel}" in e for e in validate_package(staging, outputs))


def test_legacy_shop_blueprint_cut_list_is_not_required(package):
    staging, outputs = package
    assert not (outputs / "shop-blueprint").exists()
    assert not any("shop-blueprint" in e for e in validate_package(staging, outputs))


def test_cut_list_from_another_revision_is_rejected(package):
    staging, outputs = package
    (outputs / "fabrication" / "cut-list.json").write_text(json.dumps({"revision_id": "rev-0", "revision_hash": "hash-0"}))
    assert any(e.startswith("REVISION_MISMATCH") for e in validate_package(staging, outputs))


def test_inconsistent_svg_titles_still_detected(package):
    staging, outputs = package
    (outputs / SVG_SHEET_FILENAMES[0]).write_text('<svg data-date="2026-10-11" data-title="Other"/>')
    assert any(e.startswith("INCONSISTENT_TITLES") for e in validate_package(staging, outputs))
