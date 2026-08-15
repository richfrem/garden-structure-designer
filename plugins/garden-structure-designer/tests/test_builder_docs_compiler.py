import sys
import os
import json
import pytest
from pathlib import Path

# Add scripts to sys.path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from builder_docs_compiler import generate_builder_docs, generate_budget_estimate, generate_lumber_purchase_list, generate_assembly_guide

@pytest.fixture
def mock_staging(tmp_path):
    staging = tmp_path / "context" / "staging"
    staging.mkdir(parents=True)
    outputs = tmp_path / "outputs"
    outputs.mkdir(parents=True)
    shop_bp = outputs / "shop-blueprint"
    shop_bp.mkdir(parents=True)

    structure_data = {
        "jurisdiction": {"region": "BC_Vancouver_Island"},
        "layout": {"shape": "hexagon", "post_count": 6, "inscribed_radius_ft": 10.0},
        "members": {
            "posts": {"nominal_size": "6x6", "cut_length_ft": 8.0, "board_feet": 120.0},
            "beams": {"nominal_size": "6x12", "actual_depth_in": 11.25, "board_feet": 240.0}
        },
        "roof": {
            "pitch": "4:12",
            "primary_rafters": {"count": 6, "nominal_size": "4x6", "cut_length_ft": 8.5, "actual_depth_in": 5.5, "actual_width_in": 3.5, "overhang_ft": 0.75, "board_feet": 180.0}
        },
        "hub": {"type": "polygonal", "radius_min_ft": 0.6},
        "bracing": {
            "enabled": True,
            "brace": {"nominal_size": "4x4", "count_per_post": 2, "constraints": {"run_ft": 1.5}, "board_feet": 60.0}
        },
        "geometry": {
            "compound_cut": {"miter_deg": 28.71, "bevel_deg": 9.10},
            "beam_ring": {"beam_miter_deg": 30.0, "interior_angle_deg": 120.0}
        }
    }

    cut_list_data = {
        "total_board_feet": 600.0,
        "items": [
            {"id": "P1", "role": "post", "nominal": "6x6", "cut_length_ft": 8.0, "board_feet": 20.0},
            {"id": "B1", "role": "beam", "nominal": "6x12", "cut_length_ft": 10.0, "board_feet": 40.0}
        ]
    }

    with open(staging / "structure.json", "w", encoding="utf-8") as f:
        json.dump(structure_data, f)

    with open(shop_bp / "SB01-cut-list.json", "w", encoding="utf-8") as f:
        json.dump(cut_list_data, f)

    return tmp_path

def test_missing_cut_list_fails(tmp_path):
    staging = tmp_path / "context" / "staging"
    staging.mkdir(parents=True)
    outputs = tmp_path / "outputs"
    outputs.mkdir(parents=True)
    
    with open(staging / "structure.json", "w", encoding="utf-8") as f:
        json.dump({"layout": {"shape": "hexagon"}}, f)
        
    res = generate_builder_docs(staging_dir=staging, outputs_dir=outputs)
    assert res["status"] == "FAIL"
    assert "SB01-cut-list.json missing" in res["reason"]

def test_generate_builder_docs_success(mock_staging):
    staging = mock_staging / "context" / "staging"
    outputs = mock_staging / "outputs"
    
    res = generate_builder_docs(staging_dir=staging, outputs_dir=outputs)
    assert res["status"] == "COMPLETE"
    assert (outputs / "budget-estimate.md").exists()
    assert (outputs / "lumber-purchase-list.md").exists()
    assert (outputs / "assembly-guide.md").exists()
    
    assembly_guide = (outputs / "assembly-guide.md").read_text(encoding="utf-8")
    assert "Phase 4.3 — Tripod-First Hub and Rafter Hoisting" in assembly_guide
    assert "miter 28.71" in assembly_guide or "28.71°" in assembly_guide
