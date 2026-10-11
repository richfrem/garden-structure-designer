"""C4 Stage 7: validate the exact DXF bytes being packaged; never regenerate drawings after approval."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

import ezdxf
import pytest

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from test_compile_package import _minimal_structure, mock_package_env  # type: ignore[import]  # noqa: E402,F401
import compile_package as compile_package_module  # type: ignore[import]  # noqa: E402
from compile_package import compile_package  # type: ignore[import]  # noqa: E402
from constants import SHEET_FILENAMES  # type: ignore[import]  # noqa: E402
from export_cad import export_sheets  # type: ignore[import]  # noqa: E402
from revision_identity import compute_revision_hash  # type: ignore[import]  # noqa: E402
from ezdxf_adapter import EzdxfAdapter  # type: ignore[import]  # noqa: E402


@pytest.fixture(autouse=True)
def _no_pdf_toolchain(monkeypatch):
    """PDF conversion shells out to npx (network); Stage 7 DXF behavior is independent of it."""
    monkeypatch.setattr(compile_package_module, "convert_md_to_pdf", lambda *a, **k: (False, "stubbed"))


def _run(env):
    return compile_package(
        staging_dir=env / "context" / "staging", outputs_dir=env / "outputs", md_filename="pergola_plan.md"
    )


def _stage4_export(env):
    """Simulate Stage 4: the CAD sheets exist before Stage 7 runs."""
    export_sheets(_minimal_structure(), env / "outputs" / "cad", EzdxfAdapter())


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_stage7_does_not_regenerate_missing_dxfs(mock_package_env):
    shutil.rmtree(mock_package_env / "outputs" / "cad")
    result = _run(mock_package_env)
    assert result["status"] == "FAIL"
    assert "MISSING_DXF" in result["reason"]
    assert not (mock_package_env / "outputs" / "cad").exists() or not any(
        (mock_package_env / "outputs" / "cad").iterdir()
    )


def test_stage7_keeps_approved_dxf_bytes(mock_package_env):
    _stage4_export(mock_package_env)
    cad = mock_package_env / "outputs" / "cad"
    before = {name: _digest(cad / name) for name in SHEET_FILENAMES.values()}
    result = _run(mock_package_env)
    assert result["status"] in ("COMPLETE", "FALLBACK")
    assert {name: _digest(cad / name) for name in SHEET_FILENAMES.values()} == before


def test_stage7_rejects_tampered_dxf_with_parsed_validator(mock_package_env):
    _stage4_export(mock_package_env)
    path = mock_package_env / "outputs" / "cad" / SHEET_FILENAMES["SB01"]
    doc = ezdxf.readfile(path)
    entity = next(e for e in doc.modelspace() if e.has_xdata("GSD"))
    entity.vertices[0].dxf.location = entity.vertices[0].dxf.location + (5.0, 0, 0)
    doc.saveas(path)
    result = _run(mock_package_env)
    assert result["status"] == "FAIL"
    assert "bounds differ" in result["reason"]


def test_manifest_has_no_invented_schema_defaults(mock_package_env):
    """meta.schema_version / topology_family absent in the structure must not be fabricated."""
    _stage4_export(mock_package_env)
    _run(mock_package_env)
    manifest = json.loads((mock_package_env / "outputs" / "package-manifest.json").read_text())
    assert manifest["schema_version"] is None
    assert manifest["topology_family"] is None


def _approval(root, **overrides):
    structure = json.loads((root / "context" / "staging" / "structure.json").read_text())
    meta = structure["meta"]
    report = {"may_claim_success": True, "summary": "Approved", "revision_id": meta["revision_id"],
              "revision_hash": compute_revision_hash(structure), "hash_algorithm": "gsd-json-v1"}
    report.update(overrides)
    (root / "context" / "staging" / "drawing-red-team-report.json").write_text(json.dumps(report))


def test_approval_bound_to_current_revision_passes(mock_package_env):
    _stage4_export(mock_package_env)
    _approval(mock_package_env)
    assert _run(mock_package_env)["status"] in ("COMPLETE", "FALLBACK")


@pytest.mark.parametrize("overrides", [
    {"revision_id": "another-revision"},
    {"revision_hash": "0" * 64},
    {"hash_algorithm": "md5"},
])
def test_approval_for_another_revision_blocks_packaging(mock_package_env, overrides):
    _stage4_export(mock_package_env)
    _approval(mock_package_env, **overrides)
    result = _run(mock_package_env)
    assert result["status"] == "BLOCKED" and "not bound to the current revision" in result["reason"]


def test_approval_without_revision_binding_blocks_packaging(mock_package_env):
    _stage4_export(mock_package_env)
    (mock_package_env / "context" / "staging" / "drawing-red-team-report.json").write_text(
        json.dumps({"may_claim_success": True, "summary": "legacy report"})
    )
    assert _run(mock_package_env)["status"] == "BLOCKED"
