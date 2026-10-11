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

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Strictly follow deterministic execution contracts for chrome-verification.
- Input parameters must resolve from staging structure.json.

## Quick start


## Workflow
1. **Input Phase**: Load parameters for chrome-verification.
2. **Execution Phase**: Process and emit deterministic output.
3. **Gate Phase**: Validate schema and physics integrity.

## Verification


## References
- [Acceptance Criteria](references/acceptance-criteria.md)
