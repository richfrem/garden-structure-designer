"""generate_quality_dashboard: status is derived from the reports and only COMPLETED for an approved, current revision."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import generate_quality_dashboard as dashboard  # type: ignore[import]  # noqa: E402
from revision_identity import stamp_revision  # type: ignore[import]  # noqa: E402


@pytest.fixture
def env(tmp_path, monkeypatch):
    staging, outputs = tmp_path / "staging", tmp_path / "outputs"
    staging.mkdir()
    monkeypatch.setattr(dashboard, "staging_dir", lambda: staging)
    monkeypatch.setattr(dashboard, "outputs_dir", lambda: outputs)
    structure = stamp_revision({"layout": {"post_count": 6}})
    (staging / "structure.json").write_text(json.dumps(structure))
    return {"staging": staging, "outputs": outputs, "structure": structure}


def _approve(env, **overrides):
    meta = env["structure"]["meta"]
    report = {"status": "PASS", "may_claim_success": True, "reviewer": "run_drawing_red_team.py", "summary": "ok",
              "revision_id": meta["revision_id"], "revision_hash": meta["revision_hash"], "hash_algorithm": "gsd-json-v1"}
    report.update(overrides)
    (env["staging"] / "drawing-red-team-report.json").write_text(json.dumps(report))
    (env["staging"] / "drawing-content-report.json").write_text(json.dumps(
        {"status": "PASS", "files": [{"file": "plan.svg", "status": "PASS", "failure_codes": []}]}))


def _generate(env):
    dashboard.main()
    return (env["outputs"] / "quality-dashboard.md").read_text()


def test_approved_current_revision_is_completed(env):
    _approve(env)
    text = _generate(env)
    assert "- Overall status: COMPLETED" in text
    assert "- May claim success: true" in text
    assert "`plan.svg`: PASS" in text


def test_missing_red_team_report_is_never_completed(env):
    assert "Overall status: COMPLETED" not in _generate(env)


def test_failed_repair_blocks(env):
    _approve(env)
    (env["staging"] / "repair-report.json").write_text(json.dumps({"status": "FAIL", "attempts": []}))
    assert "- Overall status: BLOCKED / FAILED" in _generate(env)


def test_open_drift_axes_block(env):
    _approve(env)
    (env["staging"] / "drift_report.json").write_text(json.dumps({"failed_axes": ["svg_coordinate"]}))
    assert "- Overall status: BLOCKED / FAILED" in _generate(env)


def test_physics_checks_are_listed(env):
    _approve(env)
    (env["staging"] / "physics-validation-report.json").write_text(json.dumps(
        {"status": "PASS", "checks": [{"name": "L/d", "status": "PASS", "value": 20, "limit": 50}]}))
    assert "- L/d: PASS (Val: 20, Lim: 50)" in _generate(env)


def test_approval_for_another_revision_is_not_completed(env):
    _approve(env, revision_id="old-revision")
    text = _generate(env)
    assert "Overall status: COMPLETED" not in text and "STALE_APPROVAL" in text


def test_dashboard_and_insights_record_the_revision(env):
    _approve(env)
    meta = env["structure"]["meta"]
    assert f"- Revision: {meta['revision_id']}" in _generate(env)
    insights = json.loads((env["outputs"] / "run-insights.json").read_text())
    assert insights["revision_id"] == meta["revision_id"] and insights["status"] == "COMPLETED"
