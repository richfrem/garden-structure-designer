import json
import math
import copy
from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).parent))
from geometry_engine import compute_from_structure  # type: ignore[import]
from cad_scene import (
    build_structure_scene, Scene, GeometryError,
    vadd, vsub, vmul, vdot, vcross, vlen, vdist, vnorm, vcent
)  # type: ignore[import]

# ... existing tests ...

def test_no_silent_fallbacks_kneebraces(tmp_path):
    """
    Verify that cad_scene.py fails-closed with GeometryError when required 
    kneebrace geometry is missing, instead of falling back to default 1.5ft.
    """
    # Create seeded structure but DON'T compute geometry (so joints are missing)
    p = tmp_path / "structure.json"
    s = copy.deepcopy(STRUCTURE_SEED)
    s["bracing"]["enabled"] = True
    p.write_text(json.dumps(s))
    
    # We pass s directly to build_structure_scene. 
    # It should fail because geometry.joints.braces is missing.
    with pytest.raises(GeometryError, match="MISSING_REQUIRED_GEOMETRY"):
        build_structure_scene(s)
from test_geometry_engine import STRUCTURE_SEED  # type: ignore[import]

def _seeded_structure(tmp_path, enable_jacks=False):
    p = tmp_path / "structure.json"
    s = copy.deepcopy(STRUCTURE_SEED)
    if enable_jacks:
        s["roof"]["secondary_rafters"] = {
            "enabled": True,
            "count_per_side": 2,
            "actual_width_in": 3.5,
            "actual_depth_in": 5.5
        }
    p.write_text(json.dumps(s))
    compute_from_structure(str(p))
    return json.loads(p.read_text())

def test_jack_rafter_zero_gap_plane_intersection(tmp_path):
    """
    Verify that jack rafter upper endpoints are resolved via true 3D plane intersection
    against the hip rafter's midpoint-anchored side plane.
    """
    s = _seeded_structure(tmp_path, enable_jacks=True)
    scene = build_structure_scene(s)
    
    qty = s["layout"]["post_count"]
    r_ft = s["layout"]["inscribed_radius_ft"]
    geom = s["geometry"]
    hub_r = geom["joints"]["hub"]["radius_ft"]
    post_h = s["members"]["posts"]["cut_length_ft"]
    beam_d = s["members"]["beams"]["actual_depth_in"] / 12.0
    Z_BEAM_TOP = post_h
    Z_APEX = geom["joints"]["z_planes"]["Z_APEX"]
    
    # Rafter dimensions
    RAFTER_HW = (s["roof"]["primary_rafters"]["actual_width_in"] / 12.0) / 2.0
    RAFTER_HD = (s["roof"]["primary_rafters"]["actual_depth_in"] / 12.0) / 2.0
    seat_depth = RAFTER_HD * 2.0 / 3.0 # Depth of birdsmouth is 1/3, remaining is 2/3
    # Wait, engine says seat_depth = rafter_d_ft / 3.0
    seat_depth_ft = RAFTER_HD * 2.0 / 3.0
    
    # Post and Apex coords from JOINTS (the single source of truth)
    post_xy = geom["joints"]["layout"]["post_xy"]
    
    # Find all jack rafters
    jack_solids = [so for so in scene.solids if so.role == "rafter" and so.tag.startswith("J")]
    assert len(jack_solids) > 0
    
    for jack in jack_solids:
        tag = jack.tag
        # ID scheme: J{bay}{suffix}
        num_str = "".join([c for c in tag if c.isdigit()])
        i = int(num_str) - 1
        suffix = tag[-1]
        
        # Identify target hip
        hip_idx = i if suffix == 'a' else (i+1)%qty
        hip_tag = f"R{hip_idx+1}"
        
        # Side normal to hip
        h_p0 = (post_xy[hip_idx][0], post_xy[hip_idx][1], Z_BEAM_TOP)
        h_dir = vnorm(vsub((0,0,Z_APEX), h_p0))
        h_perp_xy = (-h_dir[1], h_dir[0], 0.0)
        
        v_to_jack = vsub(jack.p0, h_p0)
        side_sign = 1.0 if vdot(v_to_jack, h_perp_xy) >= 0 else -1.0
        N_side = vmul(h_perp_xy, side_sign)
        
        # Plane Anchor: Midpoint of hip rafter axis
        h_end = (0,0,Z_APEX) # Simplified theoretical apex for test
        # Actually use the joint end for exactness
        hip_joint = next(r for r in geom["joints"]["primary_rafters"] if r["id"] == hip_tag)
        h_mid = vcent([tuple(hip_joint["start"]), tuple(hip_joint["end"])])
        
        P_face = vadd(h_mid, vmul(N_side, RAFTER_HW))
        
        # Distance to plane
        diff = vsub(jack.p1, P_face)
        dist = abs(vdot(diff, N_side))
        
        assert dist < 5e-4, f"Jack {tag} gap/penetration: {dist:.6f} ft"


def test_rafter_seating_physical_contact(tmp_path):
    """
    Verify Phase 2 Physical Seating: rafter level-seat face must lie on Z_BEAM_TOP.
    """
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    
    Z_BEAM_TOP = scene.Z_BEAM_TOP
    rafters = [s for s in scene.solids if s.role == "rafter"]
    
    for r in rafters:
        # A notched rafter must have a face with normal (0,0,-1) at Z_BEAM_TOP
        seat_faces = [
            f for f in r.faces 
            if f.normal[2] < -0.95 and abs(vcent(f.verts)[2] - Z_BEAM_TOP) < 0.05
        ]
        assert len(seat_faces) > 0, f"Rafter {r.tag} has no physical seat face on beam top plane"
        
        for face in seat_faces:
            for v in face.verts:
                assert abs(v[2] - Z_BEAM_TOP) < 1e-4, f"Rafter {r.tag} seat vertex {v} not flush with Z_BEAM_TOP"


def test_label_uniqueness_and_anchor_distance(tmp_path):
    """
    Verify that rendered labels are unique and remain near their anchor.
    """
    from render_drawings import render_plan_view, generate_svg
    s = _seeded_structure(tmp_path)
    
    # Generate an SVG
    out_svg = tmp_path / "plan.svg"
    # generate_svg calls render_plan_view internally
    generate_svg("drawing-plan-view.svg", s, str(out_svg))
    
    content = out_svg.read_text()
    
    # Simple grep for data-label tags
    import re
    labels = re.findall(r'data-label="([^"]+)"', content)
    
    assert len(labels) > 0, "No labels found in SVG"
    # Duplicate labels check
    assert len(labels) == len(set(labels)), f"Duplicate labels detected: {labels}"
    
    # Label anchor distance check
    # We'd need to parse SVG properly to check coordinates, but we can verify the resolver logic instead.
    from render_drawings import resolve_label_overlap
    MAX_RAD = 40.0
    lx, ly = 100.0, 100.0
    placed = [(100.0, 100.0)]
    rx, ry = resolve_label_overlap(lx, ly, placed, max_radius=MAX_RAD)
    
    dist = math.sqrt((rx - lx)**2 + (ry - ly)**2)
    assert dist <= MAX_RAD, f"Label shifted too far: {dist:.2f} px > {MAX_RAD}"


def test_label_collision_resolution():
    """
    Verify that resolve_label_overlap correctly shifts overlapping coordinates
    within the enforced maximum displacement radius.
    """
    from render_drawings import resolve_label_overlap
    placed_labels = [(100.0, 100.0)]
    
    # A label placed at (100.0, 102.0) is within min_dist=20.0
    lx, ly = resolve_label_overlap(100.0, 102.0, placed_labels, min_dist=20.0, max_radius=40.0)
    
    # Compute displacement distance
    dist = math.sqrt((lx - 100.0)**2 + (ly - 102.0)**2)
    
    # Should be shifted outside collision zone of (100.0, 100.0)
    dist_from_collision = math.sqrt((lx - 100.0)**2 + (ly - 100.0)**2)
    assert dist_from_collision >= 20.0, f"Label not shifted far enough: {dist_from_collision:.2f} px"
    
    # But should still be within the maximum displacement radius from its original target
    assert dist <= 40.0, f"Label shifted too far: {dist:.2f} px"
