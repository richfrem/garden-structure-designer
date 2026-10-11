"""
M0 failing reproduction tests (TDD red) for the topology fail-closed contract.

Contract the not-yet-written stages MUST satisfy (both are stage callables of
the ``pipeline_runner`` seam, ``(structure, reports_dir, outputs_dir) -> dict``,
returning ``{"error_code": ..., "error_message": ...}`` on failure):

    validate_topology_intent.run_stage   -> Stage 0.5
    topology_compiler.run_stage          -> Stage 2

Stage 1 (geometry solve) is simulated by injecting a fixed geometry block so the
Stage 2 invariants are exercised against solved output, not intent.
"""
import copy
import importlib
import json
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from pipeline_runner import STAGE_ORDER, TopologyErrorCode, run_pipeline

DOWNSTREAM_OF_STAGE_2 = ("3", "4", "5.5", "6", "7")
DOWNSTREAM_OF_STAGE_0_5 = ("1", "2") + DOWNSTREAM_OF_STAGE_2

HEX_POST_XY = [
    [10.0, 0.0],
    [5.0, 8.66],
    [-5.0, 8.66],
    [-10.0, 0.0],
    [-5.0, -8.66],
    [5.0, -8.66],
]


def _valid_intent(**overrides):
    structure = {
        "meta": {"topology_family": "RadialHubTopology"},
        "structure": {"sides": 6},
        "layout": {"post_count": 6},
    }
    for dotpath, value in overrides.items():
        section, key = dotpath.split("__")
        structure[section][key] = value
    return structure


def _valid_geometry():
    return {
        "_sealed": True,
        "joints": {
            "layout": {
                "post_count": 6,
                "post_xy": copy.deepcopy(HEX_POST_XY),
                "beam_segments": [
                    {"id": f"B{i + 1}", "i0": i, "i1": (i + 1) % 6} for i in range(6)
                ],
            },
            "hub": {
                "type": "hexagonal_prism",
                "face_planes": {"planes": [{"id": f"H{i + 1}"} for i in range(6)]},
            },
            "primary_rafters": [{"id": f"R{i + 1}"} for i in range(6)],
            "rafters": {"primary_rafters": [{"id": f"R{i + 1}"} for i in range(6)]},
            "braces": {"enabled": False, "endpoints": []},
        },
    }


def _geometry_with(mutator):
    geometry = _valid_geometry()
    mutator(geometry["joints"])
    return geometry


def _post_xy_of_size(count):
    def mutate(joints):
        joints["layout"]["post_xy"] = copy.deepcopy(HEX_POST_XY[:count]) + [
            [float(i), float(-i)] for i in range(len(HEX_POST_XY), count)
        ]
    return mutate


def _stage_0_5():
    return importlib.import_module("validate_topology_intent").run_stage


def _stage_2():
    return importlib.import_module("topology_compiler").run_stage


def _run(tmp_path, intent, geometry=None, spies=None):
    """Run the real Stage 0.5 / Stage 2 with an injected Stage 1 geometry."""
    structure_path = tmp_path / "structure.json"
    structure_path.write_text(json.dumps(intent))

    def stage_1(structure, reports_dir, outputs_dir):
        solved = copy.deepcopy(structure)
        solved["geometry"] = copy.deepcopy(geometry if geometry is not None else _valid_geometry())
        return solved

    stages = {name: spies[name] for name in (spies or {})}
    stages["0.5"] = _stage_0_5()
    stages["1"] = stage_1
    stages["2"] = _stage_2()
    return run_pipeline(
        structure_path,
        stages=stages,
        reports_dir=tmp_path / "reports",
        outputs_dir=tmp_path / "outputs",
    )


def _assert_failed_closed(result, code, stage):
    assert result.success is False
    assert result.error_code == code.value
    assert result.failed_stage == stage


# ---------------------------------------------------------------------------
# T2.1 — Stage 0.5: intent validation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("post_count", [5, 8])
def test_t2_1_sides_vs_post_count_mismatch_fails_at_stage_0_5(tmp_path, post_count):
    result = _run(tmp_path, _valid_intent(layout__post_count=post_count))
    _assert_failed_closed(result, TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH, "0.5")


def test_t2_1_reserved_family_is_not_implemented(tmp_path):
    intent = _valid_intent()
    intent["meta"]["topology_family"] = "OrthogonalGridTopology"
    result = _run(tmp_path, intent)
    _assert_failed_closed(result, TopologyErrorCode.TOPOLOGY_NOT_IMPLEMENTED, "0.5")


def test_t2_1_unknown_family_is_rejected(tmp_path):
    intent = _valid_intent()
    intent["meta"]["topology_family"] = "NonExistent"
    result = _run(tmp_path, intent)
    _assert_failed_closed(result, TopologyErrorCode.UNKNOWN_TOPOLOGY_FAMILY, "0.5")


# ---------------------------------------------------------------------------
# T2.2 — Stage 2: solved geometry cardinality drift
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("actual_posts", [5, 8])
def test_t2_2_solved_post_xy_drift_fails_at_stage_2(tmp_path, actual_posts):
    geometry = _geometry_with(_post_xy_of_size(actual_posts))
    geometry["joints"]["layout"]["post_count"] = actual_posts
    result = _run(tmp_path, _valid_intent(), geometry)
    _assert_failed_closed(result, TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH, "2")


def test_t2_2_cached_scalar_cannot_hide_array_drift(tmp_path):
    geometry = _geometry_with(_post_xy_of_size(5))
    assert geometry["joints"]["layout"]["post_count"] == 6
    result = _run(tmp_path, _valid_intent(), geometry)
    _assert_failed_closed(result, TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH, "2")


# ---------------------------------------------------------------------------
# T2.3 — Stage 2: member / connection graph violations
# ---------------------------------------------------------------------------

def test_t2_3_duplicate_beam_id_fails(tmp_path):
    def duplicate_b1(joints):
        joints["layout"]["beam_segments"][1]["id"] = "B1"

    result = _run(tmp_path, _valid_intent(), _geometry_with(duplicate_b1))
    _assert_failed_closed(result, TopologyErrorCode.DUPLICATE_MEMBER_ID, "2")


def test_t2_3_beam_referencing_missing_post_is_dangling(tmp_path):
    # Post cardinality stays 6 so the failure isolates the connection graph:
    # B6 is retained but its end post index points past the last post.
    def dangle_b6(joints):
        joints["layout"]["beam_segments"][5]["i1"] = 6

    result = _run(tmp_path, _valid_intent(), _geometry_with(dangle_b6))
    _assert_failed_closed(result, TopologyErrorCode.DANGLING_CONNECTION_ENDPOINT, "2")


def test_t2_3_rafters_without_hub_member_is_dangling(tmp_path):
    def remove_hub(joints):
        joints["hub"] = {"type": "none"}

    result = _run(tmp_path, _valid_intent(), _geometry_with(remove_hub))
    _assert_failed_closed(result, TopologyErrorCode.DANGLING_CONNECTION_ENDPOINT, "2")


# ---------------------------------------------------------------------------
# T2.4 — Downstream stages never run after a failure
# ---------------------------------------------------------------------------

def _spies(calls, names):
    def make(name):
        def spy(structure, reports_dir, outputs_dir):
            calls.append(name)
            return structure
        return spy
    return {name: make(name) for name in names}


def test_t2_4_stage_0_5_failure_invokes_no_downstream_stage(tmp_path):
    calls = []
    spies = _spies(calls, DOWNSTREAM_OF_STAGE_2)
    result = _run(tmp_path, _valid_intent(layout__post_count=5), spies=spies)

    _assert_failed_closed(result, TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH, "0.5")
    assert calls == []
    assert not set(DOWNSTREAM_OF_STAGE_0_5) & set(result.completed_stages)


def test_t2_4_stage_2_failure_invokes_no_downstream_stage(tmp_path):
    calls = []
    spies = _spies(calls, DOWNSTREAM_OF_STAGE_2)
    result = _run(tmp_path, _valid_intent(), _geometry_with(_post_xy_of_size(5)), spies=spies)

    _assert_failed_closed(result, TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH, "2")
    assert calls == []
    assert "0.5" in result.completed_stages
    assert not set(DOWNSTREAM_OF_STAGE_2) & set(result.completed_stages)


# ---------------------------------------------------------------------------
# T2.5 — Valid baseline passes
# ---------------------------------------------------------------------------

def test_t2_5_valid_hexagon_passes_stage_0_5_and_stage_2(tmp_path):
    result = _run(tmp_path, _valid_intent())

    assert result.success is True, result.error_message
    assert result.error_code is None
    assert result.failed_stage is None
    assert result.completed_stages == list(STAGE_ORDER)


def test_t2_5_valid_hexagon_runs_downstream_stages(tmp_path):
    calls = []
    spies = _spies(calls, DOWNSTREAM_OF_STAGE_2)
    result = _run(tmp_path, _valid_intent(), spies=spies)

    assert result.success is True, result.error_message
    assert sorted(calls) == sorted(DOWNSTREAM_OF_STAGE_2)
