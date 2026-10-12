"""
test_hex_pergola_physical_geometry.py
======================================

Tests verifying physical correctness of 3D geometry and rendering:
1. Rafter profile lateral offset symmetry (no centerline collapse at seat).
2. Flat pergola rafter seating (no downward plunge through beam top).
3. 3D view footing grade clipping (no subterranean trough boxes below Z=0).
"""
import json
import math
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from geometry_engine import _add_notched_rafter  # type: ignore[import]
from cad_scene import build_structure_scene  # type: ignore[import]
from render_drawings import _depth_sorted_faces, _camera  # type: ignore[import]


def test_rafter_notched_profile_lateral_offsets():
    """Verify that rafter vertices maintain lateral offset +-hw and do not collapse to centerline."""
    resolved = {"members": []}
    p_tail = (5.75, 0.0, 9.3056)
    p_apex = (0.6495, 0.0, 9.3056)
    p_seat = (5.0, 0.0, 9.3056)
    hw = 0.145833
    hd = 0.229167
    up_hint = (0.0, 0.0, 1.0)
    
    _add_notched_rafter(
        resolved, p_tail, p_apex, p_seat, hw, hd, 0.3056,
        up_hint, "rafter", "R1", 9.0, 5.1, 0.0, {}
    )
    
    m = resolved["members"][0]
    verts = m["vertices"]
    # Total 12 vertices: 6 for left side (+hw along w), 6 for right side (-hw along w)
    assert len(verts) == 12
    # Check that Y coordinates (lateral along w=(0,1,0)) are all close to +hw or -hw, none zero
    y_coords = [v[1] for v in verts]
    for y in y_coords:
        assert abs(abs(y) - hw) < 1e-4, f"Rafter vertex lateral offset collapsed to {y}, expected {hw}"


def test_flat_pergola_rafter_seating_no_plunge():
    """For a flat pergola (pitch 0:12), rafter bottom vertices must not drop below Z_BEAM_TOP."""
    resolved = {"members": []}
    p_tail = (5.75, 0.0, 9.4583)
    p_apex = (0.6495, 0.0, 9.4583)
    p_seat = (5.0, 0.0, 9.4583)
    hw = 0.145833
    hd = 0.229167
    up_hint = (0.0, 0.0, 1.0)
    z_beam_top = 9.0
    
    _add_notched_rafter(
        resolved, p_tail, p_apex, p_seat, hw, hd, hd * 2.0,
        up_hint, "rafter", "R1", z_beam_top, 5.1, 0.0, {}
    )
    
    m = resolved["members"][0]
    verts = m["vertices"]
    z_min = min(v[2] for v in verts)
    assert z_min >= z_beam_top - 1e-4, f"Rafter vertex dropped to Z={z_min}, plunging below beam top {z_beam_top}"


def test_3d_view_footings_clipped_at_grade():
    """In 3D isometric view, footing geometry rendered above ground must not contain subterranean vertices (Z < 0)."""
    with open("context/staging/structure.json") as f:
        structure = json.load(f)
    
    scene = build_structure_scene(structure, is_blueprint=False)
    cam = _camera("isometric")
    entries = _depth_sorted_faces(scene, cam, lambda s: False, view_type="isometric")
    
    footing_faces = [face for _, face, solid in entries if solid.role == "footing"]
    assert len(footing_faces) > 0
    for face in footing_faces:
        for v in face.verts:
            assert v[2] >= -1e-4, f"Subterranean vertex Z={v[2]} found in 3D isometric view footing"


def test_polygonal_beam_ring_miters_meet_cleanly(tmp_path):
    """Adjacent beams in a regular polygonal ring must meet flush at the post corners."""
    from geometry_engine import compute_from_structure
    import json
    
    with open("context/staging/structure.json") as f:
        structure = json.load(f)
    
    # Mark unsealed for recomputing in temp path
    structure["meta"]["lifecycle"] = "ENGINEERED"
    structure["geometry"]["_sealed"] = False
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(structure))
    
    compute_from_structure(str(p))
    computed = json.loads(p.read_text())
    resolved = computed["geometry"]["joints"]["resolved_model"]
    beams = {m["id"]: m for m in resolved["members"] if m["role"] == "beam"}
    assert len(beams) == 6
    
    # Check that B1 end and B2 start meet at post P2
    b1_verts = beams["B1"]["vertices"]
    b2_verts = beams["B2"]["vertices"]
    
    # Outer end vertices of B1 vs outer start vertices of B2:
    # B1 end outer top is index 6, B2 start outer top is index 2
    b1_outer_end_top = b1_verts[6]
    b2_outer_start_top = b2_verts[2]
    dist_outer = math.dist(b1_outer_end_top, b2_outer_start_top)
    assert dist_outer < 1e-3, f"B1 and B2 outer miter corner gap {dist_outer}"
    
    # Inner end vertices of B1 vs inner start vertices of B2:
    # B1 end inner top is index 7, B2 start inner top is index 3
    b1_inner_end_top = b1_verts[7]
    b2_inner_start_top = b2_verts[3]
    dist_inner = math.dist(b1_inner_end_top, b2_inner_start_top)
    assert dist_inner < 1e-3, f"B1 and B2 inner miter corner gap {dist_inner}"

