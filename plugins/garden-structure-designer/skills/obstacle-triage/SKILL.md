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
- Stops the pipeline when reports, paths or approvals conflict, and recommends the next action; it never claims PASS and never weakens validators.
- Classifications: `PATH_SPLIT`, `RECOVERY_REQUIRED` (a C5 journal stuck in COMMITTING: run `structure_io.recover_journals` first), `MISSING_STAGING_ARTIFACT`, `DASHBOARD_STALE_OR_WRONG_PATH`, `STALE_APPROVAL` (approval for another revision), `RENDERER_PLACEHOLDER_OUTPUT`, `UNKNOWN_OBSTACLE`.
- `error_classifier.py` routes structured error codes (`TOPOLOGY_*`, `STALE_REVISION`, `RECOVERY_REQUIRED`, `MISSING_INPUT`, `MISSING_DXF`, `REVISION_MISMATCH`) to repair stages; non-retryable and human-review codes are never auto-repaired.

## Quick start
```bash
python3 scripts/run_obstacle_triage.py
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: staging reports, outputs, the legacy plugin staging directory, journals.
2. **Execution**: classify the obstacle and write `obstacle-triage-report.json` / `.md`.
3. **Gate**: follow `recommended_next_action` (`FIX_PATHS_FIRST`, `RUN_RECOVERY_FIRST`, `RERUN_REPORTS_FIRST`, `FIX_RENDERER_FIRST`, `BLOCK_AND_REPORT`).

## Verification
- `pytest tests/test_run_obstacle_triage.py tests/test_error_classifier_codes.py tests/test_repair_orchestrator_flow.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
