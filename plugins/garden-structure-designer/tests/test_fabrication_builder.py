"""fabrication_builder: pure translator of the resolved model into cut-list.json, fail-closed and revision-bound."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import fabrication_builder as fb  # type: ignore[import]  # noqa: E402
from strict_access import MissingInputError  # type: ignore[import]  # noqa: E402


def _member(mid, role, p0, p1):
    face = lambda n: {"normal": n}  # noqa: E731
    return {"id": mid, "role": role, "p0": p0, "p1": p1, "axis_u": [1, 0, 0], "axis_w": [0, 1, 0],
            "axis_d": [0, 0, 1], "faces": [face([-1, 0, 0]), face([1, 0, 0])]}


STRUCTURE = {
    "meta": {"source_hash": "src", "revision_id": "rev-1", "revision_hash": "hash-1"},
    "geometry": {
        "compound_cut": {"miter_deg": 28.71, "bevel_deg": 9.1},
        "beam_ring": {"beam_miter_deg": 30.0},
        "joints": {"resolved_model": {"constraints_resolved": True, "members": [
            _member("P1", "post", [0, 0, 0], [0, 0, 8]),
            _member("B1", "beam", [0, 0, 8], [6, 0, 8]),
            _member("R1", "rafter", [6, 0, 8], [0, 0, 10]),
            _member("Brace1a", "brace", [0, 0, 6], [1, 0, 8]),
        ]}},
    },
}


def test_cut_list_is_revision_bound_and_role_mapped():
    out = fb.build_cut_list(STRUCTURE)
    assert out["revision_id"] == "rev-1" and out["revision_hash"] == "hash-1"
    assert out["source_hash"] == "src"
    roles = {m["id"]: m["role"] for m in out["members"]}
    assert roles == {"P1": "post", "B1": "beam", "R1": "rafter_primary", "Brace1a": "brace"}


def test_angles_come_from_structure_not_defaults():
    out = fb.build_cut_list(STRUCTURE)
    rafter = next(m for m in out["members"] if m["id"] == "R1")
    assert rafter["cuts"][1]["angles"] == {"miter_deg": 28.71, "bevel_deg": 9.1}
    beam = next(m for m in out["members"] if m["id"] == "B1")
    assert beam["cuts"][0]["angles"]["miter_deg"] == 30.0


@pytest.mark.parametrize(
    "mutate,needle",
    [
        (lambda s: s["geometry"].pop("compound_cut"), "geometry.compound_cut"),
        (lambda s: s["geometry"]["beam_ring"].pop("beam_miter_deg"), "geometry.beam_ring.beam_miter_deg"),
        (lambda s: s["meta"].pop("revision_id"), "meta.revision_id"),
        (lambda s: s["meta"].pop("source_hash"), "meta.source_hash"),
    ],
)
def test_missing_inputs_fail_closed(mutate, needle):
    structure = copy.deepcopy(STRUCTURE)
    mutate(structure)
    with pytest.raises(MissingInputError, match=needle.replace(".", r"\.")):
        fb.build_cut_list(structure)


def test_unresolved_model_is_reported_not_silent(tmp_path, monkeypatch, capsys):
    structure = copy.deepcopy(STRUCTURE)
    structure["geometry"]["joints"]["resolved_model"]["constraints_resolved"] = False
    path = tmp_path / "structure.json"
    path.write_text(json.dumps(structure))
    monkeypatch.setattr(sys, "argv", ["fabrication_builder.py", str(path)])
    monkeypatch.setattr(fb, "outputs_dir", lambda: tmp_path / "outputs")
    with pytest.raises(SystemExit) as exit_info:
        fb.main()
    assert exit_info.value.code == 1
    assert "resolved" in capsys.readouterr().err


def test_main_writes_cut_list(tmp_path, monkeypatch):
    path = tmp_path / "structure.json"
    path.write_text(json.dumps(STRUCTURE))
    monkeypatch.setattr(sys, "argv", ["fabrication_builder.py", str(path)])
    monkeypatch.setattr(fb, "outputs_dir", lambda: tmp_path / "outputs")
    fb.main()
    written = json.loads((tmp_path / "outputs" / "fabrication" / "cut-list.json").read_text())
    assert written["revision_id"] == "rev-1"
