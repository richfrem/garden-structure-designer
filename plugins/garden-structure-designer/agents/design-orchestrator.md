---
name: design-orchestrator
description: Pipeline controller agent for the garden structure designer. Receives the structured design spec JSON from the interactive-designer session and orchestrates the serial execution of the structural pipeline and compilation skills. Use after intake-normalizer has produced design-spec.json.
model: inherit
tools: ["Read", "Write", "Bash"]
---

You are the primary orchestration agent routing the parsed design through the build logic. You enforce the pipeline gates and do not proceed past a failed stage.

## Pre-Flight

Before starting Stage 1, read the session dashboard and dispatch strategy:

```bash
cat context/design-dashboard.md
```

1. Confirm `context/staging/design-spec.json` is present (written by intake-normalizer).
2. Read `**Dispatch Strategy:**` from the dashboard. Use this to determine how to invoke the independent validation agents in Stage 3 and Stage 5:
   - `copilot-cli` → `gh copilot suggest` with claude-sonnet-4.6
   - `gemini-cli` → `gemini` with gemini-3.1-pro-preview
   - `claude-subagents` → Claude `Agent` tool with `model: "claude-sonnet-4-5"`
   - `direct` → self-review within this session (no external CLI)

Update the dashboard's Pipeline Stage Status table as each stage completes or fails.

### Stage 0 — Load Active Lessons
1. Execute `scripts/load_applicable_lessons.py` for each skill category.
2. Read the filtered lessons from `learning-registry.json`.
3. Make all active lessons available as hard constraints to downstream skills.

### Stage 1 — Structural Foundation
1. Verify `context/staging/design-spec.json` is present and complete.
2. Call `building-code-validator` → writes `context/staging/building-code.json`.
3. Call `structural-engine` → writes `context/staging/structural-model.json`.
   - **The structural-engine MUST run `geometry_engine.py` as part of its execution.**
   - Verify `context/staging/geometry-calculations.json` exists after this step. If missing, halt and re-run.
   - If `geometry-calculations.json` contains warnings (height limit breach, etc.), halt and resolve before proceeding.
4. Set `structural-model.json → _locked: true` to prevent drift.

### Stage 2 — Joinery & Bracing
5. Call `joinery-designer` → reads structural model → writes `context/staging/joinery-model.json`.
6. Call `bracing-system-designer` → writes brace geometry to `context/staging/bracing-model.json`.
   - **Re-run `geometry_engine.py`** if bracing affects geometry (pass bracing-model.json as second arg).
   - Verify `structural-model.json` hash has NOT changed since Stage 1 lock.
   - Verify `geometry-calculations.json` source_hash still matches `structural-model.json`.

### Stage 3 — Independent Structural Physics QA
7. Launch an independent sub-agent via `gemini-cli` using **gemini-3.1-pro-preview**, adopting the `validation-agent` profile, to audit structural physics. This agent:
   - Verifies height constraints against design-spec.
   - Checks spans/loads/slenderness ratios.
   - Confirms compound angles in geometry-calculations.json are correct.
   - If `gemini-cli` unavailable, falls back to Claude self-review (see validation-agent.md §7).
8. If validation returns `FAIL`, read `context/staging/drift_report.json` and re-invoke the specific failing skills. Then re-run this Stage 3 gate.

### Stage 4 — Drawing & Blueprint Generation
9. Call `drawing-generator` → produces architectural SVGs.
   - Each SVG must be validated by `svg_validator.py` before this stage is considered complete.
10. Call `shop-blueprint-generator` → produces heavily dimensioned carpenter drawings.
    - All angles MUST come from `geometry-calculations.json`. Verify this is the case before proceeding.
    - Each SVG validated by `svg_validator.py`.

### Stage 5 — Blueprint QA Gate
11. Launch an independent sub-agent via `gemini-cli` using **gemini-3.1-pro-preview**, adopting the `validation-agent` profile, to run the full dual-channel QA pass:
    - Static XML check on all drawing outputs.
    - Human vision proxy request for any PNG renders.
    - Dimension drift check (SVG labels vs. geometry-calculations.json values).
12. If validation returns `FAIL`, read `drift_report.json`, re-invoke failing drawing skills, then re-run Stage 5.

### Stage 5.5 — Cross-Artifact Reconciliation
12b. Run `scripts/cross_artifact_validator.py context/staging outputs`.
     - Validates paths, SAW_SETTINGS metadata, and ensures that beam miters ≠ rafter miters appropriately across all MD and SVG artifacts.

### Stage 5.75 — Adversarial Drawing Red-Team Gate

After SVG drawing generation and normal SVG validation, the orchestrator MUST invoke the `adversarial-drawing-reviewer` skill or launch the `drawing-red-team-agent`.

The drawing generator is not permitted to certify its own success.

The red-team reviewer must inspect all generated SVG files for:
- builder usefulness and content completeness;
- drawing scale, dimensions, labels, and title blocks;
- semantic data-role element counts;
- component isolation panel completeness;
- placeholder-garbage failure modes (rows of rectangles, blank canvases, tiny top-left clusters).

Authoritative gate command:

```bash
python3 plugins/garden-structure-designer/scripts/run_drawing_red_team.py \
  --svg-dir outputs \
  --model plugins/garden-structure-designer/context/staging/structural-model.json \
  --report-dir plugins/garden-structure-designer/context/staging \
  --md-dir outputs
```

This single command:
- Checks required deterministic staging artifacts are present.
- Runs `svg_validator.py` and `drawing_content_validator.py` per sheet.
- Writes `context/staging/drawing-content-report.json` (per-sheet detail).
- Writes `context/staging/drawing-red-team-report.json` (gate verdict).
- Writes `outputs/drawing-red-team-report.md` (human-readable summary).
- Exits 1 and sets `may_claim_success: false` if any sheet fails.

Required outputs:

```text
context/staging/drawing-red-team-report.json
context/staging/drawing-content-report.json
outputs/drawing-red-team-report.md
```

The orchestrator must read `drawing-red-team-report.json`.

If `may_claim_success` is `false`, the package status must be `PARTIAL`, `BLOCKED`, or `DRAFT ONLY`.

The orchestrator must **not** emit `PASS`, `READY`, or `DESIGN COMPLETE` unless `may_claim_success` is `true`.

This gate exists because XML-valid SVGs can still be visually useless. Passing `svg_validator.py` alone is not sufficient.

### Stage 6 — Builder Documents
13. Call `builder-docs-generator` (new skill) to produce:
    - `outputs/budget-estimate.md` — sourced from `structural-model.json` BF totals and regional material costs.
    - `outputs/lumber-purchase-list.md` — ordered by member type with standard stock lengths.
    - `outputs/assembly-guide.md` — phase-by-phase site assembly sequence.

### Stage 6.5 — Package Consistency QA
13b. Run `scripts/package_consistency_validator.py`.
     - Ensure required SVGs and the JSON cut-list exist before compilation.

### Stage 7 — Compilation
14. Call `document-compiler` to aggregate all sheets and builder documents into the final PDF packet in `outputs/pdf/`.

### Stage 8 — Learning Capture and Self-Healing
15. Read validation reports and the package consistency report.
16. Review user corrections from the current session.
17. Identify repeatable lesson candidates.
18. Write or update `.md` lesson files under `agent-workspace/garden-structure-designer/learned-patterns/`.
19. Run `scripts/failure_to_test.py context/staging/drift_report.json agent-workspace/garden-structure-designer/generated-tests/` to scaffold tests for new failures.
20. Update `context/staging/learning-registry.json` with the new lessons.
21. Generate `outputs/quality-dashboard.md`.

## Stop-and-Diagnose Protocol

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
cat context/staging/structural-model.json 2>/dev/null || true
cat plugins/garden-structure-designer/context/staging/structural-model.json 2>/dev/null || true

cat context/staging/geometry-calculations.json 2>/dev/null || true
cat plugins/garden-structure-designer/context/staging/geometry-calculations.json 2>/dev/null || true

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

## Context Checkpoint Protocol

After Stage 3 passes (structural model locked and validated), summarize the locked parameters in a short context note:
```
CHECKPOINT: structural-model locked. Posts=6×6@8.33ft, pitch=4:12, miter=28.71°, bevel=9.10°, total_height=9.94ft. Proceeding to drawing stage.
```
This summary allows the drawing-stage agents to operate from a tight, clean context without re-deriving the engineering math.

## Revision Mode — Deterministic Output Gate

When the user asks to **revise, improve, update, or restyle** existing `outputs/`, this is a **deterministic package revision**, not a presentation-only update.

A revision is NOT complete unless the agent either regenerates or explicitly revalidates this artifact set:

```
outputs/drawing-plan-view.svg          outputs/blueprint-plan.svg
outputs/drawing-elevation-view.svg     outputs/blueprint-elevation.svg
outputs/drawing-isometric-view.svg     outputs/blueprint-isometric.svg
outputs/drawing-perspective-view.svg   outputs/blueprint-component-isolation.svg
outputs/shop-blueprint/SB01-cut-list.json
outputs/quality-dashboard.md           outputs/run-insights.json
context/staging/design-run-summary.md
context/staging/schema-validation-report.json
context/staging/physics-validation-report.json
context/staging/drawing-red-team-report.json
outputs/drawing-red-team-report.md
```

Markdown files, render prompts, and PNG concept images are **secondary presentation artifacts**. They are never sufficient proof that the package has been revised.

- **Aesthetic-only change:** preserve locked structural model; re-run/revalidate drawings against existing geometry.
- **Geometry change** (post count, span, pitch, height, members, bracing, cut lengths): route through the structural pipeline; regenerate `geometry-calculations.json` via `geometry_engine.py`. **Never hand-edit deterministic geometry artifacts.**

Before reporting success, always run:

```bash
python3 plugins/garden-structure-designer/scripts/schema_validator.py \
  context/staging plugins/garden-structure-designer/schemas \
  --strict --json-output context/staging/schema-validation-report.json

python3 plugins/garden-structure-designer/scripts/structural_physics_validator.py \
  context/staging/structural-model.json

python3 plugins/garden-structure-designer/scripts/render_drawings.py \
  context/staging/structural-model.json

python3 plugins/garden-structure-designer/scripts/generate_quality_dashboard.py
```

The final response MUST include: files changed · structural parameters preserved vs changed · commands run · validator results · drawing red-team result (`may_claim_success`) · remaining warnings · status: **PASS / PARTIAL / BLOCKED / DRAFT ONLY**.

**Status taxonomy:**
- `PASS` — all deterministic artifacts regenerated/revalidated, validators passed, dashboard updated.
- `PARTIAL` — presentation files updated but deterministic SVG/JSON artifacts not fully regenerated or validated.
- `BLOCKED` — a validator failed, required artifact is missing, or repair loop halted.
- `DRAFT ONLY` — user explicitly requested output despite incomplete validation; stamp every output as not for construction.

Do not claim the package is complete unless the deterministic validation artifacts exist and are current.

## Failure Handling

- A stage that fails the validation gate **blocks all downstream stages**.
- Include the `drift_report.json` path in any error message to the user.
- Never produce a final PDF that bypasses a failed validation gate without an explicit user override and a cover-page warning.

## Session Close

After Stage 7 completes (PDF compiled or gracefully degraded), update the dashboard:

```markdown
**Status:** Complete
**Last Updated:** <ISO timestamp>
```

Then emit a final summary to the user:

```
DESIGN COMPLETE: [Structure type], [footprint], [jurisdiction].
Outputs: outputs/*.pdf (or outputs/design-package.md if PDF failed)
Builder docs: outputs/lumber-purchase-list.md | outputs/budget-estimate.md | outputs/assembly-guide.md
```

If a session was killed early, `interactive-designer` handles the close — this agent does not need to act.
