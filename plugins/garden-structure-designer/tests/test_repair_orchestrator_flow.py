"""repair_orchestrator decision flow: classify -> gate (human review / locked / halted / retryable) -> act -> validate."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import repair_orchestrator as ro  # type: ignore[import]  # noqa: E402


@pytest.fixture
def env(tmp_path, monkeypatch):
    staging, scripts, outputs, plugin = tmp_path / "staging", tmp_path / "scripts", tmp_path / "outputs", tmp_path / "plugin"
    for d in (staging, scripts, outputs, plugin):
        d.mkdir()
    (staging / "structure.json").write_text(json.dumps({"geometry": {"_sealed": False}}))
    (plugin / "repair-map.json").write_text("{}")
    calls, recorded, state = [], [], {"returncode": 0, "halt": False}

    def fake_run(cmd, **kwargs):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, state["returncode"], stdout="", stderr="")

    for name, value in {"staging_dir": lambda: staging, "scripts_dir": lambda: scripts, "outputs_dir": lambda: outputs,
                        "plugin_root": lambda: plugin}.items():
        monkeypatch.setattr(ro, name, value)
    monkeypatch.setattr(ro.subprocess, "run", fake_run)
    monkeypatch.setattr(ro, "record_run", lambda *a, **k: recorded.append(a))
    monkeypatch.setattr(ro, "should_halt", lambda *a, **k: state["halt"])
    return {"staging": staging, "plugin": plugin, "calls": calls, "recorded": recorded, "state": state}


def _repair(env, axes, monkeypatch, repair_map=None):
    (env["staging"] / "drift_report.json").write_text(json.dumps({"failed_axes": axes}))
    if repair_map is not None:
        (env["plugin"] / "repair-map.json").write_text(json.dumps(repair_map))
    monkeypatch.setattr(sys, "argv", ["repair_orchestrator.py"])
    ro.main()
    return json.loads((env["staging"] / "repair-report.json").read_text())


def test_no_drift_report_exits_cleanly(env, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["repair_orchestrator.py"])
    with pytest.raises(SystemExit) as info:
        ro.main()
    assert info.value.code == 0


def test_drawing_axis_reruns_renderer_then_validates(env, monkeypatch):
    report = _repair(env, ["svg_coordinate drift"], monkeypatch)
    assert report["status"] == "PASS" and report["attempts"][0]["repair_stage"] == "drawing-generator"
    assert any("render_drawings.py" in " ".join(c) for c in env["calls"])
    assert any("svg_validator.py" in " ".join(c) for c in env["calls"])


def test_failed_command_marks_report_fail(env, monkeypatch):
    env["state"]["returncode"] = 1
    report = _repair(env, ["svg_coordinate drift"], monkeypatch)
    assert report["status"] == "FAIL" and report["remaining_failures"] == ["svg_coordinate drift"]


def test_human_review_axis_is_blocked_without_running_anything(env, monkeypatch):
    report = _repair(env, ["deflection exceeds limit"], monkeypatch)
    assert report["status"] == "BLOCKED" and env["calls"] == []


def test_sealed_geometry_blocks_structural_repair(env, monkeypatch):
    (env["staging"] / "structure.json").write_text(json.dumps({"geometry": {"_sealed": True}}))
    report = _repair(env, ["beam miter mismatch"], monkeypatch)
    assert report["status"] == "BLOCKED" and env["calls"] == []


def test_repeated_failures_halt_the_repair(env, monkeypatch):
    env["state"]["halt"] = True
    report = _repair(env, ["svg_coordinate drift"], monkeypatch)
    assert report["status"] == "BLOCKED" and env["calls"] == []


def test_repair_map_action_overrides_the_stage_default(env, monkeypatch):
    _repair(env, ["svg_coordinate drift"], monkeypatch, repair_map={"svg_coordinate drift": {"action": "python3 /x/custom.py"}})
    assert env["recorded"][0][0] == "custom.py"


def test_non_retryable_structured_errors_are_never_auto_repaired(env, monkeypatch):
    report = _repair(env, ["TOPOLOGY_CARDINALITY_MISMATCH: Expected 6 beams"], monkeypatch)
    assert report["status"] == "BLOCKED" and env["calls"] == []
