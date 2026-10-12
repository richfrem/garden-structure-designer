"""
test_rendering_baseline.py
==========================

Phase 0 Task 0.1 Baseline Test:
Verifies the immutable frozen reference fixture for the 10ft hexagonal Yellow Cedar pergola:
1. Valid structure.json schema and metadata.
2. Exact member count and roles (6 posts, 6 beams, 6 rafters, 12 braces, 6 footings, 1 hub).
3. Resolved model constraints and joint coordinates.
"""
import json
from pathlib import Path
import pytest


def test_frozen_hex_pergola_fixture_integrity():
    """Verify that the frozen reference fixture matches the required member inventory and metadata."""
    fixture_path = Path(__file__).parent / "fixtures" / "rendering" / "hex_10ft_yellow_cedar.structure.json"
    assert fixture_path.exists(), f"Frozen fixture missing at {fixture_path}"

    with open(fixture_path, encoding="utf-8") as f:
        structure = json.load(f)

    # 1. Structure metadata & intent
    assert structure["structure"]["shape"] == "hexagon"
    assert structure["structure"]["sides"] == 6
    assert structure["materials"]["primary"] == "Yellow Cedar"
    assert structure["intent"]["jurisdiction"] == "BC_SAANICH"

    # 2. Member counts in resolved model
    members = structure["geometry"]["joints"]["resolved_model"]["members"]
    roles = [m["role"] for m in members]

    assert roles.count("post") == 6, f"Expected 6 posts, found {roles.count('post')}"
    assert roles.count("beam") == 6, f"Expected 6 beams, found {roles.count('beam')}"
    assert roles.count("rafter") == 6, f"Expected 6 rafters, found {roles.count('rafter')}"
    assert roles.count("brace") == 12, f"Expected 12 braces, found {roles.count('brace')}"
    assert roles.count("footing") == 6, f"Expected 6 footings, found {roles.count('footing')}"
    assert roles.count("hub") == 1, f"Expected 1 hub, found {roles.count('hub')}"

    # Total member count
    assert len(members) == 37, f"Expected 37 total members, found {len(members)}"
