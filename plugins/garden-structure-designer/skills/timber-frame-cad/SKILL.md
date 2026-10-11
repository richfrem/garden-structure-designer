---
name: timber-frame-cad
description: Parametric timber-frame CAD solid modeling and view-projection engine. Builds 3D BREP solids (posts, beams, rafters, braces, footings, hubs) using build123d, runs solid-clearance validations, and projects clean, occlusion-sorted 2D views (presentation, structural, fabrication) to SVG.
allowed-tools: Read, Write, Bash
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - outputs/model.step
    validators:
      - scripts/validate_connections.py
      - scripts/cad_backend_build123d.py
    repair_axes:
      - cad_geometry_error
      - solid_collision_warning
---

# Timber Frame CAD

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Python is 100% authoritative for 3D structure: this skill translates the resolved model into a scene (SVG projection) and build123d solids (STEP). It is **not** part of the Rust DXF path.
- `cad_backend_build123d.py` requires every section size, `structure.sides` and `Z_APEX`; missing values fail closed (no 3.5 x 5.5 in defaults).
- DXF drafting is handled by drawing-generator through the ExchangeWriter port (`export_cad.py`). The legacy `cad_backend.py` is deprecated.

## Quick start
```bash
python3 scripts/validate_connections.py [structure.json]
python3 scripts/cad_backend_build123d.py structure.json [out.step]
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: sealed structure.json with a resolved model.
2. **Execution**: `cad_scene.build_structure_scene` builds the scene used by the renderer; `cad_backend_build123d.py` writes `outputs/model.step`.
3. **Gate**: `validate_connections.py` checks physical contact (beam soffits, rafter tips on the hub face, brace feet near posts).

## Verification
- `pytest tests/test_cad_scene.py tests/test_cad_geometry_invariants.py tests/test_validate_connections.py tests/test_cad_backend_build123d.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
