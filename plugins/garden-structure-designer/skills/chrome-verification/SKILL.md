---
name: chrome-verification
plugin: garden-structure-designer
description: Runs a headless Chromium browser via Playwright to render generated SVGs, perform pixel-level heuristics (edge density, bounding box fill), and verify visual correctness against baselines.
version: 1.3.2
allowed-tools: read_file, write_file, run_command
tags:
  - verification
  - playwright
  - chromium
  - visual-smoke-test
metadata:
  garden_structure_designer:
    category: validation
    consumes:
      - outputs/*.svg
      - context/staging/structure.json
    produces:
      - context/staging/visual-smoke-report.json
      - outputs/visual-smoke-report.md
      - outputs/visual-smoke/*.png
    validators:
      - plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py
---

# Chrome Visual Verification Skill

This skill governs the visual validation of all generated construction drawings and blueprints using **headless Chromium** via **Playwright**. It ensures that the generated vector outputs are visually correct, not empty or placeholder-quality, and contain all required structural elements without visual regressions.

## Required Behavior

1. **Verify Browser Environment:** Launch Playwright with standard sync API in headless mode. If local rendering is blocked, fail-closed with `BROWSER_RENDER_BLOCKED`.
2. **Render Vectors to Raster:** Navigate to each SVG generated in `outputs/` and take a high-resolution screenshot (PNG) inside a `1600x1200` viewport.
3. **Run Perceptual & Raster Heuristics:**
   - **Non-Background Ratio:** Ensure non-background pixels exceed a minimum ratio (e.g. `0.020` for blueprints, `0.015` for drawings) to detect blank or mostly-empty sheets.
   - **Bounding Box Fill Ratio:** Ensure the structure fills the bounding box adequately.
   - **Spaghetti Hub / Density Check:** Crop the hub junction area and measure edge pixel density. Reject drawings where rafters overlap into a dense visual blob (density > max allowed).
   - **Top-Left Clutter:** Verify the model is centered and not squashed in the top-left corner.
4. **Compile Reports:** Write the final `visual-smoke-report.json` to `context/staging/` and `visual-smoke-report.md` to `outputs/`.

## Authoritative Verification Command

Execute the visual smoke test using the dedicated Playwright runner:

```bash
python3 plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py \
  --structure context/staging/structure.json \
  --svg-dir outputs \
  --out-dir outputs/visual-smoke \
  --report-json context/staging/visual-smoke-report.json \
  --report-md outputs/visual-smoke-report.md \
  --fail-on-regression
```

## Obstacle Gating

If the Chrome-based verification returns `FAIL` or `may_claim_success: false`, the orchestrator must reject the design package. Common visual failure classifications include:
- `BROWSER_RENDER_BLOCKED`: Silent Playwright or display server failure.
- `SPAGHETTI_HUB`: Rafters overlap or penetrate the center hub, resulting in high pixel density.
- `BLANK_SHEET`: Drawing failed to render any elements (low non-background ratio).
- `CLUTTERED_CORNER`: Perspective or scale issues pushing elements to the viewport boundary.
