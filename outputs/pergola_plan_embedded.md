# 10 ft Hex Cedar Gazebo — Master Plan
**Location:** Saanich, BC  
**Style:** Traditional open-rafter cedar gazebo — mortise & tenon, no metal hangers  
**Inspiration:** Natural cedar hexagonal gazebo; 6×6 posts on concrete pads, exposed rafter system with king post hub, pronounced curved knee braces  
**Revision:** 0 | April 2025

---

## 1. Project Overview

A full-size 10-foot hexagonal cedar gazebo with a 4:12 pitched hip roof converging at a central king post hub.  
All joinery is traditional mortise and tenon secured with 3/4" white oak drawbore pegs.  
No metal post hangers or joist connectors — in the tradition of timber-frame construction.

### Key Specifications

| Parameter | Value |
|-----------|-------|
| Footprint | 10'-0" point-to-point (5'-0" post radius) |
| Post spacing | 5'-0" on-centre (60° intervals) |
| Total height at hub apex | 10'-7" (10.601 ft) |
| Clearance at beam soffit | 8'-4" (8.33 ft post height) |
| Beam depth | 7-1/4" (4×8 nominal) |
| Roof pitch | 4:12 (18.43°) |
| Hip rafter miter | **28.71°** |
| Hip rafter bevel | **9.10°** |
| Rafter overhang | 12" past beam centreline |
| Posts | 6×6 Western Red Cedar |
| All members | Western Red Cedar |
| Finish | Penofin Transparent Cedar, 2–3 coats |
| Foundation | 12" dia. concrete caissons, 24" deep, J-bolt anchors |
| Location seismic / wind | Saanich BC — coastal wind ~25 psf; check E66 base spec with engineer |

---

---

## 2. Architectural Drawings

All drawings produced from locked geometry (`context/staging/structural-model.json`).  
Open SVG files in any modern browser for full zoom and inspection.

| Drawing | File | Status |
|---------|------|--------|
| Plan view (top down) | [drawing-plan-view.svg](drawing-plan-view.svg) | ✅ VALIDATED |
| Front elevation | [drawing-elevation-view.svg](drawing-elevation-view.svg) | ✅ VALIDATED |
| Isometric projection | [drawing-isometric-view.svg](drawing-isometric-view.svg) | ✅ VALIDATED |
| Perspective view | [drawing-perspective-view.svg](drawing-perspective-view.svg) | ✅ VALIDATED |

---

## 3. Shop Blueprints

Dimensioned construction drawings with title blocks for shop use.

| Sheet | File | Contents |
|-------|------|----------|
| SB-01 Plan | [blueprint-plan.svg](blueprint-plan.svg) | Plan with post layout, dimensions, post-base callout |
| SB-02 Elevation | [blueprint-elevation.svg](blueprint-elevation.svg) | Elevation with compound-cut detail balloon |
| SB-03 Isometric | [blueprint-isometric.svg](blueprint-isometric.svg) | Assembly isometric with sequence numbers 1–7 |
| SB-04 Details | [blueprint-component-isolation.svg](blueprint-component-isolation.svg) | 4 joinery details: seat cut, tenon, post-beam, caisson |

---

## 4. Structural Members & Cut List

Full machine-readable list: [`../output/shop-blueprint/SB01-cut-list.json`](../output/shop-blueprint/SB01-cut-list.json)

| ID | Member | Profile | Cut Length | Qty | Notes |
|----|--------|---------|-----------|-----|-------|
| M01 | Main posts | 6×6 WRC | 8'-4" | 6 | Square ends; seal end grain |
| M02 | Ring beam | 4×8 WRC | 5'-3" | 6 | Opposing 28.71° miters |
| M03 | Hip rafter | 4×6 WRC | 5'-4" + 12" tail | 6 | Compound: 28.71° / 9.10°; bird's mouth at beam |
| M04 | King post hub | 6×6 WRC | 2'-0" | 1 | 6× mortises at 60° intervals |
| M05 | Knee brace | 4×4 WRC | 3'-0" | 12 | 45° compound bevel both ends |
| M06 | Purlin ring | 4×4 WRC | 3'-3" | 6 | Half-lap to rafters mid-span |

**Total lumber: ~490 BF Western Red Cedar (including 10% waste)**

---

## 5. Joinery Details

All joints: traditional mortise and tenon, 3/4" white oak drawbore pegs. No metal hangers or joist connectors.

| Joint | Detail Sheet | Mortise Size | Peg Count |
|-------|-------------|-------------|-----------|
| Post top → beam | SB-04 Detail 3 | 2.125"×4.125"×3" blind | 2 pegs |
| Rafter → hub | SB-04 Detail 2 | 1.625"×3.125"×3" blind | 2 pegs |
| Knee brace → post and beam | SB-04 Detail 3 | 1.5"×3"×2.5" blind | 2 pegs per end |
| Purlin half-lap → rafter | SB-04 Detail 1 note | Half-lap depth 1.5" | 1 peg per joint |

See [SB-04 component isolation sheet](blueprint-component-isolation.svg) for full dimensioned details.

---

## 6. Compound Cut Reference

> **Test on scrap before every production run.** These angles were computed by `geometry_engine.py`.

| Cut | Miter (fence) | Bevel (blade) | End |
|-----|--------------|--------------|-----|
| Hip rafter seat cut | 28.71° | 9.10° | Top/hub end |
| Hip rafter tail | 0° | 9.10° | Tail/overhang end |
| Ring beam ends | 28.71° | 0° | Both (opposing) |
| Knee brace ends | 45° | 0° | Both ends |

---

## 7. Foundation

| Element | Spec |
|---------|------|
| Caisson diameter | 12" |
| Caisson depth | 24" below grade |
| Frost depth (Saanich BC) | 18" nominal |
| Anchor | 5/8"×10" J-bolt galvanised, set in wet concrete |
| Post base | Simpson E66 standoff (no post-in-ground) |
| Concrete | Quikrete 80 lb High-Strength, 2 bags per caisson |

Permit note: verify setback from property lines with City of Saanich (250-475-5671) before digging.  
Seismic zone 4 — confirm E66 hold-down spec with an engineer.

---

## 8. Bill of Materials Summary

| Document | File |
|----------|------|
| Detailed cut list (JSON) | [`../output/shop-blueprint/SB01-cut-list.json`](../output/shop-blueprint/SB01-cut-list.json) |
| Lumber purchase list | [`lumber-purchase-list.md`](lumber-purchase-list.md) |
| Budget estimate (CAD) | [`budget-estimate.md`](budget-estimate.md) |

**Budget range:** $3,090 – $4,850 CAD (DIY labour; Saanich BC April 2025 pricing)  
**Mid-case estimate:** $3,855 CAD

---

## 9. Assembly Sequence

Full step-by-step guide: [`assembly-guide.md`](assembly-guide.md)

| Phase | Task | Crew |
|-------|------|------|
| 1 | Site layout + caissons | 1–2 |
| 2 | Post preparation + shop cuts | 1 |
| 3 | Erect posts + beam ring | 2 min. |
| 4 | Knee braces + rafters + hub + purlins | 2–3 |
| 5 | Final finish + inspection | 1 |

Estimated build time: **4–6 days** for competent DIY crew of 2 (excludes curing time).

---

## 10. Geometry Source

All angles, heights, and lengths derive from `plugins/garden-structure-designer/scripts/geometry_engine.py`.  
Do not re-derive by hand — the engine handles the compound-angle trig correctly.  
Locked model: `context/staging/structural-model.json` (`_locked: true`)

```json
{
  "pitch": "4:12",
  "miter_deg": 28.71,
  "bevel_deg": 9.10,
  "post_cut_ft": 8.33,
  "total_height_ft": 10.601,
  "rafter_overhang_ft": 1.0
}
```

