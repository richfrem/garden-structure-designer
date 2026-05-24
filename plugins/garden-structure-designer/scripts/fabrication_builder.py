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

def main():
    if len(sys.argv) < 2: sys.exit(1)
    with open(sys.argv[1]) as f: s = json.load(f)
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
        
        cut_list.append({
            "id": bid, "role": role,
            "axis": {"start": list(p0), "end": list(p1)},
            "stock": {"cut_length_ft": round(length, 3), "order_length_ft": int(math.ceil(length/2.0)*2)},
            "cuts": [
                {"cut_id": f"{bid}-START", "angles": {"miter_deg": abs(round(m_start[0],2)), "bevel_deg": abs(round(m_start[1],2))}},
                {"cut_id": f"{bid}-END",   "angles": {"miter_deg": abs(round(m_end[0],2)),   "bevel_deg": abs(round(m_end[1],2))}}
            ]
        })
        
    out = {
        "schema": "garden-structure-designer/fabrication-cut-list/1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_hash": s["meta"]["source_hash"],
        "members": cut_list
    }
    Path("outputs/fabrication").mkdir(parents=True, exist_ok=True)
    with open("outputs/fabrication/cut-list.json", "w") as f: json.dump(out, f, indent=2)
    print("  ✓ outputs/fabrication/cut-list.json")

if __name__ == "__main__": main()
