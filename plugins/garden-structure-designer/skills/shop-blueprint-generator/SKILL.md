---
name: shop-blueprint-generator
description: Generates heavily dimensioned, technical orthographic blueprints intended strictly for carpenters and fabricators. Outputs highly detailed line-drawings packed with dimensional arrows, bolt-hole spacing coordinates, exact cut lengths, and pitch angles. All angles are READ from geometry-calculations.json — NEVER derived mentally.
allowed-tools: Read, Write, Bash
---

## Expected Inputs
- `context/staging/structural-model.json`
- `context/staging/geometry-calculations.json` (produced by geometry_engine.py)
- `context/staging/joinery-model.json`

## Pre-Flight: Run Geometry Engine If Not Present
```bash
python3 scripts/geometry_engine.py \
    context/staging/structural-model.json
```

## CRITICAL: Source of Truth for All Angles and Dimensions

**You are FORBIDDEN from computing any angle or dimension internally.**

Read all fabrication values from `context/staging/geometry-calculations.json`:

| Blueprint Field         | JSON Path                                    |
|:------------------------|:---------------------------------------------|
| Miter (saw swing)       | `compound_cut.miter_deg`                     |
| Blade Bevel             | `compound_cut.bevel_deg`                     |
| Pitch angle             | `compound_cut.pitch_angle_deg`               |
| Rafter length (total)   | `rafter.total_with_overhang_in`              |
| Roof rise               | `roof_rise.rise_in`                          |
| Total building height   | `total_height.total_height_ft`               |
| SVG coordinates         | `svg_coordinates.*`                          |

**The most common hallucination:** Using the pitch angle (e.g. 18.43°) as the compound miter setting. The miter angle for a hexagonal hip rafter at 4:12 pitch is **28.71°**, not 18.43°. The geometry engine calculates this correctly — use it.

## SVG XML Hard Rules (mandatory — same as drawing-generator)

1. Comments: `<!-- ... -->` only. **No `--` inside comment bodies.**
2. Text nodes: escape `&` → `&amp;`, `"` → `&quot;`, `<` → `&lt;`, `>` → `&gt;`
3. **Validate every SVG before writing:**
   ```bash
   python3 -c "import xml.etree.ElementTree as ET; ET.parse('outputs/blueprint-shop.svg'); print('XML OK')"
   ```
4. Then run the full validator:
   ```bash
   python3 scripts/svg_validator.py \
       outputs/<sheet>.svg context/staging/structural-model.json
   ```

## Behavior

Produce output files:
- `outputs/blueprint-plan.svg` — Footprint with post coordinates, beam ring, diagonal.
- `outputs/blueprint-elevation.svg` — Dimensioned elevation with all critical labels.
- `outputs/blueprint-isometric.svg` — Mathematically projected parallel wireframe. **NO AI image generation.** Use exact SVG polygon paths derived from the coordinate map.
- `outputs/blueprint-component-isolation.svg` — Isolated detail for compound cut geometry (rafter top/bottom, bird's mouth, hub bolt placement).

## Cut List Rules

When generating the cut list table:
- Copy `miter_deg` and `bevel_deg` verbatim from `geometry-calculations.json`.
- Format as: `Miter: XX.X° / Bevel: X.X°`
- Include a note: `⚠ Test cut on scrap before cutting all [N] pieces.`
- Never include a "Derived by" note — all values come from the geometry engine.

Always prioritize fabrication clarity over visual aesthetics. Dense dimensions, bold callout arrows, and explicit warnings are preferred.
