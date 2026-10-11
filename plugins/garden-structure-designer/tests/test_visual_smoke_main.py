"""visual_svg_smoke_test.main end-to-end on real sheets: outcomes, report identity binding, fail-closed inputs."""
from __future__ import annotations

import contextlib
import copy
import io
import json
import shutil
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN / "scripts"))
sys.path.insert(0, str(PLUGIN))
import visual_svg_smoke_test as smoke  # type: ignore[import]  # noqa: E402
from geometry_engine import compute_from_structure  # type: ignore[import]  # noqa: E402
from render_drawings import generate_svg  # type: ignore[import]  # noqa: E402
from revision_identity import stamp_revision  # type: ignore[import]  # noqa: E402
from tests.test_geometry_engine import STRUCTURE_SEED  # type: ignore[import]  # noqa: E402

SHEETS = ["drawing-plan-view.svg", "drawing-elevation-view.svg", "drawing-isometric-view.svg",
          "drawing-perspective-view.svg", "blueprint-plan.svg", "blueprint-elevation.svg",
          "blueprint-isometric.svg", "blueprint-component-isolation.svg"]

# PNG rasterization needs macOS qlmanage or a Playwright Chromium; skip (not fail) where neither exists.
CAN_RASTERIZE = sys.platform == "darwin" or smoke._sync_playwright is not None
pytestmark = pytest.mark.skipif(not CAN_RASTERIZE, reason="no SVG rasterizer (qlmanage / Playwright) available")


@pytest.fixture(scope="module")
def package(tmp_path_factory):
    root = tmp_path_factory.mktemp("smoke")
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["meta"]["topology_family"] = "RadialHubTopology"
    seed["hub"]["type"] = "hexagonal_prism"
    path = root / "structure.json"
    path.write_text(json.dumps(seed))
    with contextlib.redirect_stdout(io.StringIO()):
        structure = stamp_revision(compute_from_structure(str(path)))
    path.write_text(json.dumps(structure))
    (root / "svg").mkdir()
    for sheet in SHEETS:
        generate_svg(sheet, structure, str(root / "svg" / sheet))
    return {"root": root, "structure": structure, "path": path}


def _run(package, tmp_path, *extra, structure_path=None, svg_dir=None):
    argv = ["smoke", "--structure", str(structure_path or package["path"]), "--svg-dir", str(svg_dir or package["root"] / "svg"),
            "--out-dir", str(tmp_path / "out"), "--report-json", str(tmp_path / "report.json"),
            "--report-md", str(tmp_path / "report.md"), *extra]
    old = sys.argv
    sys.argv = argv
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                smoke.main()
                code = 0
            except SystemExit as exit_info:
                code = exit_info.code or 0
    finally:
        sys.argv = old
    report = json.loads((tmp_path / "report.json").read_text()) if (tmp_path / "report.json").exists() else None
    return code, report


def test_real_sheets_pass_and_write_both_reports(package, tmp_path):
    code, report = _run(package, tmp_path)
    assert code == 0 and report["status"] == "PASS" and report["may_claim_success"] is True
    assert [f["sheet"] for f in report["files"]] == [s.replace(".svg", "") for s in SHEETS]
    assert all(f["status"] == "PASS" and f["metrics"] for f in report["files"])
    assert "STATUS: **PASS**" in (tmp_path / "report.md").read_text()


def test_report_is_bound_to_source_hash_and_revision(package, tmp_path):
    _, report = _run(package, tmp_path)
    meta = package["structure"]["meta"]
    assert report["source_hash"] == meta["source_hash"]
    assert (report["revision_id"], report["revision_hash"]) == (meta["revision_id"], meta["revision_hash"])


def test_missing_sheet_fails_the_run(package, tmp_path):
    svg_dir = tmp_path / "svg"
    shutil.copytree(package["root"] / "svg", svg_dir)
    (svg_dir / SHEETS[0]).unlink()
    code, report = _run(package, tmp_path, svg_dir=svg_dir)
    assert code == 1 and f"SVG_MISSING: {SHEETS[0]}" in report["overall_failures"] and report["may_claim_success"] is False


def test_unsealed_geometry_is_refused(package, tmp_path):
    unsealed = copy.deepcopy(package["structure"])
    unsealed["geometry"]["_sealed"] = False
    path = tmp_path / "unsealed.json"
    path.write_text(json.dumps(unsealed))
    code, report = _run(package, tmp_path, structure_path=path)
    assert code == 1 and report is None


def test_missing_source_hash_fails_closed(package, tmp_path):
    broken = copy.deepcopy(package["structure"])
    del broken["meta"]["source_hash"]
    path = tmp_path / "broken.json"
    path.write_text(json.dumps(broken))
    code, report = _run(package, tmp_path, structure_path=path)
    assert code == 1 and report is None


def test_sheet_list_is_the_shared_constant():
    from constants import SVG_SHEET_FILENAMES
    assert list(SVG_SHEET_FILENAMES) == SHEETS
