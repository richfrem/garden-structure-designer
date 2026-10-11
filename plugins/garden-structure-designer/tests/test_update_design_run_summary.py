"""update_design_run_summary: locked-parameter summary from structure.json; absent values are labelled, revision is recorded."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import update_design_run_summary as summary  # type: ignore[import]  # noqa: E402

FULL = {
    "meta": {"source_hash": "src-1", "revision_id": "rev-9", "revision_hash": "hash-9"},
    "intent": {"jurisdiction": "BC"},
    "structure": {"type": "gazebo", "shape": "hexagon"},
    "layout": {"post_count": 6},
    "roof": {"pitch": "4:12"},
    "geometry": {
        "compound_cut": {"miter_deg": 28.71, "bevel_deg": 9.1},
        "beam_ring": {"beam_miter_deg": 30.0},
        "total_height": {"total_height_ft": 11.5},
        "svg_coordinates": {"viewBox": "0 0 10 10", "grade_y": 400},
    },
}


def _run(tmp_path, monkeypatch, structure):
    monkeypatch.setattr(summary, "staging_dir", lambda: tmp_path)
    if structure is not None:
        (tmp_path / "structure.json").write_text(json.dumps(structure))
    summary.main()
    return (tmp_path / "design-run-summary.md").read_text()


def test_locked_parameters_come_from_structure(tmp_path, monkeypatch):
    text = _run(tmp_path, monkeypatch, FULL)
    for line in ["- Structure type: gazebo", "- Plan shape: hexagon", "- Jurisdiction: BC", "- Post count: 6",
                 "- Pitch: 4:12", "- Rafter miter: 28.71", "- Rafter bevel: 9.1", "- Beam ring miter: 30.0",
                 "- Total height: 11.5", "- Source hash: src-1", "- SVG viewBox: 0 0 10 10", "- Grade Y: 400"]:
        assert line in text


def test_revision_identity_is_recorded(tmp_path, monkeypatch):
    text = _run(tmp_path, monkeypatch, FULL)
    assert "- Revision: rev-9 (hash-9)" in text


def test_absent_values_are_labelled_unknown_not_invented(tmp_path, monkeypatch):
    text = _run(tmp_path, monkeypatch, {})
    assert "- Post count: Unknown" in text and "- Rafter miter: Unknown" in text
    assert "- Revision: Unknown (Unknown)" in text


def test_missing_structure_file_still_writes_a_labelled_summary(tmp_path, monkeypatch):
    assert "- Plan shape: Unknown" in _run(tmp_path, monkeypatch, None)
