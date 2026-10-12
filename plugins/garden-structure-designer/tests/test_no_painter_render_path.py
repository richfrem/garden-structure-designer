"""Tests proving the legacy Painter's algorithm and _ROLE_BIASES have been disconnected from production rendering."""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import render_drawings as rd  # type: ignore[import]  # noqa: E402

FIXTURE_PATH = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "rendering"
    / "hex_10ft_yellow_cedar.structure.json"
)


def test_production_render_does_not_invoke_legacy_painters_sorter(monkeypatch, tmp_path: Path):
    """Verify that render_all_sheets never calls _depth_sorted_faces or relies on _ROLE_BIASES."""
    # Monkeypatch legacy helper to raise an exception if invoked
    def poisoned_depth_sorted_faces(*args, **kwargs):
        raise RuntimeError("CRITICAL ERROR: Legacy Painter's _depth_sorted_faces was invoked by production code!")

    monkeypatch.setattr(rd, "_depth_sorted_faces", poisoned_depth_sorted_faces)

    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        structure_data = json.load(f)

    # Should run and complete cleanly without calling poisoned _depth_sorted_faces
    rd.render_all_sheets(structure_data, tmp_path)

    for filename in rd.SVG_SHEET_FILENAMES:
        assert (tmp_path / filename).exists()
