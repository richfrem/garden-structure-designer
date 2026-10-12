"""End-to-end pipeline test for Milestone M5: Orthogonal Grid Pergola (Stages 0.5 -> 7).

Tests full pipeline execution on an 18ft x 12ft rectangular pergola (OrthogonalGridTopology)
with 6 posts (3x2 grid), 6 perimeter beams, 7 parallel primary rafters, and knee bracing:
- Stage 0.5 intent validation
- Stage 1 geometry engine (seals geometry, solves all prisms, checks constraints)
- Stage 2 topology compiler (graph compilation and validation)
- Stage 4 CAD export (SB01 3D wireframe, SB02 2D plan projection)
- Stage 4 SVG drafting (all 8 drawing/blueprint sheets)
- Stage 5.5 parsed DXF and cross-artifact dimension verification
- Stage 6 fabrication cut list generation
- Stage 7 package compilation with package-manifest.json SHA-256 digests
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import ezdxf
import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
sys.path.insert(0, str(PLUGIN_ROOT))
import compile_package as compile_package_module  # type: ignore[import]
from compile_package import compile_package  # type: ignore[import]
import fabrication_builder  # type: ignore[import]
from cross_artifact_validator import validate_dxf_artifacts  # type: ignore[import]
from exchange_writer import APPID  # type: ignore[import]
from export_cad import SHEET_FILENAMES, export_sheets  # type: ignore[import]
from geometry_engine import compute_from_structure  # type: ignore[import]
from render_drawings import SVG_SHEET_FILENAMES, generate_svg  # type: ignore[import]
from revision_identity import stamp_revision  # type: ignore[import]
from topology_compiler import run_stage as stage2_topology  # type: ignore[import]
from tests.test_geometry_engine import STRUCTURE_SEED  # type: ignore[import]
from validate_topology_intent import run_stage as stage05_intent  # type: ignore[import]


def _rectangular_pergola_seed() -> dict:
    """Builds a canonical 18ft x 12ft 6-post rectangular pergola seed."""
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["meta"]["topology_family"] = "OrthogonalGridTopology"
    seed["meta"]["revision_id"] = "rev-m5-pergola-001"
    seed["meta"]["source_hash"] = "e2e_m5_pergola_seed"
    seed["structure"] = {"type": "pergola", "shape": "rectangle", "sides": 4}
    seed["layout"].update({
        "shape": "rectangle",
        "length_ft": 18.0,
        "width_ft": 12.0,
        "post_count": 6,
        "grid": {"rows": 2, "cols": 3},
    })
    seed["roof"]["pitch"] = "0:12"
    seed["roof"]["primary_rafters"]["count"] = 7
    seed["roof"]["primary_rafters"]["overhang_ft"] = 1.0
    seed["hub"] = {"type": "none", "radius_min_ft": 0.0}
    seed["bracing"]["enabled"] = True
    return seed


@pytest.fixture(scope="module")
def pergola_package(tmp_path_factory):
    """Executes Stages 0.5, 1, 2, 4, 6 on the 18ft x 12ft rectangular pergola."""
    root = tmp_path_factory.mktemp("m5_pergola")
    staging = root / "context" / "staging"
    outputs = root / "outputs"
    staging.mkdir(parents=True)
    outputs.mkdir()
    structure_path = staging / "structure.json"

    seed = _rectangular_pergola_seed()

    # Stage 0.5 — Intent Validation
    intent_result = stage05_intent(seed, staging, outputs)
    assert "error_code" not in intent_result, f"Stage 0.5 failed: {intent_result}"

    # Stage 1 — Geometry Solving & Sealing
    structure_path.write_text(json.dumps(seed), encoding="utf-8")
    sealed = compute_from_structure(str(structure_path))
    assert sealed["geometry"]["_sealed"] is True

    # Stage 2 — Topology Graph Compilation
    enriched = stage2_topology(sealed, staging, outputs)
    assert "error_code" not in enriched, f"Stage 2 failed: {enriched}"
    topo = enriched["geometry"]["joints"]["topology"]
    assert topo["member_count"] > 0
    assert topo["connection_count"] > 0

    # Stamp revision binding
    stamped = stamp_revision(enriched, "rev-m5-pergola-001")
    structure_path.write_text(json.dumps(stamped), encoding="utf-8")

    # Stage 4 — SVG Drawing Sheets (8 sheets)
    for sheet in SVG_SHEET_FILENAMES:
        generate_svg(sheet, stamped, str(outputs / sheet))

    # Stage 4 — Multi-Sheet DXF Export (SB01 and SB02)
    cad_dir = outputs / "cad"
    cad_dir.mkdir()
    export_sheets(stamped, cad_dir)

    # Stage 6 — Fabrication Cut List
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(fabrication_builder, "outputs_dir", lambda: outputs)
        patch.setattr(sys, "argv", ["fabrication_builder.py", str(structure_path)])
        fabrication_builder.main()

    return {"root": root, "staging": staging, "outputs": outputs, "structure": stamped}


@pytest.fixture(scope="module")
def compiled_pergola_package(pergola_package):
    """Stage 7: package compilation and manifest digest verification."""
    staging, outputs = pergola_package["staging"], pergola_package["outputs"]
    stamped = pergola_package["structure"]

    # Red-team approval report bound to the revision
    (staging / "drawing-red-team-report.json").write_text(
        json.dumps({
            "may_claim_success": True,
            "summary": "Approved 6-post pergola (M5 test fixture)",
            "revision_id": stamped["meta"]["revision_id"],
            "revision_hash": stamped["meta"]["revision_hash"],
            "hash_algorithm": "gsd-json-v1",
        }),
        encoding="utf-8",
    )

    # Photorealistic render deliverable
    render_dir = outputs / "high-resolution-image"
    render_dir.mkdir(exist_ok=True)
    (render_dir / "pergola_render_1.png").write_bytes(b"PNG fake data for test")

    # Markdown spec document
    images = "\n".join(f"![{name}]({name})" for name in SVG_SHEET_FILENAMES)
    (outputs / "pergola_plan.md").write_text(
        f"# 18ft x 12ft Timber Frame Pergola\n{images}\n![Render](high-resolution-image/pergola_render_1.png)\n",
        encoding="utf-8",
    )

    def _no_npx(*args, **kwargs):
        raise FileNotFoundError("npx disabled for test")

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(compile_package_module, "subprocess", SimpleNamespace(run=_no_npx))
        return compile_package(staging_dir=staging, outputs_dir=outputs, md_filename="pergola_plan.md")


def test_pergola_pipeline_member_counts(pergola_package):
    """Assert 6 posts, 6 beams, 7 primary rafters, 12 knee braces, and 6 footings."""
    members = pergola_package["structure"]["geometry"]["joints"]["resolved_model"]["members"]
    roles = {m["id"]: m["role"] for m in members}
    posts = [mid for mid, r in roles.items() if r == "post"]
    beams = [mid for mid, r in roles.items() if r == "beam"]
    rafters = [mid for mid, r in roles.items() if r == "rafter"]
    braces = [mid for mid, r in roles.items() if r == "brace"]
    footings = [mid for mid, r in roles.items() if r == "footing"]

    assert len(posts) == 6, f"Expected 6 posts, got {len(posts)}"
    assert len(beams) == 6, f"Expected 6 beams, got {len(beams)}"
    assert len(rafters) == 7, f"Expected 7 rafters, got {len(rafters)}"
    assert len(braces) == 12, f"Expected 12 braces, got {len(braces)}"
    assert len(footings) == 6, f"Expected 6 footings, got {len(footings)}"
    assert "HUB" not in roles, "Pergola must not contain a HUB member"


def test_pergola_pipeline_cross_artifact_validation_passes(pergola_package):
    """Cross-artifact validator confirms 100% numerical dimension match between SVG and DXF."""
    errors = validate_dxf_artifacts(str(pergola_package["staging"]), str(pergola_package["outputs"]))
    assert errors == [], f"Cross-artifact DXF validation failed: {errors}"


def test_pergola_pipeline_produces_all_deliverables(compiled_pergola_package, pergola_package):
    """Assert all 8 SVG sheets, 2 DXFs, cut-list.json, and compiled package manifest exist."""
    outputs = pergola_package["outputs"]
    for sheet in SVG_SHEET_FILENAMES:
        assert (outputs / sheet).stat().st_size > 0, f"SVG sheet {sheet} is empty"

    assert (outputs / "cad" / "SB01-structure.dxf").stat().st_size > 0
    assert (outputs / "cad" / "SB02-plan.dxf").stat().st_size > 0

    cut_list_path = outputs / "fabrication" / "cut-list.json"
    assert cut_list_path.exists()
    cut_list = json.loads(cut_list_path.read_text(encoding="utf-8"))
    assert len(cut_list["members"]) > 0

    manifest_path = outputs / "package-manifest.json"
    assert manifest_path.exists(), "package-manifest.json must exist"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["version"] == "1.5"
    assert manifest["topology_family"] == "OrthogonalGridTopology"
    assert len(manifest["artifacts"]) > 0

    for art in manifest["artifacts"]:
        f = outputs / art["path"]
        assert f.exists(), f"Artifact {art['path']} does not exist"
        calc_digest = hashlib.sha256(f.read_bytes()).hexdigest()
        assert calc_digest == art["sha256"], f"Digest mismatch on {art['path']}"


@pytest.mark.parametrize("sheet_id", sorted(SHEET_FILENAMES))
def test_pergola_pipeline_dxf_has_zero_auditor_errors(compiled_pergola_package, pergola_package, sheet_id):
    """DXF sheets must pass ezdxf audit with 0 errors."""
    doc = ezdxf.readfile(pergola_package["outputs"] / "cad" / SHEET_FILENAMES[sheet_id])
    assert doc.audit().errors == []
    assert len(doc.modelspace()) > 0


def test_pergola_pipeline_dxf_member_ids_trace_to_structure(compiled_pergola_package, pergola_package):
    """DXF XDATA tags must trace 1:1 to structure.json member IDs."""
    expected = {m["id"] for m in pergola_package["structure"]["geometry"]["joints"]["resolved_model"]["members"]}
    doc = ezdxf.readfile(pergola_package["outputs"] / "cad" / SHEET_FILENAMES["SB01"])
    seen = {
        tag.value.split("=", 1)[1]
        for e in doc.modelspace()
        if e.has_xdata(APPID)
        for tag in e.get_xdata(APPID)
        if tag.value.startswith("MEMBER_ID=")
    }
    assert seen, "SB01 carries no member_id xdata"
    assert seen <= expected
