---
name: drawing-generator
description: Produces orthographic projections (Plan view, Elevation view), along with 3D visualizations (Perspective View, Isometric/Axonometric View) based on the structural model coordinates. Output uses consistent scaling and styling. All pixel coordinates MUST be derived from geometry-calculations.json, never computed mentally.
allowed-tools: Read, Write, Bash
---

## Expected Inputs
- `context/staging/structural-model.json`
- `context/staging/geometry-calculations.json` (produced by geometry_engine.py)
- `context/staging/joinery-model.json`

## Pre-Flight: Run Geometry Engine If Not Present
If `geometry-calculations.json` does not exist, run:
```bash
python3 scripts/geometry_engine.py \
    context/staging/structural-model.json
```

## Coordinate Derivation Protocol

**CRITICAL:** Do NOT manually compute pixel positions. Read all coordinates from `geometry-calculations.json → svg_coordinates`:

| SVG Datum       | JSON Key                                  |
|:----------------|:------------------------------------------|
| Grade baseline  | `svg_coordinates.grade_y`                 |
| Post top        | `svg_coordinates.post_top_y`              |
| Beam soffit     | `svg_coordinates.beam_soffit_y`           |
| Beam top        | `svg_coordinates.beam_top_y`              |
| Hub/roof apex   | `svg_coordinates.hub_apex_y`              |
| Scale           | `svg_coordinates.scale_px_per_ft` (42 px/ft) |

Document the derivation at the top of each SVG as an XML comment (one comment block, no double-hyphens):
```xml
<!-- COORDINATE MAP: scale=42px/ft, grade_y=640, post_top_y=Nnn, apex_y=Nnn -->
```

## SVG XML Hard Rules (mandatory pre-check before writing any SVG)

1. **Comments:** `<!-- ... -->` only. **Never use `--` inside the comment body.** This breaks XML parsers.
2. **Attribute values:** Always double-quoted.
3. **Text nodes:** Escape `&` → `&amp;`, `"` → `&quot;`, `'` → `&apos;`, `<` → `&lt;`, `>` → `&gt;`
4. **Validate before writing** (run in Bash):
   ```bash
   python3 -c "import xml.etree.ElementTree as ET; ET.parse('outputs/blueprint-elevation.svg'); print('XML OK')"
   ```
5. If validation fails, fix the XML before writing the file. A broken SVG is worse than no SVG.

## Post-Generation Validation Gate

After generating each SVG, run:
```bash
python3 scripts/svg_validator.py \
    outputs/<sheet>.svg context/staging/structural-model.json
```
Do not proceed to the next sheet if validation fails.

## Behavior

Produce four distinct drawings:
1. **Plan View** — Top-down orthographic. Show post grid, beam ring, diagonal labels, north arrow.
2. **Elevation View** — Front/Side orthographic. Must label: post cut length, clear headroom, beam depth, total height, roof pitch, overhang.
3. **Perspective View** — Human-viewpoint with vanishing points for spatial context. Not dimension-primary.
4. **Isometric View** — Mathematically accurate parallel projection. **DO NOT use AI image generation.** Hardcode the SVG polygon paths using exact coordinates from the JSON.

## Dirty/Clean State

Each generated SVG filename must be registered in `output/document-compiler/manifest.json` with:
```json
{ "file": "...", "sourceChecksum": "<sha256 of structural-model.json>" }
```
On re-run, skip any sheet whose `sourceChecksum` still matches the current file hash.
