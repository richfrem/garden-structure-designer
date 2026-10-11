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
- Python remains 100% authoritative over 3D structural geometry, solid models, and graph topology.
- CAD export to 2D/3D DXF drafting sheets is handled downstream via the ExchangeWriter port (`export_cad.py`).

## Quick start
```bash
python3 plugins/garden-structure-designer/scripts/cad_scene.py
```

## Workflow
1. **Input Phase**: Load sealed `structure.json` geometry and joint definitions.
2. **Execution Phase**: Build 3D BREP solids (posts, beams, rafters, braces, footings, hubs) and perform solid clearance validations.
3. **Gate Phase**: Validate geometry invariants with `test_cad_geometry_invariants.py`.

## Verification
- Run `pytest plugins/garden-structure-designer/tests/test_cad_scene.py`.
- Run `pytest plugins/garden-structure-designer/tests/test_cad_geometry_invariants.py`.

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
