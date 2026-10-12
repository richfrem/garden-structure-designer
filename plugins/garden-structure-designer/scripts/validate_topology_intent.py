#!/usr/bin/env python3
"""
validate_topology_intent.py
=====================================

Purpose:
    Stage 0.5 pre-geometry gate. Validates unsealed ``structure.json`` intent
    (topology family, side/post/rafter cardinality, hub type) before any
    geometry math runs. Fails closed with a ``TopologyErrorCode``; for the radial family
    a missing ``hub.type`` or ``roof.primary_rafters.count`` is an error, never a default (spec C1).

Layer: Core

Stage Contract:
    run_stage(structure, reports_dir, outputs_dir) -> dict
    Returns ``structure`` unmodified on success, or
    ``{"error_code": <code>, "error_message": <message>}`` on failure.

Usage:
    python validate_topology_intent.py [structure_path] [--dry-run]

Key Input Dependencies:
    - unsealed structure.json: meta.topology_family, structure.sides, layout.post_count,
      roof.primary_rafters.count, hub.type

Key Functions:
    run_stage(structure, reports_dir, outputs_dir) -> dict
    main(argv=None) -> int
    _failure(code, message) -> dict                     _is_int(value) -> bool
    _validate_radial_hub(structure) -> dict | None      _validate_hub_type(hub_type, sides) -> dict | None
    _validate_orthogonal_grid(structure) -> dict | None
    _validate_grid_posts(layout) -> dict | None         _validate_grid_roof_and_hub(structure) -> dict | None

Script Dependencies:
    pipeline_runner.py (TopologyErrorCode), constants.py (family registry)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

sys.path.append(str(Path(__file__).parent.resolve()))
from constants import IMPLEMENTED_FAMILIES, RESERVED_FAMILIES
from pipeline_runner import TopologyErrorCode

MIN_RADIAL_SIDES = 5
HUB_TYPES = ("hexagonal_prism", "octagonal_prism", "polygonal_cylinder")
HUB_TYPE_SIDES = {"hexagonal_prism": 6, "octagonal_prism": 8}


def _failure(code: TopologyErrorCode, message: str) -> dict:
    """Builds the structured Stage 0.5 failure dict."""
    return {"error_code": code, "error_message": message}


def _is_int(value) -> bool:
    """True for real integers (bools excluded)."""
    return isinstance(value, int) and not isinstance(value, bool)


def _validate_hub_type(hub_type: Any, sides: int) -> Optional[dict]:
    """hub.type is required, must be a known radial type and must agree with the side count."""
    if hub_type not in HUB_TYPES:
        return _failure(
            TopologyErrorCode.HUB_TYPE_MISMATCH,
            f"hub.type {hub_type!r} must be one of {list(HUB_TYPES)}.",
        )
    expected_sides = HUB_TYPE_SIDES.get(hub_type)
    if expected_sides is not None and expected_sides != sides:
        return _failure(
            TopologyErrorCode.HUB_TYPE_MISMATCH,
            f"hub.type {hub_type!r} implies {expected_sides} sides but structure.sides is {sides}.",
        )

    return None


def _validate_radial_hub(structure: dict) -> Optional[dict]:
    """Radial intent: sides >= 5, post_count == sides, primary rafter count == sides, hub type valid for sides."""
    sides = (structure.get("structure") or {}).get("sides")
    if not _is_int(sides) or sides < MIN_RADIAL_SIDES:
        return _failure(
            TopologyErrorCode.GEOMETRY_INVALID,
            f"RadialHubTopology requires integer structure.sides >= {MIN_RADIAL_SIDES}, got {sides!r}.",
        )

    post_count = (structure.get("layout") or {}).get("post_count")
    if post_count != sides:
        return _failure(
            TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH,
            f"layout.post_count ({post_count!r}) must equal structure.sides ({sides}).",
        )

    rafter_count = ((structure.get("roof") or {}).get("primary_rafters") or {}).get("count")
    if rafter_count != sides:
        return _failure(
            TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH,
            f"roof.primary_rafters.count ({rafter_count!r}) must equal structure.sides ({sides}).",
        )

    return _validate_hub_type((structure.get("hub") or {}).get("type"), sides)


def _validate_grid_posts(layout: dict) -> Optional[dict]:
    """Validate post count and grid rows * cols cardinality for orthogonal grid."""
    post_count = layout.get("post_count")
    if not _is_int(post_count) or post_count < 4:
        return _failure(
            TopologyErrorCode.GEOMETRY_INVALID,
            f"OrthogonalGridTopology requires integer layout.post_count >= 4, got {post_count!r}.",
        )

    grid = layout.get("grid")
    if isinstance(grid, dict):
        rows, cols = grid.get("rows"), grid.get("cols")
        if _is_int(rows) and _is_int(cols) and post_count != rows * cols:
            return _failure(
                TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH,
                f"layout.post_count ({post_count}) must equal rows * cols ({rows * cols}).",
            )
    return None


def _validate_grid_roof_and_hub(structure: dict) -> Optional[dict]:
    """Validate hub type ('none' or absent) and positive rafter count for orthogonal grid."""
    hub_type = (structure.get("hub") or {}).get("type")
    if hub_type not in ("none", "", None):
        return _failure(
            TopologyErrorCode.HUB_TYPE_MISMATCH,
            f"OrthogonalGridTopology requires hub.type 'none' or absent, got {hub_type!r}.",
        )

    rafter_count = ((structure.get("roof") or {}).get("primary_rafters") or {}).get("count")
    if not _is_int(rafter_count) or rafter_count <= 0:
        return _failure(
            TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH,
            f"OrthogonalGridTopology requires integer roof.primary_rafters.count > 0, got {rafter_count!r}.",
        )
    return None


def _validate_orthogonal_grid(structure: dict) -> Optional[dict]:
    """Orthogonal grid intent: 4 sides, shape in ('square', 'rectangle'), post_count >= 4, hub type 'none'."""
    struct_block = structure.get("structure") or {}
    sides = struct_block.get("sides")
    if sides != 4:
        return _failure(
            TopologyErrorCode.GEOMETRY_INVALID,
            f"OrthogonalGridTopology requires integer structure.sides == 4, got {sides!r}.",
        )

    shape = struct_block.get("shape")
    if shape not in ("rectangle", "square"):
        return _failure(
            TopologyErrorCode.GEOMETRY_INVALID,
            f"OrthogonalGridTopology requires shape 'rectangle' or 'square', got {shape!r}.",
        )

    err = _validate_grid_posts(structure.get("layout") or {})
    if err is not None:
        return err

    return _validate_grid_roof_and_hub(structure)


def run_stage(structure: dict, reports_dir: Path, outputs_dir: Path) -> dict:
    """Pipeline Stage 0.5: reserved/unknown families and invalid intent fail closed; else returns structure."""
    family = (structure.get("meta") or {}).get("topology_family")

    if family in RESERVED_FAMILIES:
        return _failure(
            TopologyErrorCode.TOPOLOGY_NOT_IMPLEMENTED,
            f"Topology family {family!r} is reserved and not yet implemented.",
        )
    if family not in IMPLEMENTED_FAMILIES:
        return _failure(
            TopologyErrorCode.UNKNOWN_TOPOLOGY_FAMILY,
            f"Unknown meta.topology_family {family!r}.",
        )

    if family == "OrthogonalGridTopology":
        failure = _validate_orthogonal_grid(structure)
    else:
        failure = _validate_radial_hub(structure)

    return failure if failure is not None else structure


def main(argv: Optional[list] = None) -> int:
    """CLI: validate a structure.json intent (read-only) and exit 0/1."""
    parser = argparse.ArgumentParser(description="Stage 0.5 topology intent validator.")
    parser.add_argument("structure_path", nargs="?", default="structure.json")
    parser.add_argument("--dry-run", action="store_true", help="Validate and report only; write nothing.")
    args = parser.parse_args(argv)

    structure_path = Path(args.structure_path)
    structure = json.loads(structure_path.read_text(encoding="utf-8"))
    base_dir = structure_path.parent
    result = run_stage(structure, base_dir / "reports", base_dir / "outputs")

    if "error_code" in result:
        code = result["error_code"]
        code_value = code.value if isinstance(code, TopologyErrorCode) else code
        print(f"FAIL [{code_value}]: {result['error_message']}", file=sys.stderr)
        return 1

    print(f"OK: topology intent valid{' (dry run)' if args.dry_run else ''}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
