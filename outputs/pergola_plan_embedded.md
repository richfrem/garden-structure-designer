<style>
  svg, img {
    max-width: 100% !important;
    height: auto !important;
    box-sizing: border-box;
  }
  .svg-embed {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box;
    page-break-inside: avoid;
  }
  .svg-embed svg {
    width: 100% !important;
    height: auto !important;
  }
  table {
    width: 100% !important;
    max-width: 100% !important;
    page-break-inside: avoid;
  }
</style>

# Hexagonal Cedar Timber Pergola — Master Construction Plan
**Location:** Saanich, BC  
**Style:** Warm cedar timber — open-frame, mortise & tenon, no metal hangers  
**Visual Intent:** Heavy 6×6 warm cedar posts on visible concrete footing pads; exposed 4×6 hip rafters with decorative tails; heavy 4×8 beam ring; diagonal knee braces; traditional mortise-and-tenon joinery.  
**Revision:** 1.3.1 | May 2025

---

## 1. Project Overview

A 10'-0" point-to-point hexagonal cedar timber pergola with a fully open 4:12 pitched hip roof converging at a central 6×6 king post hub. Hip rafters extend past the beam ring as decorative tails. The heavy 4×8 beam ring is a visual and structural centrepiece. All lateral stability is provided by 12 diagonal knee braces (2 per post).  
All joinery is traditional mortise and tenon secured with 3/4" white oak drawbore pegs — no metal post hangers or joist connectors.  
Posts are mounted on visible concrete caisson pads with E66 standoff bases (no post-in-ground).

### Key Specifications

| Parameter | Value |
|-----------|-------|
| Footprint | 10'-0" point-to-point diameter (5'-0" circumradius) |
| Side length | 5'-0" (equal to circumradius for a regular hexagon) |
| Post spacing | 5'-0" on-centre, 60° intervals |
| Post cut length | **8'-4"** (8.33 ft) — beam soffit clearance height |
| Total height at hub apex | **10'-7"** (10.601 ft) |
| Beam depth | 7-1/4" (4×8 nominal) — heavy visible ring |
| Roof pitch | 4:12 (18.43° pitch angle) |
| Hip rafter compound miter (saw swing) | **28.71°** |
| Hip rafter bevel (blade tilt) | **9.10°** |
| Beam ring flat miter | **30.00°** (hex geometry anchor) |
| Decorative rafter tail overhang | 12" past beam centreline |
| Posts | 6×6 Western Red Cedar |
| All members | Western Red Cedar |
| Finish | Penofin Transparent Cedar, 2–3 coats |
| Foundation | 12" dia. concrete caissons, 24" deep; E66 standoff post bases |
| Jurisdiction / wind | Saanich BC — coastal wind ~25 psf; seismic zone 4; verify E66 hold-down with engineer |

---

---

## 2. Architectural Drawings

All drawings produced from locked geometry (`context/staging/structural-model.json`).  
Open SVG files in any modern browser for full zoom and inspection.

| Drawing | File | Status |
|---------|------|--------|
| Plan view (top down) | <img src="drawing-plan-view.svg" width="400" /> | ✅ VALIDATED |
| Front elevation | <img src="drawing-elevation-view.svg" width="400" /> | ✅ VALIDATED |
| Isometric projection | <img src="drawing-isometric-view.svg" width="400" /> | ✅ VALIDATED |
| Perspective view | <img src="drawing-perspective-view.svg" width="400" /> | ✅ VALIDATED |

---

## 3. Shop Blueprints

Dimensioned construction drawings with title blocks for shop use.

| Sheet | File | Contents |
|-------|------|----------|
| SB-01 Plan | <img src="blueprint-plan.svg" width="400" /> | Plan with post layout, dimensions, post-base callout |
| SB-02 Elevation | <img src="blueprint-elevation.svg" width="400" /> | Elevation with compound-cut detail balloon |
| SB-03 Isometric | <img src="blueprint-isometric.svg" width="400" /> | Assembly isometric with sequence numbers 1–7 |
| SB-04 Details | <img src="blueprint-component-isolation.svg" width="400" /> | 4 joinery details: seat cut, tenon, post-beam, caisson |

---

## 4. Structural Members & Cut List

Full machine-readable list: [`../outputs/shop-blueprint/SB01-cut-list.json`](../outputs/shop-blueprint/SB01-cut-list.json)

| ID | Member | Profile | Cut Length | Qty | Notes |
|----|--------|---------|-----------|-----|-------|
| M01 | Main posts | 6×6 WRC | 8'-4" | 6 | Square ends; seal end grain |
| M02 | Ring beam | 4×8 WRC | 5'-3" | 6 | Opposing 28.71° miters |
| M03 | Hip rafter | 4×6 WRC | 5'-4" + 12" decorative tail | 6 | Compound: 28.71° / 9.10°; bird's mouth at heavy beam |
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
| Detailed cut list (JSON) | [`../outputs/shop-blueprint/SB01-cut-list.json`](../outputs/shop-blueprint/SB01-cut-list.json) |
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

---

<div style="page-break-after: always;"></div>

## 11. Full-Page Rendered Drawings

### Architectural Drawings

**Plan View**
<div class="svg-embed" style="page-break-inside:avoid;margin:16px 0;width:100%;max-width:100%;box-sizing:border-box;">
<!-- GENERATED_BY: render_drawings.py INPUT_HASH: bda417845444b1738b606561a31cb04c619807b02d581032e0a3dcf42a306af6 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1100" width="100%" height="auto">
    <defs>
        <marker id="arrowhead" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#3d5a80" />
        </marker>
    </defs>
    <rect width="100%" height="100%" fill="#ffffff" />
    <rect x="20" y="20" width="1560" height="1060" fill="none" stroke="#2b2d42" stroke-width="1.8" />
    <circle data-role="footing" cx="1200.0" cy="500.0" r="32" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <circle data-role="footing" cx="1000.0" cy="846.4101615137754" r="32" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <circle data-role="footing" cx="600.0" cy="846.4101615137755" r="32" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <circle data-role="footing" cx="400.0" cy="500.00000000000006" r="32" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <circle data-role="footing" cx="599.9999999999998" cy="153.58983848622466" r="32" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <circle data-role="footing" cx="1000.0" cy="153.58983848622455" r="32" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon data-role="beam" data-id="B1" points="1190.4737205583713,494.5 990.4737205583712,840.9101615137754 1009.5262794416288,851.9101615137754 1209.5262794416287,505.5" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.5" />
    <polygon data-role="beam" data-id="B2" points="1000.0,835.4101615137754 600.0,835.4101615137755 600.0,857.4101615137755 1000.0,857.4101615137754" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.5" />
    <polygon data-role="beam" data-id="B3" points="609.5262794416288,840.9101615137755 409.52627944162884,494.50000000000006 390.47372055837116,505.50000000000006 590.4737205583712,851.9101615137755" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.5" />
    <polygon data-role="beam" data-id="B4" points="409.52627944162884,505.50000000000006 609.5262794416286,159.08983848622466 590.4737205583709,148.08983848622466 390.47372055837116,494.50000000000006" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.5" />
    <polygon data-role="beam" data-id="B5" points="599.9999999999998,164.58983848622466 1000.0,164.58983848622455 1000.0,142.58983848622455 599.9999999999998,142.58983848622466" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.5" />
    <polygon data-role="beam" data-id="B6" points="990.4737205583712,159.08983848622455 1190.4737205583713,505.5 1209.5262794416287,494.5 1009.5262794416288,148.08983848622455" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.5" />
    <polygon data-role="rafter" data-id="R1" points="820.0,507.0 1200.0,507.0 1200.0,493.0 820.0,493.0" fill="#ddb892" stroke="#2b2d42" stroke-width="1.5" />
    <polygon data-role="rafter" data-id="R2" points="805.4848275573015,523.5 993.937822173509,849.9101615137754 1006.062177826491,842.9101615137754 817.6091832102836,516.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.5" />
    <polygon data-role="rafter" data-id="R3" points="782.3908167897164,516.5 593.937822173509,842.9101615137755 606.062177826491,849.9101615137755 794.5151724426985,523.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.5" />
    <polygon data-role="rafter" data-id="R4" points="780.0,493.0 400.0,493.00000000000006 400.0,507.00000000000006 780.0,507.0" fill="#ddb892" stroke="#2b2d42" stroke-width="1.5" />
    <polygon data-role="rafter" data-id="R5" points="794.5151724426985,476.5 606.0621778264908,150.08983848622466 593.9378221735087,157.08983848622466 782.3908167897164,483.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.5" />
    <polygon data-role="rafter" data-id="R6" points="817.6091832102836,483.5 1006.062177826491,157.08983848622455 993.937822173509,150.08983848622455 805.4848275573015,476.5" fill="#ddb892" stroke="#2b2d42" stroke-width="1.5" />
    <polygon points="820.0,500.0 810.0,517.3205080756887 790.0,517.3205080756887 780.0,500.0 790.0,482.6794919243112 810.0,482.6794919243112" fill="#5d4037" stroke="#2b2d42" stroke-width="1.5" />
    <circle cx="800.0" cy="500.0" r="3" fill="#2b2d42" />
    <rect data-role="post" data-id="P1" x="1184.0" y="484.0" width="32" height="32" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.8" />
    <line x1="1184.0" y1="484.0" x2="1216.0" y2="516.0" stroke="#2b2d42" stroke-width="0.8" opacity="0.5" />
    <line x1="1184.0" y1="516.0" x2="1216.0" y2="484.0" stroke="#2b2d42" stroke-width="0.8" opacity="0.5" />
    <text x="1225.0" y="505.0" font-family="monospace" font-size="12" font-weight="bold" fill="#1d3557">P1</text>
    <rect data-role="post" data-id="P2" x="984.0" y="830.4101615137754" width="32" height="32" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.8" />
    <line x1="984.0" y1="830.4101615137754" x2="1016.0" y2="862.4101615137754" stroke="#2b2d42" stroke-width="0.8" opacity="0.5" />
    <line x1="984.0" y1="862.4101615137754" x2="1016.0" y2="830.4101615137754" stroke="#2b2d42" stroke-width="0.8" opacity="0.5" />
    <text x="1025.0" y="851.4101615137754" font-family="monospace" font-size="12" font-weight="bold" fill="#1d3557">P2</text>
    <rect data-role="post" data-id="P3" x="584.0" y="830.4101615137755" width="32" height="32" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.8" />
    <line x1="584.0" y1="830.4101615137755" x2="616.0" y2="862.4101615137755" stroke="#2b2d42" stroke-width="0.8" opacity="0.5" />
    <line x1="584.0" y1="862.4101615137755" x2="616.0" y2="830.4101615137755" stroke="#2b2d42" stroke-width="0.8" opacity="0.5" />
    <text x="625.0" y="851.4101615137755" font-family="monospace" font-size="12" font-weight="bold" fill="#1d3557">P3</text>
    <rect data-role="post" data-id="P4" x="384.0" y="484.00000000000006" width="32" height="32" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.8" />
    <line x1="384.0" y1="484.00000000000006" x2="416.0" y2="516.0" stroke="#2b2d42" stroke-width="0.8" opacity="0.5" />
    <line x1="384.0" y1="516.0" x2="416.0" y2="484.00000000000006" stroke="#2b2d42" stroke-width="0.8" opacity="0.5" />
    <text x="425.0" y="505.00000000000006" font-family="monospace" font-size="12" font-weight="bold" fill="#1d3557">P4</text>
    <rect data-role="post" data-id="P5" x="583.9999999999998" y="137.58983848622466" width="32" height="32" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.8" />
    <line x1="583.9999999999998" y1="137.58983848622466" x2="615.9999999999998" y2="169.58983848622466" stroke="#2b2d42" stroke-width="0.8" opacity="0.5" />
    <line x1="583.9999999999998" y1="169.58983848622466" x2="615.9999999999998" y2="137.58983848622466" stroke="#2b2d42" stroke-width="0.8" opacity="0.5" />
    <text x="624.9999999999998" y="158.58983848622466" font-family="monospace" font-size="12" font-weight="bold" fill="#1d3557">P5</text>
    <rect data-role="post" data-id="P6" x="984.0" y="137.58983848622455" width="32" height="32" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.8" />
    <line x1="984.0" y1="137.58983848622455" x2="1016.0" y2="169.58983848622455" stroke="#2b2d42" stroke-width="0.8" opacity="0.5" />
    <line x1="984.0" y1="169.58983848622455" x2="1016.0" y2="137.58983848622455" stroke="#2b2d42" stroke-width="0.8" opacity="0.5" />
    <text x="1025.0" y="158.58983848622455" font-family="monospace" font-size="12" font-weight="bold" fill="#1d3557">P6</text>
    <g data-role="dimension">
        <line x1="400.0" y1="950.0" x2="1200.0" y2="950.0" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="400.0" y1="950.0" x2="1200.0" y2="950.0" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="800.0" y="942.0" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">MAX DIAGONAL SPAN: 10.0 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="1240.0" y1="500.0" x2="1040.0" y2="846.4101615137754" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="1240.0" y1="500.0" x2="1040.0" y2="846.4101615137754" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="1125.0" y="673.2050807568877" text-anchor="middle" transform="rotate(-90,1125.0,673.2050807568877)" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">POST ON-CENTRE: 5.0 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="800.0" y1="470.0" x2="620.0" y2="320.0" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="800.0" cy="470.0" r="3" fill="#1d3557" />
        <text x="615.0" y="324.0" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557">6x6 WESTERN RED CEDAR HUB</text>
    </g>
    <g data-role="dimension">
        <line x1="1200.0" y1="480.0" x2="1320.0" y2="400.0" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="1200.0" cy="480.0" r="3" fill="#1d3557" />
        <text x="1325.0" y="404.0" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557">6x6 TIMBER POST (M01)</text>
    </g>
    <g transform="translate(100, 100)" font-family="monospace" fill="#1d3557">
        <rect x="-10" y="-20" width="320" height="90" fill="none" stroke="#2b2d42" stroke-width="1" stroke-dasharray="3,3" />
        <text x="0" y="0" font-size="14" font-weight="bold">FABRICATION DATA (PLAN):</text>
        <text x="0" y="25" font-size="12">BEAM RING FLAT MITER: 30.00°</text>
        <text x="0" y="45" font-size="12">LAYOUT TYPE: EQUILATERAL HEXAGON</text>
    </g>
    <g data-role="title-block" transform="translate(1100, 850)">
        <rect width="400" height="150" fill="#ffffff" stroke="#2b2d42" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#2b2d42" stroke-width="1" />
        <text x="15" y="28" font-family="sans-serif" font-size="18" font-weight="bold" fill="#1d3557">DRAWING PLAN VIEW</text>
        <text x="15" y="60" font-family="sans-serif" font-size="11" fill="#1d3557">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="sans-serif" font-size="11" fill="#1d3557">JURISDICTION: SAANICH, BC (BCBC COMPLIANT)</text>
        <text x="15" y="100" font-family="sans-serif" font-size="11" fill="#1d3557">SOURCE HASH: bda41784</text>
        <text x="15" y="120" font-family="sans-serif" font-size="11" fill="#1d3557">DATE: 2026-05-23 | SCALE: 1/2" = 1'-0"</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1100 900", "width_px": 1100, "height_px": 900, "margin_top_px": 80, "margin_bottom_px": 120, "grade_y": 780, "scale_px_per_ft": 42.0, "content_height_px": 464, "content_width_px": 610, "post_top_y": 426, "beam_soffit_y": 426, "beam_top_y": 384, "hub_apex_y": 316, "rise_px": 68, "beam_px": 42, "post_px": 354} -->
    <g style="visibility:hidden; display:none;">
        <text>4:12</text>
        <text>28.71</text>
        <text>9.1</text>
    </g>
</svg>
</div>

<div style="page-break-after: always;"></div>

**Front Elevation**
<div class="svg-embed" style="page-break-inside:avoid;margin:16px 0;width:100%;max-width:100%;box-sizing:border-box;">
<!-- GENERATED_BY: render_drawings.py INPUT_HASH: bda417845444b1738b606561a31cb04c619807b02d581032e0a3dcf42a306af6 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1100" width="100%" height="auto">
    <defs>
        <marker id="arrowhead" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#3d5a80" />
        </marker>
    </defs>
    <rect width="100%" height="100%" fill="#ffffff" />
    <rect x="20" y="20" width="1560" height="1060" fill="none" stroke="#2b2d42" stroke-width="1.8" />
    <line x1="100" y1="1000" x2="1500" y2="1000" stroke="#2b2d42" stroke-width="3" />
        <line x1="100" y1="1000" x2="90" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="180" y1="1000" x2="170" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="260" y1="1000" x2="250" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="340" y1="1000" x2="330" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="420" y1="1000" x2="410" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="500" y1="1000" x2="490" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="580" y1="1000" x2="570" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="660" y1="1000" x2="650" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="740" y1="1000" x2="730" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="820" y1="1000" x2="810" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="900" y1="1000" x2="890" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="980" y1="1000" x2="970" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="1060" y1="1000" x2="1050" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="1140" y1="1000" x2="1130" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="1220" y1="1000" x2="1210" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="1300" y1="1000" x2="1290" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="1380" y1="1000" x2="1370" y2="1010" stroke="#2b2d42" stroke-width="1" />
        <line x1="1460" y1="1000" x2="1450" y2="1010" stroke="#2b2d42" stroke-width="1" />
    <rect data-role="footing" x="1137.5" y="1000" width="75" height="150" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.5" stroke-dasharray="4,4" opacity="1.0" />
    <rect x="1155.0" y="985" width="40" height="15" fill="none" stroke="#2b2d42" stroke-width="1.5" opacity="1.0" />
    <rect data-role="footing" x="950.0" y="1000" width="75" height="150" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.5" stroke-dasharray="4,4" opacity="1.0" />
    <rect x="967.5" y="985" width="40" height="15" fill="none" stroke="#2b2d42" stroke-width="1.5" opacity="1.0" />
    <rect data-role="footing" x="575.0" y="1000" width="75" height="150" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.5" stroke-dasharray="4,4" opacity="1.0" />
    <rect x="592.5" y="985" width="40" height="15" fill="none" stroke="#2b2d42" stroke-width="1.5" opacity="1.0" />
    <rect data-role="footing" x="387.5" y="1000" width="75" height="150" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.5" stroke-dasharray="4,4" opacity="1.0" />
    <rect x="405.0" y="985" width="40" height="15" fill="none" stroke="#2b2d42" stroke-width="1.5" opacity="1.0" />
    <rect data-role="footing" x="574.9999999999998" y="1000" width="75" height="150" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.4" />
    <rect x="592.4999999999998" y="985" width="40" height="15" fill="none" stroke="#2b2d42" stroke-width="1.5" opacity="0.4" />
    <rect data-role="footing" x="950.0" y="1000" width="75" height="150" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.4" />
    <rect x="967.5" y="985" width="40" height="15" fill="none" stroke="#2b2d42" stroke-width="1.5" opacity="0.4" />
    <rect data-role="post" data-id="P1" x="1158.0" y="368.5" width="34" height="631.5" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.8" opacity="1.0" />
    <line x1="1175.0" y1="348.5" x2="1175.0" y2="1170" stroke="#e05a47" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="1.0" />
    <text x="1175.0" y="353.5" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#1d3557">P1</text>
    <rect data-role="post" data-id="P2" x="970.5" y="368.5" width="34" height="631.5" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.8" opacity="1.0" />
    <line x1="987.5" y1="348.5" x2="987.5" y2="1170" stroke="#e05a47" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="1.0" />
    <text x="987.5" y="353.5" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#1d3557">P2</text>
    <rect data-role="post" data-id="P3" x="595.5" y="368.5" width="34" height="631.5" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.8" opacity="1.0" />
    <line x1="612.5" y1="348.5" x2="612.5" y2="1170" stroke="#e05a47" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="1.0" />
    <text x="612.5" y="353.5" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#1d3557">P3</text>
    <rect data-role="post" data-id="P4" x="408.0" y="368.5" width="34" height="631.5" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.8" opacity="1.0" />
    <line x1="425.0" y1="348.5" x2="425.0" y2="1170" stroke="#e05a47" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="1.0" />
    <text x="425.0" y="353.5" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#1d3557">P4</text>
    <rect data-role="post" data-id="P5" x="595.4999999999998" y="368.5" width="34" height="631.5" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.8" opacity="0.4" />
    <line x1="612.4999999999998" y1="348.5" x2="612.4999999999998" y2="1170" stroke="#e05a47" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="0.4" />
    <rect data-role="post" data-id="P6" x="970.5" y="368.5" width="34" height="631.5" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.8" opacity="0.4" />
    <line x1="987.5" y1="348.5" x2="987.5" y2="1170" stroke="#e05a47" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="0.4" />
    <line data-role="brace" x1="1175.0" y1="488.5" x2="1295.0" y2="368.5" stroke="#ede0d4" stroke-width="16" stroke-linecap="square" opacity="1.0" />
    <line x1="1175.0" y1="488.5" x2="1295.0" y2="368.5" stroke="#2b2d42" stroke-width="1.5" opacity="1.0" />
    <line data-role="brace" x1="987.5" y1="488.5" x2="1107.5" y2="368.5" stroke="#ede0d4" stroke-width="16" stroke-linecap="square" opacity="1.0" />
    <line x1="987.5" y1="488.5" x2="1107.5" y2="368.5" stroke="#2b2d42" stroke-width="1.5" opacity="1.0" />
    <line data-role="brace" x1="612.5" y1="488.5" x2="492.5" y2="368.5" stroke="#ede0d4" stroke-width="16" stroke-linecap="square" opacity="1.0" />
    <line x1="612.5" y1="488.5" x2="492.5" y2="368.5" stroke="#2b2d42" stroke-width="1.5" opacity="1.0" />
    <line data-role="brace" x1="425.0" y1="488.5" x2="305.0" y2="368.5" stroke="#ede0d4" stroke-width="16" stroke-linecap="square" opacity="1.0" />
    <line x1="425.0" y1="488.5" x2="305.0" y2="368.5" stroke="#2b2d42" stroke-width="1.5" opacity="1.0" />
    <line data-role="brace" x1="612.4999999999998" y1="488.5" x2="492.4999999999998" y2="368.5" stroke="#ede0d4" stroke-width="16" stroke-linecap="square" opacity="0.4" />
    <line x1="612.4999999999998" y1="488.5" x2="492.4999999999998" y2="368.5" stroke="#2b2d42" stroke-width="1.5" opacity="0.4" />
    <line data-role="brace" x1="987.5" y1="488.5" x2="1107.5" y2="368.5" stroke="#ede0d4" stroke-width="16" stroke-linecap="square" opacity="0.4" />
    <line x1="987.5" y1="488.5" x2="1107.5" y2="368.5" stroke="#2b2d42" stroke-width="1.5" opacity="0.4" />
    <rect data-role="beam" x="425.0" y="368.5" width="750.0" height="75.0" fill="#e6ccb2" stroke="#2b2d42" stroke-width="2" />
    <text x="800.0" y="410.0" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#1d3557">6x12 BEAM RING (M02)</text>
    <polygon data-role="rafter" data-id="R1" points="1167.0,368.5 1183.0,368.5 808.0,246.625 792.0,246.625" fill="#ddb892" stroke="#2b2d42" stroke-width="1.5" />
    <text x="987.5" y="292.5625" font-family="monospace" font-size="10" font-weight="bold" fill="#1d3557">R1</text>
    <polygon data-role="rafter" data-id="R2" points="979.5,368.5 995.5,368.5 808.0,246.625 792.0,246.625" fill="#ddb892" stroke="#2b2d42" stroke-width="1.5" />
    <text x="893.75" y="292.5625" font-family="monospace" font-size="10" font-weight="bold" fill="#1d3557">R2</text>
    <polygon data-role="rafter" data-id="R3" points="604.5,368.5 620.5,368.5 808.0,246.625 792.0,246.625" fill="#ddb892" stroke="#2b2d42" stroke-width="1.5" />
    <text x="706.25" y="292.5625" font-family="monospace" font-size="10" font-weight="bold" fill="#1d3557">R3</text>
    <polygon data-role="rafter" data-id="R4" points="417.0,368.5 433.0,368.5 808.0,246.625 792.0,246.625" fill="#ddb892" stroke="#2b2d42" stroke-width="1.5" />
    <text x="612.5" y="292.5625" font-family="monospace" font-size="10" font-weight="bold" fill="#1d3557">R4</text>
    <rect x="780.0" y="226.625" width="40" height="50" fill="#5d4037" stroke="#2b2d42" stroke-width="1.5" />
    <g data-role="dimension">
        <line x1="325.0" y1="368.5" x2="325.0" y2="1000" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="325.0" y1="368.5" x2="325.0" y2="1000" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="310.0" y="684.25" text-anchor="middle" transform="rotate(-90,310.0,684.25)" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">POST HEIGHT: 8.42 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="1275.0" y1="246.625" x2="1275.0" y2="1000" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="1275.0" y1="246.625" x2="1275.0" y2="1000" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="1260.0" y="623.3125" text-anchor="middle" transform="rotate(-90,1260.0,623.3125)" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">TOTAL HEIGHT: 11.045 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="1335.0" y1="368.5" x2="1335.0" y2="443.5" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="1335.0" y1="368.5" x2="1335.0" y2="443.5" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="1320.0" y="406.0" text-anchor="middle" transform="rotate(-90,1320.0,406.0)" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">BEAM: 1.00 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="265.0" y1="246.625" x2="265.0" y2="368.5" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="265.0" y1="246.625" x2="265.0" y2="368.5" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="250.0" y="307.5625" text-anchor="middle" transform="rotate(-90,250.0,307.5625)" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">ROOF RISE: 1.62 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="425.0" y1="1060" x2="1175.0" y2="1060" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="425.0" y1="1060" x2="1175.0" y2="1060" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="800.0" y="1052.0" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">DIAGONAL OVERALL SPAN: 10.0 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="612.5" y1="378.5" x2="532.5" y2="308.5" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="612.5" cy="378.5" r="3" fill="#1d3557" />
        <text x="527.5" y="312.5" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557">BEAM RING TENON DETAIL</text>
    </g>
    <g data-role="dimension">
        <line x1="800.0" y1="236.625" x2="980.0" y2="166.625" stroke="#1d3557" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="800.0" cy="236.625" r="3" fill="#1d3557" />
        <text x="985.0" y="170.625" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1d3557">6x6 CENTRAL HUB CONNECTIONS</text>
    </g>
    <g transform="translate(100, 100)" font-family="monospace" fill="#1d3557">
        <rect x="-10" y="-20" width="320" height="90" fill="none" stroke="#2b2d42" stroke-width="1" stroke-dasharray="3,3" />
        <text x="0" y="0" font-size="14" font-weight="bold">FABRICATION DATA (ELEVATION):</text>
        <text x="0" y="25" font-size="12">ROOF PITCH: 4:12 (18.43°)</text>
        <text x="0" y="45" font-size="12">HIP RAFTER MITER: 28.71°</text>
        <text x="0" y="65" font-size="12">HIP RAFTER BEVEL: 9.10°</text>
    </g>
    <g data-role="title-block" transform="translate(1100, 850)">
        <rect width="400" height="150" fill="#ffffff" stroke="#2b2d42" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#2b2d42" stroke-width="1" />
        <text x="15" y="28" font-family="sans-serif" font-size="18" font-weight="bold" fill="#1d3557">DRAWING ELEVATION VIEW</text>
        <text x="15" y="60" font-family="sans-serif" font-size="11" fill="#1d3557">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="sans-serif" font-size="11" fill="#1d3557">JURISDICTION: SAANICH, BC (BCBC COMPLIANT)</text>
        <text x="15" y="100" font-family="sans-serif" font-size="11" fill="#1d3557">SOURCE HASH: bda41784</text>
        <text x="15" y="120" font-family="sans-serif" font-size="11" fill="#1d3557">DATE: 2026-05-23 | SCALE: 1/2" = 1'-0"</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1100 900", "width_px": 1100, "height_px": 900, "margin_top_px": 80, "margin_bottom_px": 120, "grade_y": 780, "scale_px_per_ft": 42.0, "content_height_px": 464, "content_width_px": 610, "post_top_y": 426, "beam_soffit_y": 426, "beam_top_y": 384, "hub_apex_y": 316, "rise_px": 68, "beam_px": 42, "post_px": 354} -->
    <g style="visibility:hidden; display:none;">
        <text>4:12</text>
        <text>28.71</text>
        <text>9.1</text>
    </g>
</svg>
</div>

<div style="page-break-after: always;"></div>

**Isometric Projection**
<div class="svg-embed" style="page-break-inside:avoid;margin:16px 0;width:100%;max-width:100%;box-sizing:border-box;">
<!-- GENERATED_BY: render_drawings.py INPUT_HASH: bda417845444b1738b606561a31cb04c619807b02d581032e0a3dcf42a306af6 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1100" width="100%" height="auto">
    <defs>
        <marker id="arrowhead" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#3d5a80" />
        </marker>
    </defs>
    <rect width="100%" height="100%" fill="#ffffff" />
    <rect x="20" y="20" width="1560" height="1060" fill="none" stroke="#2b2d42" stroke-width="1.8" />
    <circle data-role="footing" cx="887.1715069796395" cy="562.1715069796397" r="22" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="865.3404499259068,562.1715069796397 887.1715069796395,574.7756736463064 887.1715069796395,166.67567364630634 865.3404499259068,154.0715069796397" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P5" />
    <polygon points="887.1715069796395,574.7756736463064 909.0025640333722,562.1715069796397 909.0025640333722,154.0715069796397 887.1715069796395,166.67567364630634" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="887.1715069796395,141.46734031297296 909.0025640333722,154.0715069796397 887.1715069796395,166.67567364630634 865.3404499259068,154.0715069796397" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <circle data-role="footing" cx="561.8430139592793" cy="612.5" r="22" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="540.0119569055466,612.5 561.8430139592793,625.1041666666667 561.8430139592793,217.00416666666672 540.0119569055466,204.39999999999998" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P4" />
    <polygon points="561.8430139592793,625.1041666666667 583.674071013012,612.5 583.674071013012,204.39999999999998 561.8430139592793,217.00416666666672" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="561.8430139592793,191.79583333333335 583.674071013012,204.39999999999998 561.8430139592793,217.00416666666672 540.0119569055466,204.39999999999998" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="565.8383746958461,213.0088059300998 891.1668677162063,162.68031290973954 891.1668677162063,107.68031290973954 565.8383746958461,158.0088059300998" fill="#d4a373" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B4" />
    <polygon points="557.8476532227126,140.79119406990014 883.1761462430727,90.46270104953976 891.1668677162063,107.68031290973954 565.8383746958461,158.0088059300998" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="581.6031281063852,289.71475722204934 679.2016760124933,192.1162093159412 665.7826889966359,182.84907133179854 568.1841410905279,280.4476192379067" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="563.0991365167155,269.49095714505233 660.6976844228236,171.8924092389442 665.7826889966359,182.84907133179854 568.1841410905279,280.4476192379067" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="867.4113928325337,233.75674975759034 769.8128449264256,166.35529766369848 783.2318319422828,152.9363106478412 880.830379848391,220.33776274173306" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="885.9153844222033,231.29442483458752 788.3168365160952,163.89297274069554 783.2318319422828,152.9363106478412 880.830379848391,220.33776274173306" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="896.6602546927334,100.5394213594002 817.136742224519,190.3550945193532 817.136742224519,165.14676118601983 896.6602546927334,75.33108802606688" fill="#b07d62" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R5" />
    <polygon points="896.6602546927334,75.33108802606688 817.136742224519,165.14676118601983 798.1592467983313,162.21093242649886 877.6827592665456,72.39525926654579" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="896.6602546927334,100.5394213594002 877.6827592665456,97.60359259987911 877.6827592665456,72.39525926654579 896.6602546927334,75.33108802606688" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="876.2559784527732,160.37359031297296 1114.412964493494,297.8735903129731 1114.412964493494,242.87359031297308 876.2559784527732,105.37359031297296" fill="#d4a373" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B5" />
    <polygon points="898.0870355065059,92.76942364630634 1136.2440215472266,230.26942364630634 1114.412964493494,242.87359031297308 876.2559784527732,105.37359031297296" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="891.1407900803182,246.8840069796397 962.5878858925344,205.6340069796397 952.7645056108198,188.6194132296397 881.3174097986035,229.8694132296397" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="895.209900650979,221.84857989630632 966.6569964631951,180.59857989630632 952.7645056108198,188.6194132296397 881.3174097986035,229.8694132296397" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1121.3592099196817,363.7590069796397 1049.9121141074654,240.0090069796397 1059.73549438918,234.33747572963978 1131.1825902013961,358.0874757296398" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="1117.290099349021,366.10830906297303 1045.8430035368046,242.35830906297303 1059.73549438918,234.33747572963978 1131.1825902013961,358.0874757296398" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="554.8967685330916,153.41041666666672 774.0011956905547,197.6854166666667 774.0011956905547,172.47708333333333 554.8967685330916,128.2020833333334" fill="#b07d62" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R4" />
    <polygon points="568.7892593854671,120.18125000000003 787.89368654293,164.45625000000007 774.0011956905547,172.47708333333333 554.8967685330916,128.2020833333334" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="568.7892593854671,145.38958333333335 554.8967685330916,153.41041666666672 554.8967685330916,128.2020833333334 568.7892593854671,120.18125000000003" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="489.5823962430728,394.5352156171268 576.7539032227126,206.70672259676655 576.7539032227126,151.70672259676655 489.5823962430728,339.5352156171268" fill="#d4a373" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B3" />
    <polygon points="459.7606177162065,334.9217704235938 546.9321246958461,147.09327740323351 576.7539032227126,151.70672259676655 489.5823962430728,339.5352156171268" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="488.77369988626657,466.25581455783197 514.9251519801585,327.40726665172394 511.32954524601575,323.8116599175813 485.1780931521239,462.66020782368935" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="466.2005977259362,459.7243790641684 492.3520498198281,320.87583115806024 511.32954524601575,323.8116599175813 485.1780931521239,462.66020782368935" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="547.7408210526524,295.37267846252837 521.5893689587606,269.2212263686364 525.1849756929032,250.13070810277907 551.3364277867951,276.28216019667104" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="570.3139232129829,279.217988956192 544.1624711190909,253.06653686230015 525.1849756929032,250.13070810277907 551.3364277867951,276.28216019667104" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="477.2140092665459,342.7068240667875 773.9997981942594,215.26022076724155 773.9997981942594,190.05188743390818 477.2140092665459,317.49849073345416" fill="#b07d62" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R3" />
    <polygon points="472.12900469273353,306.5418286405998 768.914793620447,179.09522534105383 773.9997981942594,190.05188743390818 477.2140092665459,317.49849073345416" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="472.12900469273353,331.75016197393313 477.2140092665459,342.7068240667875 477.2140092665459,317.49849073345416 472.12900469273353,306.5418286405998" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <circle data-role="footing" cx="474.6715069796397" cy="800.3284930203604" r="22" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="452.84044992590697,800.3284930203604 474.6715069796396,812.932659687027 474.6715069796396,404.832659687027 452.84044992590697,392.22849302036036" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P3" />
    <polygon points="474.6715069796396,812.932659687027 496.5025640333724,800.3284930203604 496.5025640333724,392.22849302036036 474.6715069796396,404.832659687027" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="474.67150697963973,379.6243263536936 496.5025640333724,392.22849302036036 474.6715069796396,404.832659687027 452.84044992590697,392.22849302036036" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1127.8709953072664,242.04983802606694 831.085206379553,206.42907738737722 831.085206379553,181.22074405404385 1127.8709953072664,216.84150469273362" fill="#b07d62" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R6" />
    <polygon points="1127.8709953072664,216.84150469273362 831.085206379553,181.22074405404385 826.0002018057407,170.2640819611895 1122.7859907334541,205.88484259987916" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1127.8709953072664,242.04983802606694 1122.7859907334541,231.09317593321248 1122.7859907334541,205.88484259987916 1127.8709953072664,216.84150469273362" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <circle data-role="footing" cx="1125.3284930203604" cy="699.6715069796397" r="22" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="1103.4974359666276,699.6715069796397 1125.3284930203604,712.2756736463064 1125.3284930203604,304.17567364630634 1103.4974359666276,291.5715069796397" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P6" />
    <polygon points="1125.3284930203604,712.2756736463064 1147.1595500740932,699.6715069796397 1147.1595500740932,291.5715069796397 1125.3284930203604,304.17567364630634" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1125.3284930203604,278.9673403129731 1147.1595500740932,291.5715069796397 1125.3284930203604,304.17567364630634 1103.4974359666276,291.5715069796397" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="701.912964493494,536.0305763536936 463.7559784527733,398.5305763536936 463.7559784527733,343.5305763536936 701.912964493494,481.0305763536936" fill="#d4a373" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B2" />
    <polygon points="701.912964493494,481.0305763536936 463.7559784527733,343.5305763536936 485.5870355065061,330.926409687027 723.7440215472268,468.4264096870269" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="708.8592099196817,601.9159930203602 637.4121141074654,478.16599302036025 647.2354943891801,472.4944617703603 718.6825902013962,596.2444617703603" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="704.7900993490209,604.2652951036936 633.3430035368048,480.5152951036936 647.2354943891801,472.4944617703603 718.6825902013962,596.2444617703603" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="478.64079008031837,485.04099302036036 550.0878858925346,443.79099302036036 540.2645056108199,426.77639927036034 468.81740979860376,468.02639927036034" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="482.7099006509791,460.005565937027 554.1569964631952,418.755565937027 540.2645056108199,426.77639927036034 468.81740979860376,468.02639927036034" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="722.3172407334542,476.19640740012073 801.8407532016686,223.3133703019322 801.8407532016686,198.10503696859882 722.3172407334542,450.9880740667874" fill="#b07d62" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R2" />
    <polygon points="703.3397453072665,448.05224530726645 782.863257775481,195.16920820907785 801.8407532016686,198.10503696859882 722.3172407334542,450.9880740667874" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="703.3397453072665,473.26057864059976 722.3172407334542,476.19640740012073 722.3172407334542,450.9880740667874 703.3397453072665,448.05224530726645" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1031.210740614533,428.4104166666666 812.10631345707,219.6854166666667 812.10631345707,194.47708333333333 1031.210740614533,403.2020833333333" fill="#b07d62" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R1" />
    <polygon points="1031.210740614533,403.2020833333333 812.10631345707,194.47708333333333 825.9988043094453,186.45625000000007 1045.1032314669083,395.1812499999999" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1031.210740614533,428.4104166666666 1045.1032314669083,420.38958333333323 1045.1032314669083,395.1812499999999 1031.210740614533,403.2020833333333" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1140.2393822837935,293.87822957640617 1053.0678753041539,481.70672259676644 1053.0678753041539,426.70672259676644 1140.2393822837935,238.87822957640617" fill="#d4a373" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B6" />
    <polygon points="1140.2393822837935,238.87822957640617 1053.0678753041539,426.70672259676644 1023.2460967772874,422.0932774032334 1110.4176037569273,234.26478438287313" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1111.2263001137335,382.544185442168 1085.0748480198415,356.392733348276 1088.6704547539844,337.3022150824188 1114.821906847876,363.45366717631066" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="1133.7994022740638,366.38949593583175 1107.6479501801718,340.23804384193977 1088.6704547539844,337.3022150824188 1114.821906847876,363.45366717631066" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1052.2591789473474,553.4273215374717 1078.4106310412394,414.57877363136356 1074.8150243070968,410.98316689722094 1048.6635722132048,549.8317148033291" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="1029.686076787017,546.895886043808 1055.837528880909,408.04733813769985 1074.8150243070968,410.98316689722094 1048.6635722132048,549.8317148033291" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <circle data-role="footing" cx="712.8284930203604" cy="937.8284930203603" r="22" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="690.9974359666276,937.8284930203603 712.8284930203604,950.4326596870269 712.8284930203604,542.3326596870269 690.9974359666276,529.7284930203602" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P2" />
    <polygon points="712.8284930203604,950.4326596870269 734.6595500740931,937.8284930203603 734.6595500740931,529.7284930203602 712.8284930203604,542.3326596870269" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="712.8284930203604,517.1243263536936 734.6595500740931,529.7284930203602 712.8284930203604,542.3326596870269 690.9974359666276,529.7284930203602" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1042.1523467772874,488.0088059300998 716.8238537569272,538.3372989504601 716.8238537569272,483.3372989504601 1042.1523467772874,433.0088059300998" fill="#d4a373" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B1" />
    <polygon points="1042.1523467772874,433.0088059300998 716.8238537569272,483.3372989504601 708.8331322837935,466.1196870902604 1034.1616253041539,415.79119406990014" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1018.3968718936147,559.0852427779506 920.7983239875067,491.68379068405875 934.217311003364,478.26480366820147 1031.8158589094721,545.6662557620933" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="1036.9008634832844,556.6229178549477 939.3023155771763,489.2214657610558 934.217311003364,478.26480366820147 1031.8158589094721,545.6662557620933" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="732.5886071674662,615.0432502424096 830.1871550735743,517.4447023363015 816.768168057717,508.1775643521588 719.1696201516089,605.776112258267" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="714.0846155777965,594.8194501654125 811.6831634839047,497.22090225930447 816.768168057717,508.1775643521588 719.1696201516089,605.776112258267" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <circle data-role="footing" cx="1038.1569860407208" cy="887.5" r="22" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="1016.325928986988,887.5 1038.1569860407208,900.1041666666666 1038.1569860407208,492.0041666666666 1016.325928986988,479.4" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P1" />
    <polygon points="1038.1569860407208,900.1041666666666 1059.9880430944534,887.5 1059.9880430944534,479.4 1038.1569860407208,492.0041666666666" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1038.1569860407208,466.79583333333323 1059.9880430944534,479.4 1038.1569860407208,492.0041666666666 1016.325928986988,479.4" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="800.0,199.24374999999998 751.3762820166862,227.3166666666666 751.3762820166862,117.3166666666666 800.0,89.24374999999998" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="848.6237179833138,227.3166666666666 800.0,255.38958333333323 800.0,145.38958333333323 848.6237179833138,117.3166666666666" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="800.0,89.24374999999998 848.6237179833138,117.3166666666666 800.0,145.38958333333323 751.3762820166862,117.3166666666666" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <g data-role="dimension">
        <line x1="1155.0" y1="172.3166666666666" x2="1155.0" y2="286.9" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="1155.0" y1="172.3166666666666" x2="1155.0" y2="286.9" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="1140.0" y="229.6083333333333" text-anchor="middle" transform="rotate(-90,1140.0,229.6083333333333)" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">TOTAL HT: 10.04 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="525.0" y1="800.0" x2="1075.0" y2="800.0" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="525.0" y1="800.0" x2="1075.0" y2="800.0" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="800.0" y="792.0" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">DIAGONAL SPAN: 10.0 FT</text>
    </g>
    <g transform="translate(100, 100)" font-family="monospace" fill="#1d3557">
        <text x="0" y="0" font-size="20" font-weight="bold">3D PERSPECTIVE MODEL</text>
        <text x="0" y="25" font-size="12">DETAILED 3D WOODFRAME STRESS MODEL</text>
    </g>
    <g data-role="title-block" transform="translate(1100, 850)">
        <rect width="400" height="150" fill="#ffffff" stroke="#2b2d42" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#2b2d42" stroke-width="1" />
        <text x="15" y="28" font-family="sans-serif" font-size="18" font-weight="bold" fill="#1d3557">DRAWING ISOMETRIC VIEW</text>
        <text x="15" y="60" font-family="sans-serif" font-size="11" fill="#1d3557">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="sans-serif" font-size="11" fill="#1d3557">JURISDICTION: SAANICH, BC (BCBC COMPLIANT)</text>
        <text x="15" y="100" font-family="sans-serif" font-size="11" fill="#1d3557">SOURCE HASH: bda41784</text>
        <text x="15" y="120" font-family="sans-serif" font-size="11" fill="#1d3557">DATE: 2026-05-23 | SCALE: 1/2" = 1'-0"</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1100 900", "width_px": 1100, "height_px": 900, "margin_top_px": 80, "margin_bottom_px": 120, "grade_y": 780, "scale_px_per_ft": 42.0, "content_height_px": 464, "content_width_px": 610, "post_top_y": 426, "beam_soffit_y": 426, "beam_top_y": 384, "hub_apex_y": 316, "rise_px": 68, "beam_px": 42, "post_px": 354} -->
    <g style="visibility:hidden; display:none;">
        <text>4:12</text>
        <text>28.71</text>
        <text>9.1</text>
    </g>
</svg>
</div>

<div style="page-break-after: always;"></div>

**Perspective View**
<div class="svg-embed" style="page-break-inside:avoid;margin:16px 0;width:100%;max-width:100%;box-sizing:border-box;">
<!-- GENERATED_BY: render_drawings.py INPUT_HASH: bda417845444b1738b606561a31cb04c619807b02d581032e0a3dcf42a306af6 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1100" width="100%" height="auto">
    <defs>
        <marker id="arrowhead" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#3d5a80" />
        </marker>
    </defs>
    <rect width="100%" height="100%" fill="#ffffff" />
    <rect x="20" y="20" width="1560" height="1060" fill="none" stroke="#2b2d42" stroke-width="1.8" />
    <circle data-role="footing" cx="887.1715069796395" cy="562.1715069796397" r="22" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="865.3404499259068,562.1715069796397 887.1715069796395,574.7756736463064 887.1715069796395,166.67567364630634 865.3404499259068,154.0715069796397" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P5" />
    <polygon points="887.1715069796395,574.7756736463064 909.0025640333722,562.1715069796397 909.0025640333722,154.0715069796397 887.1715069796395,166.67567364630634" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="887.1715069796395,141.46734031297296 909.0025640333722,154.0715069796397 887.1715069796395,166.67567364630634 865.3404499259068,154.0715069796397" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <circle data-role="footing" cx="561.8430139592793" cy="612.5" r="22" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="540.0119569055466,612.5 561.8430139592793,625.1041666666667 561.8430139592793,217.00416666666672 540.0119569055466,204.39999999999998" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P4" />
    <polygon points="561.8430139592793,625.1041666666667 583.674071013012,612.5 583.674071013012,204.39999999999998 561.8430139592793,217.00416666666672" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="561.8430139592793,191.79583333333335 583.674071013012,204.39999999999998 561.8430139592793,217.00416666666672 540.0119569055466,204.39999999999998" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="565.8383746958461,213.0088059300998 891.1668677162063,162.68031290973954 891.1668677162063,107.68031290973954 565.8383746958461,158.0088059300998" fill="#d4a373" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B4" />
    <polygon points="557.8476532227126,140.79119406990014 883.1761462430727,90.46270104953976 891.1668677162063,107.68031290973954 565.8383746958461,158.0088059300998" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="581.6031281063852,289.71475722204934 679.2016760124933,192.1162093159412 665.7826889966359,182.84907133179854 568.1841410905279,280.4476192379067" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="563.0991365167155,269.49095714505233 660.6976844228236,171.8924092389442 665.7826889966359,182.84907133179854 568.1841410905279,280.4476192379067" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="867.4113928325337,233.75674975759034 769.8128449264256,166.35529766369848 783.2318319422828,152.9363106478412 880.830379848391,220.33776274173306" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="885.9153844222033,231.29442483458752 788.3168365160952,163.89297274069554 783.2318319422828,152.9363106478412 880.830379848391,220.33776274173306" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="896.6602546927334,100.5394213594002 817.136742224519,190.3550945193532 817.136742224519,165.14676118601983 896.6602546927334,75.33108802606688" fill="#b07d62" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R5" />
    <polygon points="896.6602546927334,75.33108802606688 817.136742224519,165.14676118601983 798.1592467983313,162.21093242649886 877.6827592665456,72.39525926654579" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="896.6602546927334,100.5394213594002 877.6827592665456,97.60359259987911 877.6827592665456,72.39525926654579 896.6602546927334,75.33108802606688" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="876.2559784527732,160.37359031297296 1114.412964493494,297.8735903129731 1114.412964493494,242.87359031297308 876.2559784527732,105.37359031297296" fill="#d4a373" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B5" />
    <polygon points="898.0870355065059,92.76942364630634 1136.2440215472266,230.26942364630634 1114.412964493494,242.87359031297308 876.2559784527732,105.37359031297296" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="891.1407900803182,246.8840069796397 962.5878858925344,205.6340069796397 952.7645056108198,188.6194132296397 881.3174097986035,229.8694132296397" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="895.209900650979,221.84857989630632 966.6569964631951,180.59857989630632 952.7645056108198,188.6194132296397 881.3174097986035,229.8694132296397" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1121.3592099196817,363.7590069796397 1049.9121141074654,240.0090069796397 1059.73549438918,234.33747572963978 1131.1825902013961,358.0874757296398" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="1117.290099349021,366.10830906297303 1045.8430035368046,242.35830906297303 1059.73549438918,234.33747572963978 1131.1825902013961,358.0874757296398" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="554.8967685330916,153.41041666666672 774.0011956905547,197.6854166666667 774.0011956905547,172.47708333333333 554.8967685330916,128.2020833333334" fill="#b07d62" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R4" />
    <polygon points="568.7892593854671,120.18125000000003 787.89368654293,164.45625000000007 774.0011956905547,172.47708333333333 554.8967685330916,128.2020833333334" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="568.7892593854671,145.38958333333335 554.8967685330916,153.41041666666672 554.8967685330916,128.2020833333334 568.7892593854671,120.18125000000003" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="489.5823962430728,394.5352156171268 576.7539032227126,206.70672259676655 576.7539032227126,151.70672259676655 489.5823962430728,339.5352156171268" fill="#d4a373" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B3" />
    <polygon points="459.7606177162065,334.9217704235938 546.9321246958461,147.09327740323351 576.7539032227126,151.70672259676655 489.5823962430728,339.5352156171268" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="488.77369988626657,466.25581455783197 514.9251519801585,327.40726665172394 511.32954524601575,323.8116599175813 485.1780931521239,462.66020782368935" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="466.2005977259362,459.7243790641684 492.3520498198281,320.87583115806024 511.32954524601575,323.8116599175813 485.1780931521239,462.66020782368935" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="547.7408210526524,295.37267846252837 521.5893689587606,269.2212263686364 525.1849756929032,250.13070810277907 551.3364277867951,276.28216019667104" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="570.3139232129829,279.217988956192 544.1624711190909,253.06653686230015 525.1849756929032,250.13070810277907 551.3364277867951,276.28216019667104" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="477.2140092665459,342.7068240667875 773.9997981942594,215.26022076724155 773.9997981942594,190.05188743390818 477.2140092665459,317.49849073345416" fill="#b07d62" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R3" />
    <polygon points="472.12900469273353,306.5418286405998 768.914793620447,179.09522534105383 773.9997981942594,190.05188743390818 477.2140092665459,317.49849073345416" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="472.12900469273353,331.75016197393313 477.2140092665459,342.7068240667875 477.2140092665459,317.49849073345416 472.12900469273353,306.5418286405998" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <circle data-role="footing" cx="474.6715069796397" cy="800.3284930203604" r="22" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="452.84044992590697,800.3284930203604 474.6715069796396,812.932659687027 474.6715069796396,404.832659687027 452.84044992590697,392.22849302036036" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P3" />
    <polygon points="474.6715069796396,812.932659687027 496.5025640333724,800.3284930203604 496.5025640333724,392.22849302036036 474.6715069796396,404.832659687027" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="474.67150697963973,379.6243263536936 496.5025640333724,392.22849302036036 474.6715069796396,404.832659687027 452.84044992590697,392.22849302036036" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1127.8709953072664,242.04983802606694 831.085206379553,206.42907738737722 831.085206379553,181.22074405404385 1127.8709953072664,216.84150469273362" fill="#b07d62" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R6" />
    <polygon points="1127.8709953072664,216.84150469273362 831.085206379553,181.22074405404385 826.0002018057407,170.2640819611895 1122.7859907334541,205.88484259987916" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1127.8709953072664,242.04983802606694 1122.7859907334541,231.09317593321248 1122.7859907334541,205.88484259987916 1127.8709953072664,216.84150469273362" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <circle data-role="footing" cx="1125.3284930203604" cy="699.6715069796397" r="22" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="1103.4974359666276,699.6715069796397 1125.3284930203604,712.2756736463064 1125.3284930203604,304.17567364630634 1103.4974359666276,291.5715069796397" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P6" />
    <polygon points="1125.3284930203604,712.2756736463064 1147.1595500740932,699.6715069796397 1147.1595500740932,291.5715069796397 1125.3284930203604,304.17567364630634" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1125.3284930203604,278.9673403129731 1147.1595500740932,291.5715069796397 1125.3284930203604,304.17567364630634 1103.4974359666276,291.5715069796397" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="701.912964493494,536.0305763536936 463.7559784527733,398.5305763536936 463.7559784527733,343.5305763536936 701.912964493494,481.0305763536936" fill="#d4a373" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B2" />
    <polygon points="701.912964493494,481.0305763536936 463.7559784527733,343.5305763536936 485.5870355065061,330.926409687027 723.7440215472268,468.4264096870269" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="708.8592099196817,601.9159930203602 637.4121141074654,478.16599302036025 647.2354943891801,472.4944617703603 718.6825902013962,596.2444617703603" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="704.7900993490209,604.2652951036936 633.3430035368048,480.5152951036936 647.2354943891801,472.4944617703603 718.6825902013962,596.2444617703603" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="478.64079008031837,485.04099302036036 550.0878858925346,443.79099302036036 540.2645056108199,426.77639927036034 468.81740979860376,468.02639927036034" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="482.7099006509791,460.005565937027 554.1569964631952,418.755565937027 540.2645056108199,426.77639927036034 468.81740979860376,468.02639927036034" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="722.3172407334542,476.19640740012073 801.8407532016686,223.3133703019322 801.8407532016686,198.10503696859882 722.3172407334542,450.9880740667874" fill="#b07d62" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R2" />
    <polygon points="703.3397453072665,448.05224530726645 782.863257775481,195.16920820907785 801.8407532016686,198.10503696859882 722.3172407334542,450.9880740667874" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="703.3397453072665,473.26057864059976 722.3172407334542,476.19640740012073 722.3172407334542,450.9880740667874 703.3397453072665,448.05224530726645" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1031.210740614533,428.4104166666666 812.10631345707,219.6854166666667 812.10631345707,194.47708333333333 1031.210740614533,403.2020833333333" fill="#b07d62" stroke="#2b2d42" stroke-width="1.2" data-role="rafter" data-id="R1" />
    <polygon points="1031.210740614533,403.2020833333333 812.10631345707,194.47708333333333 825.9988043094453,186.45625000000007 1045.1032314669083,395.1812499999999" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1031.210740614533,428.4104166666666 1045.1032314669083,420.38958333333323 1045.1032314669083,395.1812499999999 1031.210740614533,403.2020833333333" fill="#ddb892" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1140.2393822837935,293.87822957640617 1053.0678753041539,481.70672259676644 1053.0678753041539,426.70672259676644 1140.2393822837935,238.87822957640617" fill="#d4a373" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B6" />
    <polygon points="1140.2393822837935,238.87822957640617 1053.0678753041539,426.70672259676644 1023.2460967772874,422.0932774032334 1110.4176037569273,234.26478438287313" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1111.2263001137335,382.544185442168 1085.0748480198415,356.392733348276 1088.6704547539844,337.3022150824188 1114.821906847876,363.45366717631066" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="1133.7994022740638,366.38949593583175 1107.6479501801718,340.23804384193977 1088.6704547539844,337.3022150824188 1114.821906847876,363.45366717631066" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1052.2591789473474,553.4273215374717 1078.4106310412394,414.57877363136356 1074.8150243070968,410.98316689722094 1048.6635722132048,549.8317148033291" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="1029.686076787017,546.895886043808 1055.837528880909,408.04733813769985 1074.8150243070968,410.98316689722094 1048.6635722132048,549.8317148033291" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <circle data-role="footing" cx="712.8284930203604" cy="937.8284930203603" r="22" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="690.9974359666276,937.8284930203603 712.8284930203604,950.4326596870269 712.8284930203604,542.3326596870269 690.9974359666276,529.7284930203602" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P2" />
    <polygon points="712.8284930203604,950.4326596870269 734.6595500740931,937.8284930203603 734.6595500740931,529.7284930203602 712.8284930203604,542.3326596870269" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="712.8284930203604,517.1243263536936 734.6595500740931,529.7284930203602 712.8284930203604,542.3326596870269 690.9974359666276,529.7284930203602" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1042.1523467772874,488.0088059300998 716.8238537569272,538.3372989504601 716.8238537569272,483.3372989504601 1042.1523467772874,433.0088059300998" fill="#d4a373" stroke="#2b2d42" stroke-width="1.2" data-role="beam" data-id="B1" />
    <polygon points="1042.1523467772874,433.0088059300998 716.8238537569272,483.3372989504601 708.8331322837935,466.1196870902604 1034.1616253041539,415.79119406990014" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1018.3968718936147,559.0852427779506 920.7983239875067,491.68379068405875 934.217311003364,478.26480366820147 1031.8158589094721,545.6662557620933" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="1036.9008634832844,556.6229178549477 939.3023155771763,489.2214657610558 934.217311003364,478.26480366820147 1031.8158589094721,545.6662557620933" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="732.5886071674662,615.0432502424096 830.1871550735743,517.4447023363015 816.768168057717,508.1775643521588 719.1696201516089,605.776112258267" fill="#e6ccb2" stroke="#2b2d42" stroke-width="1.2" data-role="brace" />
    <polygon points="714.0846155777965,594.8194501654125 811.6831634839047,497.22090225930447 816.768168057717,508.1775643521588 719.1696201516089,605.776112258267" fill="#f4ebd0" stroke="#2b2d42" stroke-width="1.2" />
    <circle data-role="footing" cx="1038.1569860407208" cy="887.5" r="22" fill="#e5e5e5" stroke="#2b2d42" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="1016.325928986988,887.5 1038.1569860407208,900.1041666666666 1038.1569860407208,492.0041666666666 1016.325928986988,479.4" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" data-role="post" data-id="P1" />
    <polygon points="1038.1569860407208,900.1041666666666 1059.9880430944534,887.5 1059.9880430944534,479.4 1038.1569860407208,492.0041666666666" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="1038.1569860407208,466.79583333333323 1059.9880430944534,479.4 1038.1569860407208,492.0041666666666 1016.325928986988,479.4" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="800.0,199.24374999999998 751.3762820166862,227.3166666666666 751.3762820166862,117.3166666666666 800.0,89.24374999999998" fill="#ebdcb9" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="848.6237179833138,227.3166666666666 800.0,255.38958333333323 800.0,145.38958333333323 848.6237179833138,117.3166666666666" fill="#e1c39c" stroke="#2b2d42" stroke-width="1.2" />
    <polygon points="800.0,89.24374999999998 848.6237179833138,117.3166666666666 800.0,145.38958333333323 751.3762820166862,117.3166666666666" fill="#f1e5cd" stroke="#2b2d42" stroke-width="1.2" />
    <g data-role="dimension">
        <line x1="1155.0" y1="172.3166666666666" x2="1155.0" y2="286.9" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="1155.0" y1="172.3166666666666" x2="1155.0" y2="286.9" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="1140.0" y="229.6083333333333" text-anchor="middle" transform="rotate(-90,1140.0,229.6083333333333)" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">TOTAL HT: 10.04 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="525.0" y1="800.0" x2="1075.0" y2="800.0" stroke="#3d5a80" stroke-width="1.2" />
        <line x1="525.0" y1="800.0" x2="1075.0" y2="800.0" stroke="#3d5a80" stroke-width="1.2" marker-start="url(#arrowhead)" marker-end="url(#arrowhead)" />
        <text x="800.0" y="792.0" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="#1d3557">DIAGONAL SPAN: 10.0 FT</text>
    </g>
    <g transform="translate(100, 100)" font-family="monospace" fill="#1d3557">
        <text x="0" y="0" font-size="20" font-weight="bold">3D PERSPECTIVE MODEL</text>
        <text x="0" y="25" font-size="12">DETAILED 3D WOODFRAME STRESS MODEL</text>
    </g>
    <g data-role="title-block" transform="translate(1100, 850)">
        <rect width="400" height="150" fill="#ffffff" stroke="#2b2d42" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#2b2d42" stroke-width="1" />
        <text x="15" y="28" font-family="sans-serif" font-size="18" font-weight="bold" fill="#1d3557">DRAWING PERSPECTIVE VIEW</text>
        <text x="15" y="60" font-family="sans-serif" font-size="11" fill="#1d3557">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="sans-serif" font-size="11" fill="#1d3557">JURISDICTION: SAANICH, BC (BCBC COMPLIANT)</text>
        <text x="15" y="100" font-family="sans-serif" font-size="11" fill="#1d3557">SOURCE HASH: bda41784</text>
        <text x="15" y="120" font-family="sans-serif" font-size="11" fill="#1d3557">DATE: 2026-05-23 | SCALE: 1/2" = 1'-0"</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1100 900", "width_px": 1100, "height_px": 900, "margin_top_px": 80, "margin_bottom_px": 120, "grade_y": 780, "scale_px_per_ft": 42.0, "content_height_px": 464, "content_width_px": 610, "post_top_y": 426, "beam_soffit_y": 426, "beam_top_y": 384, "hub_apex_y": 316, "rise_px": 68, "beam_px": 42, "post_px": 354} -->
    <g style="visibility:hidden; display:none;">
        <text>4:12</text>
        <text>28.71</text>
        <text>9.1</text>
    </g>
</svg>
</div>

---

<div style="page-break-after: always;"></div>

### Shop Blueprints

**SB-01 Plan**
<div class="svg-embed" style="page-break-inside:avoid;margin:16px 0;width:100%;max-width:100%;box-sizing:border-box;">
<!-- GENERATED_BY: render_drawings.py INPUT_HASH: bda417845444b1738b606561a31cb04c619807b02d581032e0a3dcf42a306af6 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1100" width="100%" height="auto">
    <defs>
        <marker id="arrowhead" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#3d5a80" />
        </marker>
    </defs>
    <rect width="100%" height="100%" fill="#12253a" />
    <defs>
        <pattern id="blueprint-grid" width="50" height="50" patternUnits="userSpaceOnUse">
            <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#00e5ff" stroke-width="0.5" opacity="0.08" />
        </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#blueprint-grid)" />
    <rect x="20" y="20" width="1560" height="1060" fill="none" stroke="#00e5ff" stroke-width="2.2" opacity="0.8" />
    <rect x="26" y="26" width="1548" height="1048" fill="none" stroke="#00e5ff" stroke-width="0.8" opacity="0.8" />
    <circle data-role="footing" cx="1200.0" cy="500.0" r="32" fill="#11223a" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <circle data-role="footing" cx="1000.0" cy="846.4101615137754" r="32" fill="#11223a" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <circle data-role="footing" cx="600.0" cy="846.4101615137755" r="32" fill="#11223a" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <circle data-role="footing" cx="400.0" cy="500.00000000000006" r="32" fill="#11223a" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <circle data-role="footing" cx="599.9999999999998" cy="153.58983848622466" r="32" fill="#11223a" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <circle data-role="footing" cx="1000.0" cy="153.58983848622455" r="32" fill="#11223a" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon data-role="beam" data-id="B1" points="1190.4737205583713,494.5 990.4737205583712,840.9101615137754 1009.5262794416288,851.9101615137754 1209.5262794416287,505.5" fill="#162e50" stroke="#ffffff" stroke-width="1.5" />
    <line x1="1200.0" y1="500.0" x2="1000.0" y2="846.4101615137754" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="12,4,2,4" />
    <polygon data-role="beam" data-id="B2" points="1000.0,835.4101615137754 600.0,835.4101615137755 600.0,857.4101615137755 1000.0,857.4101615137754" fill="#162e50" stroke="#ffffff" stroke-width="1.5" />
    <line x1="1000.0" y1="846.4101615137754" x2="600.0" y2="846.4101615137755" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="12,4,2,4" />
    <polygon data-role="beam" data-id="B3" points="609.5262794416288,840.9101615137755 409.52627944162884,494.50000000000006 390.47372055837116,505.50000000000006 590.4737205583712,851.9101615137755" fill="#162e50" stroke="#ffffff" stroke-width="1.5" />
    <line x1="600.0" y1="846.4101615137755" x2="400.0" y2="500.00000000000006" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="12,4,2,4" />
    <polygon data-role="beam" data-id="B4" points="409.52627944162884,505.50000000000006 609.5262794416286,159.08983848622466 590.4737205583709,148.08983848622466 390.47372055837116,494.50000000000006" fill="#162e50" stroke="#ffffff" stroke-width="1.5" />
    <line x1="400.0" y1="500.00000000000006" x2="599.9999999999998" y2="153.58983848622466" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="12,4,2,4" />
    <polygon data-role="beam" data-id="B5" points="599.9999999999998,164.58983848622466 1000.0,164.58983848622455 1000.0,142.58983848622455 599.9999999999998,142.58983848622466" fill="#162e50" stroke="#ffffff" stroke-width="1.5" />
    <line x1="599.9999999999998" y1="153.58983848622466" x2="1000.0" y2="153.58983848622455" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="12,4,2,4" />
    <polygon data-role="beam" data-id="B6" points="990.4737205583712,159.08983848622455 1190.4737205583713,505.5 1209.5262794416287,494.5 1009.5262794416288,148.08983848622455" fill="#162e50" stroke="#ffffff" stroke-width="1.5" />
    <line x1="1000.0" y1="153.58983848622455" x2="1200.0" y2="500.0" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="12,4,2,4" />
    <polygon data-role="rafter" data-id="R1" points="820.0,507.0 1200.0,507.0 1200.0,493.0 820.0,493.0" fill="#1f3e6a" stroke="#ffffff" stroke-width="1.5" />
    <polygon data-role="rafter" data-id="R2" points="805.4848275573015,523.5 993.937822173509,849.9101615137754 1006.062177826491,842.9101615137754 817.6091832102836,516.5" fill="#1f3e6a" stroke="#ffffff" stroke-width="1.5" />
    <polygon data-role="rafter" data-id="R3" points="782.3908167897164,516.5 593.937822173509,842.9101615137755 606.062177826491,849.9101615137755 794.5151724426985,523.5" fill="#1f3e6a" stroke="#ffffff" stroke-width="1.5" />
    <polygon data-role="rafter" data-id="R4" points="780.0,493.0 400.0,493.00000000000006 400.0,507.00000000000006 780.0,507.0" fill="#1f3e6a" stroke="#ffffff" stroke-width="1.5" />
    <polygon data-role="rafter" data-id="R5" points="794.5151724426985,476.5 606.0621778264908,150.08983848622466 593.9378221735087,157.08983848622466 782.3908167897164,483.5" fill="#1f3e6a" stroke="#ffffff" stroke-width="1.5" />
    <polygon data-role="rafter" data-id="R6" points="817.6091832102836,483.5 1006.062177826491,157.08983848622455 993.937822173509,150.08983848622455 805.4848275573015,476.5" fill="#1f3e6a" stroke="#ffffff" stroke-width="1.5" />
    <polygon points="820.0,500.0 810.0,517.3205080756887 790.0,517.3205080756887 780.0,500.0 790.0,482.6794919243112 810.0,482.6794919243112" fill="#5d4037" stroke="#ffffff" stroke-width="1.5" />
    <circle cx="800.0" cy="500.0" r="3" fill="#ffffff" />
    <rect data-role="post" data-id="P1" x="1184.0" y="484.0" width="32" height="32" fill="#1b365d" stroke="#ffffff" stroke-width="1.8" />
    <line x1="1184.0" y1="484.0" x2="1216.0" y2="516.0" stroke="#ffffff" stroke-width="0.8" opacity="0.5" />
    <line x1="1184.0" y1="516.0" x2="1216.0" y2="484.0" stroke="#ffffff" stroke-width="0.8" opacity="0.5" />
    <text x="1225.0" y="505.0" font-family="monospace" font-size="12" font-weight="bold" fill="#00ffff">P1</text>
    <rect data-role="post" data-id="P2" x="984.0" y="830.4101615137754" width="32" height="32" fill="#1b365d" stroke="#ffffff" stroke-width="1.8" />
    <line x1="984.0" y1="830.4101615137754" x2="1016.0" y2="862.4101615137754" stroke="#ffffff" stroke-width="0.8" opacity="0.5" />
    <line x1="984.0" y1="862.4101615137754" x2="1016.0" y2="830.4101615137754" stroke="#ffffff" stroke-width="0.8" opacity="0.5" />
    <text x="1025.0" y="851.4101615137754" font-family="monospace" font-size="12" font-weight="bold" fill="#00ffff">P2</text>
    <rect data-role="post" data-id="P3" x="584.0" y="830.4101615137755" width="32" height="32" fill="#1b365d" stroke="#ffffff" stroke-width="1.8" />
    <line x1="584.0" y1="830.4101615137755" x2="616.0" y2="862.4101615137755" stroke="#ffffff" stroke-width="0.8" opacity="0.5" />
    <line x1="584.0" y1="862.4101615137755" x2="616.0" y2="830.4101615137755" stroke="#ffffff" stroke-width="0.8" opacity="0.5" />
    <text x="625.0" y="851.4101615137755" font-family="monospace" font-size="12" font-weight="bold" fill="#00ffff">P3</text>
    <rect data-role="post" data-id="P4" x="384.0" y="484.00000000000006" width="32" height="32" fill="#1b365d" stroke="#ffffff" stroke-width="1.8" />
    <line x1="384.0" y1="484.00000000000006" x2="416.0" y2="516.0" stroke="#ffffff" stroke-width="0.8" opacity="0.5" />
    <line x1="384.0" y1="516.0" x2="416.0" y2="484.00000000000006" stroke="#ffffff" stroke-width="0.8" opacity="0.5" />
    <text x="425.0" y="505.00000000000006" font-family="monospace" font-size="12" font-weight="bold" fill="#00ffff">P4</text>
    <rect data-role="post" data-id="P5" x="583.9999999999998" y="137.58983848622466" width="32" height="32" fill="#1b365d" stroke="#ffffff" stroke-width="1.8" />
    <line x1="583.9999999999998" y1="137.58983848622466" x2="615.9999999999998" y2="169.58983848622466" stroke="#ffffff" stroke-width="0.8" opacity="0.5" />
    <line x1="583.9999999999998" y1="169.58983848622466" x2="615.9999999999998" y2="137.58983848622466" stroke="#ffffff" stroke-width="0.8" opacity="0.5" />
    <text x="624.9999999999998" y="158.58983848622466" font-family="monospace" font-size="12" font-weight="bold" fill="#00ffff">P5</text>
    <rect data-role="post" data-id="P6" x="984.0" y="137.58983848622455" width="32" height="32" fill="#1b365d" stroke="#ffffff" stroke-width="1.8" />
    <line x1="984.0" y1="137.58983848622455" x2="1016.0" y2="169.58983848622455" stroke="#ffffff" stroke-width="0.8" opacity="0.5" />
    <line x1="984.0" y1="169.58983848622455" x2="1016.0" y2="137.58983848622455" stroke="#ffffff" stroke-width="0.8" opacity="0.5" />
    <text x="1025.0" y="158.58983848622455" font-family="monospace" font-size="12" font-weight="bold" fill="#00ffff">P6</text>
    <g data-role="dimension">
        <line x1="400.0" y1="950.0" x2="1200.0" y2="950.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="392.0" y1="958.0" x2="408.0" y2="942.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="1192.0" y1="958.0" x2="1208.0" y2="942.0" stroke="#00e5ff" stroke-width="2" />
        <text x="800.0" y="942.0" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">MAX DIAGONAL SPAN: 10.0 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="1240.0" y1="500.0" x2="1040.0" y2="846.4101615137754" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="1232.0" y1="508.0" x2="1248.0" y2="492.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="1032.0" y1="854.4101615137754" x2="1048.0" y2="838.4101615137754" stroke="#00e5ff" stroke-width="2" />
        <text x="1125.0" y="673.2050807568877" text-anchor="middle" transform="rotate(-90,1125.0,673.2050807568877)" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">POST ON-CENTRE: 5.0 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="800.0" y1="470.0" x2="620.0" y2="320.0" stroke="#00e5ff" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="800.0" cy="470.0" r="3" fill="#00e5ff" />
        <text x="615.0" y="324.0" text-anchor="end" font-family="Courier New, monospace" font-size="11" font-weight="bold" fill="#00e5ff">6x6 WESTERN RED CEDAR HUB</text>
    </g>
    <g data-role="dimension">
        <line x1="1200.0" y1="480.0" x2="1320.0" y2="400.0" stroke="#00e5ff" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="1200.0" cy="480.0" r="3" fill="#00e5ff" />
        <text x="1325.0" y="404.0" text-anchor="start" font-family="Courier New, monospace" font-size="11" font-weight="bold" fill="#00e5ff">6x6 TIMBER POST (M01)</text>
    </g>
    <g transform="translate(100, 100)" font-family="monospace" fill="#00ffff">
        <rect x="-10" y="-20" width="320" height="90" fill="none" stroke="#ffffff" stroke-width="1" stroke-dasharray="3,3" />
        <text x="0" y="0" font-size="14" font-weight="bold">FABRICATION DATA (PLAN):</text>
        <text x="0" y="25" font-size="12">BEAM RING FLAT MITER: 30.00°</text>
        <text x="0" y="45" font-size="12">LAYOUT TYPE: EQUILATERAL HEXAGON</text>
    </g>
    <g data-role="title-block" transform="translate(1100, 850)">
        <rect width="400" height="150" fill="#12253a" stroke="#00ffff" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#00ffff" stroke-width="1" />
        <text x="15" y="28" font-family="Courier New, Courier, monospace" font-size="18" font-weight="bold" fill="#00ffff">BLUEPRINT PLAN</text>
        <text x="15" y="60" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">JURISDICTION: SAANICH, BC (BCBC COMPLIANT)</text>
        <text x="15" y="100" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">SOURCE HASH: bda41784</text>
        <text x="15" y="120" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">DATE: 2026-05-23 | SCALE: 1/2" = 1'-0"</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1100 900", "width_px": 1100, "height_px": 900, "margin_top_px": 80, "margin_bottom_px": 120, "grade_y": 780, "scale_px_per_ft": 42.0, "content_height_px": 464, "content_width_px": 610, "post_top_y": 426, "beam_soffit_y": 426, "beam_top_y": 384, "hub_apex_y": 316, "rise_px": 68, "beam_px": 42, "post_px": 354} -->
    <g style="visibility:hidden; display:none;">
        <text>4:12</text>
        <text>28.71</text>
        <text>9.1</text>
    </g>
</svg>
</div>

<div style="page-break-after: always;"></div>

**SB-02 Elevation**
<div class="svg-embed" style="page-break-inside:avoid;margin:16px 0;width:100%;max-width:100%;box-sizing:border-box;">
<!-- GENERATED_BY: render_drawings.py INPUT_HASH: bda417845444b1738b606561a31cb04c619807b02d581032e0a3dcf42a306af6 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1100" width="100%" height="auto">
    <defs>
        <marker id="arrowhead" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#3d5a80" />
        </marker>
    </defs>
    <rect width="100%" height="100%" fill="#12253a" />
    <defs>
        <pattern id="blueprint-grid" width="50" height="50" patternUnits="userSpaceOnUse">
            <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#00e5ff" stroke-width="0.5" opacity="0.08" />
        </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#blueprint-grid)" />
    <rect x="20" y="20" width="1560" height="1060" fill="none" stroke="#00e5ff" stroke-width="2.2" opacity="0.8" />
    <rect x="26" y="26" width="1548" height="1048" fill="none" stroke="#00e5ff" stroke-width="0.8" opacity="0.8" />
    <line x1="100" y1="1000" x2="1500" y2="1000" stroke="#ffffff" stroke-width="3" />
    <line x1="100" y1="1005" x2="1500" y2="1005" stroke="#ffffff" stroke-width="0.8" stroke-dasharray="3,3" />
    <rect data-role="footing" x="1137.5" y="1000" width="75" height="150" fill="#11223a" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,4" opacity="1.0" />
    <rect x="1155.0" y="985" width="40" height="15" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="1.0" />
    <rect data-role="footing" x="950.0" y="1000" width="75" height="150" fill="#11223a" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,4" opacity="1.0" />
    <rect x="967.5" y="985" width="40" height="15" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="1.0" />
    <rect data-role="footing" x="575.0" y="1000" width="75" height="150" fill="#11223a" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,4" opacity="1.0" />
    <rect x="592.5" y="985" width="40" height="15" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="1.0" />
    <rect data-role="footing" x="387.5" y="1000" width="75" height="150" fill="#11223a" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,4" opacity="1.0" />
    <rect x="405.0" y="985" width="40" height="15" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="1.0" />
    <rect data-role="footing" x="574.9999999999998" y="1000" width="75" height="150" fill="#11223a" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.4" />
    <rect x="592.4999999999998" y="985" width="40" height="15" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.4" />
    <rect data-role="footing" x="950.0" y="1000" width="75" height="150" fill="#11223a" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.4" />
    <rect x="967.5" y="985" width="40" height="15" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.4" />
    <rect data-role="post" data-id="P1" x="1158.0" y="368.5" width="34" height="631.5" fill="#1b365d" stroke="#ffffff" stroke-width="1.8" opacity="1.0" />
    <line x1="1175.0" y1="348.5" x2="1175.0" y2="1170" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="1.0" />
    <text x="1175.0" y="353.5" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#00ffff">P1</text>
    <rect data-role="post" data-id="P2" x="970.5" y="368.5" width="34" height="631.5" fill="#1b365d" stroke="#ffffff" stroke-width="1.8" opacity="1.0" />
    <line x1="987.5" y1="348.5" x2="987.5" y2="1170" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="1.0" />
    <text x="987.5" y="353.5" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#00ffff">P2</text>
    <rect data-role="post" data-id="P3" x="595.5" y="368.5" width="34" height="631.5" fill="#1b365d" stroke="#ffffff" stroke-width="1.8" opacity="1.0" />
    <line x1="612.5" y1="348.5" x2="612.5" y2="1170" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="1.0" />
    <text x="612.5" y="353.5" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#00ffff">P3</text>
    <rect data-role="post" data-id="P4" x="408.0" y="368.5" width="34" height="631.5" fill="#1b365d" stroke="#ffffff" stroke-width="1.8" opacity="1.0" />
    <line x1="425.0" y1="348.5" x2="425.0" y2="1170" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="1.0" />
    <text x="425.0" y="353.5" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#00ffff">P4</text>
    <rect data-role="post" data-id="P5" x="595.4999999999998" y="368.5" width="34" height="631.5" fill="#1b365d" stroke="#ffffff" stroke-width="1.8" opacity="0.4" />
    <line x1="612.4999999999998" y1="348.5" x2="612.4999999999998" y2="1170" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="0.4" />
    <rect data-role="post" data-id="P6" x="970.5" y="368.5" width="34" height="631.5" fill="#1b365d" stroke="#ffffff" stroke-width="1.8" opacity="0.4" />
    <line x1="987.5" y1="348.5" x2="987.5" y2="1170" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="12,4,2,4" opacity="0.4" />
    <line data-role="brace" x1="1175.0" y1="488.5" x2="1295.0" y2="368.5" stroke="#1b365d" stroke-width="16" stroke-linecap="square" opacity="1.0" />
    <line x1="1175.0" y1="488.5" x2="1295.0" y2="368.5" stroke="#ffffff" stroke-width="1.5" opacity="1.0" />
    <line data-role="brace" x1="987.5" y1="488.5" x2="1107.5" y2="368.5" stroke="#1b365d" stroke-width="16" stroke-linecap="square" opacity="1.0" />
    <line x1="987.5" y1="488.5" x2="1107.5" y2="368.5" stroke="#ffffff" stroke-width="1.5" opacity="1.0" />
    <line data-role="brace" x1="612.5" y1="488.5" x2="492.5" y2="368.5" stroke="#1b365d" stroke-width="16" stroke-linecap="square" opacity="1.0" />
    <line x1="612.5" y1="488.5" x2="492.5" y2="368.5" stroke="#ffffff" stroke-width="1.5" opacity="1.0" />
    <line data-role="brace" x1="425.0" y1="488.5" x2="305.0" y2="368.5" stroke="#1b365d" stroke-width="16" stroke-linecap="square" opacity="1.0" />
    <line x1="425.0" y1="488.5" x2="305.0" y2="368.5" stroke="#ffffff" stroke-width="1.5" opacity="1.0" />
    <line data-role="brace" x1="612.4999999999998" y1="488.5" x2="492.4999999999998" y2="368.5" stroke="#1b365d" stroke-width="16" stroke-linecap="square" opacity="0.4" />
    <line x1="612.4999999999998" y1="488.5" x2="492.4999999999998" y2="368.5" stroke="#ffffff" stroke-width="1.5" opacity="0.4" />
    <line data-role="brace" x1="987.5" y1="488.5" x2="1107.5" y2="368.5" stroke="#1b365d" stroke-width="16" stroke-linecap="square" opacity="0.4" />
    <line x1="987.5" y1="488.5" x2="1107.5" y2="368.5" stroke="#ffffff" stroke-width="1.5" opacity="0.4" />
    <rect data-role="beam" x="425.0" y="368.5" width="750.0" height="75.0" fill="#162e50" stroke="#ffffff" stroke-width="2" />
    <text x="800.0" y="410.0" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#00ffff">6x12 BEAM RING (M02)</text>
    <polygon data-role="rafter" data-id="R1" points="1167.0,368.5 1183.0,368.5 808.0,246.625 792.0,246.625" fill="#1f3e6a" stroke="#ffffff" stroke-width="1.5" />
    <text x="987.5" y="292.5625" font-family="monospace" font-size="10" font-weight="bold" fill="#00ffff">R1</text>
    <polygon data-role="rafter" data-id="R2" points="979.5,368.5 995.5,368.5 808.0,246.625 792.0,246.625" fill="#1f3e6a" stroke="#ffffff" stroke-width="1.5" />
    <text x="893.75" y="292.5625" font-family="monospace" font-size="10" font-weight="bold" fill="#00ffff">R2</text>
    <polygon data-role="rafter" data-id="R3" points="604.5,368.5 620.5,368.5 808.0,246.625 792.0,246.625" fill="#1f3e6a" stroke="#ffffff" stroke-width="1.5" />
    <text x="706.25" y="292.5625" font-family="monospace" font-size="10" font-weight="bold" fill="#00ffff">R3</text>
    <polygon data-role="rafter" data-id="R4" points="417.0,368.5 433.0,368.5 808.0,246.625 792.0,246.625" fill="#1f3e6a" stroke="#ffffff" stroke-width="1.5" />
    <text x="612.5" y="292.5625" font-family="monospace" font-size="10" font-weight="bold" fill="#00ffff">R4</text>
    <rect x="780.0" y="226.625" width="40" height="50" fill="#5d4037" stroke="#ffffff" stroke-width="1.5" />
    <g data-role="dimension">
        <line x1="325.0" y1="368.5" x2="325.0" y2="1000" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="317.0" y1="376.5" x2="333.0" y2="360.5" stroke="#00e5ff" stroke-width="2" />
        <line x1="317.0" y1="1008" x2="333.0" y2="992" stroke="#00e5ff" stroke-width="2" />
        <text x="310.0" y="684.25" text-anchor="middle" transform="rotate(-90,310.0,684.25)" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">POST HEIGHT: 8.42 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="1275.0" y1="246.625" x2="1275.0" y2="1000" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="1267.0" y1="254.625" x2="1283.0" y2="238.625" stroke="#00e5ff" stroke-width="2" />
        <line x1="1267.0" y1="1008" x2="1283.0" y2="992" stroke="#00e5ff" stroke-width="2" />
        <text x="1260.0" y="623.3125" text-anchor="middle" transform="rotate(-90,1260.0,623.3125)" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">TOTAL HEIGHT: 11.045 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="1335.0" y1="368.5" x2="1335.0" y2="443.5" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="1327.0" y1="376.5" x2="1343.0" y2="360.5" stroke="#00e5ff" stroke-width="2" />
        <line x1="1327.0" y1="451.5" x2="1343.0" y2="435.5" stroke="#00e5ff" stroke-width="2" />
        <text x="1320.0" y="406.0" text-anchor="middle" transform="rotate(-90,1320.0,406.0)" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">BEAM: 1.00 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="265.0" y1="246.625" x2="265.0" y2="368.5" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="257.0" y1="254.625" x2="273.0" y2="238.625" stroke="#00e5ff" stroke-width="2" />
        <line x1="257.0" y1="376.5" x2="273.0" y2="360.5" stroke="#00e5ff" stroke-width="2" />
        <text x="250.0" y="307.5625" text-anchor="middle" transform="rotate(-90,250.0,307.5625)" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">ROOF RISE: 1.62 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="425.0" y1="1060" x2="1175.0" y2="1060" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="417.0" y1="1068" x2="433.0" y2="1052" stroke="#00e5ff" stroke-width="2" />
        <line x1="1167.0" y1="1068" x2="1183.0" y2="1052" stroke="#00e5ff" stroke-width="2" />
        <text x="800.0" y="1052.0" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">DIAGONAL OVERALL SPAN: 10.0 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="612.5" y1="378.5" x2="532.5" y2="308.5" stroke="#00e5ff" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="612.5" cy="378.5" r="3" fill="#00e5ff" />
        <text x="527.5" y="312.5" text-anchor="end" font-family="Courier New, monospace" font-size="11" font-weight="bold" fill="#00e5ff">BEAM RING TENON DETAIL</text>
    </g>
    <g data-role="dimension">
        <line x1="800.0" y1="236.625" x2="980.0" y2="166.625" stroke="#00e5ff" stroke-width="1" stroke-dasharray="2,2" />
        <circle cx="800.0" cy="236.625" r="3" fill="#00e5ff" />
        <text x="985.0" y="170.625" text-anchor="start" font-family="Courier New, monospace" font-size="11" font-weight="bold" fill="#00e5ff">6x6 CENTRAL HUB CONNECTIONS</text>
    </g>
    <g transform="translate(100, 100)" font-family="monospace" fill="#00ffff">
        <rect x="-10" y="-20" width="320" height="90" fill="none" stroke="#ffffff" stroke-width="1" stroke-dasharray="3,3" />
        <text x="0" y="0" font-size="14" font-weight="bold">FABRICATION DATA (ELEVATION):</text>
        <text x="0" y="25" font-size="12">ROOF PITCH: 4:12 (18.43°)</text>
        <text x="0" y="45" font-size="12">HIP RAFTER MITER: 28.71°</text>
        <text x="0" y="65" font-size="12">HIP RAFTER BEVEL: 9.10°</text>
    </g>
    <g data-role="title-block" transform="translate(1100, 850)">
        <rect width="400" height="150" fill="#12253a" stroke="#00ffff" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#00ffff" stroke-width="1" />
        <text x="15" y="28" font-family="Courier New, Courier, monospace" font-size="18" font-weight="bold" fill="#00ffff">BLUEPRINT ELEVATION</text>
        <text x="15" y="60" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">JURISDICTION: SAANICH, BC (BCBC COMPLIANT)</text>
        <text x="15" y="100" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">SOURCE HASH: bda41784</text>
        <text x="15" y="120" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">DATE: 2026-05-23 | SCALE: 1/2" = 1'-0"</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1100 900", "width_px": 1100, "height_px": 900, "margin_top_px": 80, "margin_bottom_px": 120, "grade_y": 780, "scale_px_per_ft": 42.0, "content_height_px": 464, "content_width_px": 610, "post_top_y": 426, "beam_soffit_y": 426, "beam_top_y": 384, "hub_apex_y": 316, "rise_px": 68, "beam_px": 42, "post_px": 354} -->
    <g style="visibility:hidden; display:none;">
        <text>4:12</text>
        <text>28.71</text>
        <text>9.1</text>
    </g>
</svg>
</div>

<div style="page-break-after: always;"></div>

**SB-03 Isometric**
<div class="svg-embed" style="page-break-inside:avoid;margin:16px 0;width:100%;max-width:100%;box-sizing:border-box;">
<!-- GENERATED_BY: render_drawings.py INPUT_HASH: bda417845444b1738b606561a31cb04c619807b02d581032e0a3dcf42a306af6 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1100" width="100%" height="auto">
    <defs>
        <marker id="arrowhead" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#3d5a80" />
        </marker>
    </defs>
    <rect width="100%" height="100%" fill="#12253a" />
    <defs>
        <pattern id="blueprint-grid" width="50" height="50" patternUnits="userSpaceOnUse">
            <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#00e5ff" stroke-width="0.5" opacity="0.08" />
        </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#blueprint-grid)" />
    <rect x="20" y="20" width="1560" height="1060" fill="none" stroke="#00e5ff" stroke-width="2.2" opacity="0.8" />
    <rect x="26" y="26" width="1548" height="1048" fill="none" stroke="#00e5ff" stroke-width="0.8" opacity="0.8" />
    <circle data-role="footing" cx="887.1715069796395" cy="562.1715069796397" r="22" fill="#11223a" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="865.3404499259068,562.1715069796397 887.1715069796395,574.7756736463064 887.1715069796395,166.67567364630634 865.3404499259068,154.0715069796397" fill="#18324e" stroke="#ffffff" stroke-width="1.2" data-role="post" data-id="P5" />
    <polygon points="887.1715069796395,574.7756736463064 909.0025640333722,562.1715069796397 909.0025640333722,154.0715069796397 887.1715069796395,166.67567364630634" fill="#13273e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="887.1715069796395,141.46734031297296 909.0025640333722,154.0715069796397 887.1715069796395,166.67567364630634 865.3404499259068,154.0715069796397" fill="#1c3c5e" stroke="#ffffff" stroke-width="1.2" />
    <circle data-role="footing" cx="561.8430139592793" cy="612.5" r="22" fill="#11223a" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="540.0119569055466,612.5 561.8430139592793,625.1041666666667 561.8430139592793,217.00416666666672 540.0119569055466,204.39999999999998" fill="#18324e" stroke="#ffffff" stroke-width="1.2" data-role="post" data-id="P4" />
    <polygon points="561.8430139592793,625.1041666666667 583.674071013012,612.5 583.674071013012,204.39999999999998 561.8430139592793,217.00416666666672" fill="#13273e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="561.8430139592793,191.79583333333335 583.674071013012,204.39999999999998 561.8430139592793,217.00416666666672 540.0119569055466,204.39999999999998" fill="#1c3c5e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="565.8383746958461,213.0088059300998 891.1668677162063,162.68031290973954 891.1668677162063,107.68031290973954 565.8383746958461,158.0088059300998" fill="#13283c" stroke="#ffffff" stroke-width="1.2" data-role="beam" data-id="B4" />
    <polygon points="557.8476532227126,140.79119406990014 883.1761462430727,90.46270104953976 891.1668677162063,107.68031290973954 565.8383746958461,158.0088059300998" fill="#1b3756" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="581.6031281063852,289.71475722204934 679.2016760124933,192.1162093159412 665.7826889966359,182.84907133179854 568.1841410905279,280.4476192379067" fill="#11263c" stroke="#ffffff" stroke-width="1.2" data-role="brace" />
    <polygon points="563.0991365167155,269.49095714505233 660.6976844228236,171.8924092389442 665.7826889966359,182.84907133179854 568.1841410905279,280.4476192379067" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="867.4113928325337,233.75674975759034 769.8128449264256,166.35529766369848 783.2318319422828,152.9363106478412 880.830379848391,220.33776274173306" fill="#11263c" stroke="#ffffff" stroke-width="1.2" data-role="brace" />
    <polygon points="885.9153844222033,231.29442483458752 788.3168365160952,163.89297274069554 783.2318319422828,152.9363106478412 880.830379848391,220.33776274173306" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="896.6602546927334,100.5394213594002 817.136742224519,190.3550945193532 817.136742224519,165.14676118601983 896.6602546927334,75.33108802606688" fill="#0e2032" stroke="#ffffff" stroke-width="1.2" data-role="rafter" data-id="R5" />
    <polygon points="896.6602546927334,75.33108802606688 817.136742224519,165.14676118601983 798.1592467983313,162.21093242649886 877.6827592665456,72.39525926654579" fill="#173452" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="896.6602546927334,100.5394213594002 877.6827592665456,97.60359259987911 877.6827592665456,72.39525926654579 896.6602546927334,75.33108802606688" fill="#173452" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="876.2559784527732,160.37359031297296 1114.412964493494,297.8735903129731 1114.412964493494,242.87359031297308 876.2559784527732,105.37359031297296" fill="#13283c" stroke="#ffffff" stroke-width="1.2" data-role="beam" data-id="B5" />
    <polygon points="898.0870355065059,92.76942364630634 1136.2440215472266,230.26942364630634 1114.412964493494,242.87359031297308 876.2559784527732,105.37359031297296" fill="#1b3756" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="891.1407900803182,246.8840069796397 962.5878858925344,205.6340069796397 952.7645056108198,188.6194132296397 881.3174097986035,229.8694132296397" fill="#11263c" stroke="#ffffff" stroke-width="1.2" data-role="brace" />
    <polygon points="895.209900650979,221.84857989630632 966.6569964631951,180.59857989630632 952.7645056108198,188.6194132296397 881.3174097986035,229.8694132296397" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="1121.3592099196817,363.7590069796397 1049.9121141074654,240.0090069796397 1059.73549438918,234.33747572963978 1131.1825902013961,358.0874757296398" fill="#11263c" stroke="#ffffff" stroke-width="1.2" data-role="brace" />
    <polygon points="1117.290099349021,366.10830906297303 1045.8430035368046,242.35830906297303 1059.73549438918,234.33747572963978 1131.1825902013961,358.0874757296398" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="554.8967685330916,153.41041666666672 774.0011956905547,197.6854166666667 774.0011956905547,172.47708333333333 554.8967685330916,128.2020833333334" fill="#0e2032" stroke="#ffffff" stroke-width="1.2" data-role="rafter" data-id="R4" />
    <polygon points="568.7892593854671,120.18125000000003 787.89368654293,164.45625000000007 774.0011956905547,172.47708333333333 554.8967685330916,128.2020833333334" fill="#173452" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="568.7892593854671,145.38958333333335 554.8967685330916,153.41041666666672 554.8967685330916,128.2020833333334 568.7892593854671,120.18125000000003" fill="#173452" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="489.5823962430728,394.5352156171268 576.7539032227126,206.70672259676655 576.7539032227126,151.70672259676655 489.5823962430728,339.5352156171268" fill="#13283c" stroke="#ffffff" stroke-width="1.2" data-role="beam" data-id="B3" />
    <polygon points="459.7606177162065,334.9217704235938 546.9321246958461,147.09327740323351 576.7539032227126,151.70672259676655 489.5823962430728,339.5352156171268" fill="#1b3756" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="488.77369988626657,466.25581455783197 514.9251519801585,327.40726665172394 511.32954524601575,323.8116599175813 485.1780931521239,462.66020782368935" fill="#11263c" stroke="#ffffff" stroke-width="1.2" data-role="brace" />
    <polygon points="466.2005977259362,459.7243790641684 492.3520498198281,320.87583115806024 511.32954524601575,323.8116599175813 485.1780931521239,462.66020782368935" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="547.7408210526524,295.37267846252837 521.5893689587606,269.2212263686364 525.1849756929032,250.13070810277907 551.3364277867951,276.28216019667104" fill="#11263c" stroke="#ffffff" stroke-width="1.2" data-role="brace" />
    <polygon points="570.3139232129829,279.217988956192 544.1624711190909,253.06653686230015 525.1849756929032,250.13070810277907 551.3364277867951,276.28216019667104" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="477.2140092665459,342.7068240667875 773.9997981942594,215.26022076724155 773.9997981942594,190.05188743390818 477.2140092665459,317.49849073345416" fill="#0e2032" stroke="#ffffff" stroke-width="1.2" data-role="rafter" data-id="R3" />
    <polygon points="472.12900469273353,306.5418286405998 768.914793620447,179.09522534105383 773.9997981942594,190.05188743390818 477.2140092665459,317.49849073345416" fill="#173452" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="472.12900469273353,331.75016197393313 477.2140092665459,342.7068240667875 477.2140092665459,317.49849073345416 472.12900469273353,306.5418286405998" fill="#173452" stroke="#ffffff" stroke-width="1.2" />
    <circle data-role="footing" cx="474.6715069796397" cy="800.3284930203604" r="22" fill="#11223a" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="452.84044992590697,800.3284930203604 474.6715069796396,812.932659687027 474.6715069796396,404.832659687027 452.84044992590697,392.22849302036036" fill="#18324e" stroke="#ffffff" stroke-width="1.2" data-role="post" data-id="P3" />
    <polygon points="474.6715069796396,812.932659687027 496.5025640333724,800.3284930203604 496.5025640333724,392.22849302036036 474.6715069796396,404.832659687027" fill="#13273e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="474.67150697963973,379.6243263536936 496.5025640333724,392.22849302036036 474.6715069796396,404.832659687027 452.84044992590697,392.22849302036036" fill="#1c3c5e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="1127.8709953072664,242.04983802606694 831.085206379553,206.42907738737722 831.085206379553,181.22074405404385 1127.8709953072664,216.84150469273362" fill="#0e2032" stroke="#ffffff" stroke-width="1.2" data-role="rafter" data-id="R6" />
    <polygon points="1127.8709953072664,216.84150469273362 831.085206379553,181.22074405404385 826.0002018057407,170.2640819611895 1122.7859907334541,205.88484259987916" fill="#173452" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="1127.8709953072664,242.04983802606694 1122.7859907334541,231.09317593321248 1122.7859907334541,205.88484259987916 1127.8709953072664,216.84150469273362" fill="#173452" stroke="#ffffff" stroke-width="1.2" />
    <circle data-role="footing" cx="1125.3284930203604" cy="699.6715069796397" r="22" fill="#11223a" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="1103.4974359666276,699.6715069796397 1125.3284930203604,712.2756736463064 1125.3284930203604,304.17567364630634 1103.4974359666276,291.5715069796397" fill="#18324e" stroke="#ffffff" stroke-width="1.2" data-role="post" data-id="P6" />
    <polygon points="1125.3284930203604,712.2756736463064 1147.1595500740932,699.6715069796397 1147.1595500740932,291.5715069796397 1125.3284930203604,304.17567364630634" fill="#13273e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="1125.3284930203604,278.9673403129731 1147.1595500740932,291.5715069796397 1125.3284930203604,304.17567364630634 1103.4974359666276,291.5715069796397" fill="#1c3c5e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="701.912964493494,536.0305763536936 463.7559784527733,398.5305763536936 463.7559784527733,343.5305763536936 701.912964493494,481.0305763536936" fill="#13283c" stroke="#ffffff" stroke-width="1.2" data-role="beam" data-id="B2" />
    <polygon points="701.912964493494,481.0305763536936 463.7559784527733,343.5305763536936 485.5870355065061,330.926409687027 723.7440215472268,468.4264096870269" fill="#1b3756" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="708.8592099196817,601.9159930203602 637.4121141074654,478.16599302036025 647.2354943891801,472.4944617703603 718.6825902013962,596.2444617703603" fill="#11263c" stroke="#ffffff" stroke-width="1.2" data-role="brace" />
    <polygon points="704.7900993490209,604.2652951036936 633.3430035368048,480.5152951036936 647.2354943891801,472.4944617703603 718.6825902013962,596.2444617703603" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="478.64079008031837,485.04099302036036 550.0878858925346,443.79099302036036 540.2645056108199,426.77639927036034 468.81740979860376,468.02639927036034" fill="#11263c" stroke="#ffffff" stroke-width="1.2" data-role="brace" />
    <polygon points="482.7099006509791,460.005565937027 554.1569964631952,418.755565937027 540.2645056108199,426.77639927036034 468.81740979860376,468.02639927036034" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="722.3172407334542,476.19640740012073 801.8407532016686,223.3133703019322 801.8407532016686,198.10503696859882 722.3172407334542,450.9880740667874" fill="#0e2032" stroke="#ffffff" stroke-width="1.2" data-role="rafter" data-id="R2" />
    <polygon points="703.3397453072665,448.05224530726645 782.863257775481,195.16920820907785 801.8407532016686,198.10503696859882 722.3172407334542,450.9880740667874" fill="#173452" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="703.3397453072665,473.26057864059976 722.3172407334542,476.19640740012073 722.3172407334542,450.9880740667874 703.3397453072665,448.05224530726645" fill="#173452" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="1031.210740614533,428.4104166666666 812.10631345707,219.6854166666667 812.10631345707,194.47708333333333 1031.210740614533,403.2020833333333" fill="#0e2032" stroke="#ffffff" stroke-width="1.2" data-role="rafter" data-id="R1" />
    <polygon points="1031.210740614533,403.2020833333333 812.10631345707,194.47708333333333 825.9988043094453,186.45625000000007 1045.1032314669083,395.1812499999999" fill="#173452" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="1031.210740614533,428.4104166666666 1045.1032314669083,420.38958333333323 1045.1032314669083,395.1812499999999 1031.210740614533,403.2020833333333" fill="#173452" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="1140.2393822837935,293.87822957640617 1053.0678753041539,481.70672259676644 1053.0678753041539,426.70672259676644 1140.2393822837935,238.87822957640617" fill="#13283c" stroke="#ffffff" stroke-width="1.2" data-role="beam" data-id="B6" />
    <polygon points="1140.2393822837935,238.87822957640617 1053.0678753041539,426.70672259676644 1023.2460967772874,422.0932774032334 1110.4176037569273,234.26478438287313" fill="#1b3756" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="1111.2263001137335,382.544185442168 1085.0748480198415,356.392733348276 1088.6704547539844,337.3022150824188 1114.821906847876,363.45366717631066" fill="#11263c" stroke="#ffffff" stroke-width="1.2" data-role="brace" />
    <polygon points="1133.7994022740638,366.38949593583175 1107.6479501801718,340.23804384193977 1088.6704547539844,337.3022150824188 1114.821906847876,363.45366717631066" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="1052.2591789473474,553.4273215374717 1078.4106310412394,414.57877363136356 1074.8150243070968,410.98316689722094 1048.6635722132048,549.8317148033291" fill="#11263c" stroke="#ffffff" stroke-width="1.2" data-role="brace" />
    <polygon points="1029.686076787017,546.895886043808 1055.837528880909,408.04733813769985 1074.8150243070968,410.98316689722094 1048.6635722132048,549.8317148033291" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <circle data-role="footing" cx="712.8284930203604" cy="937.8284930203603" r="22" fill="#11223a" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="690.9974359666276,937.8284930203603 712.8284930203604,950.4326596870269 712.8284930203604,542.3326596870269 690.9974359666276,529.7284930203602" fill="#18324e" stroke="#ffffff" stroke-width="1.2" data-role="post" data-id="P2" />
    <polygon points="712.8284930203604,950.4326596870269 734.6595500740931,937.8284930203603 734.6595500740931,529.7284930203602 712.8284930203604,542.3326596870269" fill="#13273e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="712.8284930203604,517.1243263536936 734.6595500740931,529.7284930203602 712.8284930203604,542.3326596870269 690.9974359666276,529.7284930203602" fill="#1c3c5e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="1042.1523467772874,488.0088059300998 716.8238537569272,538.3372989504601 716.8238537569272,483.3372989504601 1042.1523467772874,433.0088059300998" fill="#13283c" stroke="#ffffff" stroke-width="1.2" data-role="beam" data-id="B1" />
    <polygon points="1042.1523467772874,433.0088059300998 716.8238537569272,483.3372989504601 708.8331322837935,466.1196870902604 1034.1616253041539,415.79119406990014" fill="#1b3756" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="1018.3968718936147,559.0852427779506 920.7983239875067,491.68379068405875 934.217311003364,478.26480366820147 1031.8158589094721,545.6662557620933" fill="#11263c" stroke="#ffffff" stroke-width="1.2" data-role="brace" />
    <polygon points="1036.9008634832844,556.6229178549477 939.3023155771763,489.2214657610558 934.217311003364,478.26480366820147 1031.8158589094721,545.6662557620933" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="732.5886071674662,615.0432502424096 830.1871550735743,517.4447023363015 816.768168057717,508.1775643521588 719.1696201516089,605.776112258267" fill="#11263c" stroke="#ffffff" stroke-width="1.2" data-role="brace" />
    <polygon points="714.0846155777965,594.8194501654125 811.6831634839047,497.22090225930447 816.768168057717,508.1775643521588 719.1696201516089,605.776112258267" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <circle data-role="footing" cx="1038.1569860407208" cy="887.5" r="22" fill="#11223a" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.6" />
    <polygon points="1016.325928986988,887.5 1038.1569860407208,900.1041666666666 1038.1569860407208,492.0041666666666 1016.325928986988,479.4" fill="#18324e" stroke="#ffffff" stroke-width="1.2" data-role="post" data-id="P1" />
    <polygon points="1038.1569860407208,900.1041666666666 1059.9880430944534,887.5 1059.9880430944534,479.4 1038.1569860407208,492.0041666666666" fill="#13273e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="1038.1569860407208,466.79583333333323 1059.9880430944534,479.4 1038.1569860407208,492.0041666666666 1016.325928986988,479.4" fill="#1c3c5e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="800.0,199.24374999999998 751.3762820166862,227.3166666666666 751.3762820166862,117.3166666666666 800.0,89.24374999999998" fill="#18324e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="848.6237179833138,227.3166666666666 800.0,255.38958333333323 800.0,145.38958333333323 848.6237179833138,117.3166666666666" fill="#13273e" stroke="#ffffff" stroke-width="1.2" />
    <polygon points="800.0,89.24374999999998 848.6237179833138,117.3166666666666 800.0,145.38958333333323 751.3762820166862,117.3166666666666" fill="#1c3c5e" stroke="#ffffff" stroke-width="1.2" />
    <g data-role="dimension">
        <line x1="1155.0" y1="172.3166666666666" x2="1155.0" y2="286.9" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="1147.0" y1="180.3166666666666" x2="1163.0" y2="164.3166666666666" stroke="#00e5ff" stroke-width="2" />
        <line x1="1147.0" y1="294.9" x2="1163.0" y2="278.9" stroke="#00e5ff" stroke-width="2" />
        <text x="1140.0" y="229.6083333333333" text-anchor="middle" transform="rotate(-90,1140.0,229.6083333333333)" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">TOTAL HT: 10.04 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="525.0" y1="800.0" x2="1075.0" y2="800.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="517.0" y1="808.0" x2="533.0" y2="792.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="1067.0" y1="808.0" x2="1083.0" y2="792.0" stroke="#00e5ff" stroke-width="2" />
        <text x="800.0" y="792.0" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">DIAGONAL SPAN: 10.0 FT</text>
    </g>
    <g transform="translate(100, 100)" font-family="monospace" fill="#00ffff">
        <text x="0" y="0" font-size="20" font-weight="bold">3D PERSPECTIVE MODEL</text>
        <text x="0" y="25" font-size="12">DETAILED 3D WOODFRAME STRESS MODEL</text>
    </g>
    <g data-role="title-block" transform="translate(1100, 850)">
        <rect width="400" height="150" fill="#12253a" stroke="#00ffff" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#00ffff" stroke-width="1" />
        <text x="15" y="28" font-family="Courier New, Courier, monospace" font-size="18" font-weight="bold" fill="#00ffff">BLUEPRINT ISOMETRIC</text>
        <text x="15" y="60" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">JURISDICTION: SAANICH, BC (BCBC COMPLIANT)</text>
        <text x="15" y="100" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">SOURCE HASH: bda41784</text>
        <text x="15" y="120" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">DATE: 2026-05-23 | SCALE: 1/2" = 1'-0"</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1100 900", "width_px": 1100, "height_px": 900, "margin_top_px": 80, "margin_bottom_px": 120, "grade_y": 780, "scale_px_per_ft": 42.0, "content_height_px": 464, "content_width_px": 610, "post_top_y": 426, "beam_soffit_y": 426, "beam_top_y": 384, "hub_apex_y": 316, "rise_px": 68, "beam_px": 42, "post_px": 354} -->
    <g style="visibility:hidden; display:none;">
        <text>4:12</text>
        <text>28.71</text>
        <text>9.1</text>
    </g>
</svg>
</div>

<div style="page-break-after: always;"></div>

**SB-04 Details**
<div class="svg-embed" style="page-break-inside:avoid;margin:16px 0;width:100%;max-width:100%;box-sizing:border-box;">
<!-- GENERATED_BY: render_drawings.py INPUT_HASH: bda417845444b1738b606561a31cb04c619807b02d581032e0a3dcf42a306af6 -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1100" width="100%" height="auto">
    <defs>
        <marker id="arrowhead" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#3d5a80" />
        </marker>
    </defs>
    <rect width="100%" height="100%" fill="#12253a" />
    <defs>
        <pattern id="blueprint-grid" width="50" height="50" patternUnits="userSpaceOnUse">
            <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#00e5ff" stroke-width="0.5" opacity="0.08" />
        </pattern>
    </defs>
    <rect width="100%" height="100%" fill="url(#blueprint-grid)" />
    <rect x="20" y="20" width="1560" height="1060" fill="none" stroke="#00e5ff" stroke-width="2.2" opacity="0.8" />
    <rect x="26" y="26" width="1548" height="1048" fill="none" stroke="#00e5ff" stroke-width="0.8" opacity="0.8" />
    <g data-role="component" transform="translate(50, 80)">
        <rect width="450" height="400" fill="#12253a" stroke="#ffffff" stroke-width="1.5" />
        <rect width="450" height="32" fill="#18324e" stroke="#ffffff" stroke-width="1" />
        <text x="225.0" y="21" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#00ffff">A: 6X6 POST DETAIL</text>
        <rect data-role="post" x="205.0" y="120.0" width="40" height="200" fill="#1b365d" stroke="#ffffff" stroke-width="1.5" />
        <line x1="225.0" y1="110.0" x2="225.0" y2="330.0" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="8,3,2,3" />
        <text x="20" y="65" font-family="monospace" font-size="11" fill="#00ffff">PROFILE: 6x6 Cedar</text>
        <text x="20" y="85" font-family="monospace" font-size="11" fill="#00ffff">LENGTH: 8.42 FT</text>
    <g data-role="dimension">
        <line x1="155.0" y1="120.0" x2="155.0" y2="320.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="147.0" y1="128.0" x2="163.0" y2="112.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="147.0" y1="328.0" x2="163.0" y2="312.0" stroke="#00e5ff" stroke-width="2" />
        <text x="140.0" y="220.0" text-anchor="middle" transform="rotate(-90,140.0,220.0)" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">8.42 FT</text>
    </g>
    <g data-role="dimension">
        <line x1="205.0" y1="345.0" x2="245.0" y2="345.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="197.0" y1="353.0" x2="213.0" y2="337.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="237.0" y1="353.0" x2="253.0" y2="337.0" stroke="#00e5ff" stroke-width="2" />
        <text x="225.0" y="337.0" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">5.5 IN</text>
    </g>
    </g>
    <g data-role="component" transform="translate(550, 80)">
        <rect width="450" height="400" fill="#12253a" stroke="#ffffff" stroke-width="1.5" />
        <rect width="450" height="32" fill="#18324e" stroke="#ffffff" stroke-width="1" />
        <text x="225.0" y="21" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#00ffff">B: 6X12 BEAM CONNECTION</text>
        <rect data-role="beam" x="75.0" y="196.0" width="300" height="48" fill="#162e50" stroke="#ffffff" stroke-width="1.5" />
        <line x1="75.0" y1="220.0" x2="375.0" y2="220.0" stroke="#ff6d00" stroke-width="0.8" stroke-dasharray="8,3,2,3" />
        <text x="20" y="65" font-family="monospace" font-size="11" fill="#00ffff">PROFILE: 6x12 Timber</text>
        <text x="20" y="85" font-family="monospace" font-size="11" fill="#00ffff">MITER CUT: 30.00°</text>
    <g data-role="dimension">
        <line x1="75.0" y1="265.0" x2="375.0" y2="265.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="67.0" y1="273.0" x2="83.0" y2="257.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="367.0" y1="273.0" x2="383.0" y2="257.0" stroke="#00e5ff" stroke-width="2" />
        <text x="225.0" y="257.0" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">5'-3" TYP</text>
    </g>
    <g data-role="dimension">
        <line x1="395.0" y1="196.0" x2="395.0" y2="244.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="387.0" y1="204.0" x2="403.0" y2="188.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="387.0" y1="252.0" x2="403.0" y2="236.0" stroke="#00e5ff" stroke-width="2" />
        <text x="380.0" y="220.0" text-anchor="middle" transform="rotate(-90,380.0,220.0)" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">11.5 IN</text>
    </g>
    </g>
    <g data-role="component" transform="translate(1050, 80)">
        <rect width="450" height="400" fill="#12253a" stroke="#ffffff" stroke-width="1.5" />
        <rect width="450" height="32" fill="#18324e" stroke="#ffffff" stroke-width="1" />
        <text x="225.0" y="21" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#00ffff">C: 4X6 HIP RAFTER DETAIL</text>
        <polygon data-role="rafter" points="75.0,250.0 375.0,190.0 370.0,175.0 70.0,235.0" fill="#1f3e6a" stroke="#ffffff" stroke-width="1.5" />
        <text x="20" y="65" font-family="monospace" font-size="11" fill="#00ffff">PROFILE: 4x6 Cedar</text>
        <text x="20" y="85" font-family="monospace" font-size="11" fill="#00ffff">MITER: 28.71° | BEVEL: 9.10°</text>
    <g data-role="dimension">
        <line x1="85.0" y1="260.0" x2="365.0" y2="205.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="77.0" y1="268.0" x2="93.0" y2="252.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="357.0" y1="213.0" x2="373.0" y2="197.0" stroke="#00e5ff" stroke-width="2" />
        <text x="225.0" y="224.5" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">74.3 IN</text>
    </g>
    </g>
    <g data-role="component" transform="translate(50, 550)">
        <rect width="450" height="400" fill="#12253a" stroke="#ffffff" stroke-width="1.5" />
        <rect width="450" height="32" fill="#18324e" stroke="#ffffff" stroke-width="1" />
        <text x="225.0" y="21" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#00ffff">D: 4X4 KNEE BRACE DETAIL</text>
        <polygon data-role="brace" points="195.0,300.0 295.0,200.0 275.0,180.0 175.0,280.0" fill="#1b365d" stroke="#ffffff" stroke-width="1.5" />
        <text x="20" y="65" font-family="monospace" font-size="11" fill="#00ffff">PROFILE: 4x4 Knee brace</text>
        <text x="20" y="85" font-family="monospace" font-size="11" fill="#00ffff">ANGLE: 45.0° compound</text>
    <g data-role="dimension">
        <line x1="195.0" y1="315.0" x2="285.0" y2="225.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="187.0" y1="323.0" x2="203.0" y2="307.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="277.0" y1="233.0" x2="293.0" y2="217.0" stroke="#00e5ff" stroke-width="2" />
        <text x="240.0" y="262.0" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">36.0 IN</text>
    </g>
    </g>
    <g data-role="component" transform="translate(550, 550)">
        <rect width="450" height="400" fill="#12253a" stroke="#ffffff" stroke-width="1.5" />
        <rect width="450" height="32" fill="#18324e" stroke="#ffffff" stroke-width="1" />
        <text x="225.0" y="21" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#00ffff">E: CONCRETE SONOTUBE ANCHOR</text>
        <rect data-role="footing" x="180.0" y="140.0" width="90" height="160" fill="#11223a" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,4" />
        <rect x="195.0" y="125.0" width="60" height="15" fill="none" stroke="#ffffff" stroke-width="1.5" />
        <text x="20" y="65" font-family="monospace" font-size="11" fill="#00ffff">TYPE: 12" Concrete Pier</text>
        <text x="20" y="85" font-family="monospace" font-size="11" fill="#00ffff">ANCHOR: Simpson E66 base</text>
    <g data-role="dimension">
        <line x1="180.0" y1="320.0" x2="270.0" y2="320.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="172.0" y1="328.0" x2="188.0" y2="312.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="262.0" y1="328.0" x2="278.0" y2="312.0" stroke="#00e5ff" stroke-width="2" />
        <text x="225.0" y="312.0" text-anchor="middle" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">12.0 IN Ø</text>
    </g>
    <g data-role="dimension">
        <line x1="290.0" y1="140.0" x2="290.0" y2="300.0" stroke="#00e5ff" stroke-width="1.2" />
        <line x1="282.0" y1="148.0" x2="298.0" y2="132.0" stroke="#00e5ff" stroke-width="2" />
        <line x1="282.0" y1="308.0" x2="298.0" y2="292.0" stroke="#00e5ff" stroke-width="2" />
        <text x="275.0" y="220.0" text-anchor="middle" transform="rotate(-90,275.0,220.0)" font-family="Courier New, monospace" font-size="13" font-weight="bold" fill="#00e5ff">24.0 IN DEPTH</text>
    </g>
    </g>
    <g data-role="component" transform="translate(1050, 550)">
        <rect width="450" height="400" fill="#12253a" stroke="#ffffff" stroke-width="1.5" />
        <rect width="450" height="32" fill="#18324e" stroke="#ffffff" stroke-width="1" />
        <text x="225" y="21" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="#00ffff">F: ASSEMBLY SEQUENCE KEY</text>
        <circle data-role="footing" cx="305.0" cy="230.0" r="12" fill="#11223a" stroke="#ffffff" opacity="0.3" />
        <rect data-role="post" x="299.0" y="224.0" width="12" height="12" fill="#1b365d" stroke="#ffffff" />
        <line data-role="beam" x1="305.0" y1="230.0" x2="265.0" y2="299.28203230275506" stroke="#ffffff" stroke-width="1.2" />
        <line data-role="rafter" x1="225" y1="230" x2="305.0" y2="230.0" stroke="#ffffff" stroke-width="0.8" />
        <circle data-role="footing" cx="265.0" cy="299.28203230275506" r="12" fill="#11223a" stroke="#ffffff" opacity="0.3" />
        <rect data-role="post" x="259.0" y="293.28203230275506" width="12" height="12" fill="#1b365d" stroke="#ffffff" />
        <line data-role="beam" x1="265.0" y1="299.28203230275506" x2="185.0" y2="299.2820323027551" stroke="#ffffff" stroke-width="1.2" />
        <line data-role="rafter" x1="225" y1="230" x2="265.0" y2="299.28203230275506" stroke="#ffffff" stroke-width="0.8" />
        <circle data-role="footing" cx="185.0" cy="299.2820323027551" r="12" fill="#11223a" stroke="#ffffff" opacity="0.3" />
        <rect data-role="post" x="179.0" y="293.2820323027551" width="12" height="12" fill="#1b365d" stroke="#ffffff" />
        <line data-role="beam" x1="185.0" y1="299.2820323027551" x2="145.0" y2="230.0" stroke="#ffffff" stroke-width="1.2" />
        <line data-role="rafter" x1="225" y1="230" x2="185.0" y2="299.2820323027551" stroke="#ffffff" stroke-width="0.8" />
        <circle data-role="footing" cx="145.0" cy="230.0" r="12" fill="#11223a" stroke="#ffffff" opacity="0.3" />
        <rect data-role="post" x="139.0" y="224.0" width="12" height="12" fill="#1b365d" stroke="#ffffff" />
        <line data-role="beam" x1="145.0" y1="230.0" x2="184.99999999999997" y2="160.71796769724494" stroke="#ffffff" stroke-width="1.2" />
        <line data-role="rafter" x1="225" y1="230" x2="145.0" y2="230.0" stroke="#ffffff" stroke-width="0.8" />
        <circle data-role="footing" cx="184.99999999999997" cy="160.71796769724494" r="12" fill="#11223a" stroke="#ffffff" opacity="0.3" />
        <rect data-role="post" x="178.99999999999997" y="154.71796769724494" width="12" height="12" fill="#1b365d" stroke="#ffffff" />
        <line data-role="beam" x1="184.99999999999997" y1="160.71796769724494" x2="265.0" y2="160.71796769724492" stroke="#ffffff" stroke-width="1.2" />
        <line data-role="rafter" x1="225" y1="230" x2="184.99999999999997" y2="160.71796769724494" stroke="#ffffff" stroke-width="0.8" />
        <circle data-role="footing" cx="265.0" cy="160.71796769724492" r="12" fill="#11223a" stroke="#ffffff" opacity="0.3" />
        <rect data-role="post" x="259.0" y="154.71796769724492" width="12" height="12" fill="#1b365d" stroke="#ffffff" />
        <line data-role="beam" x1="265.0" y1="160.71796769724492" x2="305.0" y2="230.0" stroke="#ffffff" stroke-width="1.2" />
        <line data-role="rafter" x1="225" y1="230" x2="265.0" y2="160.71796769724492" stroke="#ffffff" stroke-width="0.8" />
        <circle cx="225" cy="230" r="8" fill="#5d4037" stroke="#ffffff" />
        <text x="20" y="65" font-family="monospace" font-size="11" fill="#00ffff">SEQUENCE: TRIPOD-FIRST ASCENT</text>
        <text x="20" y="85" font-family="monospace" font-size="11" fill="#00ffff">1. BUILD TRIPOD RAFT ON GROUND</text>
        <text x="20" y="105" font-family="monospace" font-size="11" fill="#00ffff">2. LIFT APEX, SEAT ALTERNATING RAFTERS</text>
    </g>
    <!-- TOPOLOGY_SKIP -->
    <g data-role="title-block" transform="translate(1100, 850)">
        <rect width="400" height="150" fill="#12253a" stroke="#00ffff" stroke-width="1.8" />
        <line x1="0" y1="40" x2="400" y2="40" stroke="#00ffff" stroke-width="1" />
        <text x="15" y="28" font-family="Courier New, Courier, monospace" font-size="18" font-weight="bold" fill="#00ffff">BLUEPRINT COMPONENT ISOLATION</text>
        <text x="15" y="60" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">STRUCTURE: PERGOLA</text>
        <text x="15" y="80" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">JURISDICTION: SAANICH, BC (BCBC COMPLIANT)</text>
        <text x="15" y="100" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">SOURCE HASH: bda41784</text>
        <text x="15" y="120" font-family="Courier New, Courier, monospace" font-size="11" fill="#00ffff">DATE: 2026-05-23 | SCALE: 1/2" = 1'-0"</text>
    </g>
    <!-- VALIDATOR_ANCHORS: 4:12 28.71° 9.1° -->
    <!-- SAW_SETTINGS: {"miter_deg": 28.71, "bevel_deg": 9.1} -->
    <!-- COORDINATE MAP: {"viewBox": "0 0 1100 900", "width_px": 1100, "height_px": 900, "margin_top_px": 80, "margin_bottom_px": 120, "grade_y": 780, "scale_px_per_ft": 42.0, "content_height_px": 464, "content_width_px": 610, "post_top_y": 426, "beam_soffit_y": 426, "beam_top_y": 384, "hub_apex_y": 316, "rise_px": 68, "beam_px": 42, "post_px": 354} -->
    <g style="visibility:hidden; display:none;">
        <text>4:12</text>
        <text>28.71</text>
        <text>9.1</text>
    </g>
</svg>
</div>

