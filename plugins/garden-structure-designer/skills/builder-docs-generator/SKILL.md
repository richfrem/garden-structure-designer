---
name: builder-docs-generator
description: Produces the three builder-facing documents that make the plugin output immediately usable for site procurement and construction: budget-estimate.md, lumber-purchase-list.md, and assembly-guide.md. Invoke as Step 13 of design-orchestrator after blueprints are validated.
allowed-tools: Read, Write
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
      - outputs/fabrication/cut-list.json
    produces:
      - outputs/assembly-guide.md
      - outputs/budget-estimate.md
      - outputs/lumber-purchase-list.md
    validators:
      - scripts/assembly_guide_validator.py
    repair_axes:
      - schema_error
---

# Builder Docs Generator

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Produces `assembly-guide.md`, `budget-estimate.md` and `lumber-purchase-list.md` from `structure.json` and `outputs/fabrication/cut-list.json` (Stage 6 documents).
- Every structural input is required: a missing miter/bevel, section size, region, side count or brace data stops generation (`MISSING_INPUT`); nothing is guessed.
- Board feet are derived as (actual width x depth / 12) x cut length; the tripod hoisting section is emitted only when the rafter count divides into three equal sets (hexagon: 'three alternating rafters').
- Unit prices and hardware allowances are disclosed planning assumptions, not structural inputs.

## Quick start
```bash
python3 scripts/builder_docs_compiler.py [staging_dir] [outputs_dir]
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: structure.json and the fabrication cut list.
2. **Execution**: write the three markdown documents into `outputs/`.
3. **Gate**: `assembly_guide_validator.py` checks saw settings and the hex tripod method against the structure.

## Verification
- `pytest tests/test_builder_docs_compiler.py tests/test_assembly_guide_validator.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
