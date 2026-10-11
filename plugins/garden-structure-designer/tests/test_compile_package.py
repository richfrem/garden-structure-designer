import sys
import os
import json
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from compile_package import compile_package
from export_cad import export_sheets
from ezdxf_adapter import EzdxfAdapter
from revision_identity import compute_revision_hash

def _minimal_structure():
    ring = [(0.25, 0.25), (-0.25, 0.25), (-0.25, -0.25), (0.25, -0.25)]
    vertices = [[dx, dy, z] for z in (0.0, 8.0) for dx, dy in ring]
    member = {"id": "P1", "role": "post", "p0": [0, 0, 0.0], "p1": [0, 0, 8.0], "vertices": vertices}
    return {
        "meta": {"revision_id": "11111111-2222-3333-4444-555555555555", "revision_hash": "abc123"},
        "geometry": {"joints": {"units": "feet", "resolved_model": {"constraints_resolved": True, "members": [member]}}},
    }

@pytest.fixture
def mock_package_env(tmp_path):
    staging = tmp_path / "context" / "staging"
    staging.mkdir(parents=True)
    outputs = tmp_path / "outputs"
    outputs.mkdir(parents=True)
    img_dir = outputs / "high-resolution-image"
    img_dir.mkdir(parents=True)
    
    # Gate report
    structure = _minimal_structure()
    report = {  # a Stage 5 approval bound to the exact revision being packaged
        "may_claim_success": True, "summary": "Approved",
        "revision_id": structure["meta"]["revision_id"],
        "revision_hash": compute_revision_hash(structure), "hash_algorithm": "gsd-json-v1",
    }
    with open(staging / "drawing-red-team-report.json", "w") as f:
        json.dump(report, f)
        
    (staging / "structure.json").write_text(json.dumps(_minimal_structure()))
    # Stage 4 output: C4 Stage 7 validates these exact bytes and never regenerates them.
    export_sheets(_minimal_structure(), outputs / "cad", EzdxfAdapter())

    # Photorealistic render
    (img_dir / "pergola_render_1.png").write_bytes(b"PNG fake data")
    
    # Sample SVG sheet
    (outputs / "S01-plan-view.svg").write_text('<svg width="100" height="100"><circle cx="50" cy="50" r="40"/></svg>')
    
    # Sample markdown document
    md_content = "# Test Plan\n![Plan View](S01-plan-view.svg)\n![Render](high-resolution-image/pergola_render_1.png)"
    (outputs / "pergola_plan.md").write_text(md_content)
    
    return tmp_path

def test_compile_package_blocked_if_red_team_missing(tmp_path):
    staging = tmp_path / "context" / "staging"
    staging.mkdir(parents=True)
    outputs = tmp_path / "outputs"
    outputs.mkdir(parents=True)
    
    res = compile_package(staging_dir=staging, outputs_dir=outputs, md_filename="pergola_plan.md")
    assert res["status"] == "BLOCKED"
    assert "drawing-red-team-report.json not found" in res["reason"]
    assert (outputs / "COMPILATION_BLOCKED.md").exists()

def test_compile_package_success_and_fallback(mock_package_env):
    staging = mock_package_env / "context" / "staging"
    outputs = mock_package_env / "outputs"
    
    res = compile_package(staging_dir=staging, outputs_dir=outputs, md_filename="pergola_plan.md")
    # Will result in COMPLETE or FALLBACK depending on node / md-to-pdf availability
    assert res["status"] in ("COMPLETE", "FALLBACK")
    assert (outputs / "pergola_plan_embedded.md").exists()
    embedded_text = (outputs / "pergola_plan_embedded.md").read_text()
    assert '<svg' in embedded_text
    assert 'data:image/png;base64,' in embedded_text


def test_compile_package_blocked_if_structure_missing(mock_package_env):
    staging = mock_package_env / "context" / "staging"
    outputs = mock_package_env / "outputs"
    (staging / "structure.json").unlink()

    res = compile_package(staging_dir=staging, outputs_dir=outputs, md_filename="pergola_plan.md")
    assert res["status"] == "BLOCKED"
    assert "structure.json not found" in res["reason"]

def test_compile_package_lists_validated_cad_deliverables(mock_package_env):
    staging = mock_package_env / "context" / "staging"
    outputs = mock_package_env / "outputs"

    res = compile_package(staging_dir=staging, outputs_dir=outputs, md_filename="pergola_plan.md")
    assert [Path(p).name for p in res["cad_deliverables"]] == ["SB01-structure.dxf", "SB02-plan.dxf"]
    assert all(Path(p).stat().st_size > 0 for p in res["cad_deliverables"])


def test_compile_package_writes_package_manifest(mock_package_env):
    staging = mock_package_env / "context" / "staging"
    outputs = mock_package_env / "outputs"

    res = compile_package(staging_dir=staging, outputs_dir=outputs, md_filename="pergola_plan.md")
    manifest_path = outputs / "package-manifest.json"
    assert manifest_path.exists(), "outputs/package-manifest.json must be generated"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["version"] == "1.5"
    assert manifest["revision_id"] == "11111111-2222-3333-4444-555555555555"
    assert manifest["revision_hash"] == "abc123"
    assert "artifacts" in manifest
    assert len(manifest["artifacts"]) > 0
    # Every artifact must have a valid sha256 hex digest
    for art in manifest["artifacts"]:
        assert len(art["sha256"]) == 64
        assert (outputs / art["path"]).exists()

