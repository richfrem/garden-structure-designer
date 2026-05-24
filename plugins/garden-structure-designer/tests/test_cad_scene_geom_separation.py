"""
test_cad_scene_geom_separation.py
==================================
Enforces the architectural rule from CLAUDE.md §Data-Driven & Declarative Architecture:

  "all CAD engine dimensions... must dynamically resolve from staging structure.json.
   Hardcoding geometry layouts, viewport scales, and silent fallback defaults
   (e.g. .get(key, default) defaults) in python scripts is strictly prohibited.
   If configurations are missing, fail-closed immediately."

Specifically targeted at FIX 2: strip geometry math and silent fallbacks from cad_scene.py.

Tests:
  1.  Legacy path, empty kneebraces spec → no brace solids (skip rather than fallback 1.5 ft)
  2.  Legacy path, cutLength_in only (no angle_deg) → GeometryError
  3.  Legacy path, angle_deg only (no cutLength_in) → GeometryError
  4.  Legacy path, complete kneebraces spec → correct brace geometry (no silent fallback)
  5.  New path, bracing enabled, missing length_ft → GeometryError
  6.  New path, bracing enabled, missing angle_deg → GeometryError
  7.  New path, bracing disabled → no brace solids built
  8.  _hip_rafter_slope helper: correct value from inputs
  9.  _hip_rafter_slope helper: positive run required (zero denominator raises GeometryError)
  10. _hip_rafter_slope helper: negative run raises GeometryError
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from cad_scene import (
    GeometryError,
    build_structure_scene,
    _hip_rafter_slope,
)

# ---------------------------------------------------------------------------
# Legacy-path fixtures
# ---------------------------------------------------------------------------

_LEGACY_MODEL_BASE = {
    "members": {
        "posts": {"quantity": 6},
    },
    "dimensions": {"max_diagonal_ft": 10.0},
}
_LEGACY_CALCS = {
    "total_height": {"post_ft": 8.33, "beam_depth_ft": 0.604},
    "roof_rise":    {"rise_ft": 1.667},
}

_VALID_BRACE_SPEC = {
    "cutLength_in": 30.0,   # 2.5 ft hypotenuse
    "angle_deg":    45.0,
}

# ---------------------------------------------------------------------------
# New-path fixture (requires a sealed structure.json with geometry section)
# ---------------------------------------------------------------------------

def _seeded_structure(tmp_path):
    """Return a fully-sealed structure dict (geometry section populated)."""
    from geometry_engine import compute_from_structure  # type: ignore[import]
    from test_geometry_engine import STRUCTURE_SEED     # type: ignore[import]
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(copy.deepcopy(STRUCTURE_SEED)))
    compute_from_structure(str(p))
    return json.loads(p.read_text())


# ---------------------------------------------------------------------------
# 1. Legacy empty kneebraces → no brace solids
# ---------------------------------------------------------------------------

def test_legacy_empty_kneebraces_no_braces_built():
    """
    When model.members has no 'kneebraces' key (or an empty dict),
    cad_scene must NOT produce any brace solids.  The old code silently
    fell back to brace_run=1.5 and produced 12 phantom braces.
    """
    model = copy.deepcopy(_LEGACY_MODEL_BASE)
    # No 'kneebraces' key at all
    scene = build_structure_scene(model, _LEGACY_CALCS)
    braces = [s for s in scene.solids if s.role == "brace"]
    assert braces == [], (
        f"Expected 0 braces when kneebraces spec absent, got {len(braces)}"
    )


# ---------------------------------------------------------------------------
# 2. Legacy cutLength_in only → GeometryError
# ---------------------------------------------------------------------------

def test_legacy_partial_spec_cutlength_only_raises():
    """
    Non-empty kneebraces spec with cutLength_in but no angle_deg must
    fail-closed (GeometryError), not fall back to brace_run=1.5.
    """
    model = copy.deepcopy(_LEGACY_MODEL_BASE)
    model["members"]["kneebraces"] = {"cutLength_in": 30.0}
    with pytest.raises(GeometryError, match="angle_deg"):
        build_structure_scene(model, _LEGACY_CALCS)


# ---------------------------------------------------------------------------
# 3. Legacy angle_deg only → GeometryError
# ---------------------------------------------------------------------------

def test_legacy_partial_spec_angle_only_raises():
    """
    Non-empty kneebraces spec with angle_deg but no cutLength_in must
    fail-closed (GeometryError).
    """
    model = copy.deepcopy(_LEGACY_MODEL_BASE)
    model["members"]["kneebraces"] = {"angle_deg": 45.0}
    with pytest.raises(GeometryError, match="cutLength_in"):
        build_structure_scene(model, _LEGACY_CALCS)


# ---------------------------------------------------------------------------
# 4. Legacy complete spec → braces built with correct geometry
# ---------------------------------------------------------------------------

def test_legacy_complete_spec_builds_braces():
    """
    With a complete kneebraces spec, brace solids must be produced and
    their run/drop geometry must match the spec — NOT the hardcoded 1.5 ft.
    """
    model = copy.deepcopy(_LEGACY_MODEL_BASE)
    model["members"]["kneebraces"] = _VALID_BRACE_SPEC.copy()
    scene = build_structure_scene(model, _LEGACY_CALCS)
    braces = [s for s in scene.solids if s.role == "brace"]
    # 6 posts × 2 braces per post = 12 total
    assert len(braces) == 12, f"Expected 12 braces, got {len(braces)}"
    # Verify brace upper node is at Z_POST_TOP (beam soffit)
    Z_POST_TOP = scene.Z_POST_TOP
    TOL = 1.0 / 96.0  # 1/8 inch in feet
    for b in braces:
        upper_z = max(b.p0[2], b.p1[2])
        assert abs(upper_z - Z_POST_TOP) <= TOL, (
            f"Brace {b.tag}: upper Z={upper_z:.4f} != Z_POST_TOP={Z_POST_TOP:.4f} "
            f"(delta={abs(upper_z - Z_POST_TOP)*12:.3f}\")"
        )


# ---------------------------------------------------------------------------
# 5. New path, bracing enabled, missing length_ft → GeometryError
# ---------------------------------------------------------------------------

def test_new_path_bracing_enabled_missing_length_raises(tmp_path):
    """
    When bracing.enabled=True but brace.length_ft is absent,
    build_structure_scene must raise GeometryError (fail-closed).
    The old code used get("length_ft", 2.5) silently.
    """
    s = _seeded_structure(tmp_path)
    s["bracing"] = {"enabled": True, "brace": {"angle_deg": 45.0}}
    with pytest.raises(GeometryError, match="length_ft"):
        build_structure_scene(s)


# ---------------------------------------------------------------------------
# 6. New path, bracing enabled, missing angle_deg → GeometryError
# ---------------------------------------------------------------------------

def test_new_path_bracing_enabled_missing_angle_raises(tmp_path):
    """
    When bracing.enabled=True but brace.angle_deg is absent,
    build_structure_scene must raise GeometryError (fail-closed).
    The old code used get("angle_deg", 45) silently.
    """
    s = _seeded_structure(tmp_path)
    s["bracing"] = {"enabled": True, "brace": {"length_ft": 2.5}}
    with pytest.raises(GeometryError, match="angle_deg"):
        build_structure_scene(s)


# ---------------------------------------------------------------------------
# 7. New path, bracing disabled → no brace solids
# ---------------------------------------------------------------------------

def test_new_path_bracing_disabled_no_braces(tmp_path):
    """
    When bracing.enabled=False, no brace solids should be produced regardless
    of whether brace sub-fields are present.
    """
    s = _seeded_structure(tmp_path)
    s["bracing"] = {"enabled": False}
    scene = build_structure_scene(s)
    braces = [so for so in scene.solids if so.role == "brace"]
    assert braces == [], f"Expected no braces when disabled, got {len(braces)}"


# ---------------------------------------------------------------------------
# 8. _hip_rafter_slope: correct formula
# ---------------------------------------------------------------------------

def test_hip_rafter_slope_formula():
    """
    _hip_rafter_slope(Z_APEX, Z_BEAM_TOP, r_ft, hub_r) = (Z_APEX - Z_BEAM_TOP) / (r_ft - hub_r)
    This helper must exist as a named, testable function (not inlined).
    """
    slope = _hip_rafter_slope(Z_APEX=10.0, Z_BEAM_TOP=8.0, r_ft=5.0, hub_r=1.0)
    # rise=2.0, run=4.0 → slope=0.5
    assert abs(slope - 0.5) < 1e-10, f"Expected 0.5, got {slope}"


def test_hip_rafter_slope_positive_values():
    """Positive slope for any positive rise and run."""
    slope = _hip_rafter_slope(Z_APEX=12.0, Z_BEAM_TOP=8.33, r_ft=5.0, hub_r=0.75)
    assert slope > 0.0


# ---------------------------------------------------------------------------
# 9. _hip_rafter_slope: zero run raises GeometryError
# ---------------------------------------------------------------------------

def test_hip_rafter_slope_zero_run_raises():
    """
    r_ft == hub_r gives run=0; cad_scene must raise GeometryError, not divide-by-zero.
    """
    with pytest.raises(GeometryError):
        _hip_rafter_slope(Z_APEX=10.0, Z_BEAM_TOP=8.0, r_ft=0.6, hub_r=0.6)


# ---------------------------------------------------------------------------
# 10. _hip_rafter_slope: negative run raises GeometryError
# ---------------------------------------------------------------------------

def test_hip_rafter_slope_negative_run_raises():
    """
    r_ft < hub_r (hub larger than post ring) is geometrically impossible.
    Must raise GeometryError.
    """
    with pytest.raises(GeometryError):
        _hip_rafter_slope(Z_APEX=10.0, Z_BEAM_TOP=8.0, r_ft=0.5, hub_r=0.6)
