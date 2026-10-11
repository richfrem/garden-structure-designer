"""load_applicable_lessons: lessons are matched on the design's real shape/roof; unknown values never default to hexagon."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from load_applicable_lessons import load_lessons  # type: ignore[import]  # noqa: E402

LESSONS = {"active_lessons": [
    {"id": "L-any", "category": "structural", "lesson_file": "any.md", "severity": "high"},
    {"id": "L-hex", "category": "structural", "lesson_file": "hex.md", "severity": "high", "applies_when": {"planShape": "hexagon"}},
    {"id": "L-oct", "category": "structural", "lesson_file": "oct.md", "severity": "low", "applies_when": {"planShape": "octagon"}},
    {"id": "L-roof", "category": "structural", "lesson_file": "roof.md", "severity": "low", "applies_when": {"roofType": "hub-and-hip-rafter"}},
    {"id": "L-draw", "category": "drawing", "lesson_file": "draw.md", "severity": "low"},
]}


def _run(tmp_path, design, category="structural"):
    registry, path = tmp_path / "registry.json", tmp_path / "structure.json"
    registry.write_text(json.dumps(LESSONS))
    if design is not None:
        path.write_text(json.dumps(design))
    return [x["id"] for x in load_lessons(category, str(path), str(registry))["lessons"]]


def test_matches_declared_shape_and_roof(tmp_path):
    design = {"layout": {"shape": "octagon"}, "roof": {"type": "hub-and-hip-rafter"}}
    assert _run(tmp_path, design) == ["L-any", "L-oct", "L-roof"]


def test_category_filter(tmp_path):
    assert _run(tmp_path, {"layout": {"shape": "hexagon"}}, category="drawing") == ["L-draw"]


def test_unknown_shape_does_not_default_to_hexagon(tmp_path):
    ids = _run(tmp_path, {"layout": {}, "roof": {}})
    assert "L-hex" not in ids and "L-roof" not in ids and "L-any" in ids


def test_missing_design_loads_only_unconditional_lessons(tmp_path):
    assert _run(tmp_path, None) == ["L-any"]


def test_missing_registry_returns_empty(tmp_path):
    assert load_lessons("structural", str(tmp_path / "x.json"), str(tmp_path / "none.json")) == {"lessons": []}
