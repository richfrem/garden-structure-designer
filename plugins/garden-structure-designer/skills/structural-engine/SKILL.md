---
name: structural-engine
description: Generates the structural system based on limits. Computes post placement, beam spans, and rafter geometry. Enforces real-world build constraints by validating spans against safe load paths. Writes geometry section inside structure.json via geometry_engine.py — NEVER derives math mentally.
allowed-tools: Read, Write, Bash
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - context/staging/structure.json  # enriched with members, roof, hub, footings, code, invariants, geometry sections
    validators:
      - plugins/garden-structure-designer/scripts/schema_validator.py
    repair_axes:
      - geometry_warning
      - source_hash_mismatch
---

# Structural Engine

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Strictly follow deterministic execution contracts for structural-engine.
- Input parameters must resolve from staging structure.json.

## Quick start


## Workflow
1. **Input Phase**: Load parameters for structural-engine.
2. **Execution Phase**: Process and emit deterministic output.
3. **Gate Phase**: Validate schema and physics integrity.

## Verification


## References
- [Acceptance Criteria](references/acceptance-criteria.md)
