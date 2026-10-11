---
name: adversarial-drawing-reviewer
description: Launches an independent adversarial drawing-review sub-agent to evaluate SVG outputs for builder usefulness before success can be claimed.
version: 1.3.2
allowed-tools: Read, Write, Bash, Vision
tags:
  - validation
  - svg
  - drawings
  - red-team
  - quality-gate
metadata:
  garden_structure_designer:
    category: validation
    consumes:
      - outputs/*.svg
      - context/staging/structure.json
    produces:
      - context/staging/drawing-red-team-report.json
      - outputs/drawing-red-team-report.md
    validators:
      - scripts/hardcode_guard.py
      - scripts/visual_svg_smoke_test.py
      - scripts/svg_validator.py
      - scripts/drawing_content_validator.py
    repair_axes:
      - svg_placeholder_geometry
      - svg_missing_dimensions
      - svg_missing_component_details
      - svg_not_builder_meaningful
      - visual_drift_or_regression
      - static_hardcode_violation
---

# Adversarial Drawing Reviewer Skill

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- **Stage 5.** Independent approval: drawing success is never self-certified; `may_claim_success: true` comes only from this gate.
- The report is bound to the reviewed revision (`revision_id`, `revision_hash`, `hash_algorithm gsd-json-v1`); an unstamped or hash-mismatched structure is `BLOCKED`.
- Approval requires all 8 SVG sheets to pass the peer validators and visual smoke, **and** the parsed DXF sheets and the revision-bound `fabrication/cut-list.json` to pass.
- `compile_package.py` rejects an approval that is not bound to the current revision; approvals are never carried forward to a new revision.
- `hardcode_guard.py` is the static gate for silent numeric defaults; its default targets include the hardened scripts.

## Quick start
```bash
python3 scripts/run_drawing_red_team.py --svg-dir outputs --model structure.json --report-dir context/staging --md-dir outputs
python3 scripts/hardcode_guard.py [file.py ...]
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: SVGs, DXFs, cut list, staging reports (schema, physics, visual smoke) all from the same `source_hash`.
2. **Execution**: run `svg_validator.py` and `drawing_content_validator.py` per sheet, evaluate the smoke report, validate DXFs and the cut list.
3. **Gate**: write `drawing-red-team-report.json` / `.md`; exit 0 only when `may_claim_success` is true.

## Verification
- `pytest tests/test_run_drawing_red_team.py tests/test_hardcode_guard.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
