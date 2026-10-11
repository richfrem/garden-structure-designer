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
import sys
from pathlib import Path
from typing import Any, Optional

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir
from pipeline_runner import TopologyErrorCode

IMPLEMENTED_FAMILIES = ("RadialHubTopology",)
RESERVED_FAMILIES = ("OrthogonalGridTopology", "HipRidgeTopology")


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
# Sealed-source invariants (Stage 2 fail-closed checks)
# ---------------------------------------------------------------------------

def _failure(code: TopologyErrorCode, message: str) -> dict:
    return {"error_code": code, "error_message": message}


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _check_family(structure: dict) -> Optional[dict]:
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
    return None


def _check_cardinality(structure: dict, layout: dict) -> Optional[dict]:
    post_xy = layout.get("post_xy")
    if not isinstance(post_xy, list):
        return _failure(
            TopologyErrorCode.GEOMETRY_INVALID,
            "geometry.joints.layout.post_xy must be a list.",
        )

    sides = (structure.get("structure") or {}).get("sides")
    if not _is_int(sides):
        return _failure(
            TopologyErrorCode.GEOMETRY_INVALID,
            f"RadialHubTopology requires integer structure.sides, got {sides!r}.",
        )
    if len(post_xy) != sides:
        return _failure(
            TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH,
            f"len(layout.post_xy) ({len(post_xy)}) must equal structure.sides ({sides}).",
        )

    cached_count = layout.get("post_count")
    if cached_count != len(post_xy):
        return _failure(
            TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH,
            f"layout.post_count ({cached_count!r}) drifted from len(layout.post_xy) ({len(post_xy)}).",
        )
    return None


def _check_unique_member_ids(members: list[dict[str, Any]]) -> Optional[dict]:
    seen: set[str] = set()
    for member in members:
        if member["id"] in seen:
            return _failure(
                TopologyErrorCode.DUPLICATE_MEMBER_ID,
                f"Duplicate member id {member['id']!r}.",
            )
        seen.add(member["id"])
    return None


def _check_beam_post_indices(members: list[dict[str, Any]], post_count: int) -> Optional[dict]:
    for member in members:
        if member["type"] != "beam":
            continue
        for key in ("i0", "i1"):
            index = member[key]
            if not _is_int(index) or not 0 <= index < post_count:
                return _failure(
                    TopologyErrorCode.DANGLING_CONNECTION_ENDPOINT,
                    f"Beam {member['id']!r} {key}={index!r} is outside valid post indices [0, {post_count - 1}].",
                )
    return None


def _check_connection_endpoints(
    members: list[dict[str, Any]],
    connections: list[dict[str, Any]],
) -> Optional[dict]:
    member_ids = {m["id"] for m in members}
    for connection in connections:
        for end in ("from", "to"):
            if connection[end] not in member_ids:
                return _failure(
                    TopologyErrorCode.DANGLING_CONNECTION_ENDPOINT,
                    f"Connection {connection['id']!r} {end} endpoint {connection[end]!r} is not a member.",
                )
    return None


def validate_sealed(structure: dict) -> dict:
    """
    Re-derive the topology from sealed geometry and check every Stage 2 invariant.

    Safe for in-process consumers (renderers, exporters) that must not trust a
    previously written topology receipt.  Does not mutate structure.
    Returns {"valid": True, "topology": <topology dict>} on success, or
    {"error_code": TopologyErrorCode, "error_message": str} on failure.
    """
    geometry = structure.get("geometry") or {}
    if geometry.get("_sealed") is not True:
        return _failure(TopologyErrorCode.GEOMETRY_INVALID, "geometry._sealed is not True.")

    failure = _check_family(structure)
    if failure:
        return failure

    joints = geometry.get("joints") or {}
    layout = joints.get("layout") or {}
    failure = _check_cardinality(structure, layout)
    if failure:
        return failure

    try:
        members = _build_members(joints, joints.get("braces") or {})
        failure = _check_unique_member_ids(members) or _check_beam_post_indices(members, len(layout["post_xy"]))
        if failure:
            return failure
        connections = _build_connections(joints, members)
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        return _failure(
            TopologyErrorCode.GEOMETRY_INVALID,
            f"Malformed sealed geometry: {type(exc).__name__}: {exc}",
        )

    failure = _check_connection_endpoints(members, connections)
    if failure:
        return failure

    return {"valid": True, "topology": compile_topology(structure)}


def run_stage(structure: dict, reports_dir: Path, outputs_dir: Path) -> dict:
    """Pipeline Stage 2: validate sealed geometry, then write the topology graph."""
    result = validate_sealed(structure)
    if "error_code" in result:
        return result
    structure["geometry"]["joints"]["topology"] = result["topology"]
    return structure


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

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
