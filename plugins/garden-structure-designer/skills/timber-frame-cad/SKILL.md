---
name: timber-frame-cad
description: Parametric timber-frame CAD solid modeling and view-projection engine. Builds 3D BREP solids (posts, beams, rafters, braces, footings, hubs) using build123d, runs solid-clearance validations, and projects clean, occlusion-sorted 2D views (presentation, structural, fabrication) to SVG.
allowed-tools: Read, Write, Bash
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - outputs/cad/model.step
      - outputs/cad/model.stl
    validators:
      - plugins/garden-structure-designer/scripts/cad_backend_build123d.py
    repair_axes:
      - cad_geometry_error
      - solid_collision_warning
---

# Execute solid modeling, run CAD geometry validations, and export STEP/STL files

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Strictly follow deterministic execution contracts for timber-frame-cad.
- Input parameters must resolve from staging structure.json.

## Quick start


## Workflow
1. **Input Phase**: Load parameters for timber-frame-cad.
2. **Execution Phase**: Process and emit deterministic output.
3. **Gate Phase**: Validate schema and physics integrity.

## Verification


## References
- [Acceptance Criteria](references/acceptance-criteria.md)
