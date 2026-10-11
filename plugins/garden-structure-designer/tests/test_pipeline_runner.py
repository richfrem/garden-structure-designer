import json
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from pipeline_runner import STAGE_ORDER, PipelineResult, TopologyErrorCode, run_pipeline


@pytest.fixture
def structure_path(tmp_path):
    path = tmp_path / "structure.json"
    path.write_text(json.dumps({"meta": {"topology_family": "RegularPolygonTopology"}}))
    return path


def _spy(calls, name, result=None):
    def stage(structure, reports_dir, outputs_dir):
        calls.append((name, reports_dir, outputs_dir))
        return structure if result is None else result

    return stage


def test_default_stub_chain_succeeds(structure_path):
    result = run_pipeline(structure_path)
    assert isinstance(result, PipelineResult)
    assert result.success is True
    assert result.error_code is None
    assert result.failed_stage is None
    assert result.completed_stages == list(STAGE_ORDER)
    assert result.structure["meta"]["topology_family"] == "RegularPolygonTopology"


def test_failing_stage_halts_downstream(structure_path):
    calls = []
    stages = {name: _spy(calls, name) for name in STAGE_ORDER}
    stages["2"] = _spy(calls, "2", {"error_code": TopologyErrorCode.GEOMETRY_INVALID, "error_message": "bad"})

    result = run_pipeline(structure_path, stages=stages)

    assert result.success is False
    assert result.error_code == "GEOMETRY_INVALID"
    assert result.error_message == "bad"
    assert result.failed_stage == "2"
    assert result.completed_stages == ["0", "0.5", "1"]
    assert [c[0] for c in calls] == ["0", "0.5", "1", "2"]


def test_raising_stage_halts_downstream(structure_path):
    class Boom(Exception):
        error_code = TopologyErrorCode.STALE_REVISION

    def boom(structure, reports_dir, outputs_dir):
        raise Boom("stale")

    calls = []
    result = run_pipeline(
        structure_path, stages={"1": boom, "2": _spy(calls, "2")}
    )

    assert result.success is False
    assert result.error_code == "STALE_REVISION"
    assert result.failed_stage == "1"
    assert calls == []


def test_custom_dirs_are_respected(structure_path, tmp_path):
    calls = []
    reports = tmp_path / "cand" / "reports"
    outputs = tmp_path / "cand" / "outputs"

    run_pipeline(
        structure_path,
        stages={"0": _spy(calls, "0")},
        reports_dir=str(reports),
        outputs_dir=outputs,
    )

    assert calls == [("0", reports, outputs)]


def test_stop_after_stage(structure_path):
    calls = []
    result = run_pipeline(
        structure_path,
        stages={"5.5": _spy(calls, "5.5"), "5.6": _spy(calls, "5.6")},
        stop_after_stage="5.5",
    )

    assert result.success is True
    assert result.completed_stages == ["0", "0.5", "1", "2", "3", "4", "5.5"]
    assert [c[0] for c in calls] == ["5.5"]


def test_stage_output_replaces_structure(structure_path):
    result = run_pipeline(structure_path, stages={"0": _spy([], "0", {"replaced": True})})
    assert result.structure == {"replaced": True}


def test_unknown_stage_names_rejected(structure_path):
    with pytest.raises(ValueError):
        run_pipeline(structure_path, stages={"99": _spy([], "99")})
    with pytest.raises(ValueError):
        run_pipeline(structure_path, stop_after_stage="99")


def test_error_code_registry_is_exhaustive():
    assert {c.value for c in TopologyErrorCode} == {
        "TOPOLOGY_CARDINALITY_MISMATCH",
        "DUPLICATE_MEMBER_ID",
        "DANGLING_CONNECTION_ENDPOINT",
        "ATTACHMENT_GEOMETRY_MISMATCH",
        "UNKNOWN_TOPOLOGY_FAMILY",
        "TOPOLOGY_NOT_IMPLEMENTED",
        "FEATURE_NOT_IMPLEMENTED",
        "GEOMETRY_INVALID",
        "HUB_TYPE_MISMATCH",
        "STALE_REVISION",
        "RECOVERY_REQUIRED",
    }
