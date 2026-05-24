
import sys  # type: ignore[import]
from pathlib import Path  # type: ignore[import]
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from render_drawings import generate_svg  # type: ignore[import]

# Minimal sealed structure.json dict for topology smoke-tests.
# geometry._sealed must be True; all fields referenced by render_drawings must exist.
_STRUCTURE: dict = {
    "meta": {
        "schema_version": "2.0",
        "lifecycle": "GEOMETRY_SEALED",
        "source_hash": "deadbeef" * 8,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
    },
    "intent": {"jurisdiction": "BC_SAANICH"},
    "structure": {"type": "pergola", "shape": "hexagon", "sides": 6},
    "layout": {"post_count": 6, "inscribed_radius_ft": 4.875},
    "members": {
        "posts": {
            "nominal_size": "6x6",
            "actual_width_in": 5.5,
            "actual_depth_in": 5.5,
            "cut_length_ft": 8.33,
        },
        "beams": {
            "nominal_size": "6x12",
            "actual_width_in": 5.5,
            "actual_depth_in": 11.5,
            "cut_length_ft": 5.0,
        },
        "kneebraces": {
            "nominal_size": "4x4",
            "cut_length_in": 36.0,
            "angle_deg": 45.0,
        },
    },
    "footings": {
        "diameter_in": 12.0,
        "depth_in": 48.0,
    },
    "roof": {
        "pitch": "4:12",
        "primary_rafters": {
            "count": 6,
            "nominal_size": "4x6",
            "actual_width_in": 3.5,
            "actual_depth_in": 5.5,
            "overhang_ft": 0.5,
        },
        "secondary_rafters": {
            "enabled": True,
        },
    },
    "hub": {"radius_min_ft": 0.6, "type": "polygonal"},
    "foundation": {"caisson_diameter_in": 12.0, "caisson_depth_in": 24.0},
    "bracing": {
        "enabled": False,
        "brace": {
            "actual_width_in": 3.5,
            "actual_depth_in": 3.5
        }
    },
    "geometry": {
        "_sealed": True,
        "compound_cut": {"miter_deg": 28.71, "bevel_deg": 9.10,
                         "pitch_angle_deg": 18.43, "plan_half_angle_deg": 30.0},
        "beam_ring": {"beam_miter_deg": 30.0, "plan_half_angle_deg": 30.0},
        "rafter": {
            "structural_length_ft": 5.22,
            "total_with_overhang_ft": 5.72,
            "total_with_overhang_in": 68.64,
            "slope_factor": 1.054,
        },
        "roof_rise": {"rise_ft": 1.625, "run_ft": 4.875},
        "total_height": {
            "post_ft": 8.33,
            "beam_depth_ft": 0.958,
            "roof_rise_ft": 1.625,
            "total_height_ft": 10.913,
            "total_height_in": 130.96,
        },
        "hub_radius_ft": 0.75,
        "svg_coordinates": {
            "viewBox": "0 0 1200 1000",
            "width_px": 1200,
            "height_px": 1000,
            "scale_px_per_ft": 80,
            "grade_y": 880,
            "margin_top_px": 60,
            "margin_bottom_px": 120,
            "content_height_px": 820,
            "content_width_px": 980,
            "post_top_y": 214,
            "beam_soffit_y": 214,
            "beam_top_y": 137,
            "hub_apex_y": 7,
            "rise_px": 130,
            "beam_px": 77,
            "post_px": 666,
        },
        "warnings": [],
    },
    "cad": {
        "units": "feet",
        "coordinate_system": "right_handed_z_up",
        "precision": 0.001,
    },
    "invariants": {
        "rafter_count_equals_post_count": True,
        "no_zero_length_members": True,
    },
    "presentation": {"palette": "cedar_warm"},
    "materials": {"primary": "Cedar"},
}


def test_svg_generation(tmp_path):
    from geometry_engine import compute_joints
    cuts = _STRUCTURE["geometry"]["compound_cut"]
    rl = _STRUCTURE["geometry"]["rafter"]
    rise = _STRUCTURE["geometry"]["roof_rise"]
    height = _STRUCTURE["geometry"]["total_height"]
    hub_r = _STRUCTURE["geometry"]["hub_radius_ft"]
    svg_coords = _STRUCTURE["geometry"]["svg_coordinates"]
    _STRUCTURE["geometry"]["joints"] = compute_joints(_STRUCTURE, cuts, rl, rise, height, hub_r, svg_coords)

    out = tmp_path / "plan.svg"
    generate_svg("drawing-plan-view.svg", _STRUCTURE, str(out))
    content = out.read_text()
    assert content.count('data-role="post"') == 6
    assert content.count('data-role="beam"') == 6
    assert content.count('data-role="rafter"') == 18
    assert 'SAW_SETTINGS' in content
    assert 'COORDINATE MAP' in content
