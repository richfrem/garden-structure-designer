"""Tests for Three.js presentation viewer served over loopback with Playwright."""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright

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


def test_presentation_viewer_ready_state(tmp_path: Path):
    """Verify viewer initializes, loads GLB, verifies >= 24-bit depth, and achieves ready state."""
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        structure_data = json.load(f)

    assembly = build_solid_assembly(structure_data)
    glb_path = tmp_path / "model.glb"
    export_receipt = export_assembly_glb(assembly, glb_path)

    # Render presentation screenshot via Playwright loopback server
    out_png = tmp_path / "presentation.png"
    receipt = webgl.render_presentation_screenshot(
        glb_path=glb_path,
        output_png=out_png,
        camera_type="isometric",
        width=1920,
        height=1080,
    )

    assert out_png.exists()
    assert out_png.stat().st_size > 5000  # Substantial rendered PNG image
    assert receipt.depth_bits >= 24
    assert receipt.status == "ready"
