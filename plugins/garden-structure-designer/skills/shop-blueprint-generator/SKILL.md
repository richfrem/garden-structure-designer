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
- `outputs/blueprint-component-isolation.svg` (for specific joinery cuts, e.g. birdsmouth offsets, bracket hole placement).

Always include key dimensions, lengths of wood, exact angles, and clearly marked dimensional arrows on each diagram. Do not worry about visual clutter—prioritize absolute fabrication clarity over aesthetic beauty.
