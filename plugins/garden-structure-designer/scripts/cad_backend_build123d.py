#!/usr/bin/env python3
"""
cad_backend_build123d.py
========================

Purpose:
    Pure translator of the JSON Geometry Compiler output into build123d solids.
    Reads directly from the resolved_model in structure.json geometry block,
    performing zero geometry math or assumptions.

Layer: Service / 3D Solid Modeling

Not part of the Rust CLI path: 3D solids are separate from the DXF drafting export
    (exchange_writer -> cadcraft_adapter/ezdxf_adapter); this backend only produces STEP.

Key Input Dependencies:
    - structure.json containing geometry.joints.resolved_model, structure.sides (hub polygon),
      geometry.joints.z_planes.Z_APEX and hub, and the member section sizes
      (members.posts/beams, roof.primary_rafters, bracing.brace: actual_width_in/actual_depth_in)
    - build123d library
    - constants.py (MM_PER_FOOT), path_utils.py (default outputs directory), strict_access.py

Key Functions:
    build_hub_solid(hj, z_apex, post_count, ft_to_mm) -> b3d.Solid
    build_member_solid(m, structure, ft_to_mm) -> b3d.Solid | None
    build_cad_model(structure: dict) -> b3d.Compound | None
    export_step(compound, path: str) -> bool
    main() -> None
    _section_for_role(role, structure) -> tuple[dict, str] | None

Usage Examples:
    python3 cad_backend_build123d.py context/staging/structure.json [out.step]
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.append(str(Path(__file__).parent))
from constants import MM_PER_FOOT
from path_utils import outputs_dir
from strict_access import require as _require

try:
    import build123d as b3d

    BUILD123D_AVAILABLE = True
except ImportError:
    BUILD123D_AVAILABLE = False


def _section_for_role(role: str, structure: Dict[str, Any]) -> Optional[tuple]:
    """Returns (section dict, structure.json path) for a member role, or None when the role has no solid."""
    paths = {
        "post": ("members", "posts"),
        "beam": ("members", "beams"),
        "rafter": ("roof", "primary_rafters"),
        "jack_rafter": ("roof", "primary_rafters"),
        "brace": ("bracing", "brace"),
    }
    if role not in paths:
        return None
    top, leaf = paths[role]
    return _require(_require(structure, top, "structure"), leaf, top), f"{top}.{leaf}"


def build_hub_solid(hj: Dict[str, Any], z_apex: float, post_count: int, ft_to_mm: float) -> Any:
    """Constructs a regular polygonal prism solid for the roof apex hub."""
    hr = hj["radius_ft"] * ft_to_mm
    hh = hj["height_ft"] * ft_to_mm
    az = z_apex * ft_to_mm
    with b3d.BuildPart() as p:
        with b3d.BuildSketch():
            b3d.RegularPolygon(radius=hr, side_count=post_count)
        b3d.extrude(amount=hh, both=True)
    s = p.part.translate((0, 0, az))
    s.label = "HUB"
    return s


def build_member_solid(m: Dict[str, Any], structure: Dict[str, Any], ft_to_mm: float) -> Any:
    """Translates a resolved member axis and bounding profile into a build123d Box solid."""
    p0 = [x * ft_to_mm for x in m["p0"]]
    p1 = [x * ft_to_mm for x in m["p1"]]
    u = b3d.Vector(m["axis_u"])
    d = b3d.Vector(m["axis_d"])

    length = math.sqrt(sum((p1[i] - p0[i]) ** 2 for i in range(3)))
    role = m["role"]

    resolved_section = _section_for_role(role, structure)
    if resolved_section is None:
        return None
    spec, label = resolved_section
    width = _require(spec, "actual_width_in", label) / 12.0 * ft_to_mm
    depth = _require(spec, "actual_depth_in", label) / 12.0 * ft_to_mm

    plane = b3d.Plane(origin=p0, x_dir=u, z_dir=d)
    with b3d.BuildPart(plane) as part:
        b3d.Box(length, width, depth, align=(b3d.Align.MIN, b3d.Align.CENTER, b3d.Align.CENTER))
    s = part.part
    s.label = m["id"]
    return s


def build_cad_model(structure: dict) -> Any:
    """Translates resolved_model from structure.json into a build123d Compound."""
    if not BUILD123D_AVAILABLE:
        return None
    ft_to_mm = MM_PER_FOOT
    geom = structure.get("geometry", {})
    resolved = geom.get("joints", {}).get("resolved_model", {})
    if not resolved or not resolved.get("constraints_resolved"):
        return None

    solids = []
    post_count = int(_require(_require(structure, "structure", "structure"), "sides", "structure"))

    for m in resolved.get("members", []):
        if m["role"] == "hub":
            joints = geom.get("joints", {})
            z_apex = _require(joints.get("z_planes"), "Z_APEX", "geometry.joints.z_planes")
            hj = _require(joints, "hub", "geometry.joints")
            s = build_hub_solid(hj, z_apex, post_count, ft_to_mm)
            solids.append(s)
            continue

        s = build_member_solid(m, structure, ft_to_mm)
        if s is not None:
            solids.append(s)

    return b3d.Compound(children=solids)


def export_step(compound: Any, path: str) -> bool:
    """Exports a build123d compound to a STEP CAD exchange file."""
    if not BUILD123D_AVAILABLE or compound is None:
        return False
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        if hasattr(b3d, "export_step"):
            b3d.export_step(compound, str(path))
        else:
            compound.export_step(str(path))
        return True
    except Exception:
        return False


def main() -> None:
    """CLI entrypoint reading structure.json and exporting model.step."""
    if len(sys.argv) < 2:
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        s = json.load(f)
    model = build_cad_model(s)
    if model:
        export_step(model, sys.argv[2] if len(sys.argv) > 2 else str(outputs_dir() / "model.step"))


if __name__ == "__main__":
    main()
