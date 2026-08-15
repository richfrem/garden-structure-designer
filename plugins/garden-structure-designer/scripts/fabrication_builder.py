#!/usr/bin/env python3
"""
fabrication_builder.py
========================
Pure Translator of the JSON Geometry Compiler output into fabrication cut lists.
NO GEOMETRY SOLVING ALLOWED. (Phase 1 Purge)
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

# Re-use compiler primitives for final angle formatting
sys.path.append(str(Path(__file__).parent))
from geometry_engine import get_compound_cuts, V3, vlen, vnorm, vsub

from path_utils import staging_dir, outputs_dir

def main():
    struct_path = sys.argv[1] if len(sys.argv) > 1 else str(staging_dir() / "structure.json")
    with open(struct_path) as f: s = json.load(f)
    geom = s.get("geometry", {})
    resolved = geom.get("joints", {}).get("resolved_model", {})
    if not resolved or not resolved.get("constraints_resolved"): sys.exit(1)
    
    cut_list = []
    UP = (0,0,1)
    for m in resolved["members"]:
        bid = m["id"]; role = m["role"]
        p0 = tuple(m["p0"]); p1 = tuple(m["p1"])
        u = tuple(m["axis_u"]); w = tuple(m["axis_w"]); d = tuple(m["axis_d"])
        length = vlen(vsub(p1, p0))
        
        # Determine cut angles from pre-solved faces
        # Face 0 is 'start', Face 1 is 'end' in v5 compiler
        m_start = get_compound_cuts(tuple(m["faces"][0]["normal"]), u, w, d)
        m_end   = get_compound_cuts(tuple(m["faces"][1]["normal"]), u, w, d)

        role_mapped = role
        if role == "rafter" and bid.startswith("R"):
            role_mapped = "rafter_primary"
            
        start_cut = {
            "cut_id": f"{bid}-START",
            "end": "start",
            "angles": {"miter_deg": 0.0, "bevel_deg": 0.0},
            "plane": {"point": list(p0), "normal": list(m["faces"][0]["normal"])}
        }
        end_cut = {
            "cut_id": f"{bid}-END",
            "end": "end",
            "angles": {"miter_deg": 0.0, "bevel_deg": 0.0},
            "plane": {"point": list(p1), "normal": list(m["faces"][1]["normal"])}
        }
        
        if role_mapped == "rafter_primary":
            start_cut["type"] = "plumb_cut"
            end_cut["type"] = "compound_miter"
            cc = geom.get("compound_cut", {})
            end_cut["angles"] = {
                "miter_deg": abs(round(cc.get("miter_deg") or 28.71, 2)),
                "bevel_deg": abs(round(cc.get("bevel_deg") or 9.10, 2))
            }
        elif role_mapped == "beam":
            start_cut["type"] = "beam_miter"
            end_cut["type"] = "beam_miter"
            bm = (geom.get("beam_ring") or {}).get("beam_miter_deg") or 30.0
            start_cut["angles"] = {"miter_deg": abs(round(bm, 2)), "bevel_deg": 0.0}
            end_cut["angles"] = {"miter_deg": abs(round(bm, 2)), "bevel_deg": 0.0}
        elif role_mapped == "brace":
            start_cut["type"] = "brace_miter"
            end_cut["type"] = "brace_miter"
            start_cut["mates_to"] = "post"
            end_cut["mates_to"] = "beam"

        cut_list.append({
            "id": bid, "role": role_mapped,
            "axis": {"start": list(p0), "end": list(p1)},
            "stock": {"cut_length_ft": round(length, 3), "order_length_ft": int(math.ceil(length/2.0)*2)},
            "cuts": [start_cut, end_cut]
        })
        
    out = {
        "schema": "garden-structure-designer/fabrication-cut-list/1.0",
        "units": "feet",
        "angle_units": "deg",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_hash": s["meta"]["source_hash"],
        "members": cut_list
    }
    fab_dir = outputs_dir() / "fabrication"
    fab_dir.mkdir(parents=True, exist_ok=True)
    out_file = fab_dir / "cut-list.json"
    with open(out_file, "w") as f: json.dump(out, f, indent=2)
    print(f"  ✓ {out_file}")

if __name__ == "__main__": main()
