---
name: shop-blueprint-generator
description: Generates heavily dimensioned, technical orthographic blueprints intended strictly for carpenters and fabricators. Outputs highly detailed line-drawings packed with dimensional arrows, bolt-hole spacing coordinates, exact cut lengths, and pitch angles.
allowed-tools: Read, Write
---

## Expected Inputs
`context/staging/structural-model.json`
`context/staging/joinery-model.json`

## Behavior
Acts as the technical draftsman. Unlike `drawing-generator` which outputs clean architectural visualizations, this skill strictly generates messy, detail-heavy SVG blueprints.
It should produce output files like:
- `outputs/blueprint-plan.svg`
- `outputs/blueprint-elevation.svg`
- `outputs/blueprint-isometric.svg` (for a mathematically accurate dimensioned parallel 3D wireframe. DO NOT use AI image generation for this because generative models frequently hallucinate arbitrary geometry like octagons instead of hexagons. You MUST hardcode a strict isometric mathematically projected SVG path that natively adheres to the exact post count.)
- `outputs/blueprint-component-isolation.svg` (for specific joinery cuts, e.g. birdsmouth offsets, bracket hole placement).

**CRITICAL SVG FORMATTING RULE:**
Because these are strictly XML documents, if you include text nodes (like `DWG: EL-1 (FRONT ELEVATION & PITCH)` or `5'-0"`), you MUST escape all restricted characters:
- Ampersands (`&`) became `&amp;`
- Double quotes (`"`) inside text become `&quot;`
- Single quotes (`'`) inside text become `&apos;`
- Less/Greater than (`<` / `>`) become `&lt;` / `&gt;`
Failing to escape these will immediately break the SVG markdown parser.

Always include key dimensions, lengths of wood, exact angles, and clearly marked dimensional arrows on each diagram. Do not worry about visual clutter—prioritize absolute fabrication clarity over aesthetic beauty.
