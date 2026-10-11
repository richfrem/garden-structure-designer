"""C4 parsed-DXF gates: tolerance, units, revision binding, layer colors, extras, finiteness, fail-closed inputs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from test_cross_artifact_validator import (  # type: ignore[import]  # noqa: E402,F401
    _edit_dxf,
    _member_entities,
    _run,
    workspace,
)
from constants import DXF_BOUNDS_TOL_MM  # type: ignore[import]  # noqa: E402


def test_bounds_tolerance_is_c4_0_01_mm():
    """C4: maximum absolute exchange error is 0.01 mm."""
    assert DXF_BOUNDS_TOL_MM == 0.01


def test_sub_millimetre_shift_detected(workspace):
    """A 0.5 mm drift passed the old 1 mm gate; C4 requires it to fail."""
    _, staging, outputs = workspace

    def shift(doc):
        entity = _member_entities(doc, "P1")[0]
        entity.vertices[0].dxf.location = entity.vertices[0].dxf.location + (0.5, 0, 0)

    _edit_dxf(outputs, "SB01", shift)
    assert any("member P1 bounds differ" in e for e in _run(staging, outputs))


def test_wrong_insunits_detected(workspace):
    _, staging, outputs = workspace
    _edit_dxf(outputs, "SB01", lambda doc: doc.header.__setitem__("$INSUNITS", 1))
    assert any("$INSUNITS" in e for e in _run(staging, outputs))


def test_wrong_revision_id_detected(workspace):
    structure, staging, outputs = workspace
    structure["meta"]["revision_id"] = "rev-2"
    (staging / "structure.json").write_text(json.dumps(structure))
    assert any("REVISION_ID" in e for e in _run(staging, outputs))


def test_wrong_revision_hash_detected(workspace):
    structure, staging, outputs = workspace
    structure["meta"]["revision_hash"] = "hash-2"
    (staging / "structure.json").write_text(json.dumps(structure))
    assert any("REVISION_HASH" in e for e in _run(staging, outputs))


def test_wrong_layer_color_detected(workspace):
    _, staging, outputs = workspace
    _edit_dxf(outputs, "SB01", lambda doc: setattr(doc.layers.get("FRAMING_POSTS"), "color", 7))
    assert any("FRAMING_POSTS" in e and "color" in e for e in _run(staging, outputs))


def test_untagged_structural_extra_detected(workspace):
    """C4: no untagged top-level structural extras."""
    _, staging, outputs = workspace
    _edit_dxf(
        outputs,
        "SB01",
        lambda doc: doc.modelspace().add_polyline3d([(0, 0, 0), (1, 1, 1)], dxfattribs={"layer": "FRAMING_BEAMS"}),
    )
    assert any("untagged" in e for e in _run(staging, outputs))


def test_non_finite_coordinate_detected(workspace):
    _, staging, outputs = workspace

    def poison(doc):
        entity = _member_entities(doc, "P1")[0]
        entity.vertices[0].dxf.location = (float("nan"), 0, 0)

    _edit_dxf(outputs, "SB01", poison)
    assert any("non-finite" in e for e in _run(staging, outputs))


def test_missing_units_fail_closed(workspace):
    structure, staging, outputs = workspace
    del structure["geometry"]["joints"]["units"]
    (staging / "structure.json").write_text(json.dumps(structure))
    assert any("units" in e for e in _run(staging, outputs))


def test_no_resolved_members_fail_closed(workspace):
    structure, staging, outputs = workspace
    structure["geometry"]["joints"]["resolved_model"]["members"] = []
    (staging / "structure.json").write_text(json.dumps(structure))
    assert any("NO_RESOLVED_MEMBERS" in e for e in _run(staging, outputs))
