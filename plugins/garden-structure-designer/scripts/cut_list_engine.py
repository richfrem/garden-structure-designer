#!/usr/bin/env python3
"""
cut_list_engine.py (CLI)
=====================================

Purpose:
    cut_list_engine.py Computes exact cut lengths and board-foot (BF) totals deterministically.

Layer: Execution

Usage Examples:
    python cut_list_engine.py [args]

Supported Object Types:
    JSON, SVG, Markdown

CLI Arguments:
    Varies per script, typically input file paths.

Input Files:
    context/staging/ *.json outputs/ *.svg

Output:
    Validation codes (0 or 1), generated JSON or SVG files.

Key Functions:
    Refer to module docstring or inner functions.

Script Dependencies:
    Standard library json, os, sys, math, hashlib, etc.

Consumed by:
    design-orchestrator, various skills in the pipeline.
"""
import json
import math
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import outputs_dir, staging_dir, schemas_dir, scripts_dir, agent_workspace_dir



def get_standard_length(cut_length: float) -> int:
    """Round up to the nearest standard lumber stock length (even numbers)."""
    if cut_length <= 8: return 8
    if cut_length <= 10: return 10
    if cut_length <= 12: return 12
    if cut_length <= 14: return 14
    if cut_length <= 16: return 16
    return math.ceil(cut_length / 2.0) * 2

def compute_cut_list(model_path: str, calcs_path: str, bracing_path: str = None) -> dict:
    with open(model_path) as f:
        model = json.load(f)
    with open(calcs_path) as f:
        calcs = json.load(f)
        
    bracing = {}
    if bracing_path and os.path.exists(bracing_path):
        with open(bracing_path) as f:
            bracing = json.load(f)

    members = model.get("members") or model.get("structuralElements", {})
    posts_data = members.get("posts", {})
    beams_data = members.get("beams") or members.get("ringBeams", {})
    roof_data = members.get("roofStructure") or model.get("roofStructure", {})

    qty = posts_data.get("quantity", 4)
    post_cut_ft = posts_data.get("cutLength_ft", 8.33)
    span_ft = posts_data.get("spanDistance_ft", 5.0)

    # Calculate actual lengths
    rafter_len_ft = calcs.get("rafter", {}).get("total_with_overhang_ft", 0)
    if rafter_len_ft == 0:
        # Fallback if geometry calc was missing something
        pitch = roof_data.get("pitch", "4:12")
        pr, rr = [float(x) for x in pitch.split(":")]
        slope_factor = math.sqrt(1 + (pr / rr) ** 2)
        overhang_ft = model.get("overhang_in", 12.0) / 12.0
        rafter_len_ft = (span_ft + overhang_ft) * slope_factor

    # Beams (assume perimeter approximation)
    interior_angle = (qty - 2) * 180.0 / qty
    beam_len_ft = 2 * span_ft * math.tan(math.radians(180/qty)) if qty > 4 else span_ft

    post_w = float(posts_data.get("width_in", 6))
    post_d = float(posts_data.get("depth_in", 6))
    beam_w = float(beams_data.get("width_in", 4))
    beam_d = float(beams_data.get("depth_in", 8))
    rafter_w = float(roof_data.get("rafters", {}).get("width_in", 4))
    rafter_d = float(roof_data.get("rafters", {}).get("depth_in", 6))

    results = []

    # 1. Posts
    p_order = get_standard_length(post_cut_ft)
    p_bf_net = (post_w * post_d / 12.0) * post_cut_ft
    p_bf_order = (post_w * post_d / 12.0) * p_order
    results.append({
        "id": "M01",
        "name": "Main posts",
        "profile": f"{int(post_w)}x{int(post_d)}",
        "width_in": post_w, "depth_in": post_d,
        "cut_length_ft": round(post_cut_ft, 2),
        "qty": qty,
        "order_length_ft": p_order,
        "bf_per_piece_net": round(p_bf_net, 2),
        "bf_per_piece_order": round(p_bf_order, 2),
        "bf_total_net": round(p_bf_net * qty, 2),
        "bf_total_order": round(p_bf_order * qty, 2)
    })

    # 2. Beams
    b_order = get_standard_length(beam_len_ft)
    b_bf_net = (beam_w * beam_d / 12.0) * beam_len_ft
    b_bf_order = (beam_w * beam_d / 12.0) * b_order
    results.append({
        "id": "M02",
        "name": "Ring beams",
        "profile": f"{int(beam_w)}x{int(beam_d)}",
        "width_in": beam_w, "depth_in": beam_d,
        "cut_length_ft": round(beam_len_ft, 2),
        "qty": qty,
        "order_length_ft": b_order,
        "bf_per_piece_net": round(b_bf_net, 2),
        "bf_per_piece_order": round(b_bf_order, 2),
        "bf_total_net": round(b_bf_net * qty, 2),
        "bf_total_order": round(b_bf_order * qty, 2)
    })

    # 3. Rafters
    r_order = get_standard_length(rafter_len_ft)
    r_bf_net = (rafter_w * rafter_d / 12.0) * rafter_len_ft
    r_bf_order = (rafter_w * rafter_d / 12.0) * r_order
    results.append({
        "id": "M03",
        "name": "Hip rafters",
        "profile": f"{int(rafter_w)}x{int(rafter_d)}",
        "width_in": rafter_w, "depth_in": rafter_d,
        "cut_length_ft": round(rafter_len_ft, 2),
        "qty": qty,
        "order_length_ft": r_order,
        "bf_per_piece_net": round(r_bf_net, 2),
        "bf_per_piece_order": round(r_bf_order, 2),
        "bf_total_net": round(r_bf_net * qty, 2),
        "bf_total_order": round(r_bf_order * qty, 2)
    })

    # 4. Hub (assume 2ft of same dimension as post)
    h_order = get_standard_length(2.0)
    h_bf_net = (post_w * post_w / 12.0) * 2.0
    h_bf_order = (post_w * post_w / 12.0) * h_order
    results.append({
        "id": "M04",
        "name": "Central hub",
        "profile": f"{int(post_w)}x{int(post_w)}",
        "width_in": post_w, "depth_in": post_w,
        "cut_length_ft": 2.0,
        "qty": 1,
        "order_length_ft": h_order,
        "bf_per_piece_net": round(h_bf_net, 2),
        "bf_per_piece_order": round(h_bf_order, 2),
        "bf_total_net": round(h_bf_net * 1, 2),
        "bf_total_order": round(h_bf_order * 1, 2)
    })

    # 5. Bracing
    if bracing:
        brace_qty = bracing.get("total_qty", qty * 2)
        brace_len = bracing.get("braces", [{}])[0].get("length_in", 36) / 12.0
        brace_mat = bracing.get("braces", [{}])[0].get("material", "4x4")
        if "x" in brace_mat:
            bw, bd = brace_mat.split(" ")[0].split("x")
            bw, bd = float(bw), float(bd)
        else:
            bw, bd = 4.0, 4.0
        
        br_order = get_standard_length(brace_len)
        br_bf_net = (bw * bd / 12.0) * brace_len
        br_bf_order = (bw * bd / 12.0) * br_order
        results.append({
            "id": "M05",
            "name": "Knee braces",
            "profile": f"{int(bw)}x{int(bd)}",
            "width_in": bw, "depth_in": bd,
            "cut_length_ft": round(brace_len, 2),
            "qty": brace_qty,
            "order_length_ft": br_order,
            "bf_per_piece_net": round(br_bf_net, 2),
            "bf_per_piece_order": round(br_bf_order, 2),
            "bf_total_net": round(br_bf_net * brace_qty, 2),
            "bf_total_order": round(br_bf_order * brace_qty, 2)
        })

    # Totals
    total_net = sum(r["bf_total_net"] for r in results)
    total_order = sum(r["bf_total_order"] for r in results)
    waste_factor = 0.10
    total_with_waste = total_order * (1 + waste_factor)

    return {
        "schema": "garden-structure-designer/cut-list/1.0",
        "source_hash": calcs.get("source_hash", ""),
        "members": results,
        "totals": {
            "bf_net": round(total_net, 1),
            "bf_order": round(total_order, 1),
            "waste_factor": waste_factor,
            "bf_with_waste": round(total_with_waste, 1)
        }
    }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 cut_list_engine.py <model.json> <calcs.json> [bracing.json]")
        sys.exit(1)
    
    model_path = sys.argv[1]
    calcs_path = sys.argv[2]
    bracing_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = compute_cut_list(model_path, calcs_path, bracing_path)
    
    # Ensure outputs dir exists
    out_dir = os.path.join(os.path.dirname(model_path), "..", "..", "outputs", "shop-blueprint")
    os.makedirs(out_dir, exist_ok=True)
    
    out_file = os.path.join(out_dir, "SB01-cut-list.json")
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
        
    print(f"Generated {out_file}")
