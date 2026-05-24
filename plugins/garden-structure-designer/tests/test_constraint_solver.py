"""
test_constraint_solver.py
=========================
Unit tests for constraint_solver.py.

Tests cover:
  1. All constraints PASS on a valid sealed structure
  2. geometry_is_sealed → FAIL on unsealed structure
  3. z_plane_ordering → FAIL on inverted Z planes
  4. hub_radius_within_beam_ring → FAIL when hub overflows beam ring
  5. brace_upper_endpoints_at_beam_soffit → FAIL on misaligned brace endpoint
  6. beam_span_matches_post_chord → WARN on large deviation
  7. beam_span_matches_post_chord → SKIP when field is absent
  8. assert_connections_valid raises ConstraintError on FAIL
  9. assert_connections_valid passes silently on valid structure
"""
from __future__ import annotations

import copy
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from constraint_solver import (
    ConstraintError,
    assert_connections_valid,
    solve_connections,
)

# ---------------------------------------------------------------------------
# Minimal valid sealed structure used as a base for all tests
# ---------------------------------------------------------------------------

_INSCRIBED_R = 4.875
_QTY         = 6
_HUB_R       = 0.75
_Z_POST_TOP  = 7.42
_BRACE_END_Z = _Z_POST_TOP   # must equal Z_POST_TOP

VALID_STRUCTURE: dict = {
    "meta": {"source_hash": "test_hash"},
    "layout": {
        "post_count": _QTY,
        "inscribed_radius_ft": _INSCRIBED_R,
    },
    "geometry": {
        "_sealed": True,
        "hub_radius_ft": _HUB_R,
        "joints": {
            "z_planes": {
                "Z_GRADE": 0.0,
                "Z_POST_TOP": _Z_POST_TOP,
                "Z_BEAM_TOP": 8.42,
                "Z_APEX": 10.045,
            },
            "braces": {
                "enabled": True,
                "endpoints": {
                    "pairs": [
                        {
                            "brace_id": "K1A",
                            "post_index": 0,
                            "toward_post_index": 1,
                            "start": [4.76, 0.20, _Z_POST_TOP - 1.5],
                            "end":   [3.88, 1.73, _BRACE_END_Z],
                        },
                    ]
                },
            },
        },
        "spans": {"beam_span_ft": 2.0 * _INSCRIBED_R * math.sin(math.pi / _QTY)},
    },
    "bracing": {"enabled": True},
}


# ---------------------------------------------------------------------------
# 1. All constraints pass on a valid structure
# ---------------------------------------------------------------------------

def test_all_pass_on_valid_structure():
    results = solve_connections(VALID_STRUCTURE)
    failures = [r for r in results if r["status"] == "FAIL"]
    assert not failures, f"Expected 0 failures, got: {failures}"
    passed = [r for r in results if r["status"] == "PASS"]
    assert len(passed) >= 4, f"Expected ≥4 PASS, got {len(passed)}"


# ---------------------------------------------------------------------------
# 2. geometry_is_sealed → FAIL when geometry not sealed
# ---------------------------------------------------------------------------

def test_unsealed_geometry_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["geometry"]["_sealed"] = False
    results = solve_connections(s)
    sealed_r = next(r for r in results if r["name"] == "geometry_is_sealed")
    assert sealed_r["status"] == "FAIL"
    assert "geometry_engine" in sealed_r["detail"]


# ---------------------------------------------------------------------------
# 3. z_plane_ordering → FAIL on inverted Z planes
# ---------------------------------------------------------------------------

def test_inverted_z_planes_fail():
    s = copy.deepcopy(VALID_STRUCTURE)
    # Swap Z_POST_TOP and Z_BEAM_TOP so ordering is violated
    s["geometry"]["joints"]["z_planes"]["Z_POST_TOP"] = 9.0
    s["geometry"]["joints"]["z_planes"]["Z_BEAM_TOP"] = 8.0
    results = solve_connections(s)
    z_r = next(r for r in results if r["name"] == "z_plane_ordering")
    assert z_r["status"] == "FAIL"
    assert "not strictly ascending" in z_r["detail"]


def test_missing_z_plane_key_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    del s["geometry"]["joints"]["z_planes"]["Z_APEX"]
    results = solve_connections(s)
    z_r = next(r for r in results if r["name"] == "z_plane_ordering")
    assert z_r["status"] == "FAIL"
    assert "Z_APEX" in z_r["detail"]


# ---------------------------------------------------------------------------
# 4. hub_radius_within_beam_ring → FAIL when hub overflows
# ---------------------------------------------------------------------------

def test_hub_overflow_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    # Set hub radius larger than beam ring face radius
    beam_ring_r = _INSCRIBED_R * math.cos(math.pi / _QTY)
    s["geometry"]["hub_radius_ft"] = beam_ring_r + 0.5
    results = solve_connections(s)
    hub_r = next(r for r in results if r["name"] == "hub_radius_within_beam_ring")
    assert hub_r["status"] == "FAIL"
    assert "overflows" in hub_r["detail"]


def test_zero_hub_radius_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["geometry"]["hub_radius_ft"] = 0.0
    results = solve_connections(s)
    hub_r = next(r for r in results if r["name"] == "hub_radius_within_beam_ring")
    assert hub_r["status"] == "FAIL"
    assert "zero" in hub_r["detail"]


# ---------------------------------------------------------------------------
# 5. brace_upper_endpoints_at_beam_soffit → FAIL on misaligned brace end
# ---------------------------------------------------------------------------

def test_misaligned_brace_endpoint_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    # Move the brace end Z 2 inches (0.167 ft) away from Z_POST_TOP
    s["geometry"]["joints"]["braces"]["endpoints"]["pairs"][0]["end"][2] = (
        _Z_POST_TOP + 2.0 / 12.0 + 0.01   # > 1 inch tolerance
    )
    results = solve_connections(s)
    brace_r = next(r for r in results if r["name"] == "brace_upper_endpoints_at_beam_soffit")
    assert brace_r["status"] == "FAIL"
    assert "K1A" in brace_r["detail"]


def test_brace_endpoint_at_tolerance_boundary_passes():
    s = copy.deepcopy(VALID_STRUCTURE)
    # 11/12 of an inch (just inside 1 inch tolerance)
    s["geometry"]["joints"]["braces"]["endpoints"]["pairs"][0]["end"][2] = (
        _Z_POST_TOP + (11.0 / 12.0) / 12.0
    )
    results = solve_connections(s)
    brace_r = next(r for r in results if r["name"] == "brace_upper_endpoints_at_beam_soffit")
    assert brace_r["status"] == "PASS"


def test_no_brace_data_skips():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["geometry"]["joints"]["braces"] = {}
    results = solve_connections(s)
    brace_r = next(r for r in results if r["name"] == "brace_upper_endpoints_at_beam_soffit")
    assert brace_r["status"] == "SKIP"


# ---------------------------------------------------------------------------
# 6. beam_span_matches_post_chord → WARN on large deviation
# ---------------------------------------------------------------------------

def test_beam_span_deviation_warns():
    s = copy.deepcopy(VALID_STRUCTURE)
    # Set beam_span_ft to something way off from the expected chord
    s["geometry"]["spans"]["beam_span_ft"] = 99.0
    results = solve_connections(s)
    span_r = next(r for r in results if r["name"] == "beam_span_matches_post_chord")
    assert span_r["status"] == "WARN"
    assert "deviates" in span_r["detail"]


# ---------------------------------------------------------------------------
# 7. beam_span_matches_post_chord → SKIP when field absent
# ---------------------------------------------------------------------------

def test_missing_beam_span_skips():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["geometry"]["spans"] = {}
    results = solve_connections(s)
    span_r = next(r for r in results if r["name"] == "beam_span_matches_post_chord")
    assert span_r["status"] == "SKIP"


# ---------------------------------------------------------------------------
# 8. assert_connections_valid raises ConstraintError on FAIL
# ---------------------------------------------------------------------------

def test_assert_raises_on_failure():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["geometry"]["_sealed"] = False
    with pytest.raises(ConstraintError, match="geometry_is_sealed"):
        assert_connections_valid(s)


def test_assert_raises_with_multiple_failures():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["geometry"]["_sealed"] = False
    # Also invert Z planes
    s["geometry"]["joints"]["z_planes"]["Z_POST_TOP"] = 9.0
    s["geometry"]["joints"]["z_planes"]["Z_BEAM_TOP"] = 8.0
    with pytest.raises(ConstraintError) as exc_info:
        assert_connections_valid(s)
    msg = str(exc_info.value)
    assert "geometry_is_sealed" in msg
    assert "z_plane_ordering" in msg


# ---------------------------------------------------------------------------
# 9. assert_connections_valid passes silently on valid structure
# ---------------------------------------------------------------------------

def test_assert_passes_on_valid_structure():
    assert_connections_valid(VALID_STRUCTURE)   # must not raise
