---
name: drawing-generator
description: Generates architectural SVG drawings and updates the composite dependency manifest.
allowed-tools: Read, Write, Bash
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - outputs/drawing-plan-view.svg
      - outputs/drawing-elevation-view.svg
    validators:
      - plugins/garden-structure-designer/scripts/svg_validator.py
    repair_axes:
      - svg_xml_invalid
      - svg_topology_mismatch
      - svg_coordinate_drift
---

# Drawing Generator

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Strictly follow deterministic execution contracts for drawing-generator.
- Input parameters must resolve from staging structure.json.

## Quick start


## Workflow
1. **Input Phase**: Load parameters for drawing-generator.
2. **Execution Phase**: Process and emit deterministic output.
3. **Gate Phase**: Validate schema and physics integrity.

## Verification


## References
- [Acceptance Criteria](references/acceptance-criteria.md)
