#!/usr/bin/env python3
"""
cad_backend_build123d.py
========================

Purpose:
    Authoritative 3D CAD B-Rep solid modeler and assembly generator.
    Translates the resolved_model from structure.json into exact OpenCASCADE B-Rep
    solids (preserving all cut miters, notches, and hub polygons) and packages them
    into a typed SolidAssembly.

Layer: Service / 3D Solid Modeling
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple

sys.path.append(str(Path(__file__).parent))
from constants import MM_PER_FOOT
from path_utils import outputs_dir
from strict_access import require as _require
from cad_render_contracts import (
    Anchor,
    LocatedMemberShape,
    AssemblyReceipt,
    SolidAssembly,
    compute_assembly_sha256,
    validate_solid_assembly,
    ContractError,
)

try:
    import build123d as b3d
    from OCP.BRepBuilderAPI import (
        BRepBuilderAPI_MakePolygon,
        BRepBuilderAPI_MakeFace,
        BRepBuilderAPI_Sewing,
        BRepBuilderAPI_MakeSolid,
    )
    from OCP.gp import gp_Pnt
    from OCP.TopoDS import TopoDS, TopoDS_Shape
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    from OCP.BRepCheck import BRepCheck_Analyzer

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
        "footing": ("members", "posts"), # default bounding section for footings
    }
    if role not in paths:
        return None
    top, leaf = paths[role]
    spec = structure.get(top, {}).get(leaf)
    if spec is None:
        return None
    return spec, f"{top}.{leaf}"


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


def make_solid_from_faces(verts: List[List[float]], faces: List[Dict[str, Any]], ft_to_mm: float = MM_PER_FOOT) -> TopoDS_Shape:
    """Constructs an exact closed B-Rep solid from planar polygon faces."""
    sewing = BRepBuilderAPI_Sewing(1e-2)
    for f in faces:
        poly = BRepBuilderAPI_MakePolygon()
        for idx in f["verts"]:
            v = verts[idx]
            poly.Add(gp_Pnt(v[0] * ft_to_mm, v[1] * ft_to_mm, v[2] * ft_to_mm))
        poly.Close()
        wire = poly.Wire()
        face = BRepBuilderAPI_MakeFace(wire, True).Face()
        sewing.Add(face)
    sewing.Perform()
    shell = TopoDS.Shell_s(sewing.SewedShape())
    maker = BRepBuilderAPI_MakeSolid()
    maker.Add(shell)
    sol = maker.Solid()

    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(sol, props)
    if props.Mass() < 0:
        sol = TopoDS.Solid_s(sol.Reversed())
    return sol


def get_shape_bounds_mm(shape: TopoDS_Shape) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """Calculates axis-aligned bounding box coordinates (min, max) in millimetres."""
    box = Bnd_Box()
    BRepBndLib.Add_s(shape, box)
    xmin, ymin, zmin, xmax, ymax, zmax = box.Get()
    return ((xmin, ymin, zmin), (xmax, ymax, zmax))


def build_member_solid(m: Dict[str, Any], structure: Dict[str, Any], ft_to_mm: float) -> Any:
    """Translates a resolved member axis and bounding profile into a build123d Solid."""
    # If the resolved model includes exact faces and vertices (e.g. notched rafters, mitered beams)
    if "faces" in m and "vertices" in m and m["faces"] and m["vertices"]:
        ocp_solid = make_solid_from_faces(m["vertices"], m["faces"], ft_to_mm)
        s = b3d.Solid(ocp_solid)
        s.label = m.get("id", "MEMBER")
        return s

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
    s.label = m.get("id", "MEMBER")
    return s


def build_solid_assembly(structure: dict) -> SolidAssembly:
    """Builds the authoritative, member-indexed SolidAssembly from structure.json."""
    if not BUILD123D_AVAILABLE:
        raise ContractError("build123d / OCP is not installed in the environment")

    ft_to_mm = MM_PER_FOOT
    geom = structure.get("geometry", {})
    resolved = geom.get("joints", {}).get("resolved_model", {})
    if not resolved or not resolved.get("constraints_resolved"):
        raise ContractError("geometry.joints.resolved_model must have constraints_resolved: true")

    post_count = int(_require(_require(structure, "structure", "structure"), "sides", "structure"))
    located_members: List[LocatedMemberShape] = []

    for m in resolved.get("members", []):
        mid = m["id"]
        role = m["role"]

        if role == "hub":
            joints = geom.get("joints", {})
            z_apex = _require(joints.get("z_planes"), "Z_APEX", "geometry.joints.z_planes")
            hj = _require(joints, "hub", "geometry.joints")
            hub_s = build_hub_solid(hj, z_apex, post_count, ft_to_mm)
            ocp_shape = hub_s.wrapped
        else:
            solid_s = build_member_solid(m, structure, ft_to_mm)
            if solid_s is None:
                raise ContractError(f"Failed to generate solid for required member {mid} ({role})")
            ocp_shape = solid_s.wrapped

        bounds = get_shape_bounds_mm(ocp_shape)
        # Calculate semantic midpoint anchor
        if "p0" in m and "p1" in m:
            mid_pt = tuple((m["p0"][i] + m["p1"][i]) / 2.0 * ft_to_mm for i in range(3))
        else:
            mid_pt = tuple((bounds[0][i] + bounds[1][i]) / 2.0 for i in range(3))

        anchor = Anchor(
            anchor_id=f"anchor_{mid}_mid",
            member_id=mid,
            kind="midpoint",
            world_mm=mid_pt,
            source_ref=f"resolved_model.{mid}",
        )

        located = LocatedMemberShape(
            member_id=mid,
            role=role,
            shape=ocp_shape,
            bounds_mm=bounds,
            anchors=(anchor,),
            source_ref=f"geometry.joints.resolved_model.{mid}",
        )
        located_members.append(located)

    # Compute overall assembly bounds
    all_min_x = min(m.bounds_mm[0][0] for m in located_members)
    all_min_y = min(m.bounds_mm[0][1] for m in located_members)
    all_min_z = min(m.bounds_mm[0][2] for m in located_members)
    all_max_x = max(m.bounds_mm[1][0] for m in located_members)
    all_max_y = max(m.bounds_mm[1][1] for m in located_members)
    all_max_z = max(m.bounds_mm[1][2] for m in located_members)
    assembly_bounds = ((all_min_x, all_min_y, all_min_z), (all_max_x, all_max_y, all_max_z))

    meta = structure.get("meta", {})
    source_hash = meta.get("source_hash", "UNSTAMPED")
    revision_id = meta.get("revision_id", "UNSTAMPED")
    revision_hash = meta.get("revision_hash", "UNSTAMPED")

    member_ids = tuple(m.member_id for m in located_members)
    member_roles = tuple((m.member_id, m.role) for m in located_members)
    structure_json_str = json.dumps(structure, sort_keys=True)
    structure_sha = hashlib.sha256(structure_json_str.encode("utf-8")).hexdigest()

    assembly_sha = compute_assembly_sha256(structure_sha, member_ids, assembly_bounds)

    receipt = AssemblyReceipt(
        schema_version="2.0",
        source_hash=source_hash,
        revision_id=revision_id,
        revision_hash=revision_hash,
        structure_sha256=structure_sha,
        assembly_input_sha256=structure_sha,
        toolchain=(("build123d", getattr(b3d, "__version__", "0.10.0")),),
        member_ids=member_ids,
        member_roles=member_roles,
        excluded_members=(),
        member_shape_hashes=(),
        assembly_sha256=assembly_sha,
    )

    assembly = SolidAssembly(
        schema_version="2.0",
        units="mm",
        coordinate_system="RH_Z_UP",
        members=tuple(located_members),
        bounds_mm=assembly_bounds,
        receipt=receipt,
    )

    validate_solid_assembly(assembly, structure)
    return assembly


def build_cad_model(structure: dict) -> Any:
    """Compatibility adapter: returns build123d.Compound wrapping the authoritative assembly."""
    if not BUILD123D_AVAILABLE:
        return None
    assembly = build_solid_assembly(structure)
    solids = [b3d.Solid(m.shape) for m in assembly.members]
    for s, m in zip(solids, assembly.members):
        s.label = m.member_id
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
