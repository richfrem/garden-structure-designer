"""
test_topology_compiler.py
=========================
Tests for topology_compiler.py.

Tests:
  1. compile_topology produces correct member counts for standard 6-post hex
  2. compile_topology produces correct connection counts
  3. All post IDs appear in post_top_to_beam_soffit connections
  4. All rafters have rafter_face_to_hub connections
  5. All braces have both foot and head connections
  6. enrich_structure writes topology into geometry.joints.topology
  7. enrich_structure raises ValueError on unsealed geometry
  8. Round-trip: compile → re-compile produces identical output
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from topology_compiler import compile_topology, enrich_structure

# ---------------------------------------------------------------------------
# Minimal sealed structure fixture
# ---------------------------------------------------------------------------

SEALED_STRUCTURE: dict = {
    "layout": {
        "post_count": 6,
        "inscribed_radius_ft": 4.875,
    },
    "geometry": {
        "_sealed": True,
        "hub_radius_ft": 0.75,
        "joints": {
            "z_planes": {"Z_GRADE": 0.0, "Z_POST_TOP": 7.42, "Z_BEAM_TOP": 8.42, "Z_APEX": 10.045},
            "layout": {
                "post_count": 6,
                "post_radius_ft": 4.875,
                "post_xy": [
                    [4.875,  0.0],
                    [2.4375, 4.2219],
                    [-2.4375, 4.2219],
                    [-4.875,  0.0],
                    [-2.4375, -4.2219],
                    [2.4375, -4.2219],
                ],
                "beam_segments": [
                    {"id": "B1", "i0": 0, "i1": 1},
                    {"id": "B2", "i0": 1, "i1": 2},
                    {"id": "B3", "i0": 2, "i1": 3},
                    {"id": "B4", "i0": 3, "i1": 4},
                    {"id": "B5", "i0": 4, "i1": 5},
                    {"id": "B6", "i0": 5, "i1": 0},
                ],
            },
            "hub": {
                "type": "polygonal",
                "face_planes": {
                    "planes": [
                        {"face_id": "H1"}, {"face_id": "H2"}, {"face_id": "H3"},
                        {"face_id": "H4"}, {"face_id": "H5"}, {"face_id": "H6"},
                    ]
                },
            },
            "rafters": {"primary_count": 6},
            "braces": {
                "enabled": True,
                "endpoints": {
                    "pairs": [
                        {"brace_id": "K1A", "post_index": 0, "toward_post_index": 1,
                         "start": [4.76, 0.20, 5.92], "end": [3.88, 1.73, 7.42]},
                        {"brace_id": "K1B", "post_index": 0, "toward_post_index": 5,
                         "start": [4.76, -0.20, 5.92], "end": [3.88, -1.73, 7.42]},
                    ]
                },
            },
        },
    },
}


# ---------------------------------------------------------------------------
# 1 & 2. Member and connection counts
# ---------------------------------------------------------------------------

def test_member_count():
    topology = compile_topology(SEALED_STRUCTURE)
    # 6 posts + 6 beams + 1 hub + 6 rafters + 2 braces = 21
    assert topology["member_count"] == 21
    assert len(topology["members"]) == 21


def test_connection_count():
    topology = compile_topology(SEALED_STRUCTURE)
    # post_to_beam: 6 beams × 2 posts = 12
    # rafter_to_hub: 6
    # brace_foot: 2
    # brace_head: 2
    # total: 22
    assert topology["connection_count"] == 22
    assert len(topology["connections"]) == 22


# ---------------------------------------------------------------------------
# 3. All posts appear in post_top_to_beam_soffit connections
# ---------------------------------------------------------------------------

def test_all_posts_in_beam_connections():
    topology = compile_topology(SEALED_STRUCTURE)
    beam_conns = [c for c in topology["connections"] if c["type"] == "post_top_to_beam_soffit"]
    connected_posts = {c["from"] for c in beam_conns}
    expected_posts = {f"P{i+1}" for i in range(6)}
    assert expected_posts == connected_posts, (
        f"Missing post-to-beam connections for: {expected_posts - connected_posts}"
    )


# ---------------------------------------------------------------------------
# 4. All rafters have rafter_face_to_hub connections
# ---------------------------------------------------------------------------

def test_all_rafters_connect_to_hub():
    topology = compile_topology(SEALED_STRUCTURE)
    hub_conns = [c for c in topology["connections"] if c["type"] == "rafter_face_to_hub"]
    connected_rafters = {c["from"] for c in hub_conns}
    expected_rafters = {f"R{i+1}" for i in range(6)}
    assert expected_rafters == connected_rafters, (
        f"Missing rafter-to-hub connections for: {expected_rafters - connected_rafters}"
    )
    # Each rafter_to_hub connection must reference a hub face
    for c in hub_conns:
        assert "hub_face" in c, f"Connection {c['id']} missing hub_face field"


# ---------------------------------------------------------------------------
# 5. All braces have foot and head connections
# ---------------------------------------------------------------------------

def test_braces_have_foot_and_head_connections():
    topology = compile_topology(SEALED_STRUCTURE)
    brace_ids = {m["id"] for m in topology["members"] if m["type"] == "brace"}
    foot_from = {c["from"] for c in topology["connections"] if c["type"] == "brace_foot_to_post_face"}
    head_from = {c["from"] for c in topology["connections"] if c["type"] == "brace_head_to_beam_soffit"}
    assert brace_ids == foot_from, f"Braces missing foot connections: {brace_ids - foot_from}"
    assert brace_ids == head_from, f"Braces missing head connections: {brace_ids - head_from}"


# ---------------------------------------------------------------------------
# 6. enrich_structure writes topology into geometry.joints.topology
# ---------------------------------------------------------------------------

def test_enrich_structure_writes_topology():
    s = copy.deepcopy(SEALED_STRUCTURE)
    assert "topology" not in s["geometry"]["joints"]
    enrich_structure(s)
    assert "topology" in s["geometry"]["joints"]
    topo = s["geometry"]["joints"]["topology"]
    assert topo["member_count"] > 0
    assert topo["connection_count"] > 0
    assert topo["schema_version"] == "1.0"
    assert topo["generated_by"] == "topology_compiler"


# ---------------------------------------------------------------------------
# 7. enrich_structure raises ValueError on unsealed geometry
# ---------------------------------------------------------------------------

def test_enrich_raises_on_unsealed():
    s = copy.deepcopy(SEALED_STRUCTURE)
    s["geometry"]["_sealed"] = False
    with pytest.raises(ValueError, match="seal geometry"):
        enrich_structure(s)


# ---------------------------------------------------------------------------
# 8. Round-trip: compiling twice produces identical topology
# ---------------------------------------------------------------------------

def test_round_trip_idempotent():
    s = copy.deepcopy(SEALED_STRUCTURE)
    topo1 = compile_topology(s)
    topo2 = compile_topology(s)
    assert topo1 == topo2, "compile_topology is not idempotent — result changed on second call"
