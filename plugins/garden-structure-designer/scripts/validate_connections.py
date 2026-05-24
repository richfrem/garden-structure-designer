#!/usr/bin/env python3
"""
validate_connections.py
=======================
Hard pre-render gate: verifies physical surface contact and architectural coherence.
v5.9: Optimized for pure JSON contract validation.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).parent))
try:
    from cad_scene import Scene, Solid, vdot, vcent, vsub, vlen, vnorm, vscl, vcross, vmul, v2_radius
    V3 = tuple[float, float, float]
except ImportError:
    pass

class ContactError(ValueError):
    """Exception raised when physical contact validations fail."""

def assert_connections_physical(scene: Scene) -> None:
    errors = validate_connections(scene)
    if errors:
        raise ContactError(f"PHYSICAL CONTACT VALIDATION FAILED — {len(errors)} error(s):\n" + "\n".join(errors))

def validate_connections(scene: Scene, structure: dict | None = None) -> list[str] | tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    
    # 1. beam_soffit_at_post_top
    for s in scene.solids:
        if s.role == "beam":
            for f in s.faces:
                if f.normal[2] < -0.8:  # bottom face
                    for v in f.verts:
                        if abs(v[2] - scene.Z_POST_TOP) > 0.0104:  # 1/8 inch tolerance
                            errors.append(f"beam_soffit: Beam {s.tag} bottom face is lifted (Z={v[2]:.4f}, expected {scene.Z_POST_TOP:.4f})")
                            break
    
    # 2. rafter_tip_on_hub_face
    has_hub = any(s.role == "hub" for s in scene.solids)
    if has_hub:
        hub_r_face = scene.hub_r * math.cos(math.pi / scene.qty)
        for s in scene.solids:
            if s.role == "rafter" and not s.tag.startswith("Jack") and not s.tag.startswith("J"):
                xy_r = v2_radius(s.p1)
                if abs(xy_r - hub_r_face) > 0.2:
                    errors.append(f"rafter_tip: Rafter {s.tag} apex is disconnected from hub face (radius={xy_r:.4f}, expected {hub_r_face:.4f})")
                    
    # 3. brace_foot_on_post_face
    has_braces = any(s.role == "brace" for s in scene.solids)
    if has_braces:
        for s in scene.solids:
            if s.role == "brace":
                lower_pt = s.p0 if s.p0[2] <= s.p1[2] else s.p1
                nearest_dist = min(
                    math.sqrt((lower_pt[0] - px) ** 2 + (lower_pt[1] - py) ** 2)
                    for px, py in scene.post_xy
                )
                if nearest_dist > 1.0:
                    errors.append(f"brace_foot: Brace {s.tag} lower foot is floating far from post face")

    if structure is not None:
        # If structure is provided, we can add the warnings/checks from the JSON structure
        # (similar to the current v5.9 implementation)
        # 1. seating check
        resolved = structure.get("geometry", {}).get("joints", {}).get("resolved_model")
        if resolved:
            for m in resolved["members"]:
                if m["role"] == "rafter":
                    for f in m["faces"]:
                        if f["normal"][2] < -0.8:
                            avg_z = sum(v[2] for v in [m["vertices"][idx] for idx in f["verts"]]) / len(f["verts"])
                            if abs(avg_z - scene.Z_BEAM_TOP) > 0.1 and abs(avg_z - scene.Z_BEAM_TOP) < 0.2:
                                warnings.append(f"seating: {m['id']} seat at Z={avg_z:.3f} (expected {scene.Z_BEAM_TOP:.3f})")
        # 2. brace foot warning
        if resolved:
            for m in resolved["members"]:
                if m["role"] == "brace":
                    p0 = tuple(m["p0"])
                    d_cl = v2_radius(p0)
                    expected_r = (structure["layout"]["inscribed_radius_ft"] - (5.5/24.0))
                    if abs(d_cl - expected_r) > 0.5:
                        warnings.append(f"brace_foot: {m['id']} foot at {d_cl*12:.1f}\" radius")
        return errors, warnings
        
    return errors

def main():
    if len(sys.argv) < 2: sys.exit(1)
    from cad_scene import build_structure_scene
    with open(sys.argv[1]) as f: structure = json.load(f)
    scene = build_structure_scene(structure, False)
    res = validate_connections(scene, structure)
    if isinstance(res, tuple):
        errors, warnings = res
    else:
        errors, warnings = res, []
    if warnings:
        print(f"VALIDATION WARNINGS — {len(warnings)} issue(s):")
        for w in warnings: print(f"  ⚠ {w}")
    if errors:
        print(f"PHYSICAL CONTACT VALIDATION FAILED — {len(errors)} error(s):")
        for e in errors: print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("PHYSICAL CONTACT VALIDATION PASSED")
        sys.exit(0)

if __name__ == "__main__": main()
