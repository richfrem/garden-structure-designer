"""run_obstacle_triage: classify why a run is blocked and recommend the next action (incl. C5 recovery / stale approval)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import run_obstacle_triage as triage  # type: ignore[import]  # noqa: E402


@pytest.fixture
def env(tmp_path, monkeypatch):
    staging, outputs, plugin = tmp_path / "context" / "staging", tmp_path / "outputs", tmp_path / "plugins" / "gsd"
    staging.mkdir(parents=True)
    outputs.mkdir()
    plugin.mkdir(parents=True)
    monkeypatch.setattr(triage, "staging_dir", lambda: staging)
    monkeypatch.setattr(triage, "outputs_dir", lambda: outputs)
    monkeypatch.setattr(triage, "plugin_root", lambda: plugin)
    return {"staging": staging, "outputs": outputs, "plugin": plugin}


def _run(env):
    triage.main()
    return json.loads((env["staging"] / "obstacle-triage-report.json").read_text())


def test_missing_structure_json(env):
    report = _run(env)
    assert "MISSING_STAGING_ARTIFACT" in report["failure_classification"]
    assert report["recommended_next_action"] == "RERUN_REPORTS_FIRST"
    assert (env["outputs"] / "obstacle-triage-report.md").exists()


def test_split_staging_is_detected_first(env):
    legacy = env["plugin"] / "context" / "staging"
    legacy.mkdir(parents=True)
    (legacy / "structure.json").write_text("{}")
    (env["staging"] / "structure.json").write_text("{}")
    report = _run(env)
    assert "PATH_SPLIT" in report["failure_classification"]
    assert report["recommended_next_action"] == "FIX_PATHS_FIRST"
    assert report["conflicting_staging_paths"] == [str(legacy)]


def test_dashboard_claiming_completion_without_approval(env):
    (env["staging"] / "structure.json").write_text("{}")
    (env["outputs"] / "quality-dashboard.md").write_text("Overall status: COMPLETED")
    assert "DASHBOARD_STALE_OR_WRONG_PATH" in _run(env)["failure_classification"]


def test_placeholder_svgs(env):
    (env["staging"] / "structure.json").write_text("{}")
    (env["staging"] / "drawing-red-team-report.json").write_text(json.dumps({"may_claim_success": False}))
    (env["outputs"] / "drawing-plan-view.svg").write_text("<svg/>")
    report = _run(env)
    assert "RENDERER_PLACEHOLDER_OUTPUT" in report["failure_classification"]
    assert report["recommended_next_action"] == "FIX_RENDERER_FIRST"


def test_unknown_obstacle_blocks_and_reports(env):
    (env["staging"] / "structure.json").write_text("{}")
    report = _run(env)
    assert report["failure_classification"] == ["UNKNOWN_OBSTACLE"]
    assert report["recommended_next_action"] == "BLOCK_AND_REPORT"
    assert "Do not claim PASS" in report["do_not_do"]


def test_committing_journal_means_recovery_required(env):
    (env["staging"] / "structure.json").write_text("{}")
    journal = env["staging"] / "journal"
    journal.mkdir()
    (journal / "t1.json").write_text(json.dumps({"txn_id": "t1", "state": "COMMITTING"}))
    report = _run(env)
    assert "RECOVERY_REQUIRED" in report["failure_classification"]
    assert report["recommended_next_action"] == "RUN_RECOVERY_FIRST"


def test_committed_journals_are_not_an_obstacle(env):
    (env["staging"] / "structure.json").write_text("{}")
    journal = env["staging"] / "journal"
    journal.mkdir()
    (journal / "t1.json").write_text(json.dumps({"txn_id": "t1", "state": "COMMITTED"}))
    assert "RECOVERY_REQUIRED" not in _run(env)["failure_classification"]


def test_approval_for_another_revision_is_stale(env):
    from revision_identity import stamp_revision

    structure = stamp_revision({"layout": {"post_count": 6}})
    (env["staging"] / "structure.json").write_text(json.dumps(structure))
    (env["staging"] / "drawing-red-team-report.json").write_text(json.dumps(
        {"may_claim_success": True, "revision_id": "old", "revision_hash": "0" * 64, "hash_algorithm": "gsd-json-v1"}))
    report = _run(env)
    assert "STALE_APPROVAL" in report["failure_classification"]
    assert report["recommended_next_action"] == "RERUN_REPORTS_FIRST"
