"""
test_hlr_bindings.py
====================

Unit test suite verifying OpenCASCADE HLR C++ bindings:
1. Multi-member registration in one HLRBRep_Algo solver.
2. Shape-filtered extraction using HLRBRep_HLRToShape.VCompound(shape) and HCompound(shape).
3. Edge traversal and coordinate retrieval.
"""
from pathlib import Path
import pytest

from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Curve


def test_hlr_global_occlusion_and_shape_filtered_extraction():
    """Verify that multiple shapes added to HLRBRep_Algo mutually occlude and can be extracted individually."""
    # Box 1 at origin, Box 2 intersecting/offset
    box1 = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0).Shape()
    box2 = BRepPrimAPI_MakeBox(gp_Pnt(5.0, 5.0, 5.0), 10.0, 10.0, 10.0).Shape()

    algo = HLRBRep_Algo()
    algo.Add(box1)
    algo.Add(box2)

    # Isometric projector
    axis = gp_Ax2(gp_Pnt(0.0, 0.0, 0.0), gp_Dir(1.0, -1.0, 1.0), gp_Dir(1.0, 1.0, 0.0))
    projector = HLRAlgo_Projector(axis)
    algo.Projector(projector)
    algo.Update()
    algo.Hide()

    hlr_shapes = HLRBRep_HLRToShape(algo)

    # Shape-filtered extraction
    v1 = hlr_shapes.VCompound(box1)
    v2 = hlr_shapes.VCompound(box2)
    h1 = hlr_shapes.HCompound(box1)
    h2 = hlr_shapes.HCompound(box2)

    assert not v1.IsNull(), "Box 1 visible compound must not be null"
    assert not v2.IsNull(), "Box 2 visible compound must not be null"
    assert not h1.IsNull(), "Box 1 hidden compound must not be null"
    assert not h2.IsNull(), "Box 2 hidden compound must not be null"

    # Count edges
    def count_edges(comp):
        exp = TopExp_Explorer(comp, TopAbs_EDGE)
        count = 0
        while exp.More():
            count += 1
            exp.Next()
        return count

    # A single isolated cube has 9 visible edges in isometric view.
    # When occluded, box1 has fewer than 9 visible edges.
    assert count_edges(v1) == 7, f"Expected 7 visible edges for occluded box1, got {count_edges(v1)}"
    assert count_edges(v2) == 9, f"Expected 9 visible edges for foreground box2, got {count_edges(v2)}"
    assert count_edges(h1) > 0, "Expected hidden edges for occluded box1"


def test_hlr_edge_coordinate_traversal():
    """Verify that TopExp_Explorer + BRepAdaptor_Curve extracts finite 2D projection coordinates."""
    box = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0).Shape()
    algo = HLRBRep_Algo()
    algo.Add(box)

    axis = gp_Ax2(gp_Pnt(0.0, 0.0, 0.0), gp_Dir(0.0, 0.0, 1.0), gp_Dir(1.0, 0.0, 0.0)) # Top view
    algo.Projector(HLRAlgo_Projector(axis))
    algo.Update()
    algo.Hide()

    hlr_shapes = HLRBRep_HLRToShape(algo)
    v = hlr_shapes.VCompound(box)

    exp = TopExp_Explorer(v, TopAbs_EDGE)
    edges = []
    while exp.More():
        e = TopoDS.Edge_s(exp.Current())
        c = BRepAdaptor_Curve(e)
        p0 = c.Value(c.FirstParameter())
        p1 = c.Value(c.LastParameter())
        edges.append(((p0.X(), p0.Y()), (p1.X(), p1.Y())))
        exp.Next()

    # Plan view of a cube is a 10x10 square -> 4 visible boundary edges
    assert len(edges) == 4, f"Expected 4 boundary edges in top view, got {len(edges)}"
    for (x1, y1), (x2, y2) in edges:
        assert abs(x1) <= 10.001 and abs(x2) <= 10.001
        assert abs(y1) <= 10.001 and abs(y2) <= 10.001
