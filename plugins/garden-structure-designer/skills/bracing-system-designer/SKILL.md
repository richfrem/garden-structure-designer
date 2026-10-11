---
name: bracing-system-designer
description: Designs the lateral stability system by placing knee braces or alternatives. Explains anti-racking mechanics.
allowed-tools: Read, Write
---

# Bracing System Designer

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Defines the `bracing` section: `enabled`, brace section sizes and `constraints` (start/end surfaces, `run_ft`). Brace geometry is solved by `geometry_engine.py`, never by hand.
- Enabled bracing means exactly **2N** braces (two per post) and each must satisfy its plane-contact constraints; disabled bracing means zero (Stage 2 enforces this).
- `validate_intent.py` requires brace width/depth and `run_ft` when bracing is enabled; no silent defaults.

## Quick start
```bash
python3 scripts/validate_intent.py [structure.json]
python3 scripts/constraint_solver.py [structure.json]
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: structural model and the user's lateral-stability preference.
2. **Execution**: set `bracing.enabled` and the brace constraints in structure.json (through the transaction authority), then re-run Stage 1-2.
3. **Gate**: `constraint_solver.py` brace endpoints sit at the beam soffit; Stage 2 brace count is 2N or 0.

## Verification
- `pytest tests/test_constraint_solver.py tests/test_topology_c2_contract.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
