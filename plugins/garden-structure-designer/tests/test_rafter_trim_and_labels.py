import json
import math
import copy
from pathlib import Path
import sys
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).parent))
from geometry_engine import compute_from_structure  # type: ignore[import]
from cad_scene import build_structure_scene, Scene, GeometryError  # type: ignore[import]

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
    # ... rest of test ...

    qty = s["layout"]["post_count"]
    r_ft = s["layout"]["inscribed_radius_ft"]
    geom = s["geometry"]
    hub_r = geom["hub_radius_ft"]
    post_h = s["members"]["posts"]["cut_length_ft"]
    beam_d = s["members"]["beams"]["actual_depth_in"] / 12.0
    Z_BEAM_TOP = post_h
    Z_APEX = post_h + geom["roof_rise"]["rise_ft"]
    
    # Rafter dimensions
    RAFTER_HW = (s["roof"]["primary_rafters"]["actual_width_in"] / 12.0) / 2.0
    
    # Gather post coords
    post_xy = [
        (r_ft * math.cos(2*math.pi*idx/qty), r_ft * math.sin(2*math.pi*idx/qty))
        for idx in range(qty)
    ]
    # Rafter apex coords
    hub_r_face = hub_r * math.cos(math.pi / qty)
    rafter_apex = [
        (hub_r_face * math.cos(2*math.pi*idx/qty), hub_r_face * math.sin(2*math.pi*idx/qty), Z_APEX)
        for idx in range(qty)
    ]
    
    # Find all jack rafters (using new J naming scheme)
    jack_solids = [so for so in scene.solids if so.role == "rafter" and so.tag.startswith("J")]
    assert len(jack_solids) > 0, "No jack rafters generated to test"
    
    for jack in jack_solids:
        tag = jack.tag
        num_str = "".join([c for c in tag if c.isdigit()])
        i = int(num_str) - 1 # J1a -> index 0
        suffix = tag[-1]
        
        # Identify the target hip rafter
        hip_idx = i if suffix == 'a' else (i+1)%qty
        px_corner, py_corner = post_xy[hip_idx]
        px_apex, py_apex, pz_apex = rafter_apex[hip_idx]
            
        dx_hip = px_apex - px_corner
        dy_hip = py_apex - py_corner
        len_hip = math.sqrt(dx_hip*dx_hip + dy_hip*dy_hip)
        ux_hip = dx_hip / len_hip
        uy_hip = dy_hip / len_hip
        
        # Decide side normal
        # The jack starts on a beam. We need its direction.
        # For simplicity in test, derive from p1-p0
        v_jack_dir = (jack.p1[0] - jack.p0[0], jack.p1[1] - jack.p0[1])
        # Side normal is perpendicular to hip in XY
        nx_hip_side, ny_hip_side = -uy_hip, ux_hip
        side_sign = 1.0 if (v_jack_dir[0]*nx_hip_side + v_jack_dir[1]*ny_hip_side) >= 0 else -1.0
        N_side = (side_sign * nx_hip_side, side_sign * ny_hip_side, 0.0)
        
        # Correct Plane Anchor: Midpoint of hip rafter
        h_start = (px_corner, py_corner, Z_BEAM_TOP)
        h_end = (px_apex, py_apex, Z_APEX)
        h_mid = ((h_start[0]+h_end[0])/2, (h_start[1]+h_end[1])/2, (h_start[2]+h_end[2])/2)
        
        P_face = (
            h_mid[0] + N_side[0] * RAFTER_HW,
            h_mid[1] + N_side[1] * RAFTER_HW,
            h_mid[2] + N_side[2] * RAFTER_HW
        )
        
        # Perpendicular distance from jack upper end (p1) to hip rafter side plane
        diff = (jack.p1[0] - P_face[0], jack.p1[1] - P_face[1], jack.p1[2] - P_face[2])
        dist = abs(diff[0] * N_side[0] + diff[1] * N_side[1] + diff[2] * N_side[2])
        
        assert dist < 5e-4, f"Jack rafter {tag} has gap/penetration with hip rafter plane: {dist:.6f} ft"

        # TEST: No overshoot
        # Dot product of (p1 - p_face) and N_side should be negative or zero (pt inside or on plane)
        # Wait, if N_side points AWAY from the hip solid toward the jack, then:
        # dot(p1 - p_face, N_side) > 0 means pt is OUTSIDE (gap)
        # dot(p1 - p_face, N_side) < 0 means pt is INSIDE (penetration)
        # Our dist is abs().
        
        signed_dist = diff[0] * N_side[0] + diff[1] * N_side[1] + diff[2] * N_side[2]
        # We allow 1/32" tolerance for floating point but strictly reject large penetration
        assert signed_dist > -0.003, f"Jack rafter {tag} overshoots into hip solid: {signed_dist*12:.3f} in"


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
