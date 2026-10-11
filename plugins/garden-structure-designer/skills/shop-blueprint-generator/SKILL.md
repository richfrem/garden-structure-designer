---
name: shop-blueprint-generator
description: Generates heavily dimensioned, technical orthographic blueprints intended strictly for carpenters and fabricators. Outputs highly detailed line-drawings packed with dimensional arrows, bolt-hole spacing coordinates, exact cut lengths, and pitch angles. All angles are READ from structure.json — NEVER derived mentally.
allowed-tools: Read, Write, Bash
---

# Shop Blueprint Generator

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Fabrication data comes from `outputs/fabrication/cut-list.json` written by `fabrication_builder.py`; it replaces the deprecated `cut_list_engine.py` and its `outputs/shop-blueprint/SB01-cut-list.json`.
- The cut list is a pure translation of the resolved model and is bound to `meta.revision_id` / `revision_hash` / `source_hash`; a missing rafter or beam angle fails closed (no 28.71 / 9.10 / 30 degree defaults).
- The dimensioned `blueprint-*.svg` sheets are produced by drawing-generator; this skill supplies the cut-list angles and lengths that annotate them.

## Quick start
```bash
python3 scripts/fabrication_builder.py [structure.json]
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: sealed structure.json with `geometry.joints.resolved_model.constraints_resolved`.
2. **Execution**: write `outputs/fabrication/cut-list.json` (schema `fabrication-cut-list/1.0`: axis, stock cut/order length, start/end cuts per member).
3. **Gate**: `package_consistency_validator.py` requires the file and checks its revision against structure.json.

## Verification
- `pytest tests/test_fabrication_builder.py tests/test_package_consistency_validator.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
