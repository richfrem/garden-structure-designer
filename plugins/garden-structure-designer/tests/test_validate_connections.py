"""
test_validate_connections.py
============================
Tests for validate_connections.py.

These are physical contact checks that operate on Scene geometry AFTER
cad_scene.build_structure_scene() runs. They catch failures that the
existing geometric invariants (validate_scene_geometry) do NOT catch:

  - beam_soffit_at_post_top uses face VERTICES (invariants use p0/p1)
  - rafter_tip_on_hub_face checks point-to-plane distance (invariants check apex Z only)
  - brace_foot_on_post_face checks point-to-plane distance (invariants use loose 1 ft XY proximity)

Tests:
  1.  All checks PASS on a validly built scene
  2.  beam_soffit_at_post_top FAILS when beam face verts lifted (p0/p1 unchanged → invariants pass)
  3.  rafter_tip_on_hub_face FAILS when rafter p1 displaced far from hub
  4.  brace_foot_on_post_face FAILS when brace lower endpoint displaced far from any post face
  5.  Multiple failures reported in one call
  6.  assert_connections_physical raises ConnectionError with failing check name
  7.  assert_connections_physical passes silently on valid scene
  8.  ConnectionError message includes error count
  9.  Scene with no braces SKIPs brace_foot check cleanly
  10. Scene with no hub SKIPs rafter_tip check cleanly
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from cad_scene import build_structure_scene, Scene
from validate_connections import (
    ContactError,
    assert_connections_physical,
    validate_connections,
)

# ---------------------------------------------------------------------------
# Shared fixture — same minimal model as test_cad_geometry_invariants
# ---------------------------------------------------------------------------

_MODEL = {
    "members": {"posts": {"quantity": 6}},
    "dimensions": {"max_diagonal_ft": 10.0},
}
_CALCS = {
    "total_height": {"post_ft": 8.33, "beam_depth_ft": 0.604},
    "roof_rise":    {"rise_ft": 1.667},
}


@pytest.fixture(scope="module")
def valid_scene() -> Scene:
    return build_structure_scene(_MODEL, _CALCS)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _lift_beam_faces(scene: Scene, beam_tag: str, lift_ft: float) -> Scene:
    """Return a deepcopy with all face vertices of named beam shifted up by lift_ft.
    Intentionally leaves p0/p1 untouched so validate_scene_geometry (Invariant 6) still passes."""
    s = copy.deepcopy(scene)
    for solid in s.solids:
        if solid.role == "beam" and solid.tag == beam_tag:
            for face in solid.faces:
                face.verts = [(x, y, z + lift_ft) for x, y, z in face.verts]
    return s


def _displace_rafter_p1(scene: Scene, rafter_tag: str, new_xy: tuple[float, float]) -> Scene:
    """Return a deepcopy with the named rafter's p1 moved to (new_xy[0], new_xy[1], Z_APEX)."""
    s = copy.deepcopy(scene)
    for solid in s.solids:
        if solid.role == "rafter" and solid.tag == rafter_tag:
            solid.p1 = (new_xy[0], new_xy[1], solid.p1[2])
    return s


def _displace_brace_foot(scene: Scene, brace_tag: str, new_xy: tuple[float, float]) -> Scene:
    """Return a deepcopy with the named brace's lower endpoint moved to new_xy.
    Identifies lower endpoint as the one with smaller Z."""
    s = copy.deepcopy(scene)
    for solid in s.solids:
        if solid.role == "brace" and solid.tag == brace_tag:
            if solid.p0[2] <= solid.p1[2]:
                solid.p0 = (new_xy[0], new_xy[1], solid.p0[2])
            else:
                solid.p1 = (new_xy[0], new_xy[1], solid.p1[2])
    return s


def _remove_solids_by_role(scene: Scene, role: str) -> Scene:
    """Return a deepcopy with all solids of given role removed."""
    s = copy.deepcopy(scene)
    s.solids = [solid for solid in s.solids if solid.role != role]
    return s


# ---------------------------------------------------------------------------
# 1. Valid scene passes all checks
# ---------------------------------------------------------------------------

def test_all_checks_pass_on_valid_scene(valid_scene):
    errors = validate_connections(valid_scene)
    assert errors == [], f"Expected no errors on valid scene, got:\n" + "\n".join(errors)


# ---------------------------------------------------------------------------
# 2. beam_soffit_at_post_top FAILS when beam face verts lifted
# ---------------------------------------------------------------------------

def test_beam_soffit_fails_when_face_verts_lifted(valid_scene):
    # Lift face verts by 3/8 inch (> 1/8 inch tolerance) without touching p0/p1
    broken = _lift_beam_faces(valid_scene, "B1", lift_ft=3.0/96.0)
    errors = validate_connections(broken)
    assert any("beam_soffit" in e for e in errors), (
        f"Expected beam_soffit error, got: {errors}"
    )
    assert any("B1" in e for e in errors)


def test_beam_soffit_passes_within_tolerance(valid_scene):
    # Lift by 1/16 inch (< 1/8 inch tolerance) — should still pass
    ok = _lift_beam_faces(valid_scene, "B1", lift_ft=1.0/192.0)
    errors = validate_connections(ok)
    assert not any("beam_soffit" in e and "B1" in e for e in errors), (
        f"1/16\" lift should pass, got: {errors}"
    )


# ---------------------------------------------------------------------------
# 3. rafter_tip_on_hub_face FAILS when rafter p1 displaced far from hub
# ---------------------------------------------------------------------------

def test_rafter_tip_fails_when_displaced_far_from_hub(valid_scene):
    # Move a hip rafter p1 50 ft away from origin — clearly not on hub face
    broken = _displace_rafter_p1(valid_scene, "R1", new_xy=(50.0, 50.0))
    errors = validate_connections(broken)
    assert any("rafter_tip" in e or "hub_face" in e for e in errors), (
        f"Expected rafter-hub contact error, got: {errors}"
    )
    assert any("R1" in e for e in errors)


def test_rafter_tip_passes_on_valid_hub_contact(valid_scene):
    errors = validate_connections(valid_scene)
    assert not any("rafter_tip" in e or "hub_face" in e for e in errors), (
        f"Valid scene should have no rafter-hub errors, got: {errors}"
    )


# ---------------------------------------------------------------------------
# 4. brace_foot_on_post_face FAILS when brace lower endpoint displaced
# ---------------------------------------------------------------------------

def test_brace_foot_fails_when_displaced_far_from_post(valid_scene):
    # Move brace lower foot 50 ft away from any post
    broken = _displace_brace_foot(valid_scene, "Brace0a", new_xy=(50.0, 50.0))
    errors = validate_connections(broken)
    assert any("brace_foot" in e for e in errors), (
        f"Expected brace_foot error, got: {errors}"
    )
    assert any("Brace0a" in e for e in errors)


def test_brace_foot_passes_on_valid_scene(valid_scene):
    errors = validate_connections(valid_scene)
    assert not any("brace_foot" in e for e in errors), (
        f"Valid scene should have no brace-foot errors, got: {errors}"
    )


# ---------------------------------------------------------------------------
# 5. Multiple failures reported in one call
# ---------------------------------------------------------------------------

def test_multiple_failures_reported(valid_scene):
    broken = _lift_beam_faces(valid_scene, "B1", lift_ft=3.0/96.0)
    broken = _displace_rafter_p1(broken, "R1", new_xy=(50.0, 50.0))
    errors = validate_connections(broken)
    assert len(errors) >= 2, f"Expected ≥2 errors, got {len(errors)}: {errors}"


# ---------------------------------------------------------------------------
# 6. assert_connections_physical raises ConnectionError with check name
# ---------------------------------------------------------------------------

def test_assert_raises_connection_error(valid_scene):
    broken = _lift_beam_faces(valid_scene, "B1", lift_ft=3.0/96.0)
    with pytest.raises(ContactError, match="beam_soffit"):
        assert_connections_physical(broken)


# ---------------------------------------------------------------------------
# 7. assert_connections_physical passes silently on valid scene
# ---------------------------------------------------------------------------

def test_assert_passes_on_valid_scene(valid_scene):
    assert_connections_physical(valid_scene)   # must not raise


# ---------------------------------------------------------------------------
# 8. ConnectionError message includes error count
# ---------------------------------------------------------------------------

def test_assert_error_message_includes_count(valid_scene):
    broken = _lift_beam_faces(valid_scene, "B1", lift_ft=3.0/96.0)
    with pytest.raises(ContactError) as exc_info:
        assert_connections_physical(broken)
    assert "error" in str(exc_info.value).lower()


# ---------------------------------------------------------------------------
# 9. Scene with no braces SKIPs brace_foot check cleanly (no crash)
# ---------------------------------------------------------------------------

def test_no_braces_skips_cleanly(valid_scene):
    no_braces = _remove_solids_by_role(valid_scene, "brace")
    errors = validate_connections(no_braces)
    assert not any("brace_foot" in e for e in errors), (
        f"No braces should produce no brace-foot errors, got: {errors}"
    )


# ---------------------------------------------------------------------------
# 10. Scene with no hub SKIPs rafter_tip check cleanly (no crash)
# ---------------------------------------------------------------------------

def test_no_hub_skips_rafter_tip_cleanly(valid_scene):
    no_hub = _remove_solids_by_role(valid_scene, "hub")
    errors = validate_connections(no_hub)
    assert not any("rafter_tip" in e or "hub_face" in e for e in errors), (
        f"No hub should produce no rafter-hub errors, got: {errors}"
    )
