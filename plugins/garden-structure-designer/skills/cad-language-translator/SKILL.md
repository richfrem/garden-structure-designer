---
name: cad-language-translator
description: >
  Translates human design intent from structure.json into formal CAD
  constraint language. This is the critical bridge between "what the user
  wants" and "what the geometry compiler can solve." No geometry is computed
  here — only constraints are defined.
model: inherit
tools: ["Read", "Write", "Bash"]
---

# Cad Language Translator

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Stage 1 prelude: defines constraints and reference planes only; **no geometry is solved here**.
- Output is the `cad_constraints` section (reference planes, member constraints, global constraints) and `meta.lifecycle = CONSTRAINTS_DEFINED`.
- Review findings still open: two `proportion_rules` booleans are constants (F-14), hidden minimums (hub radius 0.75 ft, brace run 1.5 ft) need explicit inputs (F-15), and the CLI writes `structure.json` directly instead of through the transaction authority (F-11).

## Quick start
```bash
python3 scripts/cad_language_translator.py [structure.json]
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: validated, unsealed structure.json (`assert_not_sealed(structure, 'cad_constraints')`).
2. **Execution**: derive post coordinates, footing/post/beam/roof/hub reference planes and per-member constraints from structure.json.
3. **Gate**: `geometry_engine.py` consumes the constraints in the next stage; a constraint it cannot satisfy raises instead of being repaired.

## Verification
- `pytest tests/test_cad_language_translator.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
