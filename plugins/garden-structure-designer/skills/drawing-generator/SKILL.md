---
name: drawing-generator
description: Generates architectural SVG drawings and updates the composite dependency manifest.
allowed-tools: Read, Write, Bash
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - outputs/drawing-*.svg
      - outputs/blueprint-*.svg
      - outputs/cad/SB01-structure.dxf
      - outputs/cad/SB02-plan.dxf
    validators:
      - scripts/svg_validator.py
      - scripts/drawing_content_validator.py
      - scripts/cross_artifact_validator.py
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
- **Stage 4 (+5.5).** Renders the 8 SVG sheets and writes the two DXF sheets; python owns all geometry, CADCraft only drafts.
- SVG member elements carry `data-role` and `data-tag` (the stable member id; legacy `data-id` is kept). Only member roots are tagged today (F-23): annotations are not yet individually tagged.
- The title block shows the committed revision; sheets from another revision are rejected by `svg_validator.py`.
- DXF export goes through the `ExchangeWriter` port: `CadcraftAdapter` (Rust `cadcraft-cli`, 15 s deadline) with `EzdxfAdapter` as the audited fallback. `auto` falls back silently today (F-5: spec `CAD_REQUIRED` not yet enforced).
- DXFs are currently one polyline per member; the spec target is one INSERT per member with a block (F-1). `cross_artifact_validator.py` parses both sheets (units, layers+colors, XDATA identity, revision, bounds within 0.01 mm).
- The cadcraft binary is located relative to the source repo (`vendor/cadcraft/target/release/cadcraft-cli`); in an installed skill it will be absent and the ezdxf fallback is used (F-4).

## Quick start
```bash
python3 scripts/render_drawings.py [structure.json]
python3 scripts/export_cad.py --structure structure.json --output-dir outputs/cad [--writer auto|cadcraft|ezdxf]
python3 scripts/cross_artifact_validator.py [staging_dir] [outputs_dir]
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: sealed structure.json (Stage 2 topology valid).
2. **Execution**: `render_drawings.py` -> 8 SVGs; `export_cad.py` -> `outputs/cad/SB01-structure.dxf` (3D framing) and `SB02-plan.dxf` (XY plan, Z = 0), both in millimetres (`$INSUNITS = 4`).
3. **Gate**: `svg_validator.py` + `drawing_content_validator.py` per sheet; `cross_artifact_validator.py` for the DXFs (zero auditor errors, member-id parity with structure.json, SVG/DXF dimension cross-checks).

## Verification
- `pytest tests/test_dxf_export_pipeline.py tests/test_cross_artifact_c4_gates.py tests/test_render_drawings_alignment.py tests/test_svg_validator_tags.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
