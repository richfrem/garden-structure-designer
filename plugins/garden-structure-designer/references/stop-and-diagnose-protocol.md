# Stop-and-Diagnose Protocol (orchestrator reference)

Mandatory when a run produces contradictory, stale, missing or poor outputs. Used by the `design-orchestrator` agent and the `obstacle-triage` skill (`run_obstacle_triage.py` automates the classification; v1.5 adds `RECOVERY_REQUIRED` and `STALE_APPROVAL`).

When a pipeline run produces contradictory, stale, missing, or obviously poor outputs, the agent must stop and diagnose the system state before continuing.

The agent must not immediately rewrite generators, weaken validators, regenerate outputs, or claim success.

This protocol is mandatory when any of the following are true:

- red-team report says `FAIL`, `BLOCKED`, or `may_claim_success: false`;
- quality dashboard says `COMPLETED` while red-team/content reports say `FAIL`;
- generated SVGs are visually placeholder-quality;
- required staging artifacts are missing;
- deterministic artifacts are found in more than one staging path;
- outputs were generated from one path but validated against another;
- reports are stale or have conflicting timestamps;
- validation succeeds but human-visible output is unusable;
- a producer skill appears to be certifying its own work;
- the agent is about to make a large code change to compensate for a state/path/reporting issue.

### Required Triage Steps

Before proceeding, inspect and report:

```bash
pwd
find context plugins/garden-structure-designer/context -maxdepth 4 -type f -name "*.json" | sort
ls -la outputs/
ls -la plugins/garden-structure-designer/context/staging/ || true
ls -la context/staging/ || true
```

Then check:

```bash
cat context/staging/structure.json 2>/dev/null || true
cat plugins/garden-structure-designer/context/staging/structure.json 2>/dev/null || true

cat context/staging/drawing-red-team-report.json 2>/dev/null || true
cat plugins/garden-structure-designer/context/staging/drawing-red-team-report.json 2>/dev/null || true

cat outputs/quality-dashboard.md 2>/dev/null || true
```

### Required Diagnosis

Classify the obstacle as one or more of:

```text
PATH_SPLIT
STALE_REPORT
RENDERER_PLACEHOLDER_OUTPUT
VALIDATOR_TOO_WEAK
VALIDATOR_TOO_STRICT
MISSING_STAGING_ARTIFACT
SOURCE_HASH_MISMATCH
DASHBOARD_STALE_OR_WRONG_PATH
PRODUCER_SELF_CERTIFICATION
SKILL_CONTRACT_INSUFFICIENT
RENDERER_IMPLEMENTATION_REQUIRED
HUMAN_REVIEW_REQUIRED
```

### Required Decision

After diagnosis, choose exactly one next action:

```text
FIX_PATHS_FIRST
RERUN_REPORTS_FIRST
FIX_VALIDATOR_FIRST
FIX_RENDERER_FIRST
FIX_SKILL_CONTRACT_FIRST
BLOCK_AND_REPORT
ASK_HUMAN_REVIEW
```

The agent must explain why that action was chosen.

### Hard Rule

If there is a path split or stale dashboard, fix that before rewriting renderers.

If the validator is correctly rejecting bad outputs, do not weaken the validator.

If the renderer is producing placeholder drawings and the validation path is consistent, then improve the renderer.

If reports disagree, do not continue until the report source-of-truth is reconciled.
