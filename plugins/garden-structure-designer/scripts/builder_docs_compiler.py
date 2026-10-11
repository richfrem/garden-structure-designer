#!/usr/bin/env python3
"""
builder_docs_compiler.py
========================

Purpose:
    Produces builder-facing construction documents (budget-estimate.md,
    lumber-purchase-list.md, assembly-guide.md) from the deterministic staging
    artifacts ``structure.json`` and ``outputs/fabrication/cut-list.json`` (written
    by fabrication_builder.py). Quantities and lengths come from the cut list, section
    sizes from structure.json, and board feet are derived as (width x depth / 12) x length.
    Every structural input is required: missing data fails closed (no silent defaults).

Layer: Execution / Document Generation

Key Input Dependencies:
    - context/staging/structure.json (jurisdiction, structure.sides, members, roof, bracing, geometry angles)
    - outputs/fabrication/cut-list.json (fabrication-cut-list/1.0 members with stock lengths)
    - path_utils.py (default staging/outputs directories), strict_access.py (fail-closed required inputs)

Key Functions:
    generate_builder_docs(staging_dir=None, outputs_dir=None) -> dict
    generate_lumber_purchase_list(structure, cut_list) -> str
    generate_budget_estimate(structure, cut_list) -> str
    generate_assembly_guide(structure, cut_list) -> str
    build_schedule_groups(structure, cut_list) -> list[dict]
    build_schedule_row(group) -> str
    total_board_feet(groups) -> float
    math_ceil(val) -> float
    main() -> None
    _hub_phase_lines(sides, rafters) -> list[str]

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/builder_docs_compiler.py [staging_dir] [outputs_dir]
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.append(str(Path(__file__).parent))
from path_utils import outputs_dir as default_outputs_dir
from path_utils import staging_dir as default_staging_dir
from strict_access import MissingInputError as BuilderDocsInputError
from strict_access import require as _need

CUT_LIST_RELPATH = Path("fabrication") / "cut-list.json"
BOARD_FEET_DIVISOR = 12.0  # (width_in x depth_in / 12) x length_ft

# Planning allowances disclosed in the budget estimate; not structural inputs.
BUDGET_RATE_PER_BF = 4.50
BUDGET_HARDWARE_CAD = 450.00
BUDGET_ROOFING_CAD = 350.00
BUDGET_FOUNDATION_CAD = 600.00
SCREWS_PER_POST = 8
SEAT_FASTENERS_PER_RAFTER = 2
TRIPOD_RAFTERS = 3

# cut-list role -> (table label, structure.json section path holding the nominal/actual section)
SCHEDULE_ROLES: Dict[str, tuple] = {
    "post": ("Posts", ("members", "posts")),
    "beam": ("Beams", ("members", "beams")),
    "rafter_primary": ("Primary Rafters", ("roof", "primary_rafters")),
    "brace": ("Knee Braces", ("bracing", "brace")),
}


def math_ceil(val: float) -> float:
    """Returns the ceiling of a float value as a float."""
    return float(math.ceil(val))


def _section(structure: Dict[str, Any], path: tuple) -> Dict[str, Any]:
    """Resolves a required structure.json section such as ('members', 'posts')."""
    node: Any = structure
    for depth, key in enumerate(path):
        node = _need(node, key, ".".join(path[:depth]) or "structure")
    return node


def build_schedule_groups(structure: Dict[str, Any], cut_list: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Groups cut-list members by role and derives quantity, lengths and net board feet per group."""
    members = _need(cut_list, "members", "cut-list")
    groups: List[Dict[str, Any]] = []
    for role, (label, path) in SCHEDULE_ROLES.items():
        pieces = [m for m in members if m.get("role") == role]
        if not pieces:
            if role == "brace" and _need(structure, "bracing", "structure").get("enabled"):
                raise BuilderDocsInputError("MISSING_INPUT: cut-list has no brace members while bracing.enabled")
            if role == "brace":
                continue
            raise BuilderDocsInputError(f"MISSING_INPUT: cut-list has no {role} members")
        section = _section(structure, path)
        site = ".".join(path)
        width = float(_need(section, "actual_width_in", site))
        depth = float(_need(section, "actual_depth_in", site))
        cuts = [float(_need(_need(m, "stock", f"cut-list {m.get('id')}"), "cut_length_ft", f"cut-list {m.get('id')}.stock")) for m in pieces]
        orders = [float(m["stock"]["order_length_ft"]) for m in pieces]
        groups.append({
            "role": role, "label": label, "nominal": _need(section, "nominal_size", site), "qty": len(pieces),
            "cut_ft": max(cuts), "order_ft": max(orders),
            "bf": sum(width * depth / BOARD_FEET_DIVISOR * c for c in cuts),
        })
    return groups


def build_schedule_row(group: Dict[str, Any]) -> str:
    """Formats the markdown timber-schedule row for one role group."""
    return (
        f"| {group['label']} | {group['nominal']} | {group['qty']} | {group['cut_ft']:.2f}' "
        f"| {group['order_ft']:.1f}' | {group['bf']:.2f} |"
    )


def total_board_feet(groups: List[Dict[str, Any]]) -> float:
    """Sums net board feet over all role groups."""
    return sum(g["bf"] for g in groups)


def _group_qty(groups: List[Dict[str, Any]], role: str) -> int:
    """Returns the piece count of ``role`` (the schedule always contains posts and rafters)."""
    return next(g["qty"] for g in groups if g["role"] == role)


def generate_lumber_purchase_list(structure: Dict[str, Any], cut_list: Dict[str, Any]) -> str:
    """Generates the formatted markdown lumber purchase and hardware procurement list."""
    region = _need(_need(structure, "jurisdiction", "structure"), "region", "jurisdiction")
    groups = build_schedule_groups(structure, cut_list)
    p_qty, r_qty = _group_qty(groups, "post"), _group_qty(groups, "rafter_primary")
    post_nominal = next(g["nominal"] for g in groups if g["role"] == "post")
    lines = [
        "# Lumber Purchase & Hardware Procurement List",
        f"**Jurisdiction / Region:** {region}",
        f"**Total Board Feet (Net Fabrication):** {total_board_feet(groups):.2f} BF\n",
        "## 1. Timber Schedule (Order Lengths Include Waste Allowance)",
        "| Member Role | Nominal Size | Quantity | Cut Length (ft) | Recommended Stock Order Length | Subtotal (BF) |",
        "|---|---|---|---|---|---|",
        *[build_schedule_row(g) for g in groups],
        "\n## 2. Hardware Schedule",
        f"- Post Standoff Bases: Heavy-duty {post_nominal} galvanized post bases (Qty: {p_qty})",
        f"- Structural Screws / Lags: 1/2\" x 6\" RSS Heavy Duty Screws (Qty: {p_qty * SCREWS_PER_POST})",
        f"- Rafter Seat Fasteners: Hurricane ties / structural timber screws (Qty: {r_qty * SEAT_FASTENERS_PER_RAFTER})",
        f"- Concrete Footings: 18\" diameter caissons with J-bolts (Qty: {p_qty})",
    ]
    return "\n".join(lines)


def generate_budget_estimate(structure: Dict[str, Any], cut_list: Dict[str, Any]) -> str:
    """Generates the estimated material costs breakdown markdown document."""
    region = _need(_need(structure, "jurisdiction", "structure"), "region", "jurisdiction")
    total_bf = total_board_feet(build_schedule_groups(structure, cut_list))
    lumber_cost = total_bf * BUDGET_RATE_PER_BF
    total_materials = lumber_cost + BUDGET_HARDWARE_CAD + BUDGET_ROOFING_CAD + BUDGET_FOUNDATION_CAD

    region_display = region.replace("_", " ")
    lines = [
        "# Budget Estimate & Material Cost Breakdown",
        f"**Pricing Region:** {region} (Default Rate Basis)",
        f"**Estimated Material Subtotal:** ${total_materials:,.2f} CAD\n",
        "## 1. Material Cost Line Items",
        f"- **Structural Timber ({total_bf:.1f} BF @ ${BUDGET_RATE_PER_BF:.2f}/BF):** ${lumber_cost:,.2f}",
        f"- **Hardware & Fasteners:** ${BUDGET_HARDWARE_CAD:,.2f}",
        f"- **Roofing & Decking Materials:** ${BUDGET_ROOFING_CAD:,.2f}",
        f"- **Foundation Concrete & Rebar:** ${BUDGET_FOUNDATION_CAD:,.2f}\n",
        "## 2. Mandatory Disclosures & Exclusions",
        "- **LABOR EXCLUSION:** This estimate covers materials ONLY. Professional timber frame installation labor is estimated at **$2,500.00 – $4,500.00** depending on site accessibility.",
        "- **TAX EXCLUSION:** Prices exclude provincial/federal sales taxes (GST/PST/HST) and local delivery fees.",
        f"- **SUPPLIER RECOMMENDATIONS:** Sourced via regional timber suppliers in {region_display}.",
    ]
    return "\n".join(lines)


def _hub_phase_lines(sides: int, rafters: int) -> List[str]:
    """Hub/rafter hoisting steps; the tripod method applies only when the rafters divide into three equal sets."""
    if sides % TRIPOD_RAFTERS == 0:
        step = sides // TRIPOD_RAFTERS
        spacing = "alternating " if step == 2 else f"every {step}th "
        return [
            "### Phase 4.3 — Tripod-First Hub and Rafter Hoisting",
            f"1. Install three {spacing}rafters into the central hub on ground level.",
            f"2. Hoist this tripod assembly onto three {spacing}beam seats on the beam ring.",
            "3. Temporarily brace the tripod to the beam ring to establish stable self-supporting apex.",
            f"4. Install the remaining {rafters - TRIPOD_RAFTERS} rafters one at a time into the open hub slots.",
            "5. Confirm hub is centred over the layout stake with plumb bob.",
            f"6. Secure structural fasteners and pegs only after all {rafters} rafters are seated and verified.\n",
        ]
    return [
        "### Phase 4.3 — Balanced Hub and Rafter Hoisting",
        "1. Seat the hub on temporary support at its design elevation, centred over the layout stake.",
        "2. Install rafters in opposing pairs around the beam ring to keep the hub balanced.",
        f"3. Confirm hub plumb after each pair until all {rafters} rafters are seated.",
        f"4. Secure structural fasteners and pegs only after all {rafters} rafters are seated and verified.\n",
    ]


def generate_assembly_guide(structure: Dict[str, Any], cut_list: Dict[str, Any]) -> str:
    """Generates the site erection and assembly sequence guide markdown."""
    sides = int(_need(_need(structure, "structure", "structure"), "sides", "structure"))
    shape = _need(_need(structure, "layout", "structure"), "shape", "layout")
    geom = _need(structure, "geometry", "structure")
    cc = _need(geom, "compound_cut", "geometry")
    miter = float(_need(cc, "miter_deg", "geometry.compound_cut"))
    bevel = float(_need(cc, "bevel_deg", "geometry.compound_cut"))
    bm = float(_need(_need(geom, "beam_ring", "geometry"), "beam_miter_deg", "geometry.beam_ring"))
    hub_type = _need(_need(structure, "hub", "structure"), "type", "hub")
    rafters = _group_qty(build_schedule_groups(structure, cut_list), "rafter_primary")

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
    if hub_type != "none":
        lines.extend(_hub_phase_lines(sides, rafters))
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
    """Loads inputs, produces all 3 markdown documents, and outputs stage results (FAIL on missing inputs)."""
    s_dir = Path(staging_dir) if staging_dir is not None else default_staging_dir()
    o_dir = Path(outputs_dir) if outputs_dir is not None else default_outputs_dir()

    struct_path = s_dir / "structure.json"
    cut_list_path = o_dir / CUT_LIST_RELPATH

    if not struct_path.exists():
        return {"status": "FAIL", "reason": f"structure.json missing at {struct_path}"}

    if not cut_list_path.exists():
        return {"status": "FAIL", "reason": f"cut-list.json missing at {cut_list_path}"}

    structure = json.loads(struct_path.read_text(encoding="utf-8"))
    cut_list = json.loads(cut_list_path.read_text(encoding="utf-8"))

    try:
        documents = {
            "lumber-purchase-list.md": generate_lumber_purchase_list(structure, cut_list),
            "budget-estimate.md": generate_budget_estimate(structure, cut_list),
            "assembly-guide.md": generate_assembly_guide(structure, cut_list),
        }
    except BuilderDocsInputError as error:
        return {"status": "FAIL", "reason": str(error)}

    o_dir.mkdir(parents=True, exist_ok=True)
    for name, text in documents.items():
        (o_dir / name).write_text(text, encoding="utf-8")

    return {
        "stage": "builder-docs-generator",
        "status": "COMPLETE",
        "outputs": [str(o_dir / name) for name in documents],
        "regional_pricing": structure["jurisdiction"]["region"],
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
