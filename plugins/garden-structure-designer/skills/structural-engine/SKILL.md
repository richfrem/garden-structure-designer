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
      - scripts/schema_validator.py
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
- **Stages 1-3.** Geometry is solved by `geometry_engine.py` and validated by `topology_compiler.py` (Stage 2) and `structural_physics_validator.py` (Stage 3); math is never derived mentally.
- Stage 2 compares the **actual solved arrays** with the declared intent: N posts, N beams (`layout.beam_segments`), N primary rafters (`geometry.joints.primary_rafters`, mirrored exactly), N hub faces `H1..HN`, 2N braces when bracing is enabled (0 otherwise), a regular finite polygon. A cached count scalar is never an authority.
- Stage 3 is a **screening** check with required inputs (a missing dimension yields `BLOCKED`, not a defaulted result). It is not a design check or engineering certification: jurisdiction-specific snow/wind design checks are still open (F-20).
- Known open findings: `geometry.compound_cut` is a fixed 28.71/9.1 constant (F-25), brace ids are legacy `K<i>A/B` (F-18), `geometry_engine` writes the canonical file directly (F-11).
- Re-solving after an intent change must create a new revision: `reset_derived.py` applies the reset through the C5 transaction (CAS, new revision, derived artifacts purged).

## Quick start
```bash
python3 scripts/geometry_engine.py [structure.json]
python3 scripts/topology_compiler.py [structure.json]
python3 scripts/structural_physics_validator.py [structure.json]
python3 scripts/constraint_solver.py [structure.json]
python3 scripts/schema_validator.py [staging_dir] [schema_dir]
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Stage 1**: `geometry_engine.py` seals `geometry` (z planes, layout, beam segments, hub face planes, rafters, braces, resolved model).
2. **Stage 2**: `topology_compiler.py` validates the sealed arrays and writes `geometry.joints.topology`; failures return a structured error code and nothing downstream runs.
3. **Stage 3**: `structural_physics_validator.py` writes `physics-validation-report.json` (bound to `source_hash` and the revision); `constraint_solver.py` and `schema_validator.py` add joint and schema checks.

## Verification
- `pytest tests/test_geometry_engine.py tests/test_topology_c2_contract.py tests/test_physics_validator_strict.py tests/test_constraint_solver.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
