#!/usr/bin/env python3
"""
render_drawings.py (CLI)
=====================================
Purpose:
    Pure Translator of the 'DEAD' geometry contract in structure.json.
    NO MATH ALLOWED. (Phase 1 Purge)
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).parent))
from cad_scene import build_structure_scene, validate_scene_geometry, vcent, vdot, vsub, vlen, vnorm

TITLE_BLOCK_W: int = 400
TITLE_BLOCK_H: int = 150

# --- Pure Translation Utilities ---

def project_iso(x: float, y: float, z: float, scale: float, cx: float, cy: float) -> tuple[float, float]:
    """30/30 Isometric Projection (Literal)"""
    iso_x = cx + (x - y) * math.cos(math.radians(30)) * scale
    iso_y = cy + (x + y) * math.sin(math.radians(30)) * scale - z * scale
    return iso_x, iso_y

def project_plan(x: float, y: float, z: float, scale: float, cx: float, cy: float) -> tuple[float, float]:
    return (cx + x * scale, cy + y * scale)

def project_elev(x: float, y: float, z: float, scale: float, cx: float, cy: float) -> tuple[float, float]:
    return (cx + x * scale, cy - z * scale)

def get_label_style(role: str, view: str) -> dict:
    styles = {
        "plan": {"high": 16, "medium": 12, "low": 9},
        "elevation": {"high": 14, "medium": 10, "low": 8},
        "3d": {"high": 12, "medium": 9, "low": 7},
    }
    v_type = "3d" if view in ("isometric", "perspective") else view
    vs = styles.get(v_type, styles["plan"])
    if role in ("post", "beam", "hub"): return {"size": vs["high"], "weight": "bold", "opacity": 1.0}
    if role == "rafter": return {"size": vs["medium"], "weight": "normal", "opacity": 0.9}
    return {"size": vs["low"], "weight": "normal", "opacity": 0.75}

# --- Core Page Renderers (Pure Translation) ---

def render_generic_view(structure: dict, filename: str, proj_func, view_type: str) -> list[str]:
    svg_list = []
    is_blueprint = "blueprint" in filename
    palette = _get_palette(structure, is_blueprint)
    coords = structure["geometry"]["svg_coordinates"]
    scene = build_structure_scene(structure, is_blueprint=is_blueprint)
    
    # Projection parameters from coords
    scale = coords["scale_px_per_ft"]
    cx, cy = coords["width_px"] / 2, coords["grade_y"] if "elevation" in view_type else coords["height_px"] / 2
    
    # Backface Culling Vector
    cam = (0,0,1) if "plan" in view_type else (0,-1,0) if "elevation" in view_type else (1,1,1)
    cam = vnorm(cam)
    
    face_entries = []
    for solid in scene.solids:
        # Presentation view filtering
        if "perspective" in filename or "drawing" in filename and "plan" not in filename:
             if solid.role == "purlin" or (solid.role == "rafter" and (solid.tag.startswith("Jack") or solid.tag.startswith("J"))): continue
        
        for face in solid.faces:
            if vdot(face.normal, cam) < -0.1: continue # Standard backface cull
            # Depth sorting
            c = vcent(face.verts)
            depth = vdot(c, cam)
            # Minimal role bias for Z-fighting
            bias = {"hub":0.05, "rafter":0.04, "beam":0.03, "brace":0.02, "post":0.01}.get(solid.role, 0)
            face_entries.append((depth + bias, face, solid))
            
    face_entries.sort(key=lambda t: t[0])
    
    for _, face, solid in face_entries:
        pts2d = [proj_func(v[0], v[1], v[2], scale, cx, cy) for v in face.verts]
        pts_str = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts2d)
        svg_list.append(f'    <polygon data-role="{face.role}" data-id="{face.tag}" points="{pts_str}" fill="{face.color}" stroke="{palette["outline"]}" stroke-width="1.2" />')

    # Annotations pass (Deduplicated)
    rendered_ids = set()
    label_svgs = []
    for solid in scene.solids:
        if solid.tag in rendered_ids: continue
        style = get_label_style(solid.role, view_type)
        mid = vcent([solid.p0, solid.p1])
        lx, ly = proj_func(mid[0], mid[1], mid[2], scale, cx, cy)
        # Apply simple role-based offset (dead logic)
        if solid.role == "beam": ly -= 15
        elif solid.role == "post": lx += 15
        elif solid.role == "hub": ly -= 20
        
        label_svgs.append(f'    <text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="{style["size"]}" font-weight="{style["weight"]}" fill="{palette["text"]}" opacity="{style["opacity"]}" data-label="{solid.tag}">{solid.tag}</text>')
        rendered_ids.add(solid.tag)
        
    svg_list.append('  <g id="annotation-labels-layer">')
    svg_list.extend(label_svgs)
    svg_list.append('  </g>')
    return svg_list

def _get_palette(s: dict, bp: bool) -> dict:
    p = {"post":"#1b365d","beam":"#162e50","rafter":"#1f3e6a","brace":"#1b365d","footing":"#11223a","outline":"#ffffff","text":"#00ffff"} if bp else {"post":"#f4ebd0","beam":"#e6ccb2","rafter":"#ddb892","brace":"#ede0d4","footing":"#e5e5e5","outline":"#2b2d42","text":"#1d3557"}
    return p

def generate_svg(filename: str, structure: dict, output_path: str) -> None:
    coords = structure["geometry"]["svg_coordinates"]
    w, h = coords["width_px"], coords["height_px"]
    header = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">', f'  <rect width="100%" height="100%" fill="{"#12253a" if "blueprint" in filename else "#ffffff"}" />']
    
    if "plan" in filename: content = render_generic_view(structure, filename, project_plan, "plan")
    elif "elevation" in filename: content = render_generic_view(structure, filename, project_elev, "elevation")
    else: content = render_generic_view(structure, filename, project_iso, "isometric")
    
    with open(output_path, "w") as f: f.write("\n".join(header + content + ["</svg>"]))

def main():
    if len(sys.argv) < 2: sys.exit(1)
    with open(sys.argv[1]) as f: s = json.load(f)
    out_dir = Path("outputs")
    for f in ["drawing-plan-view.svg", "drawing-elevation-view.svg", "drawing-isometric-view.svg", "blueprint-plan.svg", "blueprint-elevation.svg", "blueprint-isometric.svg"]:
        generate_svg(f, s, out_dir / f)
        print(f"  ✓ {f}")

if __name__ == "__main__": main()
