"""Footing solids come from structure.json footings.diameter_in / depth_in (no hardcoded footing geometry)."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN / "scripts"))
sys.path.insert(0, str(PLUGIN))
from constants import FOOTING_STUB_ABOVE_GRADE_FT  # type: ignore[import]  # noqa: E402
from geometry_engine import compute_from_structure  # type: ignore[import]  # noqa: E402
from tests.test_geometry_engine import STRUCTURE_SEED  # type: ignore[import]  # noqa: E402


def _footings(tmp_path, **footing_overrides):
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["footings"].update(footing_overrides)
    path = tmp_path / "structure.json"
    path.write_text(json.dumps(seed))
    with contextlib.redirect_stdout(io.StringIO()):
        solved = compute_from_structure(str(path))
    return [m for m in solved["geometry"]["joints"]["resolved_model"]["members"] if m["role"] == "footing"]


def _extent(member, axis):
    values = [v[axis] for v in member["vertices"]]
    return max(values) - min(values)


def test_footing_depth_and_width_follow_the_declared_footing(tmp_path):
    footing = _footings(tmp_path, diameter_in=12, depth_in=24)[0]
    z = [v[2] for v in footing["vertices"]]
    assert min(z) == pytest.approx(-2.0) and max(z) == pytest.approx(FOOTING_STUB_ABOVE_GRADE_FT)
    assert _extent(footing, 0) == pytest.approx(1.0) and _extent(footing, 1) == pytest.approx(1.0)


def test_a_larger_footing_is_drawn_larger(tmp_path):
    footing = _footings(tmp_path, diameter_in=18, depth_in=36)[0]
    assert min(v[2] for v in footing["vertices"]) == pytest.approx(-3.0)
    assert _extent(footing, 0) == pytest.approx(1.5)


def test_one_footing_per_post(tmp_path):
    members = _footings(tmp_path)
    assert [m["id"] for m in members] == [f"FT{i}" for i in range(1, 7)]
