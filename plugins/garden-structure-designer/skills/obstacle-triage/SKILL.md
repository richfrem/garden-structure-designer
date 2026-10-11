---
name: obstacle-triage
description: Stops the pipeline when outputs, reports, paths, or validators conflict. Classifies systemic obstacles before generation or repair continues.
version: 1.3.3
allowed-tools: Read, Write, Bash
tags:
  - triage
  - validation
  - reliability
  - self-healing
  - path-consistency
metadata:
  garden_structure_designer:
    category: reliability
    consumes:
      - context/staging/*.json
      - plugins/garden-structure-designer/context/staging/*.json
      - outputs/*.svg
      - outputs/quality-dashboard.md
    produces:
      - context/staging/obstacle-triage-report.json
      - outputs/obstacle-triage-report.md
    repair_axes:
      - path_split
      - stale_report
      - renderer_placeholder_output
      - dashboard_wrong_path
      - missing_staging_artifact
---

# Obstacle Triage Skill

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Strictly follow deterministic execution contracts for obstacle-triage.
- Input parameters must resolve from staging structure.json.

## Quick start


## Workflow
1. **Input Phase**: Load parameters for obstacle-triage.
2. **Execution Phase**: Process and emit deterministic output.
3. **Gate Phase**: Validate schema and physics integrity.

## Verification


## References
- [Acceptance Criteria](references/acceptance-criteria.md)
