#!/usr/bin/env python3
"""
load_applicable_lessons.py
==========================

Purpose:
    Self-evolution support: lists the active lessons of a category (structural, drawing, ...) from
    the learning registry whose applies_when conditions (planShape, roofType) match the current
    design. Shape and roof come only from the design's own declaration; an undeclared value never
    defaults to "hexagon"/"hub-and-hip-rafter", it simply fails to match conditional lessons.

Layer: Execution / Learning Loop

Key Input Dependencies:
    - context/staging/learning-registry.json (active_lessons)
    - context/staging/structure.json (layout.shape / planShape, roof.type / roofType)
    - path_utils.py

Key Functions:
    load_lessons(category, design_path, registry_path) -> dict
    _design_context(design_path) -> tuple[str | None, str | None]
    _applies(lesson, shape, roof) -> bool

Usage Examples:
    python3 load_applicable_lessons.py --category structural [--design structure.json] [--registry registry.json]
"""
import json
import os
import sys
from pathlib import Path
from typing import Optional
sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir

def _design_context(design_path: str) -> tuple[Optional[str], Optional[str]]:
    """(plan shape, roof type) declared by the design; None when the design does not declare them."""
    if not os.path.exists(design_path):
        return None, None
    with open(design_path) as f:
        design = json.load(f)
    shape = (design.get("layout") or {}).get("shape") or design.get("planShape")
    roof = (design.get("roof") or {}).get("type") or design.get("roofType")
    return shape, roof


def _applies(lesson: dict, shape: Optional[str], roof: Optional[str]) -> bool:
    """A lesson applies when each of its conditions equals the design's declared value (unknown never matches)."""
    conditions = lesson.get("applies_when", {})
    if "planShape" in conditions and conditions["planShape"] != shape:
        return False
    return not ("roofType" in conditions and conditions["roofType"] != roof)


def load_lessons(category: str, design_path: str, registry_path: str) -> dict:
    """Returns the active lessons of ``category`` whose applies_when conditions match the design."""
    if not os.path.exists(registry_path):
        return {"lessons": []}

    with open(registry_path) as f:
        registry = json.load(f)

    shape, roof = _design_context(design_path)
    return {
        "lessons": [
            {"id": lesson["id"], "file": lesson["lesson_file"], "severity": lesson["severity"]}
            for lesson in registry.get("active_lessons", [])
            if lesson.get("category") == category and _applies(lesson, shape, roof)
        ]
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default="structural")
    parser.add_argument("--design", default=str(staging_dir() / "structure.json"))
    parser.add_argument("--registry", default=str(staging_dir() / "learning-registry.json"))
    args = parser.parse_args()
    
    result = load_lessons(args.category, args.design, args.registry)
    print(json.dumps(result, indent=2))
