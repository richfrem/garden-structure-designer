#!/usr/bin/env python3
"""
cad_projection_hlr.py
=====================

Purpose:
    Authoritative vector CAD projection engine using OpenCASCADE C++ Hidden Line
    Removal (HLR) algorithms (HLRBRep_Algo, HLRBRep_HLRToShape, HLRAlgo_Projector).
    Provides true 3D mutual occlusion, member-specific extraction (preserving data-role
    and data-tag without spatial guessing), curve extraction, and SVG path generation.

Layer: Domain / Geometry Projections
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Dict, List, Literal, Optional, Sequence, Tuple

from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS, TopoDS_Shape

from cad_camera import CameraSpec, SheetTransform, to_sheet
from cad_render_contracts import SolidAssembly, LocatedMemberShape


Point2D = Tuple[float, float]


@dataclass(frozen=True)
class ProjectedEdge:
    """A projected 2D curve segment extracted from OpenCASCADE HLR."""
    member_id: str
    role: str
    visibility: Literal["visible", "hidden"]
    edge_kind: Literal["sharp", "outline", "seam"]
    start_pt: Point2D
    end_pt: Point2D
    intermediate_pts: Tuple[Point2D, ...] = ()
    contributing_members: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.contributing_members and self.member_id:
            object.__setattr__(self, "contributing_members", (self.member_id,))

    @property
    def is_line(self) -> bool:
        return len(self.intermediate_pts) == 0

    def to_svg_path(self, transform: Optional[SheetTransform] = None) -> str:
        """Converts the projected 2D edge to an SVG path 'd' string."""
        p0 = self.start_pt
        p1 = self.end_pt
        if transform:
            p0 = to_sheet(p0, transform)
            p1 = to_sheet(p1, transform)

        if self.is_line:
            return f"M {p0[0]:.2f} {p0[1]:.2f} L {p1[0]:.2f} {p1[1]:.2f}"

        # Polyline approximation for curved segments
        pts = [p0]
        for mid in self.intermediate_pts:
            pts.append(to_sheet(mid, transform) if transform else mid)
        pts.append(p1)

        cmds = [f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"]
        for p in pts[1:]:
            cmds.append(f"L {p[0]:.2f} {p[1]:.2f}")
        return " ".join(cmds)


@dataclass(frozen=True)
class MemberHLRResult:
    """HLR results for a single member under mutual assembly occlusion."""
    member_id: str
    role: str
    visible_edges: Tuple[ProjectedEdge, ...]
    hidden_edges: Tuple[ProjectedEdge, ...]


@dataclass(frozen=True)
class HLRProjectionResult:
    """Full assembly HLR projection result for a specific camera view."""
    camera_id: str
    members: Dict[str, MemberHLRResult]


def _extract_edges_from_compound(
    compound: TopoDS_Shape,
    member_id: str,
    role: str,
    visibility: Literal["visible", "hidden"],
    edge_kind: Literal["sharp", "outline"],
) -> List[ProjectedEdge]:
    """Extracts ProjectedEdge records from an HLR compound."""
    if compound.IsNull():
        return []

    edges: List[ProjectedEdge] = []
    exp = TopExp_Explorer(compound, TopAbs_EDGE)
    while exp.More():
        edge = TopoDS.Edge_s(exp.Current())
        curve = BRepAdaptor_Curve(edge)
        u1 = curve.FirstParameter()
        u2 = curve.LastParameter()

        # Check if curve is linear or curved
        curve_type = curve.GetType()
        # GeomAbs_Line == 0
        if curve_type == 0:
            p0 = curve.Value(u1)
            p1 = curve.Value(u2)
            edges.append(
                ProjectedEdge(
                    member_id=member_id,
                    role=role,
                    visibility=visibility,
                    edge_kind=edge_kind,
                    start_pt=(p0.X(), p0.Y()),
                    end_pt=(p1.X(), p1.Y()),
                )
            )
        else:
            # Sample curve adaptively
            p0 = curve.Value(u1)
            p1 = curve.Value(u2)
            # Sample 8 points along curve
            samples = []
            num_samples = 8
            for i in range(1, num_samples):
                t = u1 + (u2 - u1) * (i / num_samples)
                pt = curve.Value(t)
                samples.append((pt.X(), pt.Y()))

            edges.append(
                ProjectedEdge(
                    member_id=member_id,
                    role=role,
                    visibility=visibility,
                    edge_kind=edge_kind,
                    start_pt=(p0.X(), p0.Y()),
                    end_pt=(p1.X(), p1.Y()),
                    intermediate_pts=tuple(samples),
                )
            )

        exp.Next()

    return edges


def project_assembly_hlr(
    assembly: SolidAssembly,
    camera: CameraSpec,
) -> HLRProjectionResult:
    """
    Executes global OpenCASCADE HLR on the assembly and extracts member-attributed edges.
    """
    # Create OpenCASCADE projector coordinate system
    # Axis: center at camera target, Z direction along camera outward, X direction along camera right
    axis = gp_Ax2(
        gp_Pnt(*camera.target_mm),
        gp_Dir(*camera.outward),
        gp_Dir(*camera.right),
    )
    projector = HLRAlgo_Projector(axis)

    algorithm = HLRBRep_Algo()
    # Feed every solid into the single global solver
    for member in assembly.members:
        algorithm.Add(member.shape, 0)

    algorithm.Projector(projector)
    algorithm.Update()
    algorithm.Hide()

    extractor = HLRBRep_HLRToShape(algorithm)

    member_results: Dict[str, MemberHLRResult] = {}

    for member in assembly.members:
        # Sharp visible and hidden
        v_comp = extractor.VCompound(member.shape)
        h_comp = extractor.HCompound(member.shape)
        # Outline / silhouette visible and hidden
        ov_comp = extractor.OutLineVCompound(member.shape)
        oh_comp = extractor.OutLineHCompound(member.shape)

        v_edges = _extract_edges_from_compound(v_comp, member.member_id, member.role, "visible", "sharp")
        v_edges.extend(_extract_edges_from_compound(ov_comp, member.member_id, member.role, "visible", "outline"))

        h_edges = _extract_edges_from_compound(h_comp, member.member_id, member.role, "hidden", "sharp")
        h_edges.extend(_extract_edges_from_compound(oh_comp, member.member_id, member.role, "hidden", "outline"))

        member_results[member.member_id] = MemberHLRResult(
            member_id=member.member_id,
            role=member.role,
            visible_edges=tuple(v_edges),
            hidden_edges=tuple(h_edges),
        )

    return HLRProjectionResult(
        camera_id=camera.camera_id,
        members=member_results,
    )


def _edge_canonical_key(edge: ProjectedEdge, tol: float = 0.01) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Generates an orientation-invariant quantized key for an edge segment."""
    p0 = (round(edge.start_pt[0] / tol), round(edge.start_pt[1] / tol))
    p1 = (round(edge.end_pt[0] / tol), round(edge.end_pt[1] / tol))
    return (min(p0, p1), max(p0, p1))


def deduplicate_coincident_edges(
    edges: Sequence[ProjectedEdge],
    tol_mm: float = 0.01,
) -> List[ProjectedEdge]:
    """
    Deduplicates coincident edges, giving precedence to visible edges over hidden edges,
    and combining all participating members into contributing_members.
    """
    groups: Dict[Tuple[Tuple[int, int], Tuple[int, int]], List[ProjectedEdge]] = {}
    for edge in edges:
        key = _edge_canonical_key(edge, tol_mm)
        if key not in groups:
            groups[key] = []
        groups[key].append(edge)

    deduped: List[ProjectedEdge] = []
    for key, cluster in groups.items():
        if len(cluster) == 1:
            deduped.append(cluster[0])
            continue

        # Sort: visible first, then alphabetically by member_id
        cluster.sort(key=lambda e: (0 if e.visibility == "visible" else 1, e.member_id))
        primary = cluster[0]

        all_members = sorted(
            list(
                set(
                    m
                    for e in cluster
                    for m in (e.contributing_members if e.contributing_members else (e.member_id,))
                )
            )
        )

        deduped_edge = ProjectedEdge(
            member_id=primary.member_id,
            role=primary.role,
            visibility=primary.visibility,
            edge_kind=primary.edge_kind,
            start_pt=primary.start_pt,
            end_pt=primary.end_pt,
            intermediate_pts=primary.intermediate_pts,
            contributing_members=tuple(all_members),
        )
        deduped.append(deduped_edge)

    return deduped
