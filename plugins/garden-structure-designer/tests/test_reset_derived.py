"""reset_derived goes through the C5 transaction authority (CAS + journal + purge) instead of writing canonical directly."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import reset_derived  # type: ignore[import]  # noqa: E402
import structure_io  # type: ignore[import]  # noqa: E402
from revision_identity import stamp_revision  # type: ignore[import]  # noqa: E402

SEALED = {
    "meta": {"lifecycle": "GEOMETRY_SEALED"},
    "geometry": {"_sealed": True, "joints": {}},
    "cad": {"_sealed": True},
    "layout": {"post_count": 6},
}


@pytest.fixture
def canonical(tmp_path):
    path = tmp_path / "context" / "staging" / "structure.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(stamp_revision(SEALED)))
    (tmp_path / "outputs").mkdir()
    (tmp_path / "outputs" / "drawing-plan-view.svg").write_text("<svg/>")
    (path.parent / "design-spec.json").write_text("{}")
    (path.parent / "notes.txt").write_text("user input")
    return path


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def test_reset_unseals_through_a_new_revision_and_purges_derived_files(canonical, tmp_path):
    before = _load(canonical)["meta"]["revision_id"]
    reset_derived.main([str(canonical)])
    data = _load(canonical)
    assert data["geometry"]["_sealed"] is False and data["cad"]["_sealed"] is False
    assert data["meta"]["lifecycle"] == "ENGINEERED"
    assert data["meta"]["revision_id"] != before
    assert not (tmp_path / "outputs" / "drawing-plan-view.svg").exists()
    assert not (canonical.parent / "design-spec.json").exists()
    assert (canonical.parent / "notes.txt").exists()
    journals = list((canonical.parent / "journal").glob("*.json"))
    assert len(journals) == 1 and json.loads(journals[0].read_text())["state"] == "COMMITTED"


def test_reset_is_a_noop_when_nothing_changes(canonical, tmp_path, capsys):
    reset_derived.main([str(canonical)])
    revision = _load(canonical)["meta"]["revision_id"]
    (tmp_path / "outputs" / "drawing-plan-view.svg").write_text("<svg/>")
    reset_derived.main([str(canonical)])
    assert _load(canonical)["meta"]["revision_id"] == revision
    assert (tmp_path / "outputs" / "drawing-plan-view.svg").exists()
    assert "No changes needed" in capsys.readouterr().out


def test_missing_file_exits_nonzero(tmp_path):
    with pytest.raises(SystemExit) as exit_info:
        reset_derived.main([str(tmp_path / "nope.json")])
    assert exit_info.value.code == 1


def test_update_structure_failure_leaves_canonical_and_cleans_candidate(canonical):
    original = canonical.read_text()

    def boom(data):
        raise RuntimeError("mutator failed")

    with pytest.raises(RuntimeError):
        structure_io.update_structure(canonical, boom)
    assert canonical.read_text() == original
    candidates = canonical.parent / "candidates"
    assert not candidates.exists() or not any(candidates.iterdir())
