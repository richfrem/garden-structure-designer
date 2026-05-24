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

This skill is invoked when the pipeline encounters contradictory state, failed gates, or obviously poor outputs.

It must run before large code rewrites or repeated regeneration attempts.

## Required Checks

1. Identify active working directory.
2. Locate all staging directories.
3. Locate structural model and geometry calculations.
4. Locate validation reports.
5. Compare timestamps and source hashes.
6. Inspect output SVG size and semantic content.
7. Inspect dashboard status.
8. Compare dashboard status with red-team status.
9. Classify the failure.
10. Recommend the next action.

## Output

Write:

```text
context/staging/obstacle-triage-report.json
outputs/obstacle-triage-report.md
```

Use this JSON shape:

```json
{
  "schema": "garden-structure-designer/obstacle-triage-report/1.0",
  "status": "PASS|BLOCKED|ACTION_REQUIRED",
  "failure_classification": [
    "PATH_SPLIT",
    "STALE_REPORT",
    "RENDERER_PLACEHOLDER_OUTPUT"
  ],
  "active_staging_path": "context/staging",
  "conflicting_staging_paths": [
    "plugins/garden-structure-designer/context/staging"
  ],
  "evidence": [
    "structure.json found in context/staging but not plugin staging",
    "quality-dashboard.md says COMPLETED while red-team report says FAIL"
  ],
  "recommended_next_action": "FIX_PATHS_FIRST",
  "do_not_do": [
    "Do not weaken validators",
    "Do not claim PASS",
    "Do not compile PDF"
  ]
}
```
