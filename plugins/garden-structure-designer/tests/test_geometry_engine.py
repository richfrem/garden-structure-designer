import pytest
import os
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from geometry_engine import compute

def test_hex_beam_miter_angle():
    # Mock model for hexagonal structure
    model_path = os.path.join(os.path.dirname(__file__), "fixtures", "mock_hex_model.json")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "w") as f:
        json.dump({
            "members": {"posts": {"quantity": 6, "spanDistance_ft": 5.0}},
            "roofStructure": {"pitch": "4:12"}
        }, f)
        
    result = compute(model_path)
    assert result["beam_ring"]["beam_miter_deg"] == 30.0
    assert round(result["compound_cut"]["miter_deg"], 2) == 28.71
    assert round(result["compound_cut"]["pitch_angle_deg"], 2) == 18.43
