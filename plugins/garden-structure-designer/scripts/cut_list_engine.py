#!/usr/bin/env python3
"""
cut_list_engine.py
==================

Purpose:
    Produces preliminary shop lumber cut lists and board-foot schedules.
    DEPRECATED: Reads legacy dual-dict inputs. Use fabrication_builder.py
    which operates on resolved_model from geometry_engine.py.

Layer: Execution / Fabrication (Legacy Fallback)

Key Input Dependencies:
    - context/staging/structure.json (or model and geometry JSON files)

Key Functions:
    get_standard_length(cut_length: float) -> int
    parse_member_dimensions(members, roof_data) -> tuple
    compute_member_spans(posts_data, model, calcs, roof_data, qty) -> tuple
    build_post_record(...) -> dict
    build_beam_record(...) -> dict
    build_rafter_record(...) -> dict
    build_hub_record(...) -> dict
    build_brace_record(...) -> dict | None
    compute_cut_list(model_path, calcs_path, bracing_path=None) -> dict
    main() -> None

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/cut_list_engine.py [model.json] [calcs.json]
"""
from __future__ import annotations

import json
import math
import os
import sys
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

warnings.warn(
    "cut_list_engine.py is DEPRECATED. Use fabrication_builder.py instead — "
    "it reads cut lengths from the resolved_model produced by geometry_engine.py.",
    DeprecationWarning,
    stacklevel=2,
)

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import outputs_dir, staging_dir


def get_standard_length(cut_length: float) -> int:
    """Rounds up to standard nominal lumber order length (even numbers)."""
    if cut_length <= 8:
        return 8
    if cut_length <= 10:
        return 10
    if cut_length <= 12:
        return 12
    if cut_length <= 14:
        return 14
    if cut_length <= 16:
        return 16
    return int(math.ceil(cut_length / 2.0) * 2)


def parse_member_dimensions(
    posts_data: Dict[str, Any],
    beams_data: Dict[str, Any],
    roof_data: Dict[str, Any],
) -> Tuple[float, float, float, float, float, float]:
    """Extracts actual width and depth dimensions in inches for framing members."""
    post_w = float(posts_data.get("width_in") or posts_data.get("actual_width_in") or 6.0)
    post_d = float(posts_data.get("depth_in") or posts_data.get("actual_depth_in") or 6.0)
    beam_w = float(beams_data.get("width_in") or beams_data.get("actual_width_in") or 4.0)
    beam_d = float(beams_data.get("depth_in") or beams_data.get("actual_depth_in") or 8.0)
    raf_spec = roof_data.get("rafters") or roof_data.get("primary_rafters") or {}
    rafter_w = float(raf_spec.get("width_in") or raf_spec.get("actual_width_in") or 4.0)
    rafter_d = float(raf_spec.get("depth_in") or raf_spec.get("actual_depth_in") or 6.0)
    return (post_w, post_d, beam_w, beam_d, rafter_w, rafter_d)


def compute_member_spans(
    posts_data: Dict[str, Any],
    model: Dict[str, Any],
    calcs: Dict[str, Any],
    roof_data: Dict[str, Any],
    qty: int,
) -> Tuple[float, float, float]:
    """Calculates cut lengths for posts, ring beams, and rafters."""
    post_cut_ft = posts_data.get("cutLength_ft") or posts_data.get("cut_length_ft") or 8.33
    span_ft = posts_data.get("spanDistance_ft") or (model.get("layout") or {}).get("inscribed_radius_ft") or 5.0

    rafter_len_ft = (calcs.get("rafter") or {}).get("total_with_overhang_ft") or 0.0
    if rafter_len_ft == 0:
        pitch = roof_data.get("pitch") or "4:12"
        pr, rr = [float(x) for x in pitch.split(":")]
        slope_factor = math.sqrt(1 + (pr / rr) ** 2)
        overhang_ft = (float(model.get("overhang_in") or 12.0)) / 12.0
        rafter_len_ft = (span_ft + overhang_ft) * slope_factor

    beam_len_ft = 2 * span_ft * math.tan(math.radians(180 / qty)) if qty > 4 else span_ft
    return (post_cut_ft, beam_len_ft, rafter_len_ft)


def build_post_record(post_w: float, post_d: float, post_cut_ft: float, qty: int) -> Dict[str, Any]:
    """Builds cut list entry for main framing posts."""
    p_order = get_standard_length(post_cut_ft)
    p_bf_net = (post_w * post_d / 12.0) * post_cut_ft
    p_bf_order = (post_w * post_d / 12.0) * p_order
    return {
        "id": "M01",
        "name": "Main posts",
        "profile": f"{int(post_w)}x{int(post_d)}",
        "width_in": post_w,
        "depth_in": post_d,
        "cut_length_ft": round(post_cut_ft, 2),
        "qty": qty,
        "order_length_ft": p_order,
        "bf_per_piece_net": round(p_bf_net, 2),
        "bf_per_piece_order": round(p_bf_order, 2),
        "bf_total_net": round(p_bf_net * qty, 2),
        "bf_total_order": round(p_bf_order * qty, 2),
    }


def build_beam_record(beam_w: float, beam_d: float, beam_len_ft: float, qty: int) -> Dict[str, Any]:
    """Builds cut list entry for perimeter ring beams."""
    b_order = get_standard_length(beam_len_ft)
    b_bf_net = (beam_w * beam_d / 12.0) * beam_len_ft
    b_bf_order = (beam_w * beam_d / 12.0) * b_order
    return {
        "id": "M02",
        "name": "Ring beams",
        "profile": f"{int(beam_w)}x{int(beam_d)}",
        "width_in": beam_w,
        "depth_in": beam_d,
        "cut_length_ft": round(beam_len_ft, 2),
        "qty": qty,
        "order_length_ft": b_order,
        "bf_per_piece_net": round(b_bf_net, 2),
        "bf_per_piece_order": round(b_bf_order, 2),
        "bf_total_net": round(b_bf_net * qty, 2),
        "bf_total_order": round(b_bf_order * qty, 2),
    }


def build_rafter_record(rafter_w: float, rafter_d: float, rafter_len_ft: float, qty: int) -> Dict[str, Any]:
    """Builds cut list entry for primary roof hip rafters."""
    r_order = get_standard_length(rafter_len_ft)
    r_bf_net = (rafter_w * rafter_d / 12.0) * rafter_len_ft
    r_bf_order = (rafter_w * rafter_d / 12.0) * r_order
    return {
        "id": "M03",
        "name": "Hip rafters",
        "profile": f"{int(rafter_w)}x{int(rafter_d)}",
        "width_in": rafter_w,
        "depth_in": rafter_d,
        "cut_length_ft": round(rafter_len_ft, 2),
        "qty": qty,
        "order_length_ft": r_order,
        "bf_per_piece_net": round(r_bf_net, 2),
        "bf_per_piece_order": round(r_bf_order, 2),
        "bf_total_net": round(r_bf_net * qty, 2),
        "bf_total_order": round(r_bf_order * qty, 2),
    }


def build_hub_record(post_w: float) -> Dict[str, Any]:
    """Builds cut list entry for central apex hub block."""
    h_order = get_standard_length(2.0)
    h_bf_net = (post_w * post_w / 12.0) * 2.0
    h_bf_order = (post_w * post_w / 12.0) * h_order
    return {
        "id": "M04",
        "name": "Central hub",
        "profile": f"{int(post_w)}x{int(post_w)}",
        "width_in": post_w,
        "depth_in": post_w,
        "cut_length_ft": 2.0,
        "qty": 1,
        "order_length_ft": h_order,
        "bf_per_piece_net": round(h_bf_net, 2),
        "bf_per_piece_order": round(h_bf_order, 2),
        "bf_total_net": round(h_bf_net * 1, 2),
        "bf_total_order": round(h_bf_order * 1, 2),
    }


def build_brace_record(bracing: Dict[str, Any], default_qty: int) -> Optional[Dict[str, Any]]:
    """Builds cut list entry for lateral knee braces if present."""
    if not bracing:
        return None
    brace_qty = bracing.get("total_qty") or (default_qty * 2)
    first_brace = (bracing.get("braces") or [{}])[0]
    brace_len = float(first_brace.get("length_in") or 36.0) / 12.0
    brace_mat = first_brace.get("material") or "4x4"
    if "x" in brace_mat:
        parts = brace_mat.split(" ")[0].split("x")
        bw, bd = float(parts[0]), float(parts[1])
    else:
        bw, bd = 4.0, 4.0

    br_order = get_standard_length(brace_len)
    br_bf_net = (bw * bd / 12.0) * brace_len
    br_bf_order = (bw * bd / 12.0) * br_order
    return {
        "id": "M05",
        "name": "Knee braces",
        "profile": f"{int(bw)}x{int(bd)}",
        "width_in": bw,
        "depth_in": bd,
        "cut_length_ft": round(brace_len, 2),
        "qty": brace_qty,
        "order_length_ft": br_order,
        "bf_per_piece_net": round(br_bf_net, 2),
        "bf_per_piece_order": round(br_bf_order, 2),
        "bf_total_net": round(br_bf_net * brace_qty, 2),
        "bf_total_order": round(br_bf_order * brace_qty, 2),
    }


def compute_cut_list(
    model_path: str,
    calcs_path: str,
    bracing_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Computes full bill of materials cut list and board feet totals from model dicts."""
    with open(model_path, encoding="utf-8") as f:
        model = json.load(f)
    with open(calcs_path, encoding="utf-8") as f:
        calcs = json.load(f)

    bracing = {}
    if bracing_path and os.path.exists(bracing_path):
        with open(bracing_path, encoding="utf-8") as f:
            bracing = json.load(f)

    members = model.get("members") or model.get("structuralElements", {})
    posts_data = members.get("posts", {})
    beams_data = members.get("beams") or members.get("ringBeams", {})
    roof_data = members.get("roofStructure") or model.get("roofStructure", {})

    layout = model.get("layout") or {}
    qty = posts_data.get("quantity") or posts_data.get("count") or layout.get("post_count") or 4
    post_cut_ft, beam_len_ft, rafter_len_ft = compute_member_spans(posts_data, model, calcs, roof_data, qty)
    post_w, post_d, beam_w, beam_d, rafter_w, rafter_d = parse_member_dimensions(posts_data, beams_data, roof_data)

    results = [
        build_post_record(post_w, post_d, post_cut_ft, qty),
        build_beam_record(beam_w, beam_d, beam_len_ft, qty),
        build_rafter_record(rafter_w, rafter_d, rafter_len_ft, qty),
        build_hub_record(post_w),
    ]

    brace_rec = build_brace_record(bracing, qty)
    if brace_rec:
        results.append(brace_rec)

    total_net = sum(r["bf_total_net"] for r in results)
    total_order = sum(r["bf_total_order"] for r in results)
    waste_factor = 0.10
    total_with_waste = total_order * (1 + waste_factor)

    return {
        "schema": "garden-structure-designer/cut-list/1.0",
        "source_hash": calcs.get("source_hash") or (calcs.get("meta") or {}).get("source_hash") or "",
        "members": results,
        "totals": {
            "bf_net": round(total_net, 1),
            "bf_order": round(total_order, 1),
            "waste_factor": waste_factor,
            "bf_with_waste": round(total_with_waste, 1),
        },
    }


def main() -> None:
    """CLI entrypoint computing cut list and saving outputs/shop-blueprint/SB01-cut-list.json."""
    m_path = sys.argv[1] if len(sys.argv) > 1 else str(staging_dir() / "structure.json")
    c_path = sys.argv[2] if len(sys.argv) > 2 else m_path
    b_path = sys.argv[3] if len(sys.argv) > 3 else None

    result = compute_cut_list(m_path, c_path, b_path)
    out_dir = outputs_dir() / "shop-blueprint"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "SB01-cut-list.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Generated {out_file}")


if __name__ == "__main__":
    main()
