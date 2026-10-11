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
- All rendered elements must carry semantic `data-role` and `data-tag` attributes matching stable member IDs.
- Primary CAD drafting export routes through the ExchangeWriter port (`export_cad.py`).

## Quick start
```bash
python3 plugins/garden-structure-designer/scripts/render_drawings.py [structure_path]
python3 plugins/garden-structure-designer/scripts/export_cad.py [structure_path] [outputs_cad_dir]
```

## Workflow
1. **Input Phase**: Load sealed `structure.json` geometry and topological graph.
2. **Execution Phase**: 
   - Render all 8 SVG sheets (plan, elevation, isometric, perspective, blueprints, component isolation) with visible IDs.
   - Export multi-sheet DXF deliverables: `SB01-structure.dxf` (3D framing) and `SB02-plan.dxf` (2D planar projection) via `CadcraftAdapter` (or fallback `EzdxfAdapter`).
3. **Gate Phase**: 
   - Validate SVGs with `svg_validator.py` and `drawing_content_validator.py`.
   - Validate DXFs with `cross_artifact_validator.py` asserting zero auditor errors, 1:1 member ID parity, and SVG/DXF dimension cross-checks.

## Verification
- Run `pytest plugins/garden-structure-designer/tests/test_dxf_export_pipeline.py`.
- Run `pytest plugins/garden-structure-designer/tests/test_drafting_standards.py`.

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
