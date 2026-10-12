#!/usr/bin/env python3
"""
cad_export_glb.py
=================

Purpose:
    Exports the authoritative SolidAssembly to binary glTF (GLB) for photorealistic
    WebGL presentation rendering, generating a sidecar JSON manifest with member IDs,
    roles, bounds, and cryptographic assembly hash.

Layer: Service / GLB Exporter
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple

import build123d as b3d

from cad_render_contracts import SolidAssembly, Bounds3


@dataclass(frozen=True)
class GlbExportReceipt:
    """Cryptographic provenance receipt binding exported GLB to solid assembly."""
    glb_path: str
    manifest_path: str
    glb_sha256: str
    assembly_sha256: str
    member_count: int
    file_size_bytes: int


def export_assembly_glb(
    assembly: SolidAssembly,
    output_glb_path: Path,
    linear_deflection: float = 0.5,  # 0.5mm chord tolerance for tessellation
    angular_deflection: float = 0.1,  # ~5.7 deg angular tolerance
) -> GlbExportReceipt:
    """
    Exports SolidAssembly to a binary GLB file and companion manifest.
    """
    output_glb_path = Path(output_glb_path).resolve()
    output_glb_path.parent.mkdir(parents=True, exist_ok=True)

    # Construct build123d Compound with labeled children
    solids = []
    member_manifest_entries = []

    for m in assembly.members:
        # Wrap native OCP shape into build123d.Solid
        s = b3d.Solid(m.shape)
        s.label = m.member_id
        solids.append(s)

        member_manifest_entries.append({
            "member_id": m.member_id,
            "role": m.role,
            "bounds_mm": m.bounds_mm,
            "anchors": [
                {
                    "anchor_id": a.anchor_id,
                    "kind": a.kind,
                    "world_mm": a.world_mm,
                }
                for a in m.anchors
            ],
        })

    compound = b3d.Compound(children=solids)

    # Export using build123d.export_gltf.
    # Note: build123d defaults to assuming solids are in meters if Unit.MM is passed (dividing by 1000).
    # Since our solid assembly coordinates are already in millimeters, Unit.M exports raw mm 1:1.
    success = b3d.export_gltf(
        compound,
        str(output_glb_path),
        unit=b3d.Unit.M,
        binary=True,
        linear_deflection=linear_deflection,
        angular_deflection=angular_deflection,
    )
    if not success or not output_glb_path.exists():
        raise RuntimeError(f"Failed to export GLB to {output_glb_path}")

    # OpenCASCADE RWGltf_CafWriter automatically adds a -90 deg rotation around X
    # to convert from Z-up to glTF Y-up. For true CAD alignment (RH_Z_UP), we strip
    # this root rotation so that standard glTF viewers and WebGL renderers receive
    # the exact upright CAD assembly matching the 2D drawings and SQLite/JSON coordinates.
    try:
        import struct
        with open(output_glb_path, "rb") as f:
            glb_raw = f.read()
        magic, ver, total_len = struct.unpack("<III", glb_raw[:12])
        if magic == 0x46546C67:  # 'glTF'
            chunk0_len, chunk0_type = struct.unpack("<II", glb_raw[12:20])
            json_bytes = glb_raw[20 : 20 + chunk0_len]
            bin_chunk = glb_raw[20 + chunk0_len :]
            gltf_dict = json.loads(json_bytes.decode("utf-8"))
            if gltf_dict.get("nodes") and "rotation" in gltf_dict["nodes"][0]:
                del gltf_dict["nodes"][0]["rotation"]
                new_json_bytes = json.dumps(gltf_dict, separators=(",", ":")).encode("utf-8")
                pad = (4 - (len(new_json_bytes) % 4)) % 4
                new_json_bytes += b" " * pad
                new_chunk0_header = struct.pack("<II", len(new_json_bytes), chunk0_type)
                new_total_len = 12 + 8 + len(new_json_bytes) + len(bin_chunk)
                new_header = struct.pack("<III", magic, ver, new_total_len)
                with open(output_glb_path, "wb") as f:
                    f.write(new_header + new_chunk0_header + new_json_bytes + bin_chunk)
    except Exception as norm_err:
        # Non-fatal fallback: preserve file if binary patching fails
        pass

    # Compute GLB sha256
    hasher = hashlib.sha256()
    with open(output_glb_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    glb_sha = hasher.hexdigest()

    # Write sidecar manifest
    manifest_path = output_glb_path.with_name(f"{output_glb_path.name}.manifest.json")
    manifest_data = {
        "schema_version": "2.0",
        "assembly_sha256": assembly.receipt.assembly_sha256,
        "glb_sha256": glb_sha,
        "units": "mm",
        "coordinate_system": "RH_Z_UP",
        "bounds_mm": assembly.bounds_mm,
        "members": member_manifest_entries,
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

    return GlbExportReceipt(
        glb_path=str(output_glb_path),
        manifest_path=str(manifest_path),
        glb_sha256=glb_sha,
        assembly_sha256=assembly.receipt.assembly_sha256,
        member_count=len(assembly.members),
        file_size_bytes=output_glb_path.stat().st_size,
    )
