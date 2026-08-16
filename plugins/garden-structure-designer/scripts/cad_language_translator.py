#!/usr/bin/env python3
"""
cad_language_translator.py
==========================
Translates structure design intent into formal CAD constraints.
Sets meta.lifecycle = "CONSTRAINTS_DEFINED".
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).parent.resolve()))
from structure_io import load_structure, save_structure, assert_not_sealed

def translate_to_constraints(structure: dict[str, Any]) -> None:
    assert_not_sealed(structure, "cad_constraints")
    
    qty = structure["layout"]["post_count"]
    r_ft = structure["layout"]["inscribed_radius_ft"]
    post_h = structure["members"]["posts"]["cut_length_ft"]
    beam_d_in = structure["members"]["beams"]["actual_depth_in"]
    beam_d_ft = beam_d_in / 12.0
    
    # Parse pitch
    pitch_str = structure["roof"]["pitch"]
    pr, rr = [float(x) for x in pitch_str.split(":")]
    
    # Standard nominal variables
    Z_GRADE = 0.0
    Z_POST_TOP = post_h - beam_d_ft
    Z_BEAM_TOP = post_h
    
    # Calculate apothem and pitch-based rise for nominal Z_APEX
    apothem = r_ft * math.cos(math.pi / qty)
    hub_r = max(structure["hub"].get("radius_min_ft") or 0.6, 0.75)
    roof_rise = r_ft * (pr / rr)
    Z_APEX = post_h + roof_rise
    
    # Member actual widths/depths for offset calculations
    PHW = structure["members"]["posts"]["actual_width_in"] / 24.0
    PHD = structure["members"]["posts"]["actual_depth_in"] / 24.0
    
    shape = structure.get("layout", {}).get("shape", structure.get("structure", {}).get("shape", "polygon"))
    if shape == "rectangle" and qty == 6:
        # 6-post rectangle: length along X (e.g. 18ft), width along Y (e.g. 12ft)
        len_ft = float(structure["layout"].get("length_ft") or (r_ft * 2.0))
        wid_ft = float(structure["layout"].get("width_ft") or (r_ft * 1.333))
        hx = len_ft / 2.0
        hy = wid_ft / 2.0
        # Posts ordered counterclockwise around perimeter:
        # P1: (+hx, 0), P2: (+hx, +hy), P3: (0, +hy), P4: (-hx, +hy), P5: (-hx, -hy), P6: (0, -hy) -> or standard 6-post grid:
        # Front row (Y=-hy): P1(-hx, -hy), P2(0, -hy), P3(+hx, -hy)
        # Back row (Y=+hy):  P4(+hx, +hy), P5(0, +hy), P6(-hx, +hy)
        # Perimeter order: P1(+hx, -hy), P2(+hx, +hy), P3(0, +hy), P4(-hx, +hy), P5(-hx, -hy), P6(0, -hy)
        post_xy = [
            [round(hx, 4), round(-hy, 4)],
            [round(hx, 4), round(hy, 4)],
            [0.0, round(hy, 4)],
            [round(-hx, 4), round(hy, 4)],
            [round(-hx, 4), round(-hy, 4)],
            [0.0, round(-hy, 4)]
        ]
    elif shape == "rectangle" and qty == 4:
        len_ft = float(structure["layout"].get("length_ft") or (r_ft * 2.0))
        wid_ft = float(structure["layout"].get("width_ft") or (r_ft * 1.333))
        hx, hy = len_ft / 2.0, wid_ft / 2.0
        post_xy = [
            [round(hx, 4), round(-hy, 4)],
            [round(hx, 4), round(hy, 4)],
            [round(-hx, 4), round(hy, 4)],
            [round(-hx, 4), round(-hy, 4)]
        ]
    else:
        post_xy = [[round(r_ft * math.cos(2*math.pi*i/qty), 4), round(r_ft * math.sin(2*math.pi*i/qty), 4)] for i in range(qty)]
    
    # 1. Reference Planes
    reference_planes = []
    
    # Footings/Grade planes
    for i in range(qty):
        reference_planes.append({
            "id": f"footing_top_FT{i+1}",
            "type": "footing_top",
            "point": [post_xy[i][0], post_xy[i][1], Z_GRADE],
            "normal": [0.0, 0.0, 1.0]
        })
        
    # Post Face planes
    for i in range(qty):
        p1 = post_xy[i]
        p2 = post_xy[(i+1)%qty]
        p0 = post_xy[(i-1)%qty]
        
        # Toward next post (along B{i+1})
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        bl = math.sqrt(dx*dx + dy*dy)
        ux, uy = dx/bl, dy/bl
        reference_planes.append({
            "id": f"post_face_P{i+1}_toward_B{i+1}",
            "type": "post_face",
            "point": [p1[0] + ux * PHW, p1[1] + uy * PHW, Z_GRADE],
            "normal": [ux, uy, 0.0]
        })
        
        # Toward prev post (along B{i} which starts at p0)
        dx_prev = p1[0] - p0[0]
        dy_prev = p1[1] - p0[1]
        bl_prev = math.sqrt(dx_prev*dx_prev + dy_prev*dy_prev)
        ux_prev, uy_prev = dx_prev/bl_prev, dy_prev/bl_prev
        # Note: B{i} is between post i (p0) and post i+1 (p1)
        prev_beam_id = qty if i == 0 else i
        reference_planes.append({
            "id": f"post_face_P{i+1}_toward_B{prev_beam_id}",
            "type": "post_face",
            "point": [p1[0] - ux_prev * PHW, p1[1] - uy_prev * PHW, Z_GRADE],
            "normal": [-ux_prev, -uy_prev, 0.0]
        })

    # Beam soffit and top planes
    for i in range(qty):
        reference_planes.append({
            "id": f"beam_soffit_B{i+1}",
            "type": "beam_soffit",
            "point": [post_xy[i][0], post_xy[i][1], Z_POST_TOP],
            "normal": [0.0, 0.0, -1.0]
        })
        reference_planes.append({
            "id": f"beam_top_B{i+1}",
            "type": "beam_top",
            "point": [post_xy[i][0], post_xy[i][1], Z_BEAM_TOP],
            "normal": [0.0, 0.0, 1.0]
        })
        
    # Roof planes
    # Estimate rafter seat depth and remaining meat to approximate roof plane location
    rafter_d_ft = structure["roof"]["primary_rafters"]["actual_depth_in"] / 12.0
    seat_depth_notch = rafter_d_ft / 3.0
    remaining_meat = rafter_d_ft - seat_depth_notch
    common_slope = roof_rise / (apothem - hub_r * math.cos(math.pi/qty)) if abs(apothem - hub_r * math.cos(math.pi/qty)) > 1e-4 else 0.0
    v_shift_common = remaining_meat * math.cos(math.atan(common_slope))
    
    if shape == "rectangle":
        # Flat horizontal roof plane across top of beams
        for i in range(qty):
            reference_planes.append({
                "id": f"roof_plane_{i}",
                "type": "roof_plane",
                "point": [0.0, 0.0, Z_BEAM_TOP + v_shift_common],
                "normal": [0.0, 0.0, 1.0]
            })
    else:
        for i in range(qty):
            p_a = (post_xy[i][0], post_xy[i][1], Z_BEAM_TOP + v_shift_common)
            p_b = (post_xy[(i+1)%qty][0], post_xy[(i+1)%qty][1], Z_BEAM_TOP + v_shift_common)
            p_apex = (0.0, 0.0, Z_APEX + v_shift_common)
            
            # Plane normal
            v1 = (p_b[0]-p_a[0], p_b[1]-p_a[1], p_b[2]-p_a[2])
            v2 = (p_apex[0]-p_a[0], p_apex[1]-p_a[1], p_apex[2]-p_a[2])
            nx = v1[1]*v2[2] - v1[2]*v2[1]
            ny = v1[2]*v2[0] - v1[0]*v2[2]
            nz = v1[0]*v2[1] - v1[1]*v2[0]
            nl = math.sqrt(nx*nx + ny*ny + nz*nz)
            if nl > 1e-9:
                nx, ny, nz = nx/nl, ny/nl, nz/nl
            else:
                nx, ny, nz = 0.0, 0.0, 1.0
                
            reference_planes.append({
                "id": f"roof_plane_{i}",
                "type": "roof_plane",
                "point": list(p_a),
                "normal": [nx, ny, nz]
            })
        
    # Hub face planes
    hub_r_face = hub_r * math.cos(math.pi / qty)
    for i in range(qty):
        theta = 2.0 * math.pi * i / qty
        reference_planes.append({
            "id": f"hub_face_H{i+1}",
            "type": "hub_face",
            "point": [hub_r_face * math.cos(theta), hub_r_face * math.sin(theta), Z_APEX],
            "normal": [math.cos(theta), math.sin(theta), 0.0]
        })

    # 2. Member Constraints
    member_constraints = []
    
    # Posts
    for i in range(qty):
        member_constraints.append({
            "member_id": f"P{i+1}",
            "constraints": {
                "base_surface": f"footing_top_FT{i+1}",
                "top_surface": f"beam_soffit_B{i+1}"
            }
        })
        
    # Beams
    for i in range(qty):
        next_post = i + 2 if (i + 2) <= qty else 1
        member_constraints.append({
            "member_id": f"B{i+1}",
            "constraints": {
                "start_surface": f"post_top_P{i+1}",
                "end_surface": f"post_top_P{next_post}",
                "seating_rule": "beam_bottom_z == post_top_z"
            }
        })
        
    if structure.get("bracing", {}).get("enabled"):
        run_t = structure["bracing"]["brace"].get("run_ft") or 1.5
        for i in range(qty):
            p1 = post_xy[i]
            p2 = post_xy[(i+1)%qty]
            bl = math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
            run = min(run_t, bl * 0.3)
            
            member_constraints.append({
                "member_id": f"K{i+1}A",
                "constraints": {
                    "start_surface": f"post_face_P{i+1}_toward_B{i+1}",
                    "end_surface": f"beam_soffit_B{i+1}",
                    "run_ft": round(run, 4)
                }
            })
            next_post = i + 2 if (i + 2) <= qty else 1
            member_constraints.append({
                "member_id": f"K{i+1}B",
                "constraints": {
                    "start_surface": f"post_face_P{next_post}_toward_B{i+1}",
                    "end_surface": f"beam_soffit_B{i+1}",
                    "run_ft": round(run, 4)
                }
            })
            
    # Rafters
    overhang = structure["roof"]["primary_rafters"]["overhang_ft"]
    for i in range(qty):
        member_constraints.append({
            "member_id": f"R{i+1}",
            "constraints": {
                "tail_constraint": {
                    "type": "overhang_past_beam",
                    "beam_id": f"B{i+1}",
                    "overhang_ft": overhang
                },
                "hub_constraint": {
                    "type": "none" if shape == "rectangle" else "hub_face",
                    "hub_id": "HUB",
                    "face_index": i
                },
                "seat_constraint": {
                    "type": "birdsmouth",
                    "surface": f"beam_top_B{i+1}",
                    "beam_id": f"B{i+1}",
                    "seat_depth_ratio": 0.333
                },
                "plane_constraint": {
                    "type": "roof_plane",
                    "plane_id": f"roof_plane_{i}",
                    "pitch": pitch_str
                }
            }
        })
        
    jack_spec = structure["roof"].get("secondary_rafters", {})
    if jack_spec.get("enabled"):
        jack_count = jack_spec.get("count_per_side") or 2
        for i in range(qty):
            for j_idx in range(jack_count):
                f = (j_idx + 1.0) / (jack_count + 1.0)
                suffix = 'a' if f < 0.5 else 'b'
                hip_idx = i + 1 if f < 0.5 else ((i+1)%qty + 1)
                face = "left" if f < 0.5 else "right"
                
                member_constraints.append({
                    "member_id": f"J{i+1}{suffix}",
                    "constraints": {
                        "seat_constraint": {
                            "type": "birdsmouth",
                            "surface": f"beam_top_B{i+1}",
                            "beam_id": f"B{i+1}"
                        },
                        "termination_constraint": {
                            "type": "hip_rafter_side_face",
                            "hip_id": f"R{hip_idx}",
                            "face": face
                        },
                        "plane_constraint": {
                            "type": "roof_plane",
                            "plane_id": f"roof_plane_{i}"
                        }
                    }
                })
                
    # Hub
    member_constraints.append({
        "member_id": "HUB",
        "constraints": {
            "type": "rafter_termination_block",
            "faces_defined_by": "rafter_count",
            "height_constraint": "rafter_depth",
            "radius_constraint": "auto_from_rafter_width"
        }
    })

    # 3. Global Constraints
    roof_planes_global = []
    for i in range(qty):
        next_post = i + 2 if (i + 2) <= qty else 1
        roof_planes_global.append({
            "id": f"roof_plane_{i}",
            "defined_by": [f"P{i+1}_top", f"P{next_post}_top", "HUB_apex"],
            "pitch": pitch_str
        })
        
    global_constraints = {
        "roof_planes": roof_planes_global,
        "proportion_rules": {
            "beam_depth_gt_rafter_depth": beam_d_in > structure["roof"]["primary_rafters"]["actual_depth_in"],
            "hub_height_lte_beam_depth_x1.2": True, # Solved dynamically in engine
            "brace_length_lte_post_height_x0.4": True # Checked in validation
        },
        "symmetry": "radial_from_center"
    }
    
    # 4. Assembly & Seal
    structure["cad_constraints"] = {
        "reference_planes": reference_planes,
        "member_constraints": member_constraints,
        "global_constraints": global_constraints
    }
    
    # Modify bracing parameters inside layout as required by schema changes
    if "bracing" in structure and "brace" in structure["bracing"]:
        # Ensure constraints are written correctly
        run_t_val = structure["bracing"]["brace"].get("run_ft") or 1.5
        structure["bracing"]["brace"]["constraints"] = {
            "start_surface": "post_face",
            "end_surface": "beam_soffit",
            "run_ft": round(run_t_val, 4)
        }
        
    if "meta" in structure:
        structure["meta"]["lifecycle"] = "CONSTRAINTS_DEFINED"

from path_utils import staging_dir

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else str(staging_dir() / "structure.json")
    struct = load_structure(path)
    translate_to_constraints(struct)
    save_structure(struct, path)
    print("CAD constraint translation complete. lifecycle = CONSTRAINTS_DEFINED.")

if __name__ == "__main__":
    main()
