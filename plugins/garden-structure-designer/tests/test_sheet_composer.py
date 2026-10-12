"""Tests for sheet_composer.py: vector and raster backgrounds with midpoint labeling and dimensions."""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from cad_backend_build123d import build_solid_assembly  # type: ignore[import]  # noqa: E402
from cad_camera import create_standard_camera, SheetTransform  # type: ignore[import]  # noqa: E402
from cad_projection_hlr import project_assembly_hlr  # type: ignore[import]  # noqa: E402
import sheet_composer as sc  # type: ignore[import]  # noqa: E402

FIXTURE_PATH = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "rendering"
    / "hex_10ft_yellow_cedar.structure.json"
)


def test_compose_sheet_vector():
    """Verify compose_sheet generates valid SVG with HLR vector background, title block, and labels."""
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        structure_data = json.load(f)

    assembly = build_solid_assembly(structure_data)
    camera = create_standard_camera("isometric", target_mm=(0.0, 0.0, 1500.0))
    hlr_result = project_assembly_hlr(assembly, camera)

    sheet_spec = sc.SheetSpec(
        sheet_id="SB01",
        dwg_name="Isometric Framing Blueprint",
        is_blueprint=True,
        width_px=1600,
        height_px=1200,
    )

    svg_content = sc.compose_sheet(
        assembly=assembly,
        camera=camera,
        sheet_spec=sheet_spec,
        background=hlr_result,
        structure=structure_data,
    )

    assert "<svg" in svg_content
    assert "</svg>" in svg_content
    assert 'data-role="title-block"' in svg_content
    assert 'data-tag="HUB"' in svg_content
    assert 'data-tag="P1"' in svg_content
    # Check validator anchors
    assert "VALIDATOR_ANCHORS" in svg_content


def test_compose_sheet_raster(tmp_path: Path):
    """Verify compose_sheet overlays annotations on an embedded WebGL raster PNG background."""
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        structure_data = json.load(f)

    assembly = build_solid_assembly(structure_data)
    camera = create_standard_camera("isometric", target_mm=(0.0, 0.0, 1500.0))

    # Fake a small valid 1x1 PNG or write a dummy file
    dummy_png = tmp_path / "bg.png"
    import base64
    # 1x1 white PNG base64
    png_bytes = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVR4nGNiAAAABgADNjd8qAAAAABJRU5ErkJggg==")
    dummy_png.write_bytes(png_bytes)

    sheet_spec = sc.SheetSpec(
        sheet_id="DWG-03",
        dwg_name="Isometric Shaded Presentation",
        is_blueprint=False,
        width_px=1600,
        height_px=1200,
    )

    svg_content = sc.compose_sheet(
        assembly=assembly,
        camera=camera,
        sheet_spec=sheet_spec,
        background=dummy_png,
        structure=structure_data,
    )

    assert "<svg" in svg_content
    assert "<image" in svg_content
    assert 'data-role="presentation-canvas"' in svg_content
    assert 'data-tag="P1"' in svg_content
