"""
test_validate_intent.py
=======================
Unit tests for validate_intent.py.

Tests cover:
  1.  All checks pass on a valid structure (staging-model values)
  2.  Missing layout.post_count → FAIL
  3.  post_count < 3 → FAIL
  4.  Deeply nested missing field (roof.primary_rafters.count) → FAIL
  5.  Invalid roof.pitch format → FAIL
  6.  Missing hub.radius_min_ft → FAIL
  7.  Missing cad.precision → FAIL
  8.  cad.units wrong value → FAIL
  9.  cad.coordinate_system wrong value → FAIL
  10. cad.precision out of range → FAIL
  11. Bracing enabled, missing brace.length_ft → FAIL
  12. Bracing enabled, brace.angle_deg out of [5, 85] → FAIL
  13. Bracing disabled → brace sub-fields not required
  14. assert_intent_valid raises IntentError with all failure names
  15. assert_intent_valid passes silently on valid structure
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from validate_intent import IntentError, assert_intent_valid, validate_intent

# ---------------------------------------------------------------------------
# Valid fixture built from staging-model values
# ---------------------------------------------------------------------------

VALID_STRUCTURE: dict = {
    "layout": {
        "post_count": 6,
        "inscribed_radius_ft": 4.875,
    },
    "roof": {
        "pitch": "4:12",
        "primary_rafters": {
            "count": 6,
            "overhang_ft": 0.75,
            "actual_width_in": 3.5,
            "actual_depth_in": 5.5,
        },
    },
    "members": {
        "posts": {
            "actual_width_in": 5.5,
            "cut_length_ft": 8.42,
        },
        "beams": {
            "actual_depth_in": 12.0,
        },
    },
    "hub": {
        "type": "polygonal",
        "radius_min_ft": 0.6,
    },
    "cad": {
        "units": "feet",
        "coordinate_system": "right_handed_z_up",
        "precision": 0.001,
    },
    "bracing": {
        "enabled": False,
    },
}


# ---------------------------------------------------------------------------
# 1. All checks pass on a valid structure
# ---------------------------------------------------------------------------

def test_all_pass_on_valid_structure():
    errors = validate_intent(VALID_STRUCTURE)
    assert errors == [], f"Expected no errors, got: {errors}"


# ---------------------------------------------------------------------------
# 2. Missing layout.post_count → FAIL
# ---------------------------------------------------------------------------

def test_missing_post_count_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    del s["layout"]["post_count"]
    errors = validate_intent(s)
    assert any("layout.post_count" in e for e in errors), f"Expected post_count error, got: {errors}"
    assert any("MISSING" in e for e in errors)


# ---------------------------------------------------------------------------
# 3. post_count < 3 → FAIL
# ---------------------------------------------------------------------------

def test_post_count_less_than_3_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["layout"]["post_count"] = 2
    errors = validate_intent(s)
    assert any("layout.post_count" in e for e in errors), f"Expected post_count range error, got: {errors}"
    assert any("OUT_OF_RANGE" in e for e in errors)


def test_post_count_exactly_3_passes():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["layout"]["post_count"] = 3
    errors = validate_intent(s)
    assert not any("layout.post_count" in e for e in errors), f"post_count=3 should pass, got: {errors}"


# ---------------------------------------------------------------------------
# 4. Deeply nested missing field → FAIL
# ---------------------------------------------------------------------------

def test_missing_nested_rafter_count_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    del s["roof"]["primary_rafters"]["count"]
    errors = validate_intent(s)
    assert any("roof.primary_rafters.count" in e for e in errors), f"Expected rafter count error, got: {errors}"


# ---------------------------------------------------------------------------
# 5. Invalid roof.pitch format → FAIL
# ---------------------------------------------------------------------------

def test_invalid_pitch_format_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["roof"]["pitch"] = "steep"
    errors = validate_intent(s)
    assert any("roof.pitch" in e for e in errors), f"Expected pitch format error, got: {errors}"
    assert any("OUT_OF_RANGE" in e for e in errors)


def test_pitch_wrong_denominator_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["roof"]["pitch"] = "4:10"
    errors = validate_intent(s)
    assert any("roof.pitch" in e for e in errors)


def test_pitch_valid_formats_pass():
    for pitch in ("3:12", "4:12", "12:12"):
        s = copy.deepcopy(VALID_STRUCTURE)
        s["roof"]["pitch"] = pitch
        errors = validate_intent(s)
        assert not any("roof.pitch" in e for e in errors), f"pitch={pitch!r} should pass, got: {errors}"


# ---------------------------------------------------------------------------
# 6. Missing hub.radius_min_ft → FAIL
# ---------------------------------------------------------------------------

def test_missing_hub_radius_min_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    del s["hub"]["radius_min_ft"]
    errors = validate_intent(s)
    assert any("hub.radius_min_ft" in e for e in errors), f"Expected hub.radius_min_ft error, got: {errors}"


def test_zero_hub_radius_min_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["hub"]["radius_min_ft"] = 0.0
    errors = validate_intent(s)
    assert any("hub.radius_min_ft" in e for e in errors)
    assert any("OUT_OF_RANGE" in e for e in errors)


# ---------------------------------------------------------------------------
# 7. Missing cad.precision → FAIL
# ---------------------------------------------------------------------------

def test_missing_cad_precision_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    del s["cad"]["precision"]
    errors = validate_intent(s)
    assert any("cad.precision" in e for e in errors), f"Expected cad.precision error, got: {errors}"


# ---------------------------------------------------------------------------
# 8. cad.units wrong value → FAIL
# ---------------------------------------------------------------------------

def test_cad_units_wrong_value_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["cad"]["units"] = "meters"
    errors = validate_intent(s)
    assert any("cad.units" in e for e in errors), f"Expected cad.units error, got: {errors}"
    assert any("OUT_OF_RANGE" in e for e in errors)


# ---------------------------------------------------------------------------
# 9. cad.coordinate_system wrong value → FAIL
# ---------------------------------------------------------------------------

def test_cad_coordinate_system_wrong_value_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["cad"]["coordinate_system"] = "left_handed"
    errors = validate_intent(s)
    assert any("cad.coordinate_system" in e for e in errors), f"Expected coordinate_system error, got: {errors}"


# ---------------------------------------------------------------------------
# 10. cad.precision out of range → FAIL
# ---------------------------------------------------------------------------

def test_cad_precision_out_of_range_fails():
    for bad in (0.0, 1.0, 5.0):
        s = copy.deepcopy(VALID_STRUCTURE)
        s["cad"]["precision"] = bad
        errors = validate_intent(s)
        assert any("cad.precision" in e for e in errors), f"precision={bad} should fail, got: {errors}"
        assert any("OUT_OF_RANGE" in e for e in errors)


def test_cad_precision_valid_value_passes():
    for good in (0.001, 0.01, 0.5):
        s = copy.deepcopy(VALID_STRUCTURE)
        s["cad"]["precision"] = good
        errors = validate_intent(s)
        assert not any("cad.precision" in e for e in errors), f"precision={good} should pass, got: {errors}"


# ---------------------------------------------------------------------------
# 11. Bracing enabled, missing brace.length_ft → FAIL
# ---------------------------------------------------------------------------

def test_bracing_enabled_missing_constraints_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["bracing"] = {"enabled": True, "brace": {"nominal_size": "4x4", "actual_width_in": 3.5, "actual_depth_in": 3.5, "count_per_post": 2}}
    errors = validate_intent(s)
    assert any("bracing.brace.constraints.start_surface" in e for e in errors), f"Expected start_surface error, got: {errors}"
    assert any("bracing.brace.constraints.end_surface" in e for e in errors), f"Expected end_surface error, got: {errors}"


def test_bracing_enabled_valid_brace_passes():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["bracing"] = {"enabled": True, "brace": {"nominal_size": "4x4", "actual_width_in": 3.5, "actual_depth_in": 3.5, "count_per_post": 2,
                                               "constraints": {"start_surface": "post_face", "end_surface": "beam_soffit"}}}
    errors = validate_intent(s)
    assert not any("bracing.brace" in e for e in errors), f"Valid brace should pass, got: {errors}"


# ---------------------------------------------------------------------------
# 13. Bracing disabled → brace sub-fields not required
# ---------------------------------------------------------------------------

def test_bracing_disabled_no_brace_fields_required():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["bracing"] = {"enabled": False}
    errors = validate_intent(s)
    assert not any("bracing.brace" in e for e in errors), f"Disabled bracing should not require brace fields, got: {errors}"


def test_bracing_key_absent_no_brace_fields_required():
    s = copy.deepcopy(VALID_STRUCTURE)
    del s["bracing"]
    errors = validate_intent(s)
    assert not any("bracing.brace" in e for e in errors), f"Absent bracing should not require brace fields, got: {errors}"


# ---------------------------------------------------------------------------
# 14. assert_intent_valid raises IntentError with all failure names
# ---------------------------------------------------------------------------

def test_assert_raises_on_missing_field():
    s = copy.deepcopy(VALID_STRUCTURE)
    del s["layout"]["post_count"]
    with pytest.raises(IntentError, match="layout.post_count"):
        assert_intent_valid(s)


def test_assert_raises_with_multiple_failures():
    s = copy.deepcopy(VALID_STRUCTURE)
    del s["layout"]["post_count"]
    del s["hub"]["radius_min_ft"]
    with pytest.raises(IntentError) as exc_info:
        assert_intent_valid(s)
    msg = str(exc_info.value)
    assert "layout.post_count" in msg
    assert "hub.radius_min_ft" in msg


def test_assert_error_message_includes_count():
    s = copy.deepcopy(VALID_STRUCTURE)
    del s["layout"]["post_count"]
    del s["hub"]["radius_min_ft"]
    with pytest.raises(IntentError) as exc_info:
        assert_intent_valid(s)
    assert "2 error" in str(exc_info.value)


# ---------------------------------------------------------------------------
# 15. assert_intent_valid passes silently on valid structure
# ---------------------------------------------------------------------------

def test_assert_passes_on_valid_structure():
    assert_intent_valid(VALID_STRUCTURE)   # must not raise
