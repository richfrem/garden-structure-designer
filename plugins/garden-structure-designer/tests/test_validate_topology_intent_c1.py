"""C1 Stage 0.5: required radial intent fields fail closed; family registry is shared with Stage 2."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import constants  # type: ignore[import]  # noqa: E402
import topology_compiler  # type: ignore[import]  # noqa: E402
import validate_topology_intent as stage05  # type: ignore[import]  # noqa: E402
from pipeline_runner import TopologyErrorCode  # type: ignore[import]  # noqa: E402
from test_topology_invariants import _valid_intent  # type: ignore[import]  # noqa: E402


def _run(structure):
    return stage05.run_stage(structure, Path("reports"), Path("outputs"))


def test_valid_hexagon_passes():
    structure = _valid_intent()
    assert _run(structure) is structure


def test_missing_hub_type_fails_closed():
    structure = _valid_intent()
    del structure["hub"]["type"]
    assert _run(structure)["error_code"] is TopologyErrorCode.HUB_TYPE_MISMATCH


def test_missing_hub_section_fails_closed():
    structure = _valid_intent()
    del structure["hub"]
    assert _run(structure)["error_code"] is TopologyErrorCode.HUB_TYPE_MISMATCH


def test_missing_rafter_count_fails_closed():
    structure = _valid_intent()
    del structure["roof"]["primary_rafters"]["count"]
    assert _run(structure)["error_code"] is TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH


def test_family_registry_is_single_sourced():
    assert stage05.IMPLEMENTED_FAMILIES is constants.IMPLEMENTED_FAMILIES
    assert stage05.RESERVED_FAMILIES is constants.RESERVED_FAMILIES
    assert topology_compiler.IMPLEMENTED_FAMILIES is constants.IMPLEMENTED_FAMILIES
    assert topology_compiler.RESERVED_FAMILIES is constants.RESERVED_FAMILIES


def test_valid_orthogonal_grid_passes():
    structure = {
        "meta": {"topology_family": "OrthogonalGridTopology"},
        "structure": {"sides": 4, "shape": "rectangle"},
        "layout": {"post_count": 6, "grid": {"rows": 2, "cols": 3}},
        "roof": {"primary_rafters": {"count": 7}},
        "hub": {"type": "none"},
    }
    assert _run(structure) is structure


def test_orthogonal_grid_invalid_sides_fails():
    structure = {
        "meta": {"topology_family": "OrthogonalGridTopology"},
        "structure": {"sides": 6, "shape": "rectangle"},
        "layout": {"post_count": 6},
        "roof": {"primary_rafters": {"count": 6}},
        "hub": {"type": "none"},
    }
    assert _run(structure)["error_code"] is TopologyErrorCode.GEOMETRY_INVALID


def test_orthogonal_grid_hub_type_mismatch_fails():
    structure = {
        "meta": {"topology_family": "OrthogonalGridTopology"},
        "structure": {"sides": 4, "shape": "rectangle"},
        "layout": {"post_count": 6},
        "roof": {"primary_rafters": {"count": 6}},
        "hub": {"type": "hexagonal_prism"},
    }
    assert _run(structure)["error_code"] is TopologyErrorCode.HUB_TYPE_MISMATCH


def test_orthogonal_grid_cardinality_mismatch_fails():
    structure = {
        "meta": {"topology_family": "OrthogonalGridTopology"},
        "structure": {"sides": 4, "shape": "rectangle"},
        "layout": {"post_count": 6, "grid": {"rows": 2, "cols": 4}},
        "roof": {"primary_rafters": {"count": 6}},
        "hub": {"type": "none"},
    }
    assert _run(structure)["error_code"] is TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH

