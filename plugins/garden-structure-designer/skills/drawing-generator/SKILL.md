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

Each generated SVG filename must be registered in `outputs/document-compiler/manifest.json` with:
```json
{ "file": "...", "sourceChecksum": "<sha256 of structural-model.json>" }
```
On re-run, skip any sheet whose `sourceChecksum` still matches the current file hash.

## Gotchas

- **Double-hyphen inside SVG XML comments breaks all parsers.** Even a single `--` inside a comment body causes `xml.etree.ElementTree.parse()` to throw; the sheet is rejected by the validator. Check every comment before writing.
- **`grade_y=640` is not a constant.** The grade baseline Y coordinate is scale-dependent. Always read `svg_coordinates.grade_y` from geometry-calculations.json. Hardcoding 640 will misalign all vertical coordinates when scale changes.
- **Checksum skip does not account for joinery/bracing changes.** If bracing-system-designer ran after the last drawing pass (and set `bracing_added: true` in structural-model.json) but did not change the model's structural dimensions, the hash will appear unchanged. Always check `bracing_added` flag and force-regenerate affected sheets.
- **Perspective view is NOT AI-generated.** Perspective SVGs must be built from SVG polygon paths computed from the coordinate map. Any AI image generation is forbidden and will fail the validation gate.
- **Four distinct sheets are required.** Plan, Elevation, Perspective, and Isometric must all be generated and individually validated before the stage is considered complete. A missing sheet is a blocking failure.

## Smoke Test

1. **Standard four-sheet generation:** Given a validated structural-model.json with geometry-calculations.json present: all four sheets generated, `svg_validator.py` exits 0 for each, manifest.json updated with current checksums. ✓
2. **Idempotent re-run:** Re-run with unchanged structural-model hash and no `bracing_added` flag: all sheets skipped (logged as "up to date"), manifest unchanged. ✓
3. **Validator rejection triggers halt:** A sheet with a double-hyphen comment body: `svg_validator.py` returns non-zero, skill halts and reports the specific XML error. ✓

## Completion: HANDOFF_BLOCK

On successful completion emit this block so the design-orchestrator can gate Stage 4:

```json
{
  "stage": "drawing-generator",
  "status": "COMPLETE",
  "sheets_generated": ["plan", "elevation", "perspective", "isometric"],
  "sheets_validated": 4,
  "manifest_updated": true,
  "next_stage": "shop-blueprint-generator"
}
```

If any sheet fails validation, set `"status": "FAIL"`, list the failed sheets in `"validation_failures"`, and return to the orchestrator.
