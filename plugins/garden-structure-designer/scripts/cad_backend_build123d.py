#!/usr/bin/env python3
"""
cad_backend_build123d.py
========================
Pure Translator of the JSON Geometry Compiler output into build123d solids.
NO MATH ALLOWED. (Phase 1 Purge)
"""
from __future__ import annotations
import math
import sys
from pathlib import Path
from typing import Any

try:
    import build123d as b3d
    BUILD123D_AVAILABLE = True
except ImportError:
    BUILD123D_AVAILABLE = False

def build_cad_model(structure: dict) -> b3d.Compound | None:
    if not BUILD123D_AVAILABLE: return None
    FT_TO_MM = 304.8
    geom = structure.get("geometry", {})
    resolved = geom.get("joints", {}).get("resolved_model", {})
    if not resolved or not resolved.get("constraints_resolved"): return None
    
    solids = []
    for m in resolved["members"]:
        if m["role"] == "hub":
             # Hub is a special polygonal extrude
             hj = geom["joints"]["hub"]
             hr = hj["radius_ft"] * FT_TO_MM; hh = hj["height_ft"] * FT_TO_MM; az = geom["joints"]["z_planes"]["Z_APEX"] * FT_TO_MM
             with b3d.BuildPart() as p:
                 with b3d.BuildSketch(): b3d.RegularPolygon(radius=hr, side_count=structure["layout"]["post_count"])
                 b3d.extrude(amount=hh, both=True)
             s = p.part.translate((0, 0, az))
             s.label = "HUB"; solids.append(s)
             continue

        # Standard member translation from pre-solved vertices (using p0, p1, and profile)
        # build123d prefers axis-driven box for simple members
        p0 = [x * FT_TO_MM for x in m["p0"]]
        p1 = [x * FT_TO_MM for x in m["p1"]]
        u = b3d.Vector(m["axis_u"])
        w = b3d.Vector(m["axis_w"])
        d = b3d.Vector(m["axis_d"])
        
        length = math.sqrt(sum((p1[i]-p0[i])**2 for i in range(3)))
        # Profile from structure members
        role = m["role"]
        if role == "post": spec = structure["members"]["posts"]
        elif role == "beam": spec = structure["members"]["beams"]
        elif role == "rafter": spec = structure["roof"]["primary_rafters"]
        elif role == "brace": spec = structure["bracing"]["brace"]
        else: continue
        
        width = spec["actual_width_in"] / 12.0 * FT_TO_MM
        depth = spec["actual_depth_in"] / 12.0 * FT_TO_MM
        
        plane = b3d.Plane(origin=p0, x_dir=u, z_dir=d)
        with b3d.BuildPart(plane) as part:
            b3d.Box(length, width, depth, align=(b3d.Align.MIN, b3d.Align.CENTER, b3d.Align.CENTER))
        s = part.part; s.label = m["id"]; solids.append(s)
        
    return b3d.Compound(children=solids)

def export_step(compound: b3d.Compound | None, path: str) -> bool:
    if not BUILD123D_AVAILABLE or compound is None: return False
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        if hasattr(b3d, "export_step"): b3d.export_step(compound, str(path))
        else: compound.export_step(str(path))
        return True
    except Exception: return False

def main():
    if len(sys.argv) < 2: sys.exit(1)
    with open(sys.argv[1]) as f: s = json.load(f)
    model = build_cad_model(s)
    if model: export_step(model, "outputs/model.step")

if __name__ == "__main__": main()
