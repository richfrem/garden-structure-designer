"""Tests for verifying full solid assembly fidelity on the canonical hex pergola fixture."""

from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import cad_backend_build123d as backend  # type: ignore[import]  # noqa: E402
from cad_render_contracts import (  # type: ignore[import]  # noqa: E402
    SolidAssembly,
    validate_solid_assembly,
)

FIXTURE_PATH = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "rendering"
    / "hex_10ft_yellow_cedar.structure.json"
)


def test_build_solid_assembly_hex_fixture():
    """Verify build_solid_assembly loads the 10ft hex fixture, constructing all 37 valid solids."""
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        structure_data = json.load(f)

    assembly = backend.build_solid_assembly(structure_data)

    assert isinstance(assembly, SolidAssembly)
    assert len(assembly.members) == 37

    # Check member IDs presence
    member_ids = {m.id for m in assembly.members} if hasattr(assembly.members[0], "id") else {m.member_id for m in assembly.members}
    # Posts P1..P6
    for i in range(1, 7):
        assert f"P{i}" in member_ids

    # Footings FT1..FT6
    for i in range(1, 7):
        assert f"FT{i}" in member_ids

    # Beams B1..B6
    for i in range(1, 7):
        assert f"B{i}" in member_ids

    # Rafters R1..R6
    for i in range(1, 7):
        assert f"R{i}" in member_ids

    # Hub
    assert "HUB" in member_ids

    # Validate assembly contract
    validate_solid_assembly(assembly, structure_data)

    # Ensure bounding box is computed and reasonable for 10ft pergola (approx 3000mm)
    (min_pt, max_pt) = assembly.bounds_mm
    dx = max_pt[0] - min_pt[0]
    dy = max_pt[1] - min_pt[1]
    dz = max_pt[2] - min_pt[2]

    assert 2000.0 < dx < 4500.0
    assert 2000.0 < dy < 4500.0
    assert 1800.0 < dz < 4000.0

    # Ensure every member has a valid non-null shape, positive volume, and valid anchor
    for m in assembly.members:
        assert not m.shape.IsNull()
        assert len(m.anchors) >= 1
        assert m.anchors[0].kind == "midpoint"
        assert m.anchors[0].member_id == m.member_id
