"""
test_multi_shape_geometry.py
=============================
Integration tests verifying CAD kernel and deterministic geometry engine
correctness across non-hexagonal structure shapes (4-post square and 8-post octagon).
"""

import copy
import json
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from validate_intent import validate_intent
from cad_language_translator import translate_to_constraints
from geometry_engine import compute_from_structure
from topology_compiler import compile_topology
from cad_scene import build_structure_scene, validate_scene_geometry
from test_geometry_engine import STRUCTURE_SEED


def _create_shape_seed(shape: str, post_count: int, radius_ft: float, pitch: str = "4:12") -> dict:
    """Create a fully valid structure.json seed tailored for a specific shape and post count."""
    s = copy.deepcopy(STRUCTURE_SEED)
    s["structure"]["shape"] = shape
    s["layout"]["shape"] = shape
    s["layout"]["post_count"] = post_count
    s["layout"]["inscribed_radius_ft"] = radius_ft
    s["roof"]["pitch"] = pitch
    s["roof"]["primary_rafters"]["count"] = post_count
    s["members"]["posts"]["quantity"] = post_count
    s["members"]["beams"]["quantity"] = post_count
    s["bracing"]["count_per_post"] = 2
    # Secondary elements
    s["roof"]["secondary_rafters"]["enabled"] = False
    return s


# ---------------------------------------------------------------------------
# Square (4-Post) Geometry Invariant Tests
# ---------------------------------------------------------------------------

def test_square_4post_geometry_pipeline(tmp_path):
    """End-to-end geometry and CAD scene resolution for a 4-post square pergola."""
    seed = _create_shape_seed("square", 4, 6.0, "4:12")
    
    # 1. Validate Intent Pre-Gate
    errs = validate_intent(seed)
    assert len(errs) == 0, f"Intent validation failed for square pergola: {errs}"
    
    # 2. Translate CAD Constraints
    translate_to_constraints(seed)
    assert "cad_constraints" in seed
    assert len(seed["cad_constraints"]["member_constraints"]) > 0
    
    # 3. Deterministic Geometry Math
    p = tmp_path / "square_structure.json"
    p.write_text(json.dumps(seed))
    compute_from_structure(str(p))
    resolved_structure = json.loads(p.read_text())
    
    assert resolved_structure["meta"]["lifecycle"] == "GEOMETRY_SEALED"
    assert "resolved_model" in resolved_structure["geometry"]["joints"]
    
    # Check post positions forming a square
    pxy = resolved_structure["geometry"]["joints"]["layout"]["post_xy"]
    assert len(pxy) == 4
    # (6, 0), (0, 6), (-6, 0), (0, -6)
    assert abs(pxy[0][0] - 6.0) < 1e-3 and abs(pxy[0][1] - 0.0) < 1e-3
    assert abs(pxy[1][0] - 0.0) < 1e-3 and abs(pxy[1][1] - 6.0) < 1e-3
    assert abs(pxy[2][0] - (-6.0)) < 1e-3 and abs(pxy[2][1] - 0.0) < 1e-3
    assert abs(pxy[3][0] - 0.0) < 1e-3 and abs(pxy[3][1] - (-6.0)) < 1e-3
    
    # 4. Topology Compilation
    topology = compile_topology(resolved_structure)
    resolved_structure["geometry"]["joints"]["topology"] = topology
    assert len(topology["members"]) == 4 + 8 + 1  # 4 posts + 8 braces + 1 hub = 13
    assert len(topology["connections"]) > 0
    
    # 5. CAD 3D Scene Invariants & Topology
    scene = build_structure_scene(resolved_structure)
    validate_scene_geometry(scene)
    
    # Posts, Beams, Rafters, Braces counts
    posts = [s for s in scene.solids if s.role == "post"]
    beams = [s for s in scene.solids if s.role == "beam"]
    rafters = [s for s in scene.solids if s.role == "rafter"]
    braces = [s for s in scene.solids if s.role == "brace"]
    hubs = [s for s in scene.solids if s.role == "hub"]
    
    assert len(posts) == 4
    assert len(beams) == 4
    assert len(rafters) == 4
    assert len(braces) == 8
    assert len(hubs) == 1
    
    # Beam spans should all be equal: side of square with circumradius R = R * sqrt(2) ≈ 8.485 ft
    expected_beam_span = 6.0 * math.sqrt(2.0)
    for b in beams:
        b_len = math.sqrt((b.p1[0]-b.p0[0])**2 + (b.p1[1]-b.p0[1])**2)
        assert abs(b_len - expected_beam_span) < 1e-2


# ---------------------------------------------------------------------------
# Octagon (8-Post) Geometry Invariant Tests
# ---------------------------------------------------------------------------

def test_octagon_8post_geometry_pipeline(tmp_path):
    """End-to-end geometry and CAD scene resolution for an 8-post octagonal pavilion."""
    seed = _create_shape_seed("octagon", 8, 8.0, "5:12")
    
    # 1. Validate Intent Pre-Gate
    errs = validate_intent(seed)
    assert len(errs) == 0, f"Intent validation failed for octagon pavilion: {errs}"
    
    # 2. Translate CAD Constraints
    translate_to_constraints(seed)
    assert "cad_constraints" in seed
    
    # 3. Deterministic Geometry Math
    p = tmp_path / "octagon_structure.json"
    p.write_text(json.dumps(seed))
    compute_from_structure(str(p))
    resolved_structure = json.loads(p.read_text())
    
    assert resolved_structure["meta"]["lifecycle"] == "GEOMETRY_SEALED"
    assert "resolved_model" in resolved_structure["geometry"]["joints"]
    
    # Check post positions: 8 posts at 45 degree intervals
    pxy = resolved_structure["geometry"]["joints"]["layout"]["post_xy"]
    assert len(pxy) == 8
    for i, pt in enumerate(pxy):
        angle = 2 * math.pi * i / 8
        assert abs(pt[0] - round(8.0 * math.cos(angle), 4)) < 1e-3
        assert abs(pt[1] - round(8.0 * math.sin(angle), 4)) < 1e-3
        
    # 4. Topology Compilation
    topology = compile_topology(resolved_structure)
    resolved_structure["geometry"]["joints"]["topology"] = topology
    assert len(topology["members"]) == 8 + 16 + 1  # 8 posts + 16 braces + 1 hub = 25
    assert len(topology["connections"]) > 0
    
    # 5. CAD 3D Scene Invariants & Topology
    scene = build_structure_scene(resolved_structure)
    validate_scene_geometry(scene)
    
    posts = [s for s in scene.solids if s.role == "post"]
    beams = [s for s in scene.solids if s.role == "beam"]
    rafters = [s for s in scene.solids if s.role == "rafter"]
    braces = [s for s in scene.solids if s.role == "brace"]
    hubs = [s for s in scene.solids if s.role == "hub"]
    
    assert len(posts) == 8
    assert len(beams) == 8
    assert len(rafters) == 8
    assert len(braces) == 16
    assert len(hubs) == 1
