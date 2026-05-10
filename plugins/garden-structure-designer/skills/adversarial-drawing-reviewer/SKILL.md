---
name: adversarial-drawing-reviewer
description: Launches an independent adversarial drawing-review sub-agent to evaluate SVG outputs for builder usefulness before success can be claimed.
version: 1.3.2
allowed-tools: Read, Write, Bash
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
      - context/staging/structural-model.json
      - context/staging/geometry-calculations.json
    produces:
      - context/staging/drawing-red-team-report.json
      - outputs/drawing-red-team-report.md
    validators:
      - plugins/garden-structure-designer/scripts/svg_validator.py
      - plugins/garden-structure-designer/scripts/drawing_content_validator.py
    repair_axes:
      - svg_placeholder_geometry
      - svg_missing_dimensions
      - svg_missing_component_details
      - svg_not_builder_meaningful
---

# Adversarial Drawing Reviewer Skill

This skill exists to prevent green-check theater.

The drawing generator cannot certify its own success.

This skill must launch or simulate an independent adversarial review of every generated SVG before the package can be marked `PASS`.

## Required Behavior

1. Read all SVG outputs in `outputs/`.
2. Read deterministic model files:
   - `context/staging/structural-model.json`
   - `context/staging/geometry-calculations.json`
3. Run `svg_validator.py` if available.
4. Run `drawing_content_validator.py` if available.
5. Launch the `drawing-red-team-agent` or conduct the same review using its criteria.
6. Write:
   - `context/staging/drawing-red-team-report.json`
   - `outputs/drawing-red-team-report.md`
7. Set `may_claim_success` to `true` only when all drawings are builder-meaningful.

## Mandatory Failure Rule

If the generated drawings are mostly blank, tiny, childish, symbolic, or placeholder-quality, this skill must return `FAIL` or `PARTIAL`.

Do not allow `PASS` merely because XML validation passes.

## Required Commands

At minimum run:

```bash
for f in outputs/*.svg; do
  python3 plugins/garden-structure-designer/scripts/svg_validator.py \
    "$f" \
    plugins/garden-structure-designer/context/staging/structural-model.json
done
```

If implemented:

```bash
for f in outputs/*.svg; do
  python3 plugins/garden-structure-designer/scripts/drawing_content_validator.py \
    "$f" \
    plugins/garden-structure-designer/context/staging/structural-model.json
done
```

Then perform adversarial review using the `drawing-red-team-agent` rubric.

## Final Gate

The orchestrator must read:

```text
context/staging/drawing-red-team-report.json
```

If:

```json
"may_claim_success": false
```

then the package status must not be `PASS`.

Allowed statuses are:

```text
PARTIAL
BLOCKED
DRAFT ONLY
```

The job is not done until this skill approves the drawings.
