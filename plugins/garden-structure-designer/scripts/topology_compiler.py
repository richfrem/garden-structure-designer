#!/usr/bin/env python3
"""
topology_compiler.py
====================
Post-seal enrichment pass: derives an explicit topology graph from the
sealed geometry data already stored in geometry.joints and writes it to
geometry.joints.topology.

Pipeline position:
    geometry_engine.py  (seals geometry)
        ↓
    topology_compiler.py  (enriches joints with explicit member + connection graph)
        ↓
    constraint_solver.py  (validates connections)
        ↓
    cad_scene.py / render_drawings.py

Why a separate pass (not baked into geometry_engine.py):
  geometry_engine computes and seals scalar dimensions (Z-planes, lengths, angles).
  topology_compiler converts that sealed data into an explicit graph representation.
  Keeping them separate allows topology to be re-derived from sealed geometry
  without re-running the full geometry computation.

Output (written in-place to structure dict and optionally saved to file):
  geometry.joints.topology.members      — flat member list with type + key attributes
  geometry.joints.topology.connections  — flat connection list with from/to/type
"""
from __future__ import annotations

import argparse
import json
from typing import Any


# ---------------------------------------------------------------------------
# Member builders
# ---------------------------------------------------------------------------

def _build_members(joints: dict, bracing: dict) -> list[dict[str, Any]]:
    """Derive flat members list from sealed joints data."""
    members: list[dict[str, Any]] = []

    layout = joints.get("layout", {})
    post_xy_list = layout.get("post_xy", [])
    beam_segments = layout.get("beam_segments", [])

    # Posts — one per post_xy entry
    for i, (x, y) in enumerate(post_xy_list):
        members.append({"id": f"P{i+1}", "type": "post", "xy": [x, y]})

    # Beams — one per beam_segment
    for seg in beam_segments:
        members.append({
            "id":   seg["id"],
            "type": "beam",
            "i0":   seg["i0"],
            "i1":   seg["i1"],
        })

    # Hub
    hub = joints.get("hub", {})
    if hub.get("type") and hub.get("type") != "none":
        members.append({"id": "HUB", "type": "hub", "hub_type": hub.get("type")})

    primary_count = joints.get("rafters", {}).get("primary_count") or 0
    for i in range(primary_count):
        members.append({"id": f"R{i+1}", "type": "rafter", "subtype": "hip"})

    # Braces
    endpoints = bracing.get("endpoints", [])
    if isinstance(endpoints, dict):
        pairs = endpoints.get("pairs", [])
        for pair in pairs:
            members.append({
                "id":           pair["brace_id"],
                "type":         "brace",
                "post_index":   pair["post_index"],
                "toward_index": pair["toward_post_index"],
            })
    elif isinstance(endpoints, list):
        qty = len(post_xy_list)
        for ep in endpoints:
            brace_id = ep["id"]
            # e.g., K1A -> post 0, toward 1; K1B -> post 1, toward 0
            if brace_id.startswith("K") and len(brace_id) >= 3:
                try:
                    p_num = int(brace_id[1:-1]) - 1
                    suffix = brace_id[-1]
                    if suffix == 'A':
                        post_idx = p_num
                        toward_idx = (p_num + 1) % qty
                    else:
                        post_idx = (p_num + 1) % qty
                        toward_idx = p_num
                    members.append({
                        "id":           brace_id,
                        "type":         "brace",
                        "post_index":   post_idx,
                        "toward_index": toward_idx,
                    })
                except ValueError:
                    pass

    return members


def _build_connections(
    joints: dict,
    members: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Derive flat connection list from sealed joints data."""
    connections: list[dict[str, Any]] = []

    # --- Post → Beam (each beam spans two posts) ---
    beam_members = [m for m in members if m["type"] == "beam"]
    for beam in beam_members:
        i0 = beam["i0"]
        i1 = beam["i1"]
        p0_id = f"P{i0 + 1}"
        p1_id = f"P{i1 + 1}"
        connections.append({
            "id":   f"J-{p0_id}-{beam['id']}",
            "type": "post_top_to_beam_soffit",
            "from": p0_id,
            "to":   beam["id"],
        })
        connections.append({
            "id":   f"J-{p1_id}-{beam['id']}",
            "type": "post_top_to_beam_soffit",
            "from": p1_id,
            "to":   beam["id"],
        })

    # --- Rafter → Hub (each hip rafter terminates at a hub face) ---
    hub_face_planes = joints.get("hub", {}).get("face_planes", {}).get("planes", [])
    rafter_members = [m for m in members if m["type"] == "rafter"]
    for i, rafter in enumerate(rafter_members):
        hub_face_id = hub_face_planes[i]["face_id"] if i < len(hub_face_planes) else "HUB"
        connections.append({
            "id":       f"J-{rafter['id']}-HUB",
            "type":     "rafter_face_to_hub",
            "from":     rafter["id"],
            "to":       "HUB",
            "hub_face": hub_face_id,
        })

    # --- Brace → Post (lower foot) and Brace → Beam (upper head) ---
    layout = joints.get("layout", {})
    beam_segments = layout.get("beam_segments", [])
    brace_members = [m for m in members if m["type"] == "brace"]
    for brace in brace_members:
        post_idx   = brace["post_index"]
        toward_idx = brace["toward_index"]
        post_id    = f"P{post_idx + 1}"
        # Find beam that connects post_idx to toward_idx
        beam_id = next(
            (seg["id"] for seg in beam_segments
             if (seg["i0"] == post_idx and seg["i1"] == toward_idx)
             or (seg["i0"] == toward_idx and seg["i1"] == post_idx)),
            None,
        )
        connections.append({
            "id":   f"J-{brace['id']}-{post_id}",
            "type": "brace_foot_to_post_face",
            "from": brace["id"],
            "to":   post_id,
        })
        if beam_id:
            connections.append({
                "id":   f"J-{brace['id']}-{beam_id}",
                "type": "brace_head_to_beam_soffit",
                "from": brace["id"],
                "to":   beam_id,
            })

    return connections


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compile_topology(structure: dict) -> dict:
    """
    Derive and return the topology section dict without mutating structure.
    Caller should write the result to structure["geometry"]["joints"]["topology"].
    """
    joints  = structure.get("geometry", {}).get("joints", {})
    bracing = joints.get("braces", {})

    members     = _build_members(joints, bracing)
    connections = _build_connections(joints, members)

    return {
        "schema_version": "1.0",
        "generated_by":   "topology_compiler",
        "member_count":   len(members),
        "connection_count": len(connections),
        "members":     members,
        "connections": connections,
    }


def enrich_structure(structure: dict) -> None:
    """
    Compile topology and write it into structure["geometry"]["joints"]["topology"].
    Mutates structure in place.  Does NOT set _sealed (caller's responsibility).
    Raises ValueError if geometry is not yet sealed.
    """
    if not structure.get("geometry", {}).get("_sealed"):
        raise ValueError("geometry._sealed is False — seal geometry before enriching topology")
    topology = compile_topology(structure)
    structure.setdefault("geometry", {}).setdefault("joints", {})["topology"] = topology


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Enrich a sealed structure.json with an explicit topology graph."
    )
    parser.add_argument("structure", nargs="?", default=str(staging_dir() / "structure.json"), help="Path to sealed structure.json")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print topology JSON to stdout without writing")
    args = parser.parse_args()

    with open(args.structure, encoding="utf-8") as f:
        structure = json.load(f)

    enrich_structure(structure)
    topology = structure["geometry"]["joints"]["topology"]

    if args.dry_run:
        print(json.dumps(topology, indent=2))
    else:
        with open(args.structure, "w", encoding="utf-8") as f:
            json.dump(structure, f, indent=2)
        m = topology["member_count"]
        c = topology["connection_count"]
        print(f"  topology compiled: {m} members, {c} connections → {args.structure}")


if __name__ == "__main__":
    main()
