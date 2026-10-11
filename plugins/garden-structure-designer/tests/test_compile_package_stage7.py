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
