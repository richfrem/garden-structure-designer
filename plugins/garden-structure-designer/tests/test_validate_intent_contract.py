"""validate_intent contract completeness: everything downstream stages read must be required here (no silent guessing)."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from test_geometry_engine import STRUCTURE_SEED  # type: ignore[import]  # noqa: E402
from validate_intent import validate_intent  # type: ignore[import]  # noqa: E402


def _without(path: str, seed=None) -> dict:
    structure = copy.deepcopy(seed or STRUCTURE_SEED)
    node = structure
    *parents, leaf = path.split(".")
    for key in parents:
        node = node[key]
    del node[leaf]
    return structure


def test_real_seed_is_a_valid_intent():
    assert validate_intent(copy.deepcopy(STRUCTURE_SEED)) == []


@pytest.mark.parametrize(
    "path",
    [
        "intent.jurisdiction",
        "structure.sides",
        "footings.diameter_in",
        "footings.depth_in",
        "members.posts.actual_depth_in",
        "members.beams.actual_width_in",
        "bracing.brace.actual_width_in",
        "bracing.brace.actual_depth_in",
        "bracing.brace.constraints.run_ft",
    ],
)
def test_downstream_inputs_are_required(path):
    errors = validate_intent(_without(path))
    assert any(e.startswith("MISSING") and path in e for e in errors), errors


def test_brace_dimensions_not_required_when_bracing_is_disabled():
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["bracing"]["enabled"] = False
    del seed["bracing"]["brace"]["actual_width_in"]
    assert validate_intent(seed) == []


def test_blank_jurisdiction_is_rejected():
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["intent"]["jurisdiction"] = "  "
    assert any("intent.jurisdiction" in e for e in validate_intent(seed))
