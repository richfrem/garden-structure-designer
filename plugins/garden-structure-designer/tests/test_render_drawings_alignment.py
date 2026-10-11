"""render_drawings: member tagging (data-tag), no hardcoded sheet content, revision stamp, no latent NameError."""
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
from geometry_engine import compute_from_structure  # type: ignore[import]  # noqa: E402
from render_drawings import generate_svg  # type: ignore[import]  # noqa: E402
from revision_identity import stamp_revision  # type: ignore[import]  # noqa: E402
from tests.test_geometry_engine import STRUCTURE_SEED  # type: ignore[import]  # noqa: E402

SHEETS = ["drawing-plan-view.svg", "drawing-elevation-view.svg", "drawing-isometric-view.svg",
          "drawing-perspective-view.svg", "blueprint-plan.svg", "blueprint-elevation.svg",
          "blueprint-isometric.svg", "blueprint-component-isolation.svg"]


def _solved(tmp_path, sides=6):
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["meta"]["topology_family"] = "RadialHubTopology"
    seed["structure"]["sides"], seed["layout"]["post_count"] = sides, sides
    seed["roof"]["primary_rafters"]["count"] = sides
    seed["hub"]["type"] = {6: "hexagonal_prism", 8: "octagonal_prism"}.get(sides, "polygonal_cylinder")
    path = tmp_path / "structure.json"
    path.write_text(json.dumps(seed))
    with contextlib.redirect_stdout(io.StringIO()):
        return compute_from_structure(str(path))


def _render(structure, sheet, tmp_path):
    out = tmp_path / sheet
    generate_svg(sheet, structure, str(out))
    return out.read_text()


@pytest.fixture(scope="module")
def hex_structure(tmp_path_factory):
    return _solved(tmp_path_factory.mktemp("hex"))


@pytest.mark.parametrize("sheet", SHEETS)
def test_every_data_id_has_a_matching_data_tag(hex_structure, tmp_path, sheet):
    svg = _render(hex_structure, sheet, tmp_path)
    pairs = re.findall(r'<[^>]*\bdata-id="([^"]+)"[^>]*>', svg)
    assert pairs, "member elements must be tagged"
    for tag in pairs:
        assert re.search(rf'data-id="{re.escape(tag)}"[^>]*data-tag="{re.escape(tag)}"|data-tag="{re.escape(tag)}"[^>]*data-id="{re.escape(tag)}"', svg)


@pytest.mark.parametrize("sheet", SHEETS)
def test_data_tags_are_real_member_ids(hex_structure, tmp_path, sheet):
    members = {m["id"] for m in hex_structure["geometry"]["joints"]["resolved_model"]["members"]}
    tags = set(re.findall(r'data-tag="([^"]+)"', _render(hex_structure, sheet, tmp_path)))
    assert tags and tags <= members, sorted(tags - members)


def test_hub_panel_seat_count_follows_sides(tmp_path):
    octagon = _solved(tmp_path, sides=8)
    assert "8 RAFTER SEATS" in _render(octagon, "blueprint-component-isolation.svg", tmp_path)


def test_beam_panel_uses_the_declared_beam_size(hex_structure, tmp_path):
    svg = _render(hex_structure, "blueprint-component-isolation.svg", tmp_path)
    assert hex_structure["members"]["beams"]["nominal_size"] in svg and "4x8" not in svg


def test_no_hardcoded_date_and_revision_is_shown_when_stamped(hex_structure, tmp_path):
    stamped = stamp_revision(hex_structure)
    svg = _render(stamped, "drawing-plan-view.svg", tmp_path)
    assert "2026-05-24" not in svg
    assert f"REVISION: {stamped['meta']['revision_id'][:8]}" in svg


def test_component_sheet_without_post_spacing_does_not_crash(hex_structure, tmp_path):
    structure = copy.deepcopy(hex_structure)
    del structure["layout"]["post_spacing_ft"]
    assert "BEAM B1 DETAIL" in _render(structure, "blueprint-component-isolation.svg", tmp_path)
