"""Tests for render_presentation_webgl.py: lifecycle, timeout handling, and receipts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from cad_backend_build123d import build_solid_assembly  # type: ignore[import]  # noqa: E402
from cad_export_glb import export_assembly_glb  # type: ignore[import]  # noqa: E402
import render_presentation_webgl as webgl  # type: ignore[import]  # noqa: E402

FIXTURE_PATH = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "rendering"
    / "hex_10ft_yellow_cedar.structure.json"
)


def test_render_presentation_isometric_and_perspective(tmp_path: Path):
    """Verify both isometric and perspective presentation screenshots render and produce receipts."""
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        structure_data = json.load(f)

    assembly = build_solid_assembly(structure_data)
    glb_path = tmp_path / "model.glb"
    export_assembly_glb(assembly, glb_path)

    # 1. Isometric
    iso_png = tmp_path / "iso_render.png"
    receipt_iso = webgl.render_presentation_screenshot(
        glb_path=glb_path,
        output_png=iso_png,
        camera_type="isometric",
        width=1280,
        height=720,
    )
    assert iso_png.exists()
    assert receipt_iso.camera_type == "isometric"
    assert receipt_iso.depth_bits >= 24

    # 2. Perspective
    persp_png = tmp_path / "persp_render.png"
    receipt_persp = webgl.render_presentation_screenshot(
        glb_path=glb_path,
        output_png=persp_png,
        camera_type="perspective",
        width=1280,
        height=720,
    )
    assert persp_png.exists()
    assert receipt_persp.camera_type == "perspective"
    assert receipt_persp.depth_bits >= 24
