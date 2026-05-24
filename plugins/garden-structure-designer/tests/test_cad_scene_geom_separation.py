"""
test_cad_scene_geom_separation.py
==================================
Enforces the architectural rule from CLAUDE.md §Data-Driven & Declarative Architecture:

   "all CAD engine dimensions... must dynamically resolve from staging structure.json.
    Hardcoding geometry layouts, viewport scales, and silent fallback defaults
    (e.g. .get(key, default) defaults) in python scripts is strictly prohibited.
    If configurations are missing, fail-closed immediately."

Specifically targeted at ensuring cad_scene.py acts as a pure translator of the compiler's output.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).parent))
from cad_scene import (
    GeometryError,
    build_structure_scene,
)

# ---------------------------------------------------------------------------
# Seed helper
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
# 1. Unresolved/missing resolved_model raises GeometryError
# ---------------------------------------------------------------------------

def test_missing_resolved_model_raises():
    """Verify that build_structure_scene fails closed if resolved_model is missing."""
    empty_model = {"geometry": {}}
    with pytest.raises(GeometryError, match="must be fully resolved"):
        build_structure_scene(empty_model)


# ---------------------------------------------------------------------------
# 2. Bracing disabled -> no brace solids built
# ---------------------------------------------------------------------------

def test_new_path_bracing_disabled_no_braces(tmp_path):
    """
    When bracing.enabled=False, no brace solids should be produced.
    """
    s = _seeded_structure(tmp_path)
    s["bracing"]["enabled"] = False
    s.pop("geometry", None)  # Remove sealed geometry section so compute_from_structure can re-compute it
    # Re-run compute to update the resolved model
    from geometry_engine import compute_from_structure
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(s))
    compute_from_structure(str(p))
    s_updated = json.loads(p.read_text())
    
    scene = build_structure_scene(s_updated)
    braces = [so for so in scene.solids if so.role == "brace"]
    assert braces == [], f"Expected no braces when disabled, got {len(braces)}"
