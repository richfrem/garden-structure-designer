"""build123d solid backend: resolved_model translation with no silent structural defaults."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
b3d = pytest.importorskip("build123d")
import cad_backend_build123d as backend  # type: ignore[import]  # noqa: E402
from constants import MM_PER_FOOT  # type: ignore[import]  # noqa: E402

STRUCTURE = {
    "structure": {"sides": 8},
    "layout": {"post_count": 8},
    "members": {"posts": {"actual_width_in": 5.5, "actual_depth_in": 5.5}},
    "geometry": {
        "joints": {
            "z_planes": {"Z_APEX": 9.0},
            "hub": {"radius_ft": 0.5, "height_ft": 0.8},
            "resolved_model": {
                "constraints_resolved": True,
                "members": [
                    {"id": "P1", "role": "post", "p0": [0, 0, 0], "p1": [0, 0, 10],
                     "axis_u": [0, 0, 1], "axis_d": [1, 0, 0]},
                    {"id": "HUB", "role": "hub"},
                ],
            },
        }
    },
}


def test_member_length_uses_mm_per_foot():
    solid = backend.build_member_solid(STRUCTURE["geometry"]["joints"]["resolved_model"]["members"][0], STRUCTURE, MM_PER_FOOT)
    assert solid.bounding_box().size.Z == pytest.approx(10 * MM_PER_FOOT, rel=1e-6)


def test_missing_section_size_fails_closed():
    structure = copy.deepcopy(STRUCTURE)
    del structure["members"]["posts"]["actual_width_in"]
    member = structure["geometry"]["joints"]["resolved_model"]["members"][0]
    with pytest.raises(ValueError, match="members.posts.actual_width_in"):
        backend.build_member_solid(member, structure, MM_PER_FOOT)


def test_hub_polygon_side_count_follows_structure_sides():
    model = backend.build_cad_model(STRUCTURE)
    hub = next(s for s in model.children if s.label == "HUB")
    assert len(hub.faces()) == STRUCTURE["structure"]["sides"] + 2  # N side faces + 2 caps


def test_missing_z_apex_fails_closed_when_hub_present():
    structure = copy.deepcopy(STRUCTURE)
    del structure["geometry"]["joints"]["z_planes"]["Z_APEX"]
    with pytest.raises(ValueError, match="Z_APEX"):
        backend.build_cad_model(structure)


def test_missing_sides_fails_closed():
    structure = copy.deepcopy(STRUCTURE)
    del structure["structure"]["sides"]
    with pytest.raises(ValueError, match="structure.sides"):
        backend.build_cad_model(structure)
