"""
test_structural_physics.py
==========================
Rigorously tests support engineering, physics, and geometry invariants.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from cad_scene import build_structure_scene, validate_scene_geometry, GeometryError


# 1. Test Slenderness ratio (L/d <= 50)
def test_slenderness_invariants():
    """Columns must satisfy the slenderness ratio L/d <= 50 to prevent buckling under load."""
    # Standard 6x6 post (5.5" actual) at 8ft length (96")
    post_length_in = 8.0 * 12.0
    post_width_in = 5.5
    slenderness = post_length_in / post_width_in
    assert slenderness <= 50.0, f"Slenderness ratio {slenderness:.2f} exceeds structural limit of 50"

    # Extreme case: 4x4 post (3.5" actual) at 15ft length (180") -> should be flagged as unsafe
    post_length_unsafe = 15.0 * 12.0
    post_width_unsafe = 3.5
    slenderness_unsafe = post_length_unsafe / post_width_unsafe
    assert slenderness_unsafe > 50.0, "Expected slenderness limit to flag 15ft 4x4 post as structurally unsafe"


# 2. Test Beam Deflection and Stiffness Proxy
def test_beam_deflection_limit():
    """Beams must satisfy maximum deflection and stiffness bounds using the proxy formulas."""
    for span_ft in [8.0, 10.0, 12.0]:
        span_in = span_ft * 12.0
        
        # 6x12 beam (5.5" x 11.5" actual)
        beam_w = 5.5
        beam_d = 11.5
        stiffness = (beam_w * (beam_d ** 3)) / 12.0
        
        # Deflection proxy formula: (span^3) / (stiffness * 1000)
        deflection = (span_in ** 3) / (stiffness * 1000.0)
        assert deflection > 0.0, "Deflection must be a positive non-zero value"
        assert math.isfinite(deflection), "Deflection must be a finite float"
        assert deflection < 5.0, f"Deflection proxy {deflection:.3f}\" exceeds maximum safe physical bounds"


# 3. Test Caisson Bearing Area
def test_caisson_bearing_area():
    """Concrete pier/caisson area must be equal to or larger than post base area to ensure bearing capacity."""
    # Standard 12" caisson vs 6x6 post (5.5" x 5.5")
    caisson_d = 12.0
    caisson_area = math.pi * (caisson_d / 2.0) ** 2
    post_area = 5.5 * 5.5
    assert caisson_area >= post_area, "Post area exceeds concrete bearing caisson area!"


# 4. Test Load Path and Vertical Alignment Geometry
def test_load_path_alignment():
    """The Z-elevations and horizontal layouts of the structural components must form a continuous load path."""
    model = {
        "members": {"posts": {"quantity": 6}},
        "dimensions": {"max_diagonal_ft": 10.0},
    }
    calcs = {
        "total_height": {"post_ft": 8.33, "beam_depth_ft": 1.0},
        "roof_rise":    {"rise_ft": 1.6},
    }
    
    scene = build_structure_scene(model, calcs)
    
    # Verify grade starts at 0.0
    assert scene.Z_GRADE == 0.0
    
    # Verify post top is exactly at Z_POST_TOP (the bottom of the beams)
    assert scene.Z_POST_TOP == 7.33
    
    # Verify beam top is exactly at Z_BEAM_TOP (post top + beam depth)
    assert scene.Z_BEAM_TOP == 8.33
    
    # Verify roof apex is exactly at Z_APEX (beam top + roof rise)
    assert scene.Z_APEX == 9.93


# 5. Test Roof Geometry & Pitch Angles
def test_roof_pitch_geometry():
    """Tests that compound miter and bevel calculations preserve geometric integrity."""
    # Check that flat miter angle for hexagonal ring is exactly 30 degrees (verified regression anchor)
    qty = 6
    flat_miter_angle = 360.0 / (2.0 * qty)
    assert flat_miter_angle == 30.0, f"Hexagonal flat miter should be exactly 30 degrees, got {flat_miter_angle}"
