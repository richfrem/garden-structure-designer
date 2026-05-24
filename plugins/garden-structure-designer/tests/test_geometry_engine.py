import json
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from geometry_engine import compute_from_structure  # type: ignore[import]

STRUCTURE_SEED = {
    "meta": {
        "schema_version": "2.0", "lifecycle": "ENGINEERED",
        "source_hash": "abc123", "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z"
    },
    "intent": {"jurisdiction": "BC_SAANICH"},
    "materials": {"primary": "Cedar"},
    "structure": {"type": "pergola", "shape": "hexagon", "sides": 6},
    "layout": {"post_count": 6, "inscribed_radius_ft": 4.875, "post_spacing_ft": 4.875},
    "members": {
        "posts": {"nominal_size": "6x6", "actual_width_in": 5.5,
                  "actual_depth_in": 5.5, "cut_length_ft": 8.42},
        "beams": {"nominal_size": "6x12", "actual_width_in": 6.0,
                  "actual_depth_in": 12.0, "cut_length_ft": 5.0},
    },
    "roof": {
        "type": "hip", "pitch": "4:12", "pitch_defaulted": False,
        "primary_rafters": {
            "count": 6, "nominal_size": "4x6",
            "actual_width_in": 3.5, "actual_depth_in": 5.5, "overhang_ft": 0.75
        },
        "secondary_rafters": {
            "enabled": False, "count_per_side": 0,
            "actual_width_in": 3.5, "actual_depth_in": 5.5
        }
    },
    "hub": {"type": "polygonal", "radius_ft": "auto",
            "radius_min_ft": 0.6, "height_ratio_to_rafter": 2.5, "clearance_ft": 0.5,
            "face_alignment": "mid_angle"},
    "bracing": {
        "enabled": True, "layout": "paired_per_post",
        "brace": {"nominal_size": "4x4", "actual_width_in": 3.5,
                  "actual_depth_in": 3.5, "count_per_post": 2,
                  "constraints": {"start_surface": "post_face", "end_surface": "beam_soffit", "run_ft": 1.5}}
    },
    "footings": {"type": "sonotube", "diameter_in": 12, "depth_in": 24,
                 "concrete_grade": "20MPa"},
    "joinery": {"beam_seat_style": "exposed_tenon", "rafter_tail": "decorative_scallop",
                "rafter_seat_style": "birds_mouth"},
    "invariants": {
        "rafter_count_equals_post_count": True,
        "no_rafter_inside_hub_radius": True,
        "no_zero_length_members": True,
        "member_counts_match_sections": True
    },
    "presentation": {"view_mode": "presentation", "palette": "cedar_warm"},
    "code": {"_sealed": False},
    "geometry": {"_comment": "DERIVED", "_sealed": False},
    "cad": {"_sealed": False, "units": "feet",
            "coordinate_system": "right_handed_z_up", "precision": 0.001}
}

def test_regression_hex_4_12(tmp_path):
    """Regression anchor: hex 4:12 must produce exact canonical values."""
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(STRUCTURE_SEED))
    compute_from_structure(str(p))
    data = json.loads(p.read_text())
    geo = data["geometry"]
    assert geo["compound_cut"]["miter_deg"] == 28.71
    assert geo["compound_cut"]["bevel_deg"] == 9.10
    assert geo["beam_ring"]["beam_miter_deg"] == 30.00
    assert geo["total_height"]["total_height_ft"] == 11.045

def test_joints_payload_computed(tmp_path):
    """Verify that the fabrication-grade joints payload is generated."""
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(STRUCTURE_SEED))
    compute_from_structure(str(p))
    data = json.loads(p.read_text())
    assert "joints" in data["geometry"]
    joints = data["geometry"]["joints"]
    assert "hub" in joints
    assert "rafters" in joints
    assert "braces" in joints
    assert "beam_ring" in joints
    # For a hex, we expect 6 hub face planes
    assert len(joints["hub"]["face_planes"]["planes"]) == 6
    # We expect rafter termination points for each post
    assert len(joints["rafters"]["hub_termination_points"]["points"]) == 6

def test_geometry_section_sealed_after_compute(tmp_path):
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(STRUCTURE_SEED))
    compute_from_structure(str(p))
    data = json.loads(p.read_text())
    assert data["geometry"]["_sealed"] is True

def test_lifecycle_set_to_geometry_sealed(tmp_path):
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(STRUCTURE_SEED))
    compute_from_structure(str(p))
    data = json.loads(p.read_text())
    assert data["meta"]["lifecycle"] == "GEOMETRY_SEALED"

def test_hub_radius_gte_min(tmp_path):
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(STRUCTURE_SEED))
    compute_from_structure(str(p))
    data = json.loads(p.read_text())
    hub_r = data["geometry"]["hub_radius_ft"]
    assert hub_r >= STRUCTURE_SEED["hub"]["radius_min_ft"]

def test_hub_radius_formula_gte_cross_section(tmp_path):
    """hub_r must satisfy both: >= radius_min_ft AND >= rafter cross-section (in feet).
    Uses raw inch inputs to avoid tautology with the formula itself."""
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(STRUCTURE_SEED))
    compute_from_structure(str(p))
    data = json.loads(p.read_text())
    hub_r = data["geometry"]["hub_radius_ft"]
    rafter_w_in = STRUCTURE_SEED["roof"]["primary_rafters"]["actual_width_in"]
    rafter_d_in = STRUCTURE_SEED["roof"]["primary_rafters"]["actual_depth_in"]
    assert hub_r >= STRUCTURE_SEED["hub"]["radius_min_ft"]
    assert hub_r >= (rafter_w_in + rafter_d_in) / 12.0

def test_rafter_count_invariant_enforced(tmp_path):
    """rafter count != post count must produce a warning and exit 1."""
    import copy
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["roof"]["primary_rafters"]["count"] = 5  # mismatch: 5 != 6 posts
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(seed))
    with pytest.raises(SystemExit):
        compute_from_structure(str(p))
    data = json.loads(p.read_text())
    assert any("INVARIANT" in w for w in data["geometry"]["warnings"])

def test_compute_fails_on_already_sealed_geometry(tmp_path):
    import copy
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["geometry"]["_sealed"] = True
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(seed))
    with pytest.raises(RuntimeError, match="sealed"):
        compute_from_structure(str(p))
