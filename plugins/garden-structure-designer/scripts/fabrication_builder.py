#!/usr/bin/env python3
"""
fabrication_builder.py
======================

Purpose:
    Pure translator of the solved geometry (``geometry.joints.resolved_model``) into the
    fabrication cut list ``outputs/fabrication/cut-list.json`` (schema
    ``garden-structure-designer/fabrication-cut-list/1.0``). NO GEOMETRY SOLVING: stock
    lengths come from the solved member axes and cut angles from the sealed geometry
    block. Replaces the deprecated ``cut_list_engine.py``. Every angle and identity input
    is required; a missing value fails closed instead of falling back to a default.

Layer: Execution / Stage 6 Fabrication

Key Input Dependencies:
    - context/staging/structure.json: geometry.joints.resolved_model (constraints_resolved,
      members with p0/p1/axis_u/axis_w/axis_d/faces), geometry.compound_cut (rafter angles),
      geometry.beam_ring.beam_miter_deg (beam angles), meta.source_hash, meta.revision_id,
      meta.revision_hash
    - geometry_engine.py (vector helpers), path_utils.py, strict_access.py

Key Functions:
    build_cut_list(structure) -> dict
    main() -> None
    _cut_ends(member, role, geom) -> tuple[dict, dict]

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/fabrication_builder.py [structure.json]
"""
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).parent))
from geometry_engine import vlen, vsub
from path_utils import outputs_dir, staging_dir
from strict_access import MissingInputError, require, require_path

SCHEMA = "garden-structure-designer/fabrication-cut-list/1.0"
STOCK_STEP_FT = 2.0  # order lengths round up to the next 2 ft board


def _cut_ends(member: dict, role: str, geom: dict) -> tuple[dict, dict]:
    """Returns the (start, end) cut records for a member; angles are read from the sealed geometry."""
    p0, p1 = tuple(member["p0"]), tuple(member["p1"])
    start_cut = {
        "cut_id": f"{member['id']}-START",
        "end": "start",
        "angles": {"miter_deg": 0.0, "bevel_deg": 0.0},
        "plane": {"point": list(p0), "normal": list(member["faces"][0]["normal"])},
    }
    end_cut = {
        "cut_id": f"{member['id']}-END",
        "end": "end",
        "angles": {"miter_deg": 0.0, "bevel_deg": 0.0},
        "plane": {"point": list(p1), "normal": list(member["faces"][1]["normal"])},
    }
    if role == "rafter_primary":
        compound = require(geom, "compound_cut", "geometry")
        start_cut["type"] = "plumb_cut"
        end_cut["type"] = "compound_miter"
        end_cut["angles"] = {
            "miter_deg": abs(round(require(compound, "miter_deg", "geometry.compound_cut"), 2)),
            "bevel_deg": abs(round(require(compound, "bevel_deg", "geometry.compound_cut"), 2)),
        }
    elif role == "beam":
        beam_miter = abs(round(require(require(geom, "beam_ring", "geometry"), "beam_miter_deg", "geometry.beam_ring"), 2))
        start_cut["type"] = end_cut["type"] = "beam_miter"
        start_cut["angles"] = {"miter_deg": beam_miter, "bevel_deg": 0.0}
        end_cut["angles"] = {"miter_deg": beam_miter, "bevel_deg": 0.0}
    elif role == "brace":
        start_cut["type"] = end_cut["type"] = "brace_miter"
        start_cut["mates_to"], end_cut["mates_to"] = "post", "beam"
    return start_cut, end_cut


def build_cut_list(structure: dict[str, Any]) -> dict[str, Any]:
    """Translates the resolved model into a revision-bound cut list; raises MissingInputError when inputs are absent."""
    geom = require(structure, "geometry", "structure")
    resolved = require_path(structure, "geometry", "joints", "resolved_model")
    if not resolved.get("constraints_resolved"):
        raise MissingInputError("MISSING_INPUT: geometry.joints.resolved_model is not resolved (constraints_resolved is false)")
    meta = require(structure, "meta", "structure")

    members = []
    for member in resolved["members"]:
        role = member["role"]
        # Primary rafters carry R-prefixed ids; any other rafter keeps its role.
        role_mapped = "rafter_primary" if role == "rafter" and member["id"].startswith("R") else role
        p0, p1 = tuple(member["p0"]), tuple(member["p1"])
        length = vlen(vsub(p1, p0))
        start_cut, end_cut = _cut_ends(member, role_mapped, geom)
        members.append({
            "id": member["id"],
            "role": role_mapped,
            "axis": {"start": list(p0), "end": list(p1)},
            "stock": {"cut_length_ft": round(length, 3), "order_length_ft": int(math.ceil(length / STOCK_STEP_FT) * STOCK_STEP_FT)},
            "cuts": [start_cut, end_cut],
        })

    return {
        "schema": SCHEMA,
        "units": "feet",
        "angle_units": "deg",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_hash": require(meta, "source_hash", "meta"),
        "revision_id": require(meta, "revision_id", "meta"),
        "revision_hash": require(meta, "revision_hash", "meta"),
        "members": members,
    }


def main() -> None:
    """CLI entrypoint: reads structure.json (argv[1] or staging default) and writes outputs/fabrication/cut-list.json."""
    struct_path = sys.argv[1] if len(sys.argv) > 1 else str(staging_dir() / "structure.json")
    with open(struct_path, encoding="utf-8") as f:
        structure = json.load(f)
    try:
        out = build_cut_list(structure)
    except MissingInputError as error:
        print(f"fabrication_builder: {error}", file=sys.stderr)
        sys.exit(1)

    fab_base = Path(sys.argv[2]) if len(sys.argv) > 2 else outputs_dir()
    fab_dir = fab_base / "fabrication"
    fab_dir.mkdir(parents=True, exist_ok=True)
    out_file = fab_dir / "cut-list.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"  ✓ {out_file}")


if __name__ == "__main__":
    main()
