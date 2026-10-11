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
      - scripts/visual_svg_smoke_test.py
---

# Chrome Visual Verification Skill

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- **Stage 5.6.** Rasterizes each SVG sheet (macOS Quick Look or headless Chromium via Playwright) and checks pixel heuristics plus OpenCV topology and hub-density checks.
- The report requires `meta.source_hash` and records the revision (`revision_id`, `revision_hash`); it never reports PASS for unsealed geometry.
- A render-blocked sheet (`BROWSER_RENDER_BLOCKED`) is a failure, not a skip.

## Quick start
```bash
python3 scripts/visual_svg_smoke_test.py --structure structure.json --svg-dir outputs --out-dir outputs/visual-smoke --report-json context/staging/visual-smoke-report.json --report-md outputs/visual-smoke-report.md
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: the eight SVG sheets and the sealed structure.json.
2. **Execution**: render PNGs, evaluate metrics per sheet, optionally compare with a baseline (`--baseline-dir --fail-on-regression`).
3. **Gate**: `may_claim_success` must be true; the red-team gate consumes the report and rejects it when it predates the SVGs.

## Verification
- `pytest tests/test_visual_svg_smoke_test.py tests/test_visual_smoke_main.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
