"""Tests for cad_projection_hlr.py: global solver, member attribution, and mutual occlusion."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import cad_camera as cam  # type: ignore[import]  # noqa: E402
import cad_projection_hlr as hlr  # type: ignore[import]  # noqa: E402
from cad_backend_build123d import build_solid_assembly  # type: ignore[import]  # noqa: E402
from cad_render_contracts import SolidAssembly  # type: ignore[import]  # noqa: E402

FIXTURE_PATH = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "rendering"
    / "hex_10ft_yellow_cedar.structure.json"
)


def test_project_assembly_hlr_crossing_timbers():
    """Verify mutual occlusion on the crossing timbers fixture via cad_projection_hlr."""
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
    from OCP.gp import gp_Pnt
    from cad_render_contracts import LocatedMemberShape, AssemblyReceipt

    # Foreground timber along X axis: -500 to 500, Y: -50 to 50, Z: 100 to 200
    front_shape = BRepPrimAPI_MakeBox(gp_Pnt(-500.0, -50.0, 100.0), 1000.0, 100.0, 100.0).Shape()
    # Background timber along Y axis: X: -50 to 50, Y: -500 to 500, Z: -100 to 0
    back_shape = BRepPrimAPI_MakeBox(gp_Pnt(-50.0, -500.0, -100.0), 100.0, 1000.0, 100.0).Shape()

    m_front = LocatedMemberShape(
        member_id="M_FRONT",
        role="beam",
        shape=front_shape,
        bounds_mm=((-500, -50, 100), (500, 50, 200)),
        anchors=(),
        source_ref="test.front",
    )
    m_back = LocatedMemberShape(
        member_id="M_BACK",
        role="post",
        shape=back_shape,
        bounds_mm=((-50, -500, -100), (50, 500, 0)),
        anchors=(),
        source_ref="test.back",
    )

    receipt = AssemblyReceipt(
        schema_version="2.0",
        source_hash="test",
        revision_id="rev1",
        revision_hash="revhash",
        structure_sha256="sha",
        assembly_input_sha256="sha",
        toolchain=(("test", "1.0"),),
        member_ids=("M_FRONT", "M_BACK"),
        member_roles=(("M_FRONT", "beam"), ("M_BACK", "post")),
        excluded_members=(),
        member_shape_hashes=(),
        assembly_sha256="ashash",
    )
    assembly = SolidAssembly(
        schema_version="2.0",
        units="mm",
        coordinate_system="RH_Z_UP",
        members=(m_front, m_back),
        bounds_mm=((-500, -500, -100), (500, 500, 200)),
        receipt=receipt,
    )

    # Looking straight down from top (+Z)
    camera = cam.create_standard_camera(view_type="plan", target_mm=(0.0, 0.0, 0.0))

    result = hlr.project_assembly_hlr(assembly, camera)

    assert isinstance(result, hlr.HLRProjectionResult)
    assert result.camera_id == camera.camera_id

    # Verify members present in result
    assert "M_FRONT" in result.members
    assert "M_BACK" in result.members

    front_res = result.members["M_FRONT"]
    back_res = result.members["M_BACK"]

    # Foreground timber should have 4 visible bounding edges
    assert len(front_res.visible_edges) == 4
    # Self-hidden bottom edges: 4 edges
    assert len(front_res.hidden_edges) == 4

    # Background timber should have visible edges split into 2 disconnected wings (6 visible edges total)
    assert len(back_res.visible_edges) == 6
    # Hidden edges should include self-hidden and occluded crossing interval (6 hidden edges)
    assert len(back_res.hidden_edges) == 6


def test_project_assembly_hlr_hex_fixture():
    """Verify HLR projection succeeds on the full 37-member hexagonal pergola assembly."""
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        structure_data = json.load(f)

    assembly = build_solid_assembly(structure_data)
    camera = cam.create_standard_camera(view_type="isometric", target_mm=(0.0, 0.0, 1500.0))

    result = hlr.project_assembly_hlr(assembly, camera)

    assert isinstance(result, hlr.HLRProjectionResult)
    assert len(result.members) == 37

    # Total visible edges across all members should be substantial (> 100)
    total_visible = sum(len(m.visible_edges) for m in result.members.values())
    total_hidden = sum(len(m.hidden_edges) for m in result.members.values())

    assert total_visible > 100
    assert total_hidden > 50

    # Check key members have visible edges (posts, beams, hub)
    assert len(result.members["HUB"].visible_edges) > 0
    assert len(result.members["P1"].visible_edges) > 0
    assert len(result.members["B1"].visible_edges) > 0
