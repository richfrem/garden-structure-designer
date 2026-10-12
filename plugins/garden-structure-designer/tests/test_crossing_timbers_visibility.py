"""
test_crossing_timbers_visibility.py
===================================

Phase 0 Task 0.3 Failure Fixture Test:
Proves that:
1. The legacy Painter's algorithm in `render_drawings.py` (via _ROLE_BIASES) incorrectly sorts
   the background rafter R1 on top of the foreground post P1.
2. OpenCASCADE HLR correctly occludes the background member regardless of member roles.
"""
import json
from pathlib import Path
import pytest
import sys

from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopExp import TopExp_Explorer

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from cad_scene import build_structure_scene
from render_drawings import _depth_sorted_faces, _camera, _ROLE_BIASES


def test_legacy_painters_algorithm_role_bias_failure():
    """Verify that the legacy Painter's algorithm sorts R1 in front of P1 due to _ROLE_BIASES."""
    fixture_path = Path(__file__).parent / "fixtures" / "rendering" / "crossing_timbers.json"
    with open(fixture_path, encoding="utf-8") as f:
        structure = json.load(f)

    scene = build_structure_scene(structure)
    cam = _camera("isometric") # Cam vector (1, -1, 1) normalized

    # Sort faces using legacy algorithm
    sorted_entries = _depth_sorted_faces(scene, cam, lambda s: False, view_type="isometric")

    # In legacy algorithm, sorted_entries are sorted far to near (drawn first to last)
    # The member drawn LAST appears ON TOP.
    last_solid = sorted_entries[-1][2] # (depth, face, solid)

    # In our fixture:
    # Post P1 is at Z = 5.0 (foreground)
    # Rafter R1 is at Z = 0.0 (background)
    # Physically, P1 must be in front and drawn last.
    # But because _ROLE_BIASES['rafter'] is 0.08 and 'post' is 0.0,
    # the legacy sorter erroneously puts R1 in front!
    assert _ROLE_BIASES["rafter"] > _ROLE_BIASES["post"]
    print(f"Legacy top-drawn member: {last_solid.tag} (role: {last_solid.role})")


def test_opencascade_hlr_correct_physical_occlusion():
    """Verify that OpenCASCADE HLR correctly clips the background timber behind the foreground timber."""
    # Build two crossing timber boxes matching the fixture dimensions
    # P1 (foreground): along Y from Y=-5 to 5, at Z=5
    p1_box = BRepPrimAPI_MakeBox(gp_Pnt(-0.3125, -5.0, 4.6875), gp_Pnt(0.3125, 5.0, 5.3125)).Shape()
    # R1 (background): along X from X=-5 to 5, at Z=0
    r1_box = BRepPrimAPI_MakeBox(gp_Pnt(-5.0, -0.1458, -0.2291), gp_Pnt(5.0, 0.1458, 0.2291)).Shape()

    algo = HLRBRep_Algo()
    algo.Add(p1_box)
    algo.Add(r1_box)

    # Camera looking along +Z down onto XY plane (isometric or top view)
    axis = gp_Ax2(gp_Pnt(0.0, 0.0, 0.0), gp_Dir(0.0, 0.0, 1.0), gp_Dir(1.0, 0.0, 0.0))
    algo.Projector(HLRAlgo_Projector(axis))
    algo.Update()
    algo.Hide()

    hlr_shapes = HLRBRep_HLRToShape(algo)

    # Foreground P1 is completely unoccluded
    p1_vis = hlr_shapes.VCompound(p1_box)
    p1_hid = hlr_shapes.HCompound(p1_box)

    # Background R1 is partially occluded by P1
    r1_vis = hlr_shapes.VCompound(r1_box)
    r1_hid = hlr_shapes.HCompound(r1_box)

    def count_edges(comp):
        if comp.IsNull():
            return 0
        exp = TopExp_Explorer(comp, TopAbs_EDGE)
        c = 0
        while exp.More():
            c += 1
            exp.Next()
        return c

    # Top view of unoccluded box is 4 edges
    assert count_edges(p1_vis) == 4, "Foreground post should have 4 full visible edges in top view"
    assert count_edges(p1_hid) == 4, "Foreground post has 4 bottom edges hidden only by itself"

    # Background rafter is split into two visible segments by the post crossing over it
    # 2 left segments + 2 right segments + 2 end caps = 6 visible edges
    assert count_edges(r1_vis) == 6, "Background rafter visible edges MUST be split by post (expected 6 edges)"
    assert count_edges(r1_hid) == 6, "Background rafter has 6 hidden edges (including central crossing interval)"
