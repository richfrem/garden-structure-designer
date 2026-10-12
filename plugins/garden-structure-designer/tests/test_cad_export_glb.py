"""Tests for cad_export_glb.py: authoritative assembly to GLB export with member mapping."""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from cad_backend_build123d import build_solid_assembly  # type: ignore[import]  # noqa: E402
import cad_export_glb as exp  # type: ignore[import]  # noqa: E402

FIXTURE_PATH = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "rendering"
    / "hex_10ft_yellow_cedar.structure.json"
)


def test_export_assembly_glb(tmp_path: Path):
    """Verify export_assembly_glb exports valid GLB file and sidecar manifest matching all members."""
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        structure_data = json.load(f)

    assembly = build_solid_assembly(structure_data)
    out_glb = tmp_path / "model.glb"

    receipt = exp.export_assembly_glb(assembly, out_glb)

    assert isinstance(receipt, exp.GlbExportReceipt)
    assert out_glb.exists()
    assert out_glb.stat().st_size > 1000  # Should be substantial binary glTF

    # Check sidecar manifest
    out_json = tmp_path / "model.glb.manifest.json"
    assert out_json.exists()
    with open(out_json, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["assembly_sha256"] == assembly.receipt.assembly_sha256
    assert len(manifest["members"]) == 37

    # Ensure all member IDs exist in manifest
    member_ids = {m["member_id"] for m in manifest["members"]}
    assert "HUB" in member_ids
    assert "P1" in member_ids
    assert "B1" in member_ids
