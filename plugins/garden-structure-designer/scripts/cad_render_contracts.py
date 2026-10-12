#!/usr/bin/env python3
"""
cad_render_contracts.py
=======================

Purpose:
    Core data contracts, typed receipts, and validation models for the authoritative
    CAD solid assembly and rendering pipeline. Ensures strict provenance, immutable
    contracts, semantic anchors, and cross-layer traceability between structure.json,
    OpenCASCADE HLR vector blueprints, and WebGL presentation rendering.

Layer: Domain / Infrastructure Contracts
"""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import math
from typing import Any, Literal, Mapping, Sequence, Tuple

from OCP.TopoDS import TopoDS_Shape


Vec3 = Tuple[float, float, float]
Bounds3 = Tuple[Vec3, Vec3]


# --- Typed Domain Errors ---

class ContractError(ValueError):
    """Base error for CAD render contract violations."""


class InvalidIdentityError(ContractError):
    """Raised when a member ID, revision ID, or source hash is missing, invalid, or duplicate."""


class InvalidAnchorError(ContractError):
    """Raised when a 3D semantic anchor contains non-finite values or invalid metadata."""


class UnsupportedRoleError(ContractError):
    """Raised when an unrecognized or unsupported member role is encountered."""


class StaleArtifactError(ContractError):
    """Raised when artifact receipts or hashes fail to match the active geometry revision."""


class DuplicateMemberError(ContractError):
    """Raised when multiple members share the same member ID in an assembly."""


# --- Core Dataclasses ---

@dataclass(frozen=True)
class Anchor:
    """A semantic 3D reference point for labels, dimension strings, or joint centers."""
    anchor_id: str
    member_id: str
    kind: Literal["midpoint", "endpoint", "dimension", "joint", "datum"]
    world_mm: Vec3
    source_ref: str

    def __post_init__(self) -> None:
        if not self.anchor_id or not self.member_id:
            raise InvalidAnchorError("Anchor must have non-empty anchor_id and member_id")
        for val in self.world_mm:
            if not math.isfinite(val):
                raise InvalidAnchorError(f"Anchor {self.anchor_id} coordinate {val} is not finite")


@dataclass(frozen=True)
class LocatedMemberShape:
    """A single structural member's authoritative 3D B-Rep solid, fully located in CAD space."""
    member_id: str
    role: str
    shape: TopoDS_Shape
    bounds_mm: Bounds3
    anchors: Tuple[Anchor, ...]
    source_ref: str

    def __post_init__(self) -> None:
        if not self.member_id:
            raise InvalidIdentityError("LocatedMemberShape requires a non-empty member_id")
        if not self.role:
            raise UnsupportedRoleError(f"Member {self.member_id} requires a non-empty role")
        if self.shape.IsNull():
            raise ContractError(f"Member {self.member_id} shape is null")
        (min_pt, max_pt) = self.bounds_mm
        for pt in (min_pt, max_pt):
            for v in pt:
                if not math.isfinite(v):
                    raise ContractError(f"Member {self.member_id} bounds contain non-finite coordinate {v}")


@dataclass(frozen=True)
class AssemblyReceipt:
    """Cryptographic provenance receipt binding the solid assembly to structure.json."""
    schema_version: str
    source_hash: str
    revision_id: str
    revision_hash: str
    structure_sha256: str
    assembly_input_sha256: str
    toolchain: Tuple[Tuple[str, str], ...]
    member_ids: Tuple[str, ...]
    member_roles: Tuple[Tuple[str, str], ...]
    excluded_members: Tuple[Tuple[str, str], ...]
    member_shape_hashes: Tuple[Tuple[str, str], ...]
    assembly_sha256: str


@dataclass(frozen=True)
class SolidAssembly:
    """Authoritative, member-indexed 3D solid assembly from which all views derive."""
    schema_version: str
    units: Literal["mm"]
    coordinate_system: Literal["RH_Z_UP"]
    members: Tuple[LocatedMemberShape, ...]
    bounds_mm: Bounds3
    receipt: AssemblyReceipt

    @property
    def member_map(self) -> Mapping[str, LocatedMemberShape]:
        """Convenience map of member_id -> LocatedMemberShape."""
        return {m.member_id: m for m in self.members}

    @property
    def anchor_map(self) -> Mapping[str, Anchor]:
        """Convenience map of anchor_id -> Anchor across all members."""
        res = {}
        for m in self.members:
            for a in m.anchors:
                res[a.anchor_id] = a
        return res


def compute_assembly_sha256(
    structure_sha256: str,
    member_ids: Sequence[str],
    bounds_mm: Bounds3,
) -> str:
    """Computes a deterministic SHA256 digest identifying the assembly geometry state."""
    hasher = hashlib.sha256()
    hasher.update(structure_sha256.encode("utf-8"))
    for mid in sorted(member_ids):
        hasher.update(f":{mid}".encode("utf-8"))
    b_str = f":{bounds_mm[0][0]:.3f},{bounds_mm[0][1]:.3f},{bounds_mm[0][2]:.3f}-{bounds_mm[1][0]:.3f},{bounds_mm[1][1]:.3f},{bounds_mm[1][2]:.3f}"
    hasher.update(b_str.encode("utf-8"))
    return hasher.hexdigest()


def validate_solid_assembly(assembly: SolidAssembly, structure: dict) -> None:
    """Validates that a SolidAssembly strictly complies with the design specification."""
    if assembly.units != "mm":
        raise ContractError(f"Expected assembly units 'mm', got '{assembly.units}'")
    if assembly.coordinate_system != "RH_Z_UP":
        raise ContractError(f"Expected coordinate system 'RH_Z_UP', got '{assembly.coordinate_system}'")

    meta = structure.get("meta", {})
    if meta.get("source_hash") and assembly.receipt.source_hash != meta.get("source_hash"):
        raise StaleArtifactError(
            f"Assembly source_hash '{assembly.receipt.source_hash}' does not match structure '{meta.get('source_hash')}'"
        )
    if meta.get("revision_id") and assembly.receipt.revision_id != meta.get("revision_id"):
        raise StaleArtifactError(
            f"Assembly revision_id '{assembly.receipt.revision_id}' does not match structure '{meta.get('revision_id')}'"
        )

    # Check unique member IDs
    seen_ids = set()
    for m in assembly.members:
        if m.member_id in seen_ids:
            raise DuplicateMemberError(f"Duplicate member ID detected in assembly: {m.member_id}")
        seen_ids.add(m.member_id)

    # Validate resolved_model count matches assembly count
    resolved = structure.get("geometry", {}).get("joints", {}).get("resolved_model", {})
    source_members = resolved.get("members", [])
    if source_members and len(source_members) != len(assembly.members):
        raise ContractError(
            f"Assembly member count ({len(assembly.members)}) does not match resolved_model count ({len(source_members)})"
        )
