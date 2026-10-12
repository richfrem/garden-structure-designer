"""
test_cad_render_contracts.py
============================

Unit tests verifying cad_render_contracts.py data contracts, errors, and validation rules.
"""
import pytest
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.TopoDS import TopoDS_Shape

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from cad_render_contracts import (
    Anchor,
    LocatedMemberShape,
    AssemblyReceipt,
    SolidAssembly,
    InvalidAnchorError,
    InvalidIdentityError,
    UnsupportedRoleError,
    DuplicateMemberError,
    StaleArtifactError,
    ContractError,
    compute_assembly_sha256,
    validate_solid_assembly,
)


def test_anchor_validation():
    """Verify Anchor requires non-empty IDs and finite coordinates."""
    a = Anchor("A1", "P1", "midpoint", (0.0, 0.0, 100.0), "test")
    assert a.anchor_id == "A1"
    assert a.member_id == "P1"

    with pytest.raises(InvalidAnchorError, match="non-empty"):
        Anchor("", "P1", "midpoint", (0.0, 0.0, 100.0), "test")

    with pytest.raises(InvalidAnchorError, match="not finite"):
        Anchor("A1", "P1", "midpoint", (0.0, float("nan"), 100.0), "test")


def test_located_member_shape_validation():
    """Verify LocatedMemberShape checks for valid IDs, roles, and non-null shapes."""
    box = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0).Shape()
    m = LocatedMemberShape(
        member_id="P1",
        role="post",
        shape=box,
        bounds_mm=((0.0, 0.0, 0.0), (10.0, 10.0, 10.0)),
        anchors=(),
        source_ref="test",
    )
    assert m.member_id == "P1"

    with pytest.raises(InvalidIdentityError):
        LocatedMemberShape("", "post", box, ((0, 0, 0), (10, 10, 10)), (), "test")

    with pytest.raises(UnsupportedRoleError):
        LocatedMemberShape("P1", "", box, ((0, 0, 0), (10, 10, 10)), (), "test")

    with pytest.raises(ContractError, match="shape is null"):
        null_shape = TopoDS_Shape()
        LocatedMemberShape("P1", "post", null_shape, ((0, 0, 0), (10, 10, 10)), (), "test")


def test_solid_assembly_duplicate_member_detection():
    """Verify validate_solid_assembly rejects duplicate member IDs."""
    box = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0).Shape()
    m1 = LocatedMemberShape("P1", "post", box, ((0, 0, 0), (10, 10, 10)), (), "test")
    m2 = LocatedMemberShape("P1", "post", box, ((0, 0, 0), (10, 10, 10)), (), "test")

    receipt = AssemblyReceipt(
        schema_version="2.0",
        source_hash="src_123",
        revision_id="rev_1",
        revision_hash="rev_hash",
        structure_sha256="s_hash",
        assembly_input_sha256="in_hash",
        toolchain=(("build123d", "0.10.0"),),
        member_ids=("P1", "P1"),
        member_roles=(("P1", "post"), ("P1", "post")),
        excluded_members=(),
        member_shape_hashes=(),
        assembly_sha256="asm_sha",
    )

    assembly = SolidAssembly(
        schema_version="2.0",
        units="mm",
        coordinate_system="RH_Z_UP",
        members=(m1, m2),
        bounds_mm=((0, 0, 0), (10, 10, 10)),
        receipt=receipt,
    )

    structure = {
        "meta": {"source_hash": "src_123", "revision_id": "rev_1"},
        "geometry": {"joints": {"resolved_model": {"members": [{}, {}]}}},
    }

    with pytest.raises(DuplicateMemberError, match="Duplicate member ID"):
        validate_solid_assembly(assembly, structure)


def test_solid_assembly_stale_revision_rejection():
    """Verify validate_solid_assembly rejects mismatched revision identity."""
    box = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0).Shape()
    m1 = LocatedMemberShape("P1", "post", box, ((0, 0, 0), (10, 10, 10)), (), "test")

    receipt = AssemblyReceipt(
        schema_version="2.0",
        source_hash="src_old",
        revision_id="rev_old",
        revision_hash="rev_hash",
        structure_sha256="s_hash",
        assembly_input_sha256="in_hash",
        toolchain=(),
        member_ids=("P1",),
        member_roles=(("P1", "post"),),
        excluded_members=(),
        member_shape_hashes=(),
        assembly_sha256="asm_sha",
    )

    assembly = SolidAssembly(
        schema_version="2.0",
        units="mm",
        coordinate_system="RH_Z_UP",
        members=(m1,),
        bounds_mm=((0, 0, 0), (10, 10, 10)),
        receipt=receipt,
    )

    structure = {
        "meta": {"source_hash": "src_new", "revision_id": "rev_new"},
    }

    with pytest.raises(StaleArtifactError, match="source_hash"):
        validate_solid_assembly(assembly, structure)
