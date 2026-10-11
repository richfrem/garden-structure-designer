---
name: adversarial-drawing-reviewer
description: Launches an independent adversarial drawing-review sub-agent to evaluate SVG outputs for builder usefulness before success can be claimed.
version: 1.3.2
allowed-tools: Read, Write, Bash, Vision
tags:
  - validation
  - svg
  - drawings
  - red-team
  - quality-gate
metadata:
  garden_structure_designer:
    category: validation
    consumes:
      - outputs/*.svg
      - context/staging/structure.json
    produces:
      - context/staging/drawing-red-team-report.json
      - outputs/drawing-red-team-report.md
    validators:
      - plugins/garden-structure-designer/scripts/hardcode_guard.py
      - plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py
      - plugins/garden-structure-designer/scripts/svg_validator.py
      - plugins/garden-structure-designer/scripts/drawing_content_validator.py
    repair_axes:
      - svg_placeholder_geometry
      - svg_missing_dimensions
      - svg_missing_component_details
      - svg_not_builder_meaningful
      - visual_drift_or_regression
      - static_hardcode_violation
---

# Adversarial Drawing Reviewer Skill

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Strictly follow deterministic execution contracts for adversarial-drawing-reviewer.
- Input parameters must resolve from staging structure.json.

## Quick start


## Workflow
1. **Input Phase**: Load parameters for adversarial-drawing-reviewer.
2. **Execution Phase**: Process and emit deterministic output.
3. **Gate Phase**: Validate schema and physics integrity.

## Verification


## References
- [Acceptance Criteria](references/acceptance-criteria.md)
