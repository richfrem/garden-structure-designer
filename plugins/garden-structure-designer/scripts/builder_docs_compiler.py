#!/usr/bin/env python3
"""
builder_docs_compiler.py (CLI)
=====================================

Purpose:
    Produces builder-facing documents (budget-estimate.md, lumber-purchase-list.md, assembly-guide.md)
    from deterministic staging artifacts structure.json and SB01-cut-list.json.

Layer: Execution / Document Generation

Usage Examples:
    python builder_docs_compiler.py [staging_dir] [outputs_dir]

CLI Arguments:
    staging_dir: Optional path to context/staging directory.
    outputs_dir: Optional path to outputs directory.

Input Files:
    context/staging/structure.json
    outputs/shop-blueprint/SB01-cut-list.json

Output:
    outputs/budget-estimate.md
    outputs/lumber-purchase-list.md
    outputs/assembly-guide.md
"""

import sys
import os
import json
from pathlib import Path
import typing

# Ensure path_utils can be imported
sys.path.append(str(Path(__file__).parent))
from path_utils import staging_dir as default_staging_dir, outputs_dir as default_outputs_dir

def generate_lumber_purchase_list(structure: dict, cut_list: dict) -> str:
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
        "|---|---|---|---|---|---|"
    ]
    
    # Posts
    posts = members.get("posts", {})
    p_qty = (structure.get("layout") or {}).get("post_count") or 6
    p_cut = posts.get("cut_length_ft") or 8.0
    p_stock = max(8.0, math_ceil(p_cut + 1.0))
    p_bf = posts.get("board_feet") or 0.0
    p_nom = posts.get("nominal_size") or "6x6"
    lines.append(f"| Posts | {p_nom} | {p_qty} | {p_cut:.2f}' | {p_stock:.1f}' | {p_bf:.2f} |")
    
    # Beams
    beams = members.get("beams", {})
    b_qty = p_qty
    b_cut = beams.get("cut_length_ft") or posts.get("cut_length_ft") or 10.0
    b_stock = max(10.0, math_ceil(b_cut + 1.0))
    b_bf = beams.get("board_feet") or 0.0
    b_nom = beams.get("nominal_size") or "6x12"
    lines.append(f"| Beams | {b_nom} | {b_qty} | {b_cut:.2f}' | {b_stock:.1f}' | {b_bf:.2f} |")
    
    # Rafters
    raf = roof.get("primary_rafters", {})
    r_qty = raf.get("count") or p_qty
    r_cut = raf.get("cut_length_ft") or 8.5
    r_stock = max(10.0, math_ceil(r_cut + 1.5))
    r_bf = raf.get("board_feet") or 0.0
    r_nom = raf.get("nominal_size") or "4x6"
    lines.append(f"| Primary Rafters | {r_nom} | {r_qty} | {r_cut:.2f}' | {r_stock:.1f}' | {r_bf:.2f} |")
    
    # Braces
    if bracing.get("enabled"):
        br = bracing.get("brace", {})
        br_qty = (br.get("count_per_post") or 2) * p_qty
        br_bf = br.get("board_feet") or 0.0
        br_nom = br.get("nominal_size") or "4x4"
        lines.append(f"| Knee Braces | {br_nom} | {br_qty} | 3.00' | 8.0' (cut 2/board) | {br_bf:.2f} |")
        
    lines.extend([
        "\n## 2. Hardware Schedule",
        "- Post Standoff Bases: Heavy-duty 6x6 galvanized post bases (Qty: " + str(p_qty) + ")",
        "- Structural Screws / Lags: 1/2\" x 6\" RSS Heavy Duty Screws (Qty: " + str(p_qty * 8) + ")",
        "- Rafter Seat Fasteners: Hurricane ties / structural timber screws (Qty: " + str(r_qty * 2) + ")",
        "- Concrete Footings: 18\" diameter caissons with J-bolts (Qty: " + str(p_qty) + ")"
    ])
    
    return "\n".join(lines)

def generate_budget_estimate(structure: dict, cut_list: dict) -> str:
    region = structure.get("jurisdiction", {}).get("region") or "BC_Vancouver_Island"
    total_bf = cut_list.get("total_board_feet") or 600.0
    
    rate_per_bf = 4.50
    lumber_cost = total_bf * rate_per_bf
    hardware_cost = 450.00
    roofing_cost = 350.00
    foundation_cost = 600.00
    total_materials = lumber_cost + hardware_cost + roofing_cost + foundation_cost
    
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
        "- **SUPPLIER RECOMMENDATIONS:** Sourced via regional timber suppliers in " + region.replace("_", " ") + "."
    ]
    return "\n".join(lines)

def generate_assembly_guide(structure: dict, cut_list: dict) -> str:
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
            "6. Secure structural fasteners and pegs only after all six rafters are seated and verified.\n"
        ])
    else:
        lines.append("1. Install ridge beam and primary rafters according to roof framing plan.\n")
        
    lines.extend([
        "## Phase 4 — Roof Decking & Finishing",
        "1. Install roof tongue-and-groove decking or purlins.",
        "2. Apply underlayment and roofing shingles.",
        "3. Remove temporary bracing once structural knee braces are fully secured."
    ])
    return "\n".join(lines)

def math_ceil(val: float) -> float:
    import math
    return float(math.ceil(val))

def generate_builder_docs(staging_dir: Path = None, outputs_dir: Path = None) -> dict:
    if staging_dir is None:
        staging_dir = default_staging_dir()
    if outputs_dir is None:
        outputs_dir = default_outputs_dir()
        
    staging_dir = Path(staging_dir)
    outputs_dir = Path(outputs_dir)
    
    struct_path = staging_dir / "structure.json"
    cut_list_path = outputs_dir / "shop-blueprint" / "SB01-cut-list.json"
    
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
    
    outputs_dir.mkdir(parents=True, exist_ok=True)
    
    with open(outputs_dir / "lumber-purchase-list.md", "w", encoding="utf-8") as f:
        f.write(lumber_md)
    with open(outputs_dir / "budget-estimate.md", "w", encoding="utf-8") as f:
        f.write(budget_md)
    with open(outputs_dir / "assembly-guide.md", "w", encoding="utf-8") as f:
        f.write(assembly_md)
        
    return {
        "stage": "builder-docs-generator",
        "status": "COMPLETE",
        "outputs": [
            str(outputs_dir / "lumber-purchase-list.md"),
            str(outputs_dir / "budget-estimate.md"),
            str(outputs_dir / "assembly-guide.md")
        ],
        "regional_pricing": structure.get("jurisdiction", {}).get("region") or "BC_Vancouver_Island",
        "next_stage": "document-compiler"
    }

def main():
    s_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    o_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    res = generate_builder_docs(s_dir, o_dir)
    print(json.dumps(res, indent=2))
    if res["status"] != "COMPLETE":
        sys.exit(1)

if __name__ == "__main__":
    main()
