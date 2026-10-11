"""
test_radial_production_acceptance.py
====================================
TASK-401 Acceptance Test Suite:
Validates full end-to-end radial pipeline execution across regular polygons
N >= 5 (N = 5, 6, 8, 10, 12 sides) with:
1. Stage 0.5 Intent Validation (cardinality, hub type, topology family)
2. Stage 1 Geometry Solution (geometry._sealed = True, regular polygon coords)
3. Stage 2 Sealed Topology Compilation (N posts, N beams, N rafters, 2N braces, 1 hub)
4. Stage 4/1B CAD DXF Export (SB01 3D structure, SB02 2D plan)
5. Stage 5.5 Parsed DXF Validation & Cross-Artifact Audit (0 ezdxf errors, 1:1 ID parity)
6. Stage 7 Construction Package Compilation (embedded markdown, package-manifest.json digests)
"""

import copy
import hashlib
import json
import math
from pathlib import Path
import sys
from types import SimpleNamespace

import ezdxf
import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
sys.path.insert(0, str(PLUGIN_ROOT))

import compile_package as compile_package_module
from compile_package import compile_package
from cross_artifact_validator import validate_dxf_artifacts
from exchange_writer import APPID
from export_cad import export_sheets, SHEET_FILENAMES
import fabrication_builder
from geometry_engine import compute_from_structure
from render_drawings import generate_svg
from revision_identity import stamp_revision
from tests.test_geometry_engine import STRUCTURE_SEED
from topology_compiler import run_stage as stage2_topology
from validate_topology_intent import run_stage as stage05_intent

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


def _create_radial_seed(sides: int) -> dict:
    s = copy.deepcopy(STRUCTURE_SEED)
    s["structure"]["shape"] = "gazebo"
    s["structure"]["sides"] = sides
    s["layout"]["shape"] = "regular_polygon"
    s["layout"]["post_count"] = sides
    s["roof"]["primary_rafters"]["count"] = sides
    s["hub"]["type"] = "hexagonal_prism" if sides == 6 else ("octagonal_prism" if sides == 8 else "polygonal_cylinder")
    s["meta"]["topology_family"] = "RadialHubTopology"
    s["roof"]["secondary_rafters"]["enabled"] = False
    return s


@pytest.mark.parametrize("n_sides", [5, 6, 8, 10, 12])
def test_radial_pipeline_e2e_polygon(tmp_path, n_sides):
    """Run full Stage 0.5 -> 1 -> 2 -> 4 -> 5.5 -> 6 -> 7 pipeline for polygon with N sides."""
    staging = tmp_path / "context" / "staging"
    outputs = tmp_path / "outputs"
    staging.mkdir(parents=True)
    outputs.mkdir()
    structure_path = staging / "structure.json"

    seed = _create_radial_seed(n_sides)

    # 1. Stage 0.5 Intent Pre-Gate
    res05 = stage05_intent(seed, staging, outputs)
    assert "error_code" not in res05, f"Stage 0.5 rejected N={n_sides}: {res05}"

    # 2. Stage 1 Geometry Solution
    structure_path.write_text(json.dumps(seed), encoding="utf-8")
    sealed = compute_from_structure(str(structure_path))
    assert sealed["geometry"]["_sealed"] is True

    # Verify regular polygon post coordinates
    post_xy = sealed["geometry"]["joints"]["layout"]["post_xy"]
    assert len(post_xy) == n_sides
    r_ft = seed["layout"]["inscribed_radius_ft"]
    for i, pt in enumerate(post_xy):
        expected_angle = 2.0 * math.pi * i / n_sides
        assert abs(pt[0] - round(r_ft * math.cos(expected_angle), 4)) < 1e-3
        assert abs(pt[1] - round(r_ft * math.sin(expected_angle), 4)) < 1e-3

    # 3. Stage 2 Sealed Topology Compiler
    enriched = stage2_topology(sealed, staging, outputs)
    assert "error_code" not in enriched, f"Stage 2 rejected N={n_sides}: {enriched}"
    topo = enriched["geometry"]["joints"]["topology"]
    assert topo["member_count"] == 5 * n_sides + 1  # N posts + N beams + N rafters + 2N braces (bracing enabled in seed) + 1 hub

    # 4. Stamp pure revision
    stamped = stamp_revision(enriched)
    structure_path.write_text(json.dumps(stamped), encoding="utf-8")

    # 5. Stage 4 Render SVGs
    for sheet in SVG_SHEETS:
        generate_svg(sheet, stamped, str(outputs / sheet))
        assert (outputs / sheet).exists()
        assert (outputs / sheet).stat().st_size > 0

    # 6. Stage 6 Fabrication Cut-List
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(fabrication_builder, "outputs_dir", lambda: outputs)
        patch.setattr(sys, "argv", ["fabrication_builder.py", str(structure_path)])
        fabrication_builder.main()
    cut_list_file = outputs / "fabrication" / "cut-list.json"
    assert cut_list_file.exists()
    cut_list_data = json.loads(cut_list_file.read_text(encoding="utf-8"))
    assert len(cut_list_data["members"]) > 0

    # 7. Stage 4/1B DXF Export & Stage 5.5 Parsed DXF Validation
    cad_dir = outputs / "cad"
    cad_dir.mkdir()
    export_sheets(stamped, cad_dir)

    for sheet_id, fname in SHEET_FILENAMES.items():
        dxf_file = cad_dir / fname
        assert dxf_file.exists() and dxf_file.stat().st_size > 0
        doc = ezdxf.readfile(dxf_file)
        assert doc.audit().errors == [], f"Auditor errors in {fname} for N={n_sides}"

    cross_errors = validate_dxf_artifacts(str(staging), str(outputs))
    assert cross_errors == [], f"Cross-artifact validation errors for N={n_sides}: {cross_errors}"

    # 8. Stage 7 Package Compilation
    (staging / "drawing-red-team-report.json").write_text(
        json.dumps({"may_claim_success": True, "summary": f"Approved N={n_sides}"}), encoding="utf-8"
    )
    render_dir = outputs / "high-resolution-image"
    render_dir.mkdir(exist_ok=True)
    (render_dir / "pergola_render_1.png").write_bytes(b"PNG fake data")
    images_md = "\n".join(f"![{name}]({name})" for name in SVG_SHEETS)
    (outputs / "pergola_plan.md").write_text(
        f"# Radial Gazebo N={n_sides}\n{images_md}\n![Render](high-resolution-image/pergola_render_1.png)\n",
        encoding="utf-8"
    )

    def _no_npx(*args, **kwargs):
        raise FileNotFoundError("npx disabled for unit test")

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(compile_package_module, "subprocess", SimpleNamespace(run=_no_npx))
        pkg_res = compile_package(staging_dir=staging, outputs_dir=outputs, md_filename="pergola_plan.md")

    assert pkg_res["status"] in ("COMPLETE", "FALLBACK")
    manifest_path = outputs / "package-manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["version"] == "1.5"
    assert manifest["topology_family"] == "RadialHubTopology"
    assert len(manifest["artifacts"]) > 0

    # Verify every artifact digest in package-manifest.json
    for art in manifest["artifacts"]:
        art_path = outputs / art["path"]
        assert art_path.exists(), f"Manifest lists nonexistent artifact: {art['path']}"
        assert hashlib.sha256(art_path.read_bytes()).hexdigest() == art["sha256"]
