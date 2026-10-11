"""drawing_content_validator: per-sheet content-quality gate (characterization + bracing-aware + revision-bound report)."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import re
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN / "scripts"))
sys.path.insert(0, str(PLUGIN))
import drawing_content_validator as dcv  # type: ignore[import]  # noqa: E402
from geometry_engine import compute_from_structure  # type: ignore[import]  # noqa: E402
from render_drawings import generate_svg  # type: ignore[import]  # noqa: E402
from revision_identity import stamp_revision  # type: ignore[import]  # noqa: E402
from tests.test_geometry_engine import STRUCTURE_SEED  # type: ignore[import]  # noqa: E402

SHEETS = ["drawing-plan-view", "drawing-elevation-view", "drawing-isometric-view", "drawing-perspective-view",
          "blueprint-plan", "blueprint-elevation", "blueprint-isometric", "blueprint-component-isolation"]


def _solved(tmp_path, braces=True):
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["meta"]["topology_family"] = "RadialHubTopology"
    seed["hub"]["type"] = "hexagonal_prism"
    seed["bracing"]["enabled"] = braces
    path = tmp_path / "structure.json"
    path.write_text(json.dumps(seed))
    with contextlib.redirect_stdout(io.StringIO()):
        return stamp_revision(compute_from_structure(str(path)))


def _render(structure, sheet, tmp_path) -> str:
    out = tmp_path / f"{sheet}.svg"
    generate_svg(f"{sheet}.svg", structure, str(out))
    return out.read_text()


@pytest.fixture(scope="module")
def hex_structure(tmp_path_factory):
    return _solved(tmp_path_factory.mktemp("content"))


def _check(raw, sheet, model):
    return dcv._check_sheet(f"outputs/{sheet}.svg", raw, model)


@pytest.mark.parametrize("sheet", SHEETS)
def test_real_pipeline_sheets_pass_content_validation(hex_structure, tmp_path, sheet):
    errors, counts = _check(_render(hex_structure, sheet, tmp_path), sheet, hex_structure)
    assert errors == [], errors
    assert counts["total_elements"] > 0 and counts["semantic_total"] > 0


def test_blank_sheet_is_a_placeholder_and_stops_early():
    errors, _ = _check('<svg viewBox="0 0 100 100"><rect/></svg>', "drawing-plan-view", {})
    assert [e.split(":")[0] for e in errors] == ["SVG_PLACEHOLDER_GEOMETRY"]


def test_thin_sheet_reports_floors_and_missing_roles():
    raw = '<svg viewBox="0 0 1000 1000">' + '<rect x="500" y="500"/>' * 6 + "</svg>"
    codes = {e.split(":")[0] for e in _check(raw, "blueprint-plan", {})[0]}
    assert {"SVG_CONTENT_TOO_SMALL", "SVG_TOO_FEW_SEMANTIC_ELEMENTS", "SVG_TOO_FEW_TEXT_LABELS", "SVG_MISSING_REQUIRED_ROLE",
            "SVG_MISSING_DIMENSIONS", "SVG_MISSING_TITLE_BLOCK", "SVG_MISSING_MEMBER_IDS"} <= codes


def test_top_left_clustering_is_detected():
    raw = '<svg viewBox="0 0 1000 1000">' + '<rect x="10" y="10"/>' * 8 + "</svg>"
    assert any(e.startswith("SVG_CONTENT_TOP_LEFT_CLUSTER") for e in _check(raw, "drawing-plan-view", {})[0])


def test_missing_component_panels_are_detected(hex_structure, tmp_path):
    raw = _render(hex_structure, "blueprint-component-isolation", tmp_path)
    raw = raw.replace('data-role="component"', 'data-role="x"')
    assert any(e.startswith("SVG_MISSING_COMPONENT_DETAILS") for e in _check(raw, "blueprint-component-isolation", hex_structure)[0])


def test_missing_file_is_a_placeholder_failure(tmp_path):
    assert dcv.validate(str(tmp_path / "nope.svg"), "")[0][0].startswith("SVG_PLACEHOLDER_GEOMETRY")


# --- C2: bracing disabled means no braces are required -----------------------------------------


def test_disabled_bracing_does_not_demand_knee_braces(tmp_path):
    structure = _solved(tmp_path, braces=False)
    codes = {e.split(":")[0] for e in _check(_render(structure, "drawing-elevation-view", tmp_path), "drawing-elevation-view", structure)[0]}
    assert "SVG_MISSING_BRACES" not in codes


def test_enabled_bracing_still_demands_knee_braces(hex_structure, tmp_path):
    raw = _render(hex_structure, "drawing-elevation-view", tmp_path)
    raw = re.sub(r'data-role="brace"', 'data-role="x"', raw)
    raw = re.sub(r"(?i)brace|kicker", "x", raw)
    assert any(e.startswith("SVG_MISSING_BRACES") for e in _check(raw, "drawing-elevation-view", hex_structure)[0])


# --- report ----------------------------------------------------------------------------------


def test_report_is_idempotent_and_recomputes_status():
    report = {"files": [], "status": "PASS"}
    dcv._update_report(report, "a.svg", ["SVG_X"], {"total_elements": 1})
    dcv._update_report(report, "a.svg", [], {"total_elements": 2})
    assert len(report["files"]) == 1 and report["status"] == "PASS"
    dcv._update_report(report, "b.svg", ["SVG_Y"], {})
    assert report["status"] == "FAIL"


def test_cli_report_is_bound_to_the_revision(hex_structure, tmp_path, monkeypatch):
    svg = tmp_path / "drawing-plan-view.svg"
    svg.write_text(_render(hex_structure, "drawing-plan-view", tmp_path))
    model = tmp_path / "structure.json"
    model.write_text(json.dumps(hex_structure))
    report = tmp_path / "report.json"
    monkeypatch.setattr(sys, "argv", ["dcv", str(svg), str(model), "--json-output", str(report)])
    with pytest.raises(SystemExit) as info, contextlib.redirect_stdout(io.StringIO()):
        dcv.main()
    assert info.value.code == 0
    data = json.loads(report.read_text())
    assert data["revision_id"] == hex_structure["meta"]["revision_id"]
    assert data["source_hash"] == hex_structure["meta"]["source_hash"]
