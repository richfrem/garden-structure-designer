#!/usr/bin/env python3
"""
builder_docs_compiler.py
========================

Purpose:
    Produces builder-facing construction documents (budget-estimate.md,
    lumber-purchase-list.md, assembly-guide.md) from deterministic staging
    artifacts structure.json and SB01-cut-list.json.

Layer: Execution / Document Generation

Key Input Dependencies:
    - context/staging/structure.json (structural specification and geometry)
    - outputs/shop-blueprint/SB01-cut-list.json (cut list dimensions and board feet)

Key Functions:
    build_post_row(posts, p_qty) -> str
    build_beam_row(beams, posts, p_qty) -> str
    build_rafter_row(raf, p_qty) -> str
    build_brace_row(bracing, p_qty) -> list[str]
    build_timber_schedule_rows(members, roof, bracing, p_qty) -> list[str]
    generate_lumber_purchase_list(structure, cut_list) -> str
    generate_budget_estimate(structure, cut_list) -> str
    generate_assembly_guide(structure, cut_list) -> str
    generate_builder_docs(staging_dir=None, outputs_dir=None) -> dict
    math_ceil(val) -> float
    main() -> None

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/builder_docs_compiler.py [staging_dir] [outputs_dir]
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.append(str(Path(__file__).parent))
from path_utils import outputs_dir as default_outputs_dir
from path_utils import staging_dir as default_staging_dir


def math_ceil(val: float) -> float:
    """Returns the ceiling of a float value as a float."""
    return float(math.ceil(val))


def build_post_row(posts: Dict[str, Any], p_qty: int) -> str:
    """Formats markdown row for posts."""
    p_cut = posts.get("cut_length_ft") or 8.0
    p_stock = max(8.0, math_ceil(p_cut + 1.0))
    p_bf = posts.get("board_feet") or 0.0
    p_nom = posts.get("nominal_size") or "6x6"
    return f"| Posts | {p_nom} | {p_qty} | {p_cut:.2f}' | {p_stock:.1f}' | {p_bf:.2f} |"


def build_beam_row(beams: Dict[str, Any], posts: Dict[str, Any], p_qty: int) -> str:
    """Formats markdown row for beams."""
    b_qty = p_qty
    b_cut = beams.get("cut_length_ft") or posts.get("cut_length_ft") or 10.0
    b_stock = max(10.0, math_ceil(b_cut + 1.0))
    b_bf = beams.get("board_feet") or 0.0
    b_nom = beams.get("nominal_size") or "6x12"
    return f"| Beams | {b_nom} | {b_qty} | {b_cut:.2f}' | {b_stock:.1f}' | {b_bf:.2f} |"


def build_rafter_row(raf: Dict[str, Any], p_qty: int) -> str:
    """Formats markdown row for rafters."""
    r_qty = raf.get("count") or p_qty
    r_cut = raf.get("cut_length_ft") or 8.5
    r_stock = max(10.0, math_ceil(r_cut + 1.5))
    r_bf = raf.get("board_feet") or 0.0
    r_nom = raf.get("nominal_size") or "4x6"
    return f"| Primary Rafters | {r_nom} | {r_qty} | {r_cut:.2f}' | {r_stock:.1f}' | {r_bf:.2f} |"


def build_brace_row(bracing: Dict[str, Any], p_qty: int) -> List[str]:
    """Formats markdown row for knee braces when enabled."""
    if not bracing.get("enabled"):
        return []
    br = bracing.get("brace", {})
    br_qty = (br.get("count_per_post") or 2) * p_qty
    br_bf = br.get("board_feet") or 0.0
    br_nom = br.get("nominal_size") or "4x4"
    return [f"| Knee Braces | {br_nom} | {br_qty} | 3.00' | 8.0' (cut 2/board) | {br_bf:.2f} |"]


def build_timber_schedule_rows(
    members: Dict[str, Any],
    roof: Dict[str, Any],
    bracing: Dict[str, Any],
    p_qty: int,
) -> List[str]:
    """Builds markdown table rows for posts, beams, rafters, and knee braces."""
    rows: List[str] = [
        build_post_row(members.get("posts", {}), p_qty),
        build_beam_row(members.get("beams", {}), members.get("posts", {}), p_qty),
        build_rafter_row(roof.get("primary_rafters", {}), p_qty),
    ]
    rows.extend(build_brace_row(bracing, p_qty))
    return rows


def generate_lumber_purchase_list(structure: Dict[str, Any], cut_list: Dict[str, Any]) -> str:
    """Generates the formatted markdown lumber purchase and hardware procurement list."""
    region = structure.get("jurisdiction", {}).get("region") or "BC_Vancouver_Island"
    members = structure.get("members", {})
    roof = structure.get("roof", {})
    bracing = structure.get("bracing", {})

    total_bf_val = cut_list.get("total_board_feet") or cut_list.get("totals", {}).get("bf_net") or 0.0
    lines = [
        "# Lumber Purchase & Hardware Procurement List",
        f"**Jurisdiction / Region:** {region}",
        f"**Total Board Feet (Net Fabrication):** {total_bf_val:.2f} BF\n",
        "## 1. Timber Schedule (Order Lengths Include Waste Allowance)",
        "| Member Role | Nominal Size | Quantity | Cut Length (ft) | Recommended Stock Order Length | Subtotal (BF) |",
        "|---|---|---|---|---|---|",
    ]

    p_qty = (structure.get("layout") or {}).get("post_count") or 6
    lines.extend(build_timber_schedule_rows(members, roof, bracing, p_qty))

    raf = roof.get("primary_rafters", {})
    r_qty = raf.get("count") or p_qty
    lines.extend([
        "\n## 2. Hardware Schedule",
        f"- Post Standoff Bases: Heavy-duty 6x6 galvanized post bases (Qty: {p_qty})",
        f"- Structural Screws / Lags: 1/2\" x 6\" RSS Heavy Duty Screws (Qty: {p_qty * 8})",
        f"- Rafter Seat Fasteners: Hurricane ties / structural timber screws (Qty: {r_qty * 2})",
        f"- Concrete Footings: 18\" diameter caissons with J-bolts (Qty: {p_qty})",
    ])

    return "\n".join(lines)


def generate_budget_estimate(structure: Dict[str, Any], cut_list: Dict[str, Any]) -> str:
    """Generates the estimated material costs breakdown markdown document."""
    region = structure.get("jurisdiction", {}).get("region") or "BC_Vancouver_Island"
    total_bf = cut_list.get("total_board_feet") or 600.0

    rate_per_bf = 4.50
    lumber_cost = total_bf * rate_per_bf
    hardware_cost = 450.00
    roofing_cost = 350.00
    foundation_cost = 600.00
    total_materials = lumber_cost + hardware_cost + roofing_cost + foundation_cost

    region_display = region.replace("_", " ")
    lines = [
        "# Budget Estimate & Material Cost Breakdown",
        f"**Pricing Region:** {region} (Default Rate Basis)",
        f"**Estimated Material Subtotal:** ${total_materials:,.2f} CAD\n",
        "## 1. Material Cost Line Items",
        f"- **Structural Timber ({total_bf:.1f} BF @ ${rate_per_bf:.2f}/BF):** ${lumber_cost:,.2f}",
        f"- **Hardware & Fasteners:** ${hardware_cost:,.2f}",
        f"- **Roofing & Decking Materials:** ${roofing_cost:,.2f}",
        f"- **Foundation Concrete & Rebar:** ${foundation_cost:,.2f}\n",
        "## 2. Mandatory Disclosures & Exclusions",
        "- **LABOR EXCLUSION:** This estimate covers materials ONLY. Professional timber frame installation labor is estimated at **$2,500.00 – $4,500.00** depending on site accessibility.",
        "- **TAX EXCLUSION:** Prices exclude provincial/federal sales taxes (GST/PST/HST) and local delivery fees.",
        f"- **SUPPLIER RECOMMENDATIONS:** Sourced via regional timber suppliers in {region_display}.",
    ]
    return "\n".join(lines)


def generate_assembly_guide(structure: Dict[str, Any], cut_list: Dict[str, Any]) -> str:
    """Generates the site erection and assembly sequence guide markdown."""
    layout = structure.get("layout", {})
    shape = layout.get("shape") or "hexagon"
    geom = structure.get("geometry", {})
    cc = geom.get("compound_cut", {})
    miter = cc.get("miter_deg") or 28.71
    bevel = cc.get("bevel_deg") or 9.10
    bm = (geom.get("beam_ring") or {}).get("beam_miter_deg") or 30.0

    lines = [
        "# Structural Assembly & Site Erection Guide",
        f"**Structure Type:** {shape.title()} Timber Frame",
        f"**Saw Setting Verification:** Rafter Plumb Cut Miter: {miter:.2f}°, Bevel: {bevel:.2f}° | Beam Ring Miter: {bm:.2f}°\n",
        "> **TEST-CUT MANDATORY WARNING:** Always make test cuts on scrap lumber pieces before cutting expensive final timber members to confirm bevel and miter blade setups.\n",
        "## Phase 1 — Site Layout & Foundation",
        "1. Establish central benchmark and layout points using string lines and transit.",
        "2. Excavate caisson footings below local frost line.",
        "3. Pour concrete footings and wet-set J-bolts/post anchors.\n",
        "## Phase 2 — Post & Beam Ring Erection",
        "1. Mount standoff post bases to anchor bolts.",
        "2. Erect posts, plumb with level, and install temporary diagonal bracing.",
        f"3. Fly beam ring members (mitered at {bm:.2f}°) and fasten beam-to-post joints.\n",
        "## Phase 3 — Hub & Rafter Assembly",
    ]

    if shape == "hexagon" or structure.get("hub", {}).get("type") != "none":
        lines.extend([
            "### Phase 4.3 — Tripod-First Hub and Rafter Hoisting",
            "1. Install three alternating rafters into the central hub on ground level.",
            "2. Hoist this tripod assembly onto three alternating beam seats on the beam ring.",
            "3. Temporarily brace the tripod to the beam ring to establish stable self-supporting apex.",
            "4. Install the remaining three rafters one at a time into the open hub slots.",
            "5. Confirm hub is centred over the layout stake with plumb bob.",
            "6. Secure structural fasteners and pegs only after all six rafters are seated and verified.\n",
        ])
    else:
        lines.append("1. Install ridge beam and primary rafters according to roof framing plan.\n")

    lines.extend([
        "## Phase 4 — Roof Decking & Finishing",
        "1. Install roof tongue-and-groove decking or purlins.",
        "2. Apply underlayment and roofing shingles.",
        "3. Remove temporary bracing once structural knee braces are fully secured.",
    ])
    return "\n".join(lines)


def generate_builder_docs(
    staging_dir: Optional[Path] = None,
    outputs_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Loads inputs, produces all 3 markdown documents, and outputs stage results."""
    s_dir = Path(staging_dir) if staging_dir is not None else default_staging_dir()
    o_dir = Path(outputs_dir) if outputs_dir is not None else default_outputs_dir()

    struct_path = s_dir / "structure.json"
    cut_list_path = o_dir / "shop-blueprint" / "SB01-cut-list.json"

    if not struct_path.exists():
        return {"status": "FAIL", "reason": f"structure.json missing at {struct_path}"}

    if not cut_list_path.exists():
        return {"status": "FAIL", "reason": f"SB01-cut-list.json missing at {cut_list_path}"}

    with open(struct_path, "r", encoding="utf-8") as f:
        structure = json.load(f)
    with open(cut_list_path, "r", encoding="utf-8") as f:
        cut_list = json.load(f)

    lumber_md = generate_lumber_purchase_list(structure, cut_list)
    budget_md = generate_budget_estimate(structure, cut_list)
    assembly_md = generate_assembly_guide(structure, cut_list)

    o_dir.mkdir(parents=True, exist_ok=True)

    with open(o_dir / "lumber-purchase-list.md", "w", encoding="utf-8") as f:
        f.write(lumber_md)
    with open(o_dir / "budget-estimate.md", "w", encoding="utf-8") as f:
        f.write(budget_md)
    with open(o_dir / "assembly-guide.md", "w", encoding="utf-8") as f:
        f.write(assembly_md)

    return {
        "stage": "builder-docs-generator",
        "status": "COMPLETE",
        "outputs": [
            str(o_dir / "lumber-purchase-list.md"),
            str(o_dir / "budget-estimate.md"),
            str(o_dir / "assembly-guide.md"),
        ],
        "regional_pricing": structure.get("jurisdiction", {}).get("region") or "BC_Vancouver_Island",
        "next_stage": "document-compiler",
    }


def main() -> None:
    """CLI entrypoint for running builder docs compilation."""
    s_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    o_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    res = generate_builder_docs(s_dir, o_dir)
    print(json.dumps(res, indent=2))
    if res["status"] != "COMPLETE":
        sys.exit(1)


if __name__ == "__main__":
    main()
