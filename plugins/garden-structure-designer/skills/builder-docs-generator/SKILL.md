---
name: builder-docs-generator
description: Produces the three builder-facing documents that make the plugin output immediately usable for site procurement and construction: budget-estimate.md, lumber-purchase-list.md, and assembly-guide.md. Invoke as Step 13 of design-orchestrator after blueprints are validated.
allowed-tools: Read, Write
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - context/staging/cut-list.json
    validators:
      - plugins/garden-structure-designer/scripts/schema_validator.py
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
- Strictly follow deterministic execution contracts for builder-docs-generator.
- Input parameters must resolve from staging structure.json.

## Quick start


## Workflow
1. **Input Phase**: Load parameters for builder-docs-generator.
2. **Execution Phase**: Process and emit deterministic output.
3. **Gate Phase**: Validate schema and physics integrity.

## Verification


## References
- [Acceptance Criteria](references/acceptance-criteria.md)
