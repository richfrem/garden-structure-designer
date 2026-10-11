"""C1: structure.sides is the authoritative side count for assembly-guide rules."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from assembly_guide_validator import validate  # type: ignore[import]  # noqa: E402

GUIDE = "Test cut on scrap first. Miter 28.71 bevel 9.1."


def _write(tmp_path, structure):
    guide, calcs = tmp_path / "guide.md", tmp_path / "structure.json"
    guide.write_text(GUIDE)
    calcs.write_text(json.dumps(structure))
    return str(guide), str(calcs)


def test_hex_tripod_required_from_structure_sides(tmp_path):
    structure = {"structure": {"sides": 6}, "geometry": {"compound_cut": {"miter_deg": 28.71, "bevel_deg": 9.1}}}
    errors = validate(*_write(tmp_path, structure))
    assert any(e.startswith("HEX_TRIPOD_MISSING") for e in errors)


def test_non_hex_needs_no_tripod(tmp_path):
    structure = {"structure": {"sides": 8}, "geometry": {"compound_cut": {"miter_deg": 28.71, "bevel_deg": 9.1}}}
    assert validate(*_write(tmp_path, structure)) == []
