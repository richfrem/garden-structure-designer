"""End-to-end pipeline test: Stage 0.5 -> 1 -> 2 -> 4 -> 7 with CAD (DXF) deliverables.

Hexagonal gazebo (RadialHubTopology) runs the full chain. The rectangular pergola
(OrthogonalGridTopology) is a reserved family: Stage 0.5 and Stage 2 must reject it
fail-closed, and nothing downstream may run (architecture.md, Topology Scope).
"""
from __future__ import annotations

import copy
import json
import sys
from types import SimpleNamespace
from pathlib import Path

import ezdxf
import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
sys.path.insert(0, str(PLUGIN_ROOT))
import compile_package as compile_package_module  # type: ignore[import]  # noqa: E402
from compile_package import compile_package  # type: ignore[import]  # noqa: E402
import fabrication_builder  # type: ignore[import]  # noqa: E402
from exchange_writer import APPID  # type: ignore[import]  # noqa: E402
from export_cad import SHEET_FILENAMES, export_sheets  # type: ignore[import]  # noqa: E402
from geometry_engine import compute_from_structure  # type: ignore[import]  # noqa: E402
from pipeline_runner import TopologyErrorCode  # type: ignore[import]  # noqa: E402
from render_drawings import generate_svg  # type: ignore[import]  # noqa: E402
from revision_identity import stamp_revision  # type: ignore[import]  # noqa: E402
from topology_compiler import run_stage as stage2_topology  # type: ignore[import]  # noqa: E402
from tests.test_geometry_engine import STRUCTURE_SEED  # type: ignore[import]  # noqa: E402
from validate_topology_intent import run_stage as stage05_intent  # type: ignore[import]  # noqa: E402

SVG_SHEETS = [
    "drawing-plan-view.svg",
    "drawing-elevation-view.svg",
    "drawing-isometric-view.svg",
    "drawing-perspective-view.svg",
    "blueprint-plan.svg",
    "blueprint-elevation.svg",
    "blueprint-isometric.svg",
    "blueprint-component-isolation.svg",
]


def _hex_seed() -> dict:
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["meta"]["topology_family"] = "RadialHubTopology"
    seed["hub"]["type"] = "hexagonal_prism"
    return seed


def _rectangle_seed() -> dict:
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["meta"]["topology_family"] = "OrthogonalGridTopology"
    seed["structure"] = {"type": "pergola", "shape": "rectangle", "sides": 4}
    seed["layout"].update({"shape": "rectangle", "length_ft": 18.0, "width_ft": 12.0})
    return seed


def _seal_geometry(structure: dict, path: Path) -> dict:
    """Stage 1: run the geometry engine on ``structure`` written at ``path``."""
    path.write_text(json.dumps(structure), encoding="utf-8")
    return compute_from_structure(str(path))


@pytest.fixture(scope="module")
def hex_package(tmp_path_factory):
    """Run Stages 0.5, 1, 2, 4 on the hexagonal gazebo; return staging/outputs dirs."""
    root = tmp_path_factory.mktemp("hex_gazebo")
    staging = root / "context" / "staging"
    outputs = root / "outputs"
    staging.mkdir(parents=True)
    outputs.mkdir()
    structure_path = staging / "structure.json"

    seed = _hex_seed()
    assert stage05_intent(seed, staging, outputs) is seed, "Stage 0.5 rejected the hexagon seed"

    sealed = _seal_geometry(seed, structure_path)
    assert sealed["geometry"]["_sealed"] is True

    enriched = stage2_topology(sealed, staging, outputs)
    assert "error_code" not in enriched, enriched
    assert enriched["geometry"]["joints"]["topology"]["member_count"] > 0

    stamped = stamp_revision(enriched)
    structure_path.write_text(json.dumps(stamped), encoding="utf-8")

    for sheet in SVG_SHEETS:
        generate_svg(sheet, stamped, str(outputs / sheet))

    # Stage 4 CAD export: Stage 7 validates these exact bytes and never regenerates them (C4).
    export_sheets(stamped, outputs / "cad")

    # Stage 6 fabrication cut list (writes outputs/fabrication/cut-list.json)
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(fabrication_builder, "outputs_dir", lambda: outputs)
        patch.setattr(sys, "argv", ["fabrication_builder.py", str(structure_path)])
        fabrication_builder.main()

    return {"root": root, "staging": staging, "outputs": outputs, "structure": stamped}


@pytest.fixture(scope="module")
def compiled_hex_package(hex_package):
    """Stage 7: compile the hexagonal package (PDF export forced down the fallback path)."""
    staging, outputs = hex_package["staging"], hex_package["outputs"]
    (staging / "drawing-red-team-report.json").write_text(
        json.dumps({
            "may_claim_success": True, "summary": "Approved (test fixture)",
            "revision_id": hex_package["structure"]["meta"]["revision_id"],
            "revision_hash": hex_package["structure"]["meta"]["revision_hash"], "hash_algorithm": "gsd-json-v1",
        }), encoding="utf-8"
    )
    render_dir = outputs / "high-resolution-image"
    render_dir.mkdir()
    (render_dir / "pergola_render_1.png").write_bytes(b"PNG fake data")
    images = "\n".join(f"![{name}]({name})" for name in SVG_SHEETS)
    (outputs / "pergola_plan.md").write_text(
        f"# Hexagonal Gazebo\n{images}\n![Render](high-resolution-image/pergola_render_1.png)\n", encoding="utf-8"
    )

    def _no_npx(*args, **kwargs):
        raise FileNotFoundError("npx disabled for test")

    # Patch only compile_package's subprocess handle so the CAD adapters keep the real one.
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(compile_package_module, "subprocess", SimpleNamespace(run=_no_npx))
        return compile_package(staging_dir=staging, outputs_dir=outputs, md_filename="pergola_plan.md")


def test_hex_pipeline_stage7_completes_with_manifest(compiled_hex_package, hex_package):
    assert compiled_hex_package["status"] in ("COMPLETE", "FALLBACK")
    cad_dir = hex_package["outputs"] / "cad"
    assert [Path(p) for p in compiled_hex_package["cad_deliverables"]] == [
        cad_dir / name for name in SHEET_FILENAMES.values()
    ]


def test_hex_pipeline_produces_all_deliverables(compiled_hex_package, hex_package):
    outputs = hex_package["outputs"]
    for sheet in SVG_SHEETS:
        assert (outputs / sheet).stat().st_size > 0, sheet
    assert (outputs / "cad" / "SB01-structure.dxf").stat().st_size > 0
    assert (outputs / "cad" / "SB02-plan.dxf").stat().st_size > 0
    cut_list = json.loads((outputs / "fabrication" / "cut-list.json").read_text(encoding="utf-8"))
    assert cut_list["members"]
    assert (outputs / "pergola_plan.md").exists()
    embedded = (outputs / "pergola_plan_embedded.md").read_text(encoding="utf-8")
    assert "<svg" in embedded

    # Package manifest validation (C4/C6)
    manifest_path = outputs / "package-manifest.json"
    assert manifest_path.exists(), "outputs/package-manifest.json must exist"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["version"] == "1.5"
    assert manifest["topology_family"] == "RadialHubTopology"
    assert len(manifest["artifacts"]) > 0
    import hashlib
    for art in manifest["artifacts"]:
        f = outputs / art["path"]
        assert f.exists(), f"Artifact {art['path']} in manifest does not exist"
        calc_digest = hashlib.sha256(f.read_bytes()).hexdigest()
        assert calc_digest == art["sha256"], f"Digest mismatch on {art['path']}"



@pytest.mark.parametrize("sheet_id", sorted(SHEET_FILENAMES))
def test_hex_pipeline_dxf_has_zero_auditor_errors(compiled_hex_package, hex_package, sheet_id):
    doc = ezdxf.readfile(hex_package["outputs"] / "cad" / SHEET_FILENAMES[sheet_id])
    assert doc.audit().errors == []
    assert len(doc.modelspace()) > 0


def test_hex_pipeline_dxf_member_ids_trace_to_structure(compiled_hex_package, hex_package):
    expected = {m["id"] for m in hex_package["structure"]["geometry"]["joints"]["resolved_model"]["members"]}
    doc = ezdxf.readfile(hex_package["outputs"] / "cad" / SHEET_FILENAMES["SB01"])
    seen = {tag.value.split("=", 1)[1] for e in doc.modelspace() if e.has_xdata(APPID)
            for tag in e.get_xdata(APPID) if tag.value.startswith("MEMBER_ID=")}
    assert seen, "SB01 carries no member_id xdata"
    assert seen <= expected


def test_rectangular_pergola_rejected_fail_closed(tmp_path):
    seed = _rectangle_seed()
    stage05 = stage05_intent(seed, tmp_path, tmp_path)
    assert stage05["error_code"] == TopologyErrorCode.TOPOLOGY_NOT_IMPLEMENTED

    # Stage 2 independently rejects the reserved family even when invoked directly on sealed geometry.
    sealed = _seal_geometry(seed, tmp_path / "structure.json")
    stage2 = stage2_topology(sealed, tmp_path, tmp_path)
    assert stage2["error_code"] == TopologyErrorCode.TOPOLOGY_NOT_IMPLEMENTED

    # Nothing downstream ran.
    assert not (tmp_path / "cad").exists()
    assert not list(tmp_path.glob("*.svg"))
