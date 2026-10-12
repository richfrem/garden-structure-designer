#!/usr/bin/env python3
"""
cad_language_translator.py
==========================

Purpose:
    Translates structural design intent and topology parameters from
    structure.json into formal CAD constraint dictionaries, reference planes,
    and member surface bounds. Sets meta.lifecycle to "CONSTRAINTS_DEFINED".

Layer: Execution / Stage 1 Constraint Compilation

Key Input Dependencies:
    - context/staging/structure.json (structural specification and dimensions)

Key Functions:
    derive_post_coordinates(shape, qty, r_ft, len_ft, wid_ft) -> list[list[float]]
    build_footing_and_post_planes(post_xy, qty, z_grade, phw) -> list[dict[str, Any]]
    build_beam_planes(post_xy, qty, z_post_top, z_beam_top) -> list[dict[str, Any]]
    build_roof_slope_planes(post_xy, qty, shape, z_beam_top, z_apex, v_shift) -> list[dict[str, Any]]
    build_hub_face_planes(qty, hub_r, z_apex) -> list[dict[str, Any]]
    build_bracing_constraints(post_xy, qty, run_t) -> list[dict[str, Any]]
    build_rafter_constraints(structure, qty, shape, pitch_str) -> list[dict[str, Any]]
    build_member_constraints(structure, post_xy, qty, shape, pitch_str) -> list[dict[str, Any]]
    extract_nominal_parameters(structure) -> tuple
    translate_to_constraints(structure: dict[str, Any]) -> None
    main() -> None

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/cad_language_translator.py context/staging/structure.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir
from structure_io import assert_not_sealed, load_structure, save_structure


def derive_post_coordinates(
    shape: str,
    qty: int,
    r_ft: float,
    len_ft: float,
    wid_ft: float,
) -> List[List[float]]:
    """Derives 2D coordinates for posts based on shape (polygon, 4-post, 6-post rectangle)."""
    if shape == "rectangle" and qty == 6:
        hx, hy = len_ft / 2.0, wid_ft / 2.0
        return [
            [round(hx, 4), round(-hy, 4)],
            [round(hx, 4), round(hy, 4)],
            [0.0, round(hy, 4)],
            [round(-hx, 4), round(hy, 4)],
            [round(-hx, 4), round(-hy, 4)],
            [0.0, round(-hy, 4)],
        ]
    if shape == "rectangle" and qty == 4:
        hx, hy = len_ft / 2.0, wid_ft / 2.0
        return [
            [round(hx, 4), round(-hy, 4)],
            [round(hx, 4), round(hy, 4)],
            [round(-hx, 4), round(hy, 4)],
            [round(-hx, 4), round(-hy, 4)],
        ]
    return [
        [round(r_ft * math.cos(2 * math.pi * i / qty), 4), round(r_ft * math.sin(2 * math.pi * i / qty), 4)]
        for i in range(qty)
    ]


def build_footing_and_post_planes(
    post_xy: List[List[float]],
    qty: int,
    z_grade: float,
    phw: float,
) -> List[Dict[str, Any]]:
    """Generates footing top and post vertical face reference planes."""
    planes: List[Dict[str, Any]] = []
    for i in range(qty):
        planes.append({
            "id": f"footing_top_FT{i+1}",
            "type": "footing_top",
            "point": [post_xy[i][0], post_xy[i][1], z_grade],
            "normal": [0.0, 0.0, 1.0],
        })
        p1, p2, p0 = post_xy[i], post_xy[(i + 1) % qty], post_xy[(i - 1) % qty]
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        bl = math.sqrt(dx * dx + dy * dy)
        ux, uy = dx / bl, dy / bl
        planes.append({
            "id": f"post_face_P{i+1}_toward_B{i+1}",
            "type": "post_face",
            "point": [p1[0] + ux * phw, p1[1] + uy * phw, z_grade],
            "normal": [ux, uy, 0.0],
        })
        dx_prev, dy_prev = p1[0] - p0[0], p1[1] - p0[1]
        bl_prev = math.sqrt(dx_prev * dx_prev + dy_prev * dy_prev)
        ux_prev, uy_prev = dx_prev / bl_prev, dy_prev / bl_prev
        prev_beam_id = qty if i == 0 else i
        planes.append({
            "id": f"post_face_P{i+1}_toward_B{prev_beam_id}",
            "type": "post_face",
            "point": [p1[0] - ux_prev * phw, p1[1] - uy_prev * phw, z_grade],
            "normal": [-ux_prev, -uy_prev, 0.0],
        })
    return planes


def build_beam_planes(
    post_xy: List[List[float]],
    qty: int,
    z_post_top: float,
    z_beam_top: float,
) -> List[Dict[str, Any]]:
    """Generates horizontal beam soffit and top reference planes."""
    planes: List[Dict[str, Any]] = []
    for i in range(qty):
        planes.append({
            "id": f"beam_soffit_B{i+1}",
            "type": "beam_soffit",
            "point": [post_xy[i][0], post_xy[i][1], z_post_top],
            "normal": [0.0, 0.0, -1.0],
        })
        planes.append({
            "id": f"beam_top_B{i+1}",
            "type": "beam_top",
            "point": [post_xy[i][0], post_xy[i][1], z_beam_top],
            "normal": [0.0, 0.0, 1.0],
        })
    return planes


def build_roof_slope_planes(
    post_xy: List[List[float]],
    qty: int,
    shape: str,
    z_beam_top: float,
    z_apex: float,
    v_shift: float,
    r_count: int = 0,
) -> List[Dict[str, Any]]:
    """Generates roof sloping facet reference planes for rectangular or polygonal hips."""
    planes: List[Dict[str, Any]] = []
    if shape == "rectangle":
        count = r_count if r_count > 0 else qty
        for i in range(count):
            planes.append({
                "id": f"roof_plane_{i}",
                "type": "roof_plane",
                "point": [0.0, 0.0, z_beam_top + v_shift],
                "normal": [0.0, 0.0, 1.0],
            })
        return planes

    for i in range(qty):
        pa = (post_xy[i][0], post_xy[i][1], z_beam_top + v_shift)
        pb = (post_xy[(i + 1) % qty][0], post_xy[(i + 1) % qty][1], z_beam_top + v_shift)
        p_apex = (0.0, 0.0, z_apex + v_shift)
        v1 = (pb[0] - pa[0], pb[1] - pa[1], pb[2] - pa[2])
        v2 = (p_apex[0] - pa[0], p_apex[1] - pa[1], p_apex[2] - pa[2])
        nx = v1[1] * v2[2] - v1[2] * v2[1]
        ny = v1[2] * v2[0] - v1[0] * v2[2]
        nz = v1[0] * v2[1] - v1[1] * v2[0]
        nl = math.sqrt(nx * nx + ny * ny + nz * nz)
        norm = [nx / nl, ny / nl, nz / nl] if nl > 1e-9 else [0.0, 0.0, 1.0]
        planes.append({"id": f"roof_plane_{i}", "type": "roof_plane", "point": list(pa), "normal": norm})
    return planes


def build_hub_face_planes(
    qty: int,
    hub_r: float,
    z_apex: float,
    hub_type: str | None = None,
) -> List[Dict[str, Any]]:
    """Generates polygonal vertical facet planes for apex hub rafter termination."""
    if hub_type in ("none", "", None):
        return []
    planes: List[Dict[str, Any]] = []
    hub_r_face = hub_r * math.cos(math.pi / qty)
    for i in range(qty):
        theta = 2.0 * math.pi * i / qty
        planes.append({
            "id": f"hub_face_H{i+1}",
            "type": "hub_face",
            "point": [hub_r_face * math.cos(theta), hub_r_face * math.sin(theta), z_apex],
            "normal": [math.cos(theta), math.sin(theta), 0.0],
        })
    return planes


def build_bracing_constraints(
    post_xy: List[List[float]],
    qty: int,
    run_t: float,
) -> List[Dict[str, Any]]:
    """Builds knee brace start and end surface connection constraints."""
    constraints: List[Dict[str, Any]] = []
    for i in range(qty):
        p1 = post_xy[i]
        p2 = post_xy[(i + 1) % qty]
        bl = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        run = min(run_t, bl * 0.3)
        constraints.append({
            "member_id": f"K{i+1}A",
            "constraints": {
                "start_surface": f"post_face_P{i+1}_toward_B{i+1}",
                "end_surface": f"beam_soffit_B{i+1}",
                "run_ft": round(run, 4),
            },
        })
        next_post = i + 2 if (i + 2) <= qty else 1
        constraints.append({
            "member_id": f"K{i+1}B",
            "constraints": {
                "start_surface": f"post_face_P{next_post}_toward_B{i+1}",
                "end_surface": f"beam_soffit_B{i+1}",
                "run_ft": round(run, 4),
            },
        })
    return constraints


def build_rafter_constraints(
    structure: Dict[str, Any],
    qty: int,
    shape: str,
    pitch_str: str,
) -> List[Dict[str, Any]]:
    """Builds rafter birdsmouth seats, overhang, and apex hub connection constraints."""
    overhang = structure["roof"]["primary_rafters"]["overhang_ft"]
    constraints: List[Dict[str, Any]] = []
    r_count = structure["roof"]["primary_rafters"]["count"] if shape == "rectangle" else qty
    for i in range(r_count):
        beam_idx = (i % qty) + 1
        constraints.append({
            "member_id": f"R{i+1}",
            "constraints": {
                "tail_constraint": {"type": "overhang_past_beam", "beam_id": f"B{beam_idx}", "overhang_ft": overhang},
                "hub_constraint": {
                    "type": "none" if shape == "rectangle" else "hub_face",
                    "hub_id": "none" if shape == "rectangle" else "HUB",
                    "face_index": i,
                },
                "seat_constraint": {
                    "type": "birdsmouth",
                    "surface": f"beam_top_B{beam_idx}",
                    "beam_id": f"B{beam_idx}",
                    "seat_depth_ratio": 0.333,
                },
                "plane_constraint": {"type": "roof_plane", "plane_id": f"roof_plane_{i}", "pitch": pitch_str},
            },
        })

    jack_spec = structure["roof"].get("secondary_rafters", {})
    if jack_spec.get("enabled"):
        jack_count = jack_spec.get("count_per_side") or 2
        for i in range(qty):
            for j_idx in range(jack_count):
                f = (j_idx + 1.0) / (jack_count + 1.0)
                suffix = "a" if f < 0.5 else "b"
                hip_idx = i + 1 if f < 0.5 else ((i + 1) % qty + 1)
                face = "left" if f < 0.5 else "right"
                constraints.append({
                    "member_id": f"J{i+1}{suffix}",
                    "constraints": {
                        "seat_constraint": {"type": "birdsmouth", "surface": f"beam_top_B{i+1}", "beam_id": f"B{i+1}"},
                        "termination_constraint": {"type": "hip_face", "hip_id": f"R{hip_idx}", "face": face},
                        "plane_constraint": {"type": "roof_plane", "plane_id": f"roof_plane_{i}"},
                    },
                })
    return constraints


def build_member_constraints(
    structure: Dict[str, Any],
    post_xy: List[List[float]],
    qty: int,
    shape: str,
    pitch_str: str,
) -> List[Dict[str, Any]]:
    """Assembles full list of member constraints for posts, beams, braces, rafters, and hub."""
    constraints: List[Dict[str, Any]] = []
    for i in range(qty):
        constraints.append({
            "member_id": f"P{i+1}",
            "constraints": {"base_surface": f"footing_top_FT{i+1}", "top_surface": f"beam_soffit_B{i+1}"},
        })
    for i in range(qty):
        next_post = i + 2 if (i + 2) <= qty else 1
        constraints.append({
            "member_id": f"B{i+1}",
            "constraints": {
                "start_surface": f"post_top_P{i+1}",
                "end_surface": f"post_top_P{next_post}",
                "seating_rule": "beam_bottom_z == post_top_z",
            },
        })

    if structure.get("bracing", {}).get("enabled"):
        run_t = structure["bracing"]["brace"].get("run_ft") or 1.5
        constraints.extend(build_bracing_constraints(post_xy, qty, run_t))

    constraints.extend(build_rafter_constraints(structure, qty, shape, pitch_str))
    if structure.get("hub", {}).get("type") not in ("none", "", None):
        constraints.append({
            "member_id": "HUB",
            "constraints": {
                "type": "rafter_termination_block",
                "faces_defined_by": "rafter_count",
                "height_constraint": "rafter_depth",
                "radius_constraint": "auto_from_rafter_width",
            },
        })
    return constraints


def extract_nominal_parameters(structure: Dict[str, Any]) -> Tuple[Any, ...]:
    """Extracts dimensional layout values and computed z-levels from structure dict."""
    layout = structure["layout"]
    members = structure["members"]
    qty = layout["post_count"]
    r_ft = layout["inscribed_radius_ft"]
    post_h = members["posts"]["cut_length_ft"]
    beam_d_in = members["beams"]["actual_depth_in"]
    beam_d_ft = beam_d_in / 12.0

    pitch_str = structure["roof"]["pitch"]
    pr, rr = [float(x) for x in pitch_str.split(":")]

    z_grade = 0.0
    z_post_top = post_h - beam_d_ft
    z_beam_top = post_h
    hub_r = max(structure["hub"].get("radius_min_ft") or 0.6, 0.75)
    roof_rise = r_ft * (pr / rr)
    z_apex = post_h + roof_rise

    phw = members["posts"]["actual_width_in"] / 24.0
    shape = layout.get("shape", structure.get("structure", {}).get("shape", "polygon"))
    len_ft = float(layout.get("length_ft") or (r_ft * 2.0))
    wid_ft = float(layout.get("width_ft") or (r_ft * 1.333))

    rafter_d_ft = structure["roof"]["primary_rafters"]["actual_depth_in"] / 12.0
    seat_notch = rafter_d_ft / 3.0
    remaining_meat = rafter_d_ft - seat_notch
    apothem = r_ft * math.cos(math.pi / qty)
    denom = apothem - hub_r * math.cos(math.pi / qty)
    slope = roof_rise / denom if abs(denom) > 1e-4 else 0.0
    v_shift = remaining_meat * math.cos(math.atan(slope))

    return (qty, r_ft, shape, len_ft, wid_ft, z_grade, z_post_top, z_beam_top, z_apex, phw, hub_r, v_shift, pitch_str, beam_d_in)


def translate_to_constraints(structure: dict[str, Any]) -> None:
    """Translates high-level structure design parameters into CAD constraints dictionary."""
    assert_not_sealed(structure, "cad_constraints")

    params = extract_nominal_parameters(structure)
    (qty, r_ft, shape, len_ft, wid_ft, z_grade, z_post_top, z_beam_top, z_apex, phw, hub_r, v_shift, pitch_str, beam_d_in) = params

    post_xy = derive_post_coordinates(shape, qty, r_ft, len_ft, wid_ft)
    ref_planes = build_footing_and_post_planes(post_xy, qty, z_grade, phw)
    ref_planes.extend(build_beam_planes(post_xy, qty, z_post_top, z_beam_top))
    r_count = structure.get("roof", {}).get("primary_rafters", {}).get("count") or qty
    ref_planes.extend(build_roof_slope_planes(post_xy, qty, shape, z_beam_top, z_apex, v_shift, r_count))
    ref_planes.extend(build_hub_face_planes(qty, hub_r, z_apex, structure.get("hub", {}).get("type")))

    member_constraints = build_member_constraints(structure, post_xy, qty, shape, pitch_str)
    roof_count = r_count if shape == "rectangle" else qty
    roof_planes_global = [
        {
            "id": f"roof_plane_{i}",
            "defined_by": [f"P{i+1}_top", f"P{(i+2 if (i+2) <= qty else 1)}_top", "roof_plane"] if shape == "rectangle" else [f"P{i+1}_top", f"P{(i+2 if (i+2) <= qty else 1)}_top", "HUB_apex"],
            "pitch": pitch_str,
        }
        for i in range(roof_count)
    ]
    global_constraints = {
        "roof_planes": roof_planes_global,
        "proportion_rules": {
            "beam_depth_gt_rafter_depth": beam_d_in > structure["roof"]["primary_rafters"]["actual_depth_in"],
            "hub_height_lte_beam_depth_x1.2": True,
            "brace_length_lte_post_height_x0.4": True,
        },
        "symmetry": "radial_from_center",
    }

    structure["cad_constraints"] = {
        "reference_planes": ref_planes,
        "member_constraints": member_constraints,
        "global_constraints": global_constraints,
    }

    if "bracing" in structure and "brace" in structure["bracing"]:
        run_t_val = structure["bracing"]["brace"].get("run_ft") or 1.5
        structure["bracing"]["brace"]["constraints"] = {
            "start_surface": "post_face",
            "end_surface": "beam_soffit",
            "run_ft": round(run_t_val, 4),
        }

    if "meta" in structure:
        structure["meta"]["lifecycle"] = "CONSTRAINTS_DEFINED"


def main() -> None:
    """CLI entrypoint reading structure.json, adding cad_constraints, and saving."""
    path = sys.argv[1] if len(sys.argv) > 1 else str(staging_dir() / "structure.json")
    struct = load_structure(path)
    translate_to_constraints(struct)
    save_structure(struct, path)
    print("CAD constraint translation complete. lifecycle = CONSTRAINTS_DEFINED.")


if __name__ == "__main__":
    main()
