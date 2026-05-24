# -*- coding: utf-8 -*-
"""
fabrication_builder.py — Deterministic Stage 6 Fabrication Compiler.
Derives 3D local coordinate frames, lumber cut lengths, stock, and compound saw
angles (miter, bevel) directly from joint planes in context/staging/structure.json.
"""

import sys
import json
import math
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

# Orthonormal Vector Math Utilities
def vsub(a: tuple, b: tuple) -> tuple: return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def vadd(a: tuple, b: tuple) -> tuple: return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def vscl(a: tuple, s: float) -> tuple: return (a[0]*s, a[1]*s, a[2]*s)
def vdot(a: tuple, b: tuple) -> float: return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def vlen(a: tuple) -> float: return math.sqrt(vdot(a, a))

def vnorm(a: tuple) -> tuple:
    l = vlen(a)
    return vscl(a, 1.0 / l) if l > 1e-9 else (0.0, 0.0, 0.0)

def vcross(a: tuple, b: tuple) -> tuple:
    return (
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    )

def get_compound_cuts(N_world: tuple, x_axis: tuple, y_axis: tuple, z_axis: tuple) -> tuple[float, float]:
    """
    Project world normal into board local frame and derive compound saw angles:
    Miter: swing of saw table from perpendicular (rotation about z_axis table normal)
    Bevel: tilt of saw blade (tilt toward z_axis table normal)
    """
    n_x = vdot(N_world, x_axis)
    n_y = vdot(N_world, y_axis)
    n_z = vdot(N_world, z_axis)

    # Standardize normal pointing along the board axis (out of board cut face)
    if n_x < 0:
        n_x, n_y, n_z = -n_x, -n_y, -n_z

    miter_deg = math.degrees(math.atan2(n_y, n_x))
    bevel_deg = math.degrees(math.atan2(n_z, math.sqrt(n_x**2 + n_y**2)))

    # Convert miter angle from axial face angle to saw table swing angle (from perpendicular)
    if abs(miter_deg) > 1e-3:
        miter_saw = 90.0 - abs(miter_deg)
    else:
        miter_saw = 0.0

    return round(miter_saw, 2), round(bevel_deg, 2)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 fabrication_builder.py context/staging/structure.json", file=sys.stderr)
        sys.exit(1)

    structure_path = Path(sys.argv[1]).resolve()
    if not structure_path.exists():
        print(f"Error: {structure_path} not found.", file=sys.stderr)
        sys.exit(1)

    with open(structure_path, encoding="utf-8") as f:
        structure = json.load(f)

    # Enforce sealing contract before Stage 6 compilation
    if not structure.get("geometry", {}).get("_sealed"):
        print("Error: structure.geometry must be sealed before running Stage 6 compilation.", file=sys.stderr)
        sys.exit(1)

    geo = structure["geometry"]
    joints = geo.get("joints", {})
    if not joints:
        print("Error: geometry.joints payload not found. Rerun geometry_engine.py.", file=sys.stderr)
        sys.exit(1)

    qty = structure["layout"]["post_count"]
    source_hash = structure["meta"]["source_hash"]
    
    # Retrieve Z coordinates from joint contract
    z_planes = joints["z_planes"]
    Z_BEAM_TOP = z_planes["Z_BEAM_TOP"]

    # Member Specs
    posts_spec = structure["members"]["posts"]
    beams_spec = structure["members"]["beams"]
    rafters_spec = structure["roof"]["primary_rafters"]
    secondary_spec = structure["roof"].get("secondary_rafters", {})
    bracing_spec = structure.get("bracing", {})
    brace_spec = bracing_spec.get("brace", {}) if bracing_spec.get("enabled") else {}

    UP = (0.0, 0.0, 1.0)
    cut_list: list[dict[str, Any]] = []

    # ── 1. Posts (P1 to P6) ──────────────────────────────────────────────────
    # Axis: (px, py, Z_GRADE) to (px, py, Z_POST_TOP)
    for i, p_xy in enumerate(joints["layout"]["post_xy"]):
        bid = f"P{i+1}"
        p0 = (p_xy[0], p_xy[1], z_planes["Z_GRADE"])
        p1 = (p_xy[0], p_xy[1], z_planes["Z_POST_TOP"])
        axis_len = vdist(p0, p1)

        cut_list.append({
            "id": bid, "role": "post", "nominal_size": posts_spec["nominal_size"],
            "actual_width_in": posts_spec["actual_width_in"], "actual_depth_in": posts_spec["actual_depth_in"],
            "axis": {"start": list(p0), "end": list(p1)},
            "stock": {"cut_length_ft": round(axis_len, 3), "order_length_ft": int(math.ceil(axis_len / 2.0) * 2)},
            "cuts": [
                {"cut_id": f"{bid}-START", "end": "start", "type": "square_cut", "mates_to": "grade_footing", "plane": {"point": list(p0), "normal": [0,0,-1]}, "angles": {"miter_deg": 0.0, "bevel_deg": 0.0}},
                {"cut_id": f"{bid}-END", "end": "end", "type": "square_cut", "mates_to": "beam_soffit", "plane": {"point": list(p1), "normal": [0,0,1]}, "angles": {"miter_deg": 0.0, "bevel_deg": 0.0}}
            ]
        })

    # ── 2. Ring Beams (B1 to B6) ──────────────────────────────────────────────
    # Axis from geometry.beam_ring (using B-prefixed IDs)
    for i in range(qty):
        bid = f"B{i+1}"
        p1_xy = joints["layout"]["post_xy"][i]
        p2_xy = joints["layout"]["post_xy"][(i+1)%qty]
        bz = z_planes["Z_BEAM_CENTER"]
        p0 = (p1_xy[0], p1_xy[1], bz)
        p1 = (p2_xy[0], p2_xy[1], bz)
        axis = vsub(p1, p0)
        axis_len = vlen(axis)
        x_axis = vnorm(axis); y_axis = vnorm(vcross(UP, x_axis)); z_axis = vnorm(vcross(x_axis, y_axis))
        
        # End planes
        planes = joints["beam_ring"]["beam_end_planes"]
        pl_start = next(p for p in planes if p["beam_id"] == bid and p["end"] == "start")
        pl_end = next(p for p in planes if p["beam_id"] == bid and p["end"] == "end")
        
        miter_start, bevel_start = get_compound_cuts(pl_start["normal"], x_axis, y_axis, z_axis)
        miter_end, bevel_end = get_compound_cuts(pl_end["normal"], x_axis, y_axis, z_axis)

        cut_list.append({
            "id": bid, "role": "beam", "nominal_size": beams_spec["nominal_size"],
            "actual_width_in": beams_spec["actual_width_in"], "actual_depth_in": beams_spec["actual_depth_in"],
            "axis": {"start": list(p0), "end": list(p1)},
            "stock": {"cut_length_ft": round(axis_len, 3), "order_length_ft": int(math.ceil(axis_len / 2.0) * 2)},
            "cuts": [
                {"cut_id": f"{bid}-START", "end": "start", "type": "beam_miter", "mates_to": f"beam_B{((i-1)%qty)+1}", "plane": {"point": pl_start["point"], "normal": pl_start["normal"]}, "angles": {"miter_deg": abs(miter_start), "bevel_deg": abs(bevel_start)}},
                {"cut_id": f"{bid}-END", "end": "end", "type": "beam_miter", "mates_to": f"beam_B{((i+1)%qty)+1}", "plane": {"point": pl_end["point"], "normal": pl_end["normal"]}, "angles": {"miter_deg": abs(miter_end), "bevel_deg": abs(bevel_end)}}
            ]
        })

    # ── 3. Hip Rafters (R1 to R6) ─────────────────────────────────────────────
    # Axis from geometry.joints.primary_rafters
    seat_depth_ft = joints["rafters"]["seat_depth_ft_resolved"]
    for rj in joints.get("primary_rafters", []):
        bid = rj["id"]
        p0 = tuple(rj["start"]); p1 = tuple(rj["end"])
        axis = vsub(p1, p0); axis_len = vlen(axis)
        x_axis = vnorm(axis); y_axis = vnorm(vcross(UP, x_axis)); z_axis = vnorm(vcross(x_axis, y_axis))
        
        # Hub Face Cut
        idx = int(bid[1:]) - 1
        hub_plane = joints["hub"]["face_planes"][idx]
        miter_hub, bevel_hub = get_compound_cuts(hub_plane["normal"], x_axis, y_axis, z_axis)
        
        # Birdsmouth Seat (Bearing Face)
        p_seat = tuple(rj["seat_point"])
        miter_seat, bevel_seat = get_compound_cuts(UP, x_axis, y_axis, z_axis)
        
        cut_list.append({
            "id": bid, "role": "rafter_primary", "nominal_size": rafters_spec["nominal_size"],
            "actual_width_in": rafters_spec["actual_width_in"], "actual_depth_in": rafters_spec["actual_depth_in"],
            "axis": {"start": list(p0), "end": list(p1)},
            "stock": {"cut_length_ft": round(axis_len, 3), "order_length_ft": int(math.ceil(axis_len / 2.0) * 2)},
            "cuts": [
                {"cut_id": f"{bid}-END-HUB", "end": "end", "type": "compound_miter", "mates_to": f"hub_face_{hub_plane['id']}", "plane": {"point": hub_plane["point"], "normal": hub_plane["normal"]}, "angles": {"miter_deg": abs(miter_hub), "bevel_deg": abs(bevel_hub)}},
                {"cut_id": f"{bid}-SEAT", "end": "start", "type": "birdsmouth", "mates_to": f"beam_top_B{idx+1}", "seat_depth_ft": round(seat_depth_ft, 4), "subcuts": [{"name": "seat_cut", "plane": {"point": list(p_seat), "normal": [0,0,1]}, "angles": {"miter_deg": abs(miter_seat), "bevel_deg": abs(bevel_seat)}}]}
            ]
        })

    # ── 4. Knee Braces (K1A to K6B) ───────────────────────────────────────────
    if joints.get("braces", {}).get("enabled"):
        for bj in joints["braces"]["endpoints"]:
            bid = bj["id"]; p0 = tuple(bj["start"]); p1 = tuple(bj["end"])
            axis = vsub(p1, p0); axis_len = vlen(axis)
            x_axis = vnorm(axis); y_axis = vnorm(vcross(UP, x_axis)); z_axis = vnorm(vcross(x_axis, y_axis))
            
            # Post End
            post_idx = int("".join([c for c in bid if c.isdigit()])) - 1
            pxy = joints["layout"]["post_xy"][post_idx]
            dir_to_post = vnorm(vsub((pxy[0], pxy[1], p0[2]), p0))
            miter_post, bevel_post = get_compound_cuts(dir_to_post, x_axis, y_axis, z_axis)
            
            # Beam End
            miter_beam, bevel_beam = get_compound_cuts(UP, x_axis, y_axis, z_axis)
            
            cut_list.append({
                "id": bid, "role": "brace", "nominal_size": brace_spec["nominal_size"],
                "actual_width_in": brace_spec["actual_width_in"], "actual_depth_in": brace_spec["actual_depth_in"],
                "axis": {"start": list(p0), "end": list(p1)},
                "stock": {"cut_length_ft": round(axis_len, 3), "order_length_ft": int(math.ceil(axis_len / 2.0) * 2)},
                "cuts": [
                    {"cut_id": f"{bid}-START-POST", "end": "start", "type": "brace_miter", "mates_to": f"post_P{post_idx+1}", "angles": {"miter_deg": abs(miter_post), "bevel_deg": abs(bevel_post)}},
                    {"cut_id": f"{bid}-END-BEAM", "end": "end", "type": "brace_miter", "mates_to": f"beam_B{post_idx+1}", "angles": {"miter_deg": abs(miter_beam), "bevel_deg": abs(bevel_beam)}}
                ]
            })

    # ── 5. Secondary / Jack Rafters ──────────────────────────────────────────
    if joints.get("jack_rafters", {}).get("enabled"):
        for ep in joints["jack_rafters"]["endpoints"]:
            bid = ep["id"]; p0 = tuple(ep["start"]); p1 = tuple(ep["end"])
            axis = vsub(p1, p0); axis_len = vlen(axis)
            x_axis = vnorm(axis); y_axis = vnorm(vcross(UP, x_axis)); z_axis = vnorm(vcross(x_axis, y_axis))
            
            # Hip Side Cut
            m_id = ep["mate_id"]
            idx = int(m_id[1:]) - 1
            px_corner, py_corner = joints["layout"]["post_xy"][idx]
            dx_hip = -px_corner; dy_hip = -py_corner # Toward Apex (0,0)
            len_hip = math.sqrt(dx_hip**2 + dy_hip**2)
            n_side = (-dy_hip/len_hip, dx_hip/len_hip, 0.0)
            miter_hip, bevel_hip = get_compound_cuts(n_side, x_axis, y_axis, z_axis)
            
            cut_list.append({
                "id": bid, "role": "rafter_secondary", "nominal_size": secondary_spec["nominal_size"],
                "actual_width_in": secondary_spec["actual_width_in"], "actual_depth_in": secondary_spec["actual_depth_in"],
                "axis": {"start": list(p0), "end": list(p1)},
                "stock": {"cut_length_ft": round(axis_len, 3), "order_length_ft": int(math.ceil(axis_len / 2.0) * 2)},
                "cuts": [{"cut_id": f"{bid}-END-HIP", "end": "end", "type": "compound_miter", "mates_to": m_id, "angles": {"miter_deg": abs(miter_hip), "bevel_deg": abs(bevel_hip)}}]
            })

    # Final counts and output
    out_payload = {
        "schema": "garden-structure-designer/fabrication-cut-list/1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_hash": source_hash,
        "members": cut_list,
        "summary": {"counts": {"posts": qty, "beams": qty, "rafters_primary": qty, "rafters_secondary": len([m for m in cut_list if m["role"] == "rafter_secondary"])}}
    }

    out_dir = Path("outputs/fabrication").resolve(); out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "cut-list.json", "w", encoding="utf-8") as f: json.dump(out_payload, f, indent=2)
    print(f"  ✓ Compiled fabrication cut list -> outputs/fabrication/cut-list.json")
    purlins_spec = structure["members"].get("purlins", {})
    if purlins_spec.get("enabled", False):
        pur_w = purlins_spec.get("actual_width_in", 3.5)
        pur_d = purlins_spec.get("actual_depth_in", 3.5)
        PUR_HW = (pur_w / 12.0) / 2.0
        PUR_HD = (pur_d / 12.0) / 2.0
        s_purlin = purlins_spec.get("height_fraction", 0.55)
        Z_PURLIN = Z_BEAM_TOP + (Z_APEX - Z_BEAM_TOP) * s_purlin

        px_ex, py_ex = post_xy[0]
        len_xy_ex = math.sqrt(px_ex**2 + py_ex**2)
        slope_ex = (Z_APEX - Z_BEAM_TOP) / (len_xy_ex - hub_r)
        dy_vertical = RAFTER_HD / math.cos(math.atan(slope_ex))

        purlin_pts = []
        for i in range(qty):
            px, py = post_xy[i]
            ax, ay, az = rafter_apex[i]
            pt = (
                px + (ax - px) * s_purlin,
                py + (ay - py) * s_purlin,
                Z_PURLIN + dy_vertical
            )
            purlin_pts.append(pt)

        for i in range(qty):
            pt1 = purlin_pts[i]
            pt2 = purlin_pts[(i+1) % qty]

            axis = vsub(pt2, pt1)
            axis_len = vlen(axis)

            # Local coordinate frame
            x_axis = vnorm(axis)
            y_axis = vnorm(vcross(UP, x_axis))
            z_axis = vnorm(vcross(x_axis, y_axis))

            # Retrieve cheek planes from hip rafters
            px1, py1 = post_xy[i]
            ax1, ay1 = rafter_apex[i][0], rafter_apex[i][1]
            dx_hip1 = ax1 - px1
            dy_hip1 = ay1 - py1
            len_hip1 = math.sqrt(dx_hip1**2 + dy_hip1**2)
            N_hip1 = (-dy_hip1 / len_hip1, dx_hip1 / len_hip1, 0.0)

            px2, py2 = post_xy[(i+1) % qty]
            ax2, ay2 = rafter_apex[(i+1)%qty][0], rafter_apex[(i+1)%qty][1]
            dx_hip2 = ax2 - px2
            dy_hip2 = ay2 - py2
            len_hip2 = math.sqrt(dx_hip2**2 + dy_hip2**2)
            N_hip2 = (-dy_hip2 / len_hip2, dx_hip2 / len_hip2, 0.0)

            miter_start, bevel_start = get_compound_cuts(N_hip1, x_axis, y_axis, z_axis)
            miter_end, bevel_end = get_compound_cuts(N_hip2, x_axis, y_axis, z_axis)

            bid = f"Purlin{i+1}"
            cut_list.append({
                "id": bid,
                "role": "purlin",
                "nominal_size": purlins_spec["nominal_size"],
                "actual_width_in": pur_w,
                "actual_depth_in": pur_d,
                "axis": {
                    "start": [round(pt1[0], 4), round(pt1[1], 4), round(pt1[2], 3)],
                    "end": [round(pt2[0], 4), round(pt2[1], 4), round(pt2[2], 3)]
                },
                "stock": {
                    "cut_length_ft": round(axis_len, 3),
                    "order_length_ft": int(math.ceil(axis_len / 2.0) * 2)
                },
                "cuts": [
                    {
                        "cut_id": f"{bid}-START-HIP",
                        "end": "start",
                        "type": "compound_miter",
                        "mates_to": f"rafter_primary_R{i+1}",
                        "plane": {
                            "point": [round(pt1[0], 4), round(pt1[1], 4), round(pt1[2], 3)],
                            "normal": [round(N_hip1[0], 4), round(N_hip1[1], 4), 0.0]
                        },
                        "angles": {"miter_deg": abs(miter_start), "bevel_deg": abs(bevel_start)}
                    },
                    {
                        "cut_id": f"{bid}-END-HIP",
                        "end": "end",
                        "type": "compound_miter",
                        "mates_to": f"rafter_primary_R{((i+1)%qty)+1}",
                        "plane": {
                            "point": [round(pt2[0], 4), round(pt2[1], 4), round(pt2[2], 3)],
                            "normal": [round(N_hip2[0], 4), round(N_hip2[1], 4), 0.0]
                        },
                        "angles": {"miter_deg": abs(miter_end), "bevel_deg": abs(bevel_end)}
                    }
                ]
            })

    # Compile the final cut list document
    num_posts = qty
    num_beams = qty
    num_primary_rafters = qty
    num_secondary_rafters = len([m for m in cut_list if m["role"] == "rafter_secondary"])
    num_purlins = len([m for m in cut_list if m["role"] == "purlin"])
    num_braces = len(endpoints) if bracing_spec.get("enabled") else 0

    out_payload = {
        "schema": "garden-structure-designer/fabrication-cut-list/1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_hash": source_hash,
        "structure_path": str(structure_path.relative_to(Path.cwd())),
        "units": "feet",
        "angle_units": "deg",
        "assumptions": [
            "Saw convention: miter=rotation about board z-axis; bevel=tilt introducing z component in cut normal.",
            "Board local frame derived from member axis and global up; z-axis aligns with member depth axis."
        ],
        "tolerances": {
            "length_ft": 0.01,
            "angle_deg": 0.10,
            "plane_offset_ft": 0.0052,
            "kerf_in": 0.125
        },
        "members": cut_list,
        "summary": {
            "counts": {
                "posts": num_posts,
                "beams": num_beams,
                "rafters_primary": num_primary_rafters,
                "rafters_secondary": num_secondary_rafters,
                "purlins": num_purlins,
                "braces": num_braces
            },
            "cut_counts": {
                "post_crosscut": num_posts * 2,
                "beam_miter": num_beams * 2,
                "compound_miter": num_primary_rafters + num_secondary_rafters + (num_purlins * 2),
                "birdsmouth": num_primary_rafters + num_secondary_rafters,
                "brace_miter": num_braces * 2
            }
        }
    }

    # Save to outputs/fabrication/cut-list.json
    out_dir = Path("outputs/fabrication").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "cut-list.json"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2)

    print(f"  ✓ Compiled fabrication cut list -> {out_path.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
