#!/usr/bin/env python3
"""
topology_compiler.py
====================

Purpose:
    Stage 2. Post-seal enrichment pass: derives an explicit topology graph from the
    sealed geometry data already stored in geometry.joints and writes it to
    geometry.joints.topology, failing closed on every spec C2 invariant.

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

Stage 2 contract (spec C2): actual solved arrays are compared with the declared intent;
cached count scalars (e.g. rafters.primary_count) are never an authority. For
RadialHubTopology with N = structure.sides it requires N finite, distinct, regularly spaced
posts, N beams, N primary rafters (geometry.joints.primary_rafters, mirrored exactly at
rafters.primary_rafters), N hub face planes (ids H1..HN, one per rafter) and 2N braces when
bracing is enabled (0 otherwise). Typed attachments and footings are not yet validated.

Key Input Dependencies:
  - sealed structure.json (geometry._sealed == True, meta.topology_family, structure.sides)
  - geometry.joints.layout / primary_rafters / hub.face_planes / braces
  - constants.py (POLYGON_* tolerances), pipeline_runner.py (TopologyErrorCode), path_utils.py

Key Functions:
  run_stage(structure, reports_dir, outputs_dir) -> dict      Pipeline Stage 2
  validate_sealed(structure) -> dict                          every Stage 2 invariant, no mutation
  compile_topology(structure) -> dict                         derive the graph (no validation)
  enrich_structure(structure) -> None                         validate then write the graph in place
  main() -> None                                              CLI
  _build_members(joints, bracing) -> list[dict]               _build_connections(joints, members) -> list[dict]
  _failure(code, message) -> dict                             _is_int(value) -> bool
  _check_family / _check_cardinality / _check_polygon / _check_rafter_mirror
  _check_unique_member_ids / _check_beam_post_indices / _check_member_counts
  _build_brace_members(endpoints, qty) -> list[dict]       _validate_graph(joints, layout) -> dict | None
  _check_rafter_faces / _check_connection_endpoints
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Optional

sys.path.append(str(Path(__file__).parent.resolve()))
from constants import POLYGON_ANGLE_TOL_RAD, POLYGON_RADIUS_TOL_FT
from path_utils import staging_dir
from pipeline_runner import TopologyErrorCode

IMPLEMENTED_FAMILIES = ("RadialHubTopology",)
RESERVED_FAMILIES = ("OrthogonalGridTopology", "HipRidgeTopology")


# ---------------------------------------------------------------------------
# Member builders
# ---------------------------------------------------------------------------

def _build_brace_members(endpoints: Any, qty: int) -> list[dict[str, Any]]:
    """Brace members from either the pairs form (dict) or the legacy K<i><A|B> id list form."""
    members: list[dict[str, Any]] = []
    if isinstance(endpoints, dict):
        for pair in endpoints.get("pairs", []):
            members.append({
                "id":           pair["brace_id"],
                "type":         "brace",
                "post_index":   pair["post_index"],
                "toward_index": pair["toward_post_index"],
            })
    elif isinstance(endpoints, list):
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

    # Rafters come from the canonical solved array, never from a cached count scalar (C2).
    for rafter in joints.get("primary_rafters") or []:
        members.append({"id": rafter["id"], "type": "rafter", "subtype": "hip"})

    members.extend(_build_brace_members(bracing.get("endpoints", []), len(post_xy_list)))

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
        hub_face_id = hub_face_planes[i]["id"] if i < len(hub_face_planes) else None
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
    result = validate_sealed(structure)
    if "error_code" in result:
        raise ValueError(f"{TopologyErrorCode(result['error_code']).value}: {result['error_message']}")
    structure.setdefault("geometry", {}).setdefault("joints", {})["topology"] = result["topology"]


# ---------------------------------------------------------------------------
# Sealed-source invariants (Stage 2 fail-closed checks)
# ---------------------------------------------------------------------------

def _failure(code: TopologyErrorCode, message: str) -> dict:
    """Builds the structured Stage 2 failure dict (error_code + error_message)."""
    return {"error_code": code, "error_message": message}


def _is_int(value: Any) -> bool:
    """True for real integers (bools excluded)."""
    return isinstance(value, int) and not isinstance(value, bool)


def _check_family(structure: dict) -> Optional[dict]:
    """Rejects reserved (TOPOLOGY_NOT_IMPLEMENTED) and unknown (UNKNOWN_TOPOLOGY_FAMILY) families."""
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
    """post_xy length, structure.sides and the cached layout.post_count must agree (arrays beat scalars)."""
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
    """DUPLICATE_MEMBER_ID when two members share an id."""
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
    """Every beam end must index an existing post (DANGLING_CONNECTION_ENDPOINT otherwise)."""
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
    """Every connection from/to must name an existing member."""
    member_ids = {m["id"] for m in members}
    for connection in connections:
        for end in ("from", "to"):
            if connection[end] not in member_ids:
                return _failure(
                    TopologyErrorCode.DANGLING_CONNECTION_ENDPOINT,
                    f"Connection {connection['id']!r} {end} endpoint {connection[end]!r} is not a member.",
                )
    return None


def _check_polygon(post_xy: list) -> Optional[dict]:
    """Posts must be finite, distinct, equally distant from the centroid and equally spaced counter-clockwise."""
    try:
        points = [(float(x), float(y)) for x, y in post_xy]
    except (TypeError, ValueError):
        return _failure(TopologyErrorCode.GEOMETRY_INVALID, "layout.post_xy entries must be [x, y] numbers.")
    if not all(math.isfinite(c) for p in points for c in p):
        return _failure(TopologyErrorCode.GEOMETRY_INVALID, "layout.post_xy contains a non-finite coordinate.")
    count = len(points)
    cx, cy = sum(p[0] for p in points) / count, sum(p[1] for p in points) / count
    radii = [math.hypot(x - cx, y - cy) for x, y in points]
    if max(radii) - min(radii) > POLYGON_RADIUS_TOL_FT or min(radii) <= POLYGON_RADIUS_TOL_FT:
        return _failure(TopologyErrorCode.GEOMETRY_INVALID, f"Posts are not equidistant from the centre (radii {min(radii):.4f}..{max(radii):.4f} ft).")
    step = 2 * math.pi / count
    angles = [math.atan2(y - cy, x - cx) for x, y in points]
    for i in range(count):
        gap = (angles[(i + 1) % count] - angles[i]) % (2 * math.pi)
        if abs(gap - step) > POLYGON_ANGLE_TOL_RAD:
            return _failure(TopologyErrorCode.GEOMETRY_INVALID, f"Posts P{i + 1}->P{(i + 1) % count + 1} are not regularly spaced counter-clockwise (gap {gap:.4f} rad, expected {step:.4f}).")
    return None


def _check_rafter_mirror(joints: dict) -> Optional[dict]:
    """The compatibility mirror rafters.primary_rafters, when present, must equal the canonical array exactly."""
    mirror = (joints.get("rafters") or {}).get("primary_rafters")
    if mirror is not None and mirror != joints.get("primary_rafters"):
        return _failure(TopologyErrorCode.GEOMETRY_INVALID, "rafters.primary_rafters differs from the canonical primary_rafters array.")
    return None


def _check_member_counts(sides: int, joints: dict, members: list[dict[str, Any]]) -> Optional[dict]:
    """Beams and primary rafters must each number N; braces 2N when enabled, otherwise none."""
    braces_enabled = bool((joints.get("braces") or {}).get("enabled"))
    expected = {"beam": sides, "rafter": sides, "brace": 2 * sides if braces_enabled else 0}
    for kind, want in expected.items():
        have = sum(1 for m in members if m["type"] == kind)
        if have != want:
            return _failure(
                TopologyErrorCode.TOPOLOGY_CARDINALITY_MISMATCH,
                f"Expected {want} {kind} member(s) for {sides} sides, found {have}.",
            )
    return None


def _check_rafter_faces(joints: dict, members: list[dict[str, Any]]) -> Optional[dict]:
    """Rafter Ri must land on hub face Hi: the face plane has to exist (no implicit fallback)."""
    if not any(m["type"] == "rafter" for m in members):
        return None
    planes = ((joints.get("hub") or {}).get("face_planes") or {}).get("planes") or []
    face_ids = {plane.get("id") for plane in planes}
    for member in (m for m in members if m["type"] == "rafter"):
        face = "H" + member["id"].lstrip("R")
        if face not in face_ids:
            return _failure(
                TopologyErrorCode.DANGLING_CONNECTION_ENDPOINT,
                f"Rafter {member['id']!r} has no hub face plane {face!r}.",
            )
    return None


def _validate_graph(joints: dict, layout: dict) -> Optional[dict]:
    """Builds members and connections from the solved arrays and checks ids, indices, counts and endpoints."""
    try:
        members = _build_members(joints, joints.get("braces") or {})
        failure = (
            _check_unique_member_ids(members)
            or _check_beam_post_indices(members, len(layout["post_xy"]))
            or _check_member_counts(len(layout["post_xy"]), joints, members)
            or _check_rafter_faces(joints, members)
        )
        if failure:
            return failure
        connections = _build_connections(joints, members)
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        return _failure(
            TopologyErrorCode.GEOMETRY_INVALID,
            f"Malformed sealed geometry: {type(exc).__name__}: {exc}",
        )
    return _check_connection_endpoints(members, connections)


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

    joints = geometry.get("joints") or {}
    layout = joints.get("layout") or {}
    failure = _check_family(structure)
    failure = failure or _check_cardinality(structure, layout)
    failure = failure or _check_polygon(layout["post_xy"]) or _check_rafter_mirror(joints)
    failure = failure or _validate_graph(joints, layout)
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
    """CLI: validate a sealed structure.json and write its topology graph (direct write; see review finding F-11)."""
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
