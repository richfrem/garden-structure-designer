"""C2 Stage 2 contract: actual arrays (never cached scalars), typed counts, polygon regularity, face ids."""
from __future__ import annotations

import copy
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from test_topology_invariants import (  # type: ignore[import]  # noqa: E402
    _assert_failed_closed,
    _geometry_with,
    _run,
    _valid_intent,
)
from pipeline_runner import TopologyErrorCode  # type: ignore[import]  # noqa: E402

CARD = TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH


def _ok(result):
    assert result.success, (result.error_code, result.error_message)
    return result.structure["geometry"]["joints"]["topology"]


def test_valid_hexagon_builds_rafters_from_the_array(tmp_path):
    topology = _ok(_run(tmp_path, _valid_intent()))
    assert [m["id"] for m in topology["members"] if m["type"] == "rafter"] == [f"R{i}" for i in range(1, 7)]
    hub_faces = {c["from"]: c["hub_face"] for c in topology["connections"] if c["type"] == "rafter_face_to_hub"}
    assert hub_faces == {f"R{i}": f"H{i}" for i in range(1, 7)}


def test_missing_rafter_array_cannot_hide_behind_scalar(tmp_path):
    def drop(joints):
        joints["primary_rafters"] = []
        joints["rafters"] = {"primary_count": 6, "primary_rafters": []}

    _assert_failed_closed(_run(tmp_path, _valid_intent(), _geometry_with(drop)), CARD, "2")


def test_five_rafters_for_six_sides_fail(tmp_path):
    def drop_one(joints):
        joints["primary_rafters"] = joints["primary_rafters"][:5]
        joints["rafters"]["primary_rafters"] = joints["primary_rafters"]

    _assert_failed_closed(_run(tmp_path, _valid_intent(), _geometry_with(drop_one)), CARD, "2")


def test_rafter_mirror_must_equal_canonical_array(tmp_path):
    def diverge(joints):
        joints["rafters"]["primary_rafters"] = [{"id": f"R{i}", "extra": 1} for i in range(1, 7)]

    result = _run(tmp_path, _valid_intent(), _geometry_with(diverge))
    _assert_failed_closed(result, TopologyErrorCode.GEOMETRY_INVALID, "2")


def test_five_beams_for_six_sides_fail(tmp_path):
    def drop_beam(joints):
        joints["layout"]["beam_segments"] = joints["layout"]["beam_segments"][:5]

    _assert_failed_closed(_run(tmp_path, _valid_intent(), _geometry_with(drop_beam)), CARD, "2")


def test_missing_hub_face_for_a_rafter_is_dangling(tmp_path):
    def drop_face(joints):
        joints["hub"]["face_planes"]["planes"] = joints["hub"]["face_planes"]["planes"][:5]

    result = _run(tmp_path, _valid_intent(), _geometry_with(drop_face))
    _assert_failed_closed(result, TopologyErrorCode.DANGLING_CONNECTION_ENDPOINT, "2")


def test_enabled_bracing_requires_two_braces_per_post(tmp_path):
    def enable(joints):
        joints["braces"] = {"enabled": True, "endpoints": [{"id": f"K{i}A"} for i in range(1, 7)]}

    _assert_failed_closed(_run(tmp_path, _valid_intent(), _geometry_with(enable)), CARD, "2")


def test_disabled_bracing_with_braces_present_fails(tmp_path):
    def stray(joints):
        joints["braces"] = {"enabled": False, "endpoints": [{"id": "K1A"}]}

    _assert_failed_closed(_run(tmp_path, _valid_intent(), _geometry_with(stray)), CARD, "2")


def test_irregular_polygon_fails(tmp_path):
    def skew(joints):
        joints["layout"]["post_xy"][2] = [-5.0, 9.5]

    result = _run(tmp_path, _valid_intent(), _geometry_with(skew))
    _assert_failed_closed(result, TopologyErrorCode.GEOMETRY_INVALID, "2")


def test_non_finite_post_coordinate_fails(tmp_path):
    def poison(joints):
        joints["layout"]["post_xy"][0] = [math.nan, 0.0]

    result = _run(tmp_path, _valid_intent(), _geometry_with(poison))
    _assert_failed_closed(result, TopologyErrorCode.GEOMETRY_INVALID, "2")
