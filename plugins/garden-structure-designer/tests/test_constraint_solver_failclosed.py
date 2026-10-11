"""Required inputs must fail closed (C2): no SKIP when the intent says the data must exist."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from test_constraint_solver import VALID_STRUCTURE  # type: ignore[import]  # noqa: E402
from constraint_solver import solve_connections  # type: ignore[import]  # noqa: E402


def _status(structure, name):
    return next(r for r in solve_connections(structure) if r["name"] == name)["status"]


def test_missing_layout_fails_hub_radius_check():
    s = copy.deepcopy(VALID_STRUCTURE)
    del s["layout"]["inscribed_radius_ft"]
    assert _status(s, "hub_radius_within_beam_ring") == "FAIL"


def test_enabled_bracing_without_endpoints_fails():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["bracing"] = {"enabled": True}
    s["geometry"]["joints"]["braces"] = {}
    assert _status(s, "brace_upper_endpoints_at_beam_soffit") == "FAIL"


def test_disabled_bracing_without_endpoints_still_skips():
    s = copy.deepcopy(VALID_STRUCTURE)
    s["bracing"] = {"enabled": False}
    s["geometry"]["joints"]["braces"] = {}
    assert _status(s, "brace_upper_endpoints_at_beam_soffit") == "SKIP"
