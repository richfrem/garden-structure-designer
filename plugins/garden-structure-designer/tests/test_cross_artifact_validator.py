"""Tests for parsed DXF validation and SVG/DXF dimension cross-checks (TASK-108, TASK-203)."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import ezdxf
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from control_plane.constants import (  # type: ignore[import]  # noqa: E402
    APPID,
    CAD_SUBDIR,
    DIM_CROSSCHECK_TOL_MM,
    MM_PER_FOOT,
    SHEET_FILENAMES,
)
from cross_artifact_validator import validate, validate_dxf_artifacts  # type: ignore[import]  # noqa: E402
from export_cad import export_sheets  # type: ignore[import]  # noqa: E402
from ezdxf_adapter import EzdxfAdapter  # type: ignore[import]  # noqa: E402

POSTS_XY = [(9, -6), (9, 6), (0, 6), (-9, 6), (-9, -6), (0, -6)]
POST_HEIGHT_FT = 8.9
X_SPAN_FT = 18.0
Y_SPAN_FT = 12.0


def _prism(p0, p1, half=0.25, sides=4):
    ring = [(half * math.cos(2 * math.pi * i / sides + math.pi / 4),
             half * math.sin(2 * math.pi * i / sides + math.pi / 4)) for i in range(sides)]
    return [[p[0] + dx, p[1] + dy, p[2]] for p in (p0, p1) for dx, dy in ring]


def _member(mid, role, p0, p1):
    return {"id": mid, "role": role, "p0": p0, "p1": p1, "vertices": _prism(p0, p1)}


def _structure():
    members = []
    for i, (x, y) in enumerate(POSTS_XY, 1):
        members.append(_member(f"P{i}", "post", [x, y, 0.0], [x, y, POST_HEIGHT_FT]))
        members.append(_member(f"FT{i}", "footing", [x, y, -1.5], [x, y, 0.3]))
    for i, (a, b) in enumerate(zip(POSTS_XY, POSTS_XY[1:] + POSTS_XY[:1]), 1):
        members.append(_member(f"B{i}", "beam", [*a, 9.2], [*b, 9.2]))
    members.append(_member("R1", "rafter", [10.0, 0.0, 9.8], [0.6, 0.0, 9.8]))
    members.append(_member("HUB", "hub", [0.0, 0.0, 9.1], [0.0, 0.0, 9.9]))
    return {
        "meta": {"revision_id": "rev-1", "revision_hash": "hash-1"},
        "geometry": {"joints": {"units": "feet", "resolved_model": {"members": members}}},
    }


def _write_svgs(outputs: Path, max_span_ft=Y_SPAN_FT, post_ft=POST_HEIGHT_FT):
    (outputs / "drawing-plan-view.svg").write_text(f'<svg><text>MAX SPAN: {max_span_ft} FT</text></svg>')
    (outputs / "drawing-elevation-view.svg").write_text(f'<svg><text>POST: {post_ft} FT</text></svg>')


@pytest.fixture
def workspace(tmp_path):
    structure = _structure()
    staging, outputs = tmp_path / "staging", tmp_path / "outputs"
    staging.mkdir()
    outputs.mkdir()
    (staging / "structure.json").write_text(json.dumps(structure))
    export_sheets(structure, outputs / CAD_SUBDIR, EzdxfAdapter())
    _write_svgs(outputs)
    return structure, staging, outputs


def _run(staging, outputs):
    return validate_dxf_artifacts(str(staging), str(outputs))


def _dxf_path(outputs, sheet_id):
    return outputs / CAD_SUBDIR / SHEET_FILENAMES[sheet_id]


def _edit_dxf(outputs, sheet_id, mutate):
    path = _dxf_path(outputs, sheet_id)
    doc = ezdxf.readfile(path)
    mutate(doc)
    doc.saveas(path)


def _member_entities(doc, member_id):
    return [e for e in doc.modelspace() if e.has_xdata(APPID)
            and any(t.value == f"MEMBER_ID={member_id}" for t in e.get_xdata(APPID))]


def test_clean_export_passes(workspace):
    _, staging, outputs = workspace
    assert _run(staging, outputs) == []


def test_missing_structure(tmp_path):
    assert _run(tmp_path, tmp_path)[0].startswith("MISSING_STRUCTURE")


def test_missing_dxf_files_reported(workspace):
    _, staging, outputs = workspace
    _dxf_path(outputs, "SB02").unlink()
    errors = _run(staging, outputs)
    assert len(errors) == 1 and errors[0].startswith("MISSING_DXF")


def test_missing_member_detected(workspace):
    _, staging, outputs = workspace
    _edit_dxf(outputs, "SB01", lambda d: d.modelspace().delete_entity(_member_entities(d, "B1")[0]))
    assert any("member B1 missing" in e for e in _run(staging, outputs))


def test_extra_member_detected(workspace):
    structure, staging, outputs = workspace
    structure["geometry"]["joints"]["resolved_model"]["members"].pop(0)
    (staging / "structure.json").write_text(json.dumps(structure))
    assert any("unexpected member P1" in e for e in _run(staging, outputs))


def test_duplicate_member_detected(workspace):
    _, staging, outputs = workspace

    def duplicate(doc):
        src = _member_entities(doc, "P1")[0]
        dup = doc.modelspace().add_polyline3d(list(src.points()), dxfattribs={"layer": src.dxf.layer})
        dup.set_xdata(APPID, [(1000, t.value) for t in src.get_xdata(APPID)])

    _edit_dxf(outputs, "SB01", duplicate)
    assert any("duplicate MEMBER_ID P1" in e for e in _run(staging, outputs))


def test_wrong_layer_detected(workspace):
    _, staging, outputs = workspace
    _edit_dxf(outputs, "SB01", lambda d: _member_entities(d, "P1")[0].dxf.__setattr__("layer", "FRAMING_BEAMS"))
    assert any("member P1 on layer FRAMING_BEAMS" in e for e in _run(staging, outputs))


def test_missing_layer_detected(workspace):
    _, staging, outputs = workspace

    def drop_layer(doc):
        doc.layers.remove("FRAMING_HUBS")

    _edit_dxf(outputs, "SB01", drop_layer)
    assert any("missing layer FRAMING_HUBS" in e for e in _run(staging, outputs))


def test_wrong_sheet_id_xdata_detected(workspace):
    _, staging, outputs = workspace

    def retag(doc):
        entity = _member_entities(doc, "P1")[0]
        entity.set_xdata(APPID, [(1000, t.value.replace("SHEET_ID=SB01", "SHEET_ID=SB02"))
                                 for t in entity.get_xdata(APPID)])

    _edit_dxf(outputs, "SB01", retag)
    assert any("member P1 SHEET_ID" in e for e in _run(staging, outputs))


def test_sb01_bounds_mismatch_detected(workspace):
    _, staging, outputs = workspace

    def shift(doc):
        entity = _member_entities(doc, "P1")[0]
        entity.vertices[0].dxf.location = entity.vertices[0].dxf.location + (500, 0, 0)

    _edit_dxf(outputs, "SB01", shift)
    assert any("member P1 bounds differ" in e for e in _run(staging, outputs))


def test_sb01_superstructure_below_grade_detected(workspace):
    structure, staging, outputs = workspace
    members = structure["geometry"]["joints"]["resolved_model"]["members"]
    next(m for m in members if m["id"] == "HUB").update(p0=[0, 0, -2.0], p1=[0, 0, -1.0], vertices=[])
    (staging / "structure.json").write_text(json.dumps(structure))
    export_sheets(structure, outputs / CAD_SUBDIR, EzdxfAdapter())
    errors = _run(staging, outputs)
    assert any("HUB has Z <= 0" in e for e in errors)


def test_sb02_non_planar_detected(workspace):
    _, staging, outputs = workspace

    def lift(doc):
        entity = _member_entities(doc, "B1")[0]
        entity.vertices[0].dxf.location = entity.vertices[0].dxf.location + (0, 0, 10)

    _edit_dxf(outputs, "SB02", lift)
    assert any("non-planar" in e for e in _run(staging, outputs))


def test_unregistered_appid_detected(workspace):
    _, staging, outputs = workspace

    def strip_appid(doc):
        for entity in list(doc.modelspace()):
            if entity.has_xdata(APPID):
                entity.discard_xdata(APPID)
        doc.appids.remove(APPID)

    _edit_dxf(outputs, "SB01", strip_appid)
    errors = _run(staging, outputs)
    assert any(f"APPID {APPID} is not registered" in e for e in errors)


def test_svg_max_span_outside_footprint_detected(workspace):
    _, staging, outputs = workspace
    _write_svgs(outputs, max_span_ft=40.0)
    assert any("MAX SPAN" in e for e in _run(staging, outputs))


def test_svg_post_height_mismatch_detected(workspace):
    _, staging, outputs = workspace
    _write_svgs(outputs, post_ft=POST_HEIGHT_FT + 1)
    assert any("POST height" in e for e in _run(staging, outputs))


def test_svg_post_height_within_tolerance_passes(workspace):
    _, staging, outputs = workspace
    _write_svgs(outputs, post_ft=POST_HEIGHT_FT + (DIM_CROSSCHECK_TOL_MM / 2) / MM_PER_FOOT)
    assert _run(staging, outputs) == []


def test_dxf_dimension_text_mismatch_detected(workspace):
    _, staging, outputs = workspace

    def retext(doc):
        doc.modelspace().query("TEXT").first.dxf.text = "99'-0\""

    _edit_dxf(outputs, "SB02", retext)
    assert any("dimension text" in e for e in _run(staging, outputs))


def test_svgs_absent_skips_svg_crosscheck(workspace):
    _, staging, outputs = workspace
    for svg in outputs.glob("*.svg"):
        svg.unlink()
    assert _run(staging, outputs) == []


def test_existing_validate_unaffected_by_dxf(workspace):
    _, staging, outputs = workspace
    assert validate(str(staging), str(outputs)) == []
