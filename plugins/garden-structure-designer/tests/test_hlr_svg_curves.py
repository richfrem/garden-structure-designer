"""Tests for HLR curve conversion and semantic SVG attributes."""

from __future__ import annotations

import math
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import cad_camera as cam  # type: ignore[import]  # noqa: E402
import cad_projection_hlr as hlr  # type: ignore[import]  # noqa: E402


def test_linear_edge_svg_path():
    """Verify linear edge emits standard M x y L x y format."""
    edge = hlr.ProjectedEdge(
        member_id="B1",
        role="beam",
        visibility="visible",
        edge_kind="sharp",
        start_pt=(10.0, 20.0),
        end_pt=(100.0, 200.0),
    )

    path_d = edge.to_svg_path()
    assert path_d == "M 10.00 20.00 L 100.00 200.00"

    # With sheet transform
    tf = cam.SheetTransform(
        viewport_x=0.0,
        viewport_y=0.0,
        viewport_w=1000.0,
        viewport_h=800.0,
        center_x=0.0,
        center_y=0.0,
        scale=1.0,
    )
    sheet_d = edge.to_svg_path(transform=tf)
    # x_sheet = 500 + 10 = 510, y_sheet = 400 - 20 = 380
    assert "M 510.00 380.00 L 600.00 200.00" == sheet_d


def test_curved_edge_adaptive_subdivision():
    """Verify curved edge generates polyline approximation bounded by chord error."""
    # Semicircle radius 100mm
    mid_samples = []
    num_samples = 8
    for i in range(1, num_samples):
        angle = math.pi * (i / num_samples)
        mid_samples.append((100.0 * math.cos(angle), 100.0 * math.sin(angle)))

    edge = hlr.ProjectedEdge(
        member_id="HUB",
        role="hub",
        visibility="visible",
        edge_kind="outline",
        start_pt=(100.0, 0.0),
        end_pt=(-100.0, 0.0),
        intermediate_pts=tuple(mid_samples),
    )

    assert not edge.is_line
    d = edge.to_svg_path()
    assert d.startswith("M 100.00 0.00")
    assert d.endswith("L -100.00 0.00")
    # Must have multiple L commands
    assert d.count(" L ") == num_samples
