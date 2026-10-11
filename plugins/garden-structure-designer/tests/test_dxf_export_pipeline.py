"""Round-trip tests for the ExchangeWriter adapters (EzdxfAdapter, CadcraftAdapter)."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import ezdxf
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from cadcraft_adapter import CadcraftAdapter  # type: ignore[import]  # noqa: E402
from exchange_writer import APPID, LAYER_COLORS, MM_PER_UNIT  # type: ignore[import]  # noqa: E402
from export_cad import SHEET_FILENAMES, export_sheets  # type: ignore[import]  # noqa: E402
from ezdxf_adapter import EzdxfAdapter  # type: ignore[import]  # noqa: E402

REVISION_ID = "11111111-2222-3333-4444-555555555555"
REVISION_HASH = "abc123"
FT_TO_MM = MM_PER_UNIT["feet"]
LAYER_BY_PREFIX = {
    "P": "FRAMING_POSTS",
    "B": "FRAMING_BEAMS",
    "R": "FRAMING_RAFTERS",
    "HUB": "FRAMING_HUBS",
    "K": "FRAMING_BRACES",
    "FT": "FOOTINGS_PIERS",
}


def _prism(p0, p1, half=0.25, sides=4):
    """Return 2*sides vertices of a prism around the p0->p1 axis (vertical-safe)."""
    ring = [(half * math.cos(2 * math.pi * i / sides + math.pi / 4),
             half * math.sin(2 * math.pi * i / sides + math.pi / 4)) for i in range(sides)]
    return [[p[0] + dx, p[1] + dy, p[2]] for p in (p0, p1) for dx, dy in ring]


def _member(mid, role, p0, p1, sides=4):
    return {"id": mid, "role": role, "p0": p0, "p1": p1, "vertices": _prism(p0, p1, sides=sides)}


@pytest.fixture(scope="module")
def structure():
    posts_xy = [(9, -6), (9, 6), (0, 6), (-9, 6), (-9, -6), (0, -6)]
    members = []
    for i, (x, y) in enumerate(posts_xy, 1):
        members.append(_member(f"P{i}", "post", [x, y, 0.0], [x, y, 8.9]))
        members.append(_member(f"FT{i}", "footing", [x, y, -1.5], [x, y, 0.3]))
    for i, (a, b) in enumerate(zip(posts_xy, posts_xy[1:] + posts_xy[:1]), 1):
        members.append(_member(f"B{i}", "beam", [*a, 9.2], [*b, 9.2]))
    members.append(_member("K1A", "brace", [9.0, -5.7, 7.4], [9.0, -4.2, 8.9]))
    for i in range(6):
        ang = math.pi / 3 * i
        members.append(_member(f"R{i + 1}", "rafter", [10 * math.cos(ang), 10 * math.sin(ang), 9.8],
                               [0.6 * math.cos(ang), 0.6 * math.sin(ang), 9.8], sides=6))
    members.append(_member("HUB", "hub", [0.0, 0.0, 9.1], [0.0, 0.0, 9.9], sides=6))
    return {
        "meta": {"revision_id": REVISION_ID, "revision_hash": REVISION_HASH},
        "geometry": {"joints": {"units": "feet", "resolved_model": {"constraints_resolved": True, "members": members}}},
    }


def _adapters():
    cadcraft = CadcraftAdapter()
    return [
        pytest.param(EzdxfAdapter(), id="ezdxf"),
        pytest.param(
            cadcraft, id="cadcraft",
            marks=pytest.mark.skipif(not cadcraft.is_available(), reason="cadcraft-cli not built"),
        ),
    ]


def _xdata(entity) -> dict[str, str]:
    return dict(tag.value.split("=", 1) for tag in entity.get_xdata(APPID))


def _export(adapter, sheet_id, structure, tmp_path):
    out = tmp_path / f"{sheet_id}.dxf"
    meta = adapter.export_sheet(sheet_id, structure, out, revision_id=REVISION_ID, revision_hash=REVISION_HASH)
    doc = ezdxf.readfile(out)
    return meta, doc, [e for e in doc.modelspace() if e.has_xdata(APPID)]


def _expected_layer(member_id):
    prefix = "HUB" if member_id == "HUB" else "FT" if member_id.startswith("FT") else member_id[0]
    return LAYER_BY_PREFIX[prefix]


@pytest.mark.parametrize("adapter", _adapters())
@pytest.mark.parametrize("sheet_id", ["SB01", "SB02"])
def test_roundtrip_audit_and_metadata(adapter, sheet_id, structure, tmp_path):
    meta, doc, _ = _export(adapter, sheet_id, structure, tmp_path)
    assert doc.audit().errors == []
    assert doc.header["$INSUNITS"] == 4
    assert set(LAYER_COLORS) <= {layer.dxf.name for layer in doc.layers}
    for name, color in LAYER_COLORS.items():
        assert doc.layers.get(name).color == color
    assert meta["sheet_id"] == sheet_id
    assert meta["writer"] == adapter.name
    assert len(meta["sha256"]) == 64
    assert meta["entities_count"] == len(doc.modelspace())


@pytest.mark.parametrize("adapter", _adapters())
def test_member_xdata_and_layers(adapter, structure, tmp_path):
    _, _, members = _export(adapter, "SB01", structure, tmp_path)
    ids = {_xdata(e)["MEMBER_ID"] for e in members}
    expected = {m["id"] for m in structure["geometry"]["joints"]["resolved_model"]["members"]}
    assert ids == expected
    assert {"P1", "B1", "R1", "HUB"} <= ids
    for entity in members:
        data = _xdata(entity)
        assert entity.dxf.layer == _expected_layer(data["MEMBER_ID"])
        assert data["REVISION_ID"] == REVISION_ID
        assert data["REVISION_HASH"] == REVISION_HASH
        assert data["SHEET_ID"] == "SB01"
        assert data["ROLE"]


@pytest.mark.parametrize("adapter", _adapters())
def test_sb01_is_full_scale_3d_mm(adapter, structure, tmp_path):
    _, _, members = _export(adapter, "SB01", structure, tmp_path)
    post = next(e for e in members if _xdata(e)["MEMBER_ID"] == "P1")
    zs = [p[2] for p in post.points()]
    assert max(zs) == pytest.approx(8.9 * FT_TO_MM)
    assert min(zs) == pytest.approx(0.0)


@pytest.mark.parametrize("adapter", _adapters())
def test_sb02_is_flat_plan(adapter, structure, tmp_path):
    _, doc, members = _export(adapter, "SB02", structure, tmp_path)
    assert members
    for entity in doc.modelspace():
        pts = list(entity.points()) if entity.dxftype() == "POLYLINE" else [entity.dxf.insert]
        assert all(p[2] == 0 for p in pts)
    assert {_xdata(e)["SHEET_ID"] for e in members} == {"SB02"}


@pytest.mark.parametrize("adapter", _adapters())
def test_dimensions_on_dimension_layer(adapter, structure, tmp_path):
    _, doc, _ = _export(adapter, "SB02", structure, tmp_path)
    texts = [e.dxf.text for e in doc.modelspace().query("TEXT")]
    assert texts == ["18'-0\"", "12'-0\""]
    assert all(e.dxf.layer == "DIMENSIONS_ARCH" for e in doc.modelspace().query("TEXT"))


def test_unknown_sheet_rejected(structure, tmp_path):
    with pytest.raises(ValueError, match="Unknown sheet_id"):
        EzdxfAdapter().export_sheet("SB99", structure, tmp_path / "x.dxf",
                                    revision_id=REVISION_ID, revision_hash=REVISION_HASH)


def test_export_sheets_writes_both_files(structure, tmp_path):
    results = export_sheets(structure, tmp_path, EzdxfAdapter())
    assert [r["sheet_id"] for r in results] == list(SHEET_FILENAMES)
    for result in results:
        assert Path(result["output_path"]).name == SHEET_FILENAMES[result["sheet_id"]]
        assert Path(result["output_path"]).is_file()
