# CLAUDE.md

> AI-native plugin for garden structure design packages.

## Purpose
This is an **AI-native plugin** called `garden-structure-designer` — a multi-agent design pipeline that converts non-technical user descriptions of garden structures (pergolas, gazebos, pavilions) into professional-grade structural construction PDF packages. It is installed into agentic environments (Claude Cowork, Antigravity, Gemini CLI) via the plugin marketplace system.

---

## Key Commands
```bash
# Install via uvx (Antigravity / CLI environments)
uvx --from git+https://github.com/richfrem/garden-structure-designer plugin-add richfrem/garden-structure-designer

# Install via Claude Code marketplace
/plugin marketplace add richfrem/garden-structure-designer
/plugin install garden-structure-designer
```

---

## Architecture

### Agent Pipeline Data Flow (v1.3 Deterministic)
The pipeline uses `context/staging/` as the shared data bus. All inputs/outputs must conform to rigorous JSON Schemas.

1. **`interactive-designer`** → user interview → calls `intake-normalizer`
2. **`intake-normalizer`** → writes `design-spec.json`
3. **`design-orchestrator`** → runs sequentially through fail-closed stages:
   - **Stage 0 (Self-Healing)**: Reads `learning-registry.json` to inject lessons into prompts via `load_applicable_lessons.py`.
   - **Stage 1 (Code & Constraints)**: `building-code-validator` maps region to wind/snow constraints.
   - **Stage 2 (Deterministic Engineering)**: `structural-engine` runs `geometry_engine.py` to compute explicit dimensions, spans, and pitches.
   - **Stage 3 (Connections)**: `joinery-designer` & `bracing-system-designer` create the load-path connections.
   - **Stage 4 (Drawing & Blueprint Generation)**: `drawing-generator` & `shop-blueprint-generator` produce all 8 SVG sheets. `cut_list_engine.py` writes `SB01-cut-list.json`.
   - **Stage 5 (Blueprint QA Gate)**: `validation-agent` checks XML, geometry, dimensions, and schema/physics artifacts.
   - **Stage 5.5 (Cross-Artifact Reconciliation)**: `cross_artifact_validator.py` ensures blueprint vs. model consistency.
   - **Stage 5.75 (Drawing Red-Team Gate)**: `run_drawing_red_team.py` independently validates all SVGs for builder-usefulness. **MANDATORY before PASS.** `may_claim_success: false` blocks the package.
   - **Stage 6 (Builder Documents)**: `builder-docs-generator` produces cut lists, assembly guide, and estimates.
   - **Stage 7 (Package Consistency)**: `package_consistency_validator.py` and `assembly_guide_validator.py` enforce final parity.
   - **Stage 8 (Repair)**: Repeated failures scaffold PyTest regressions via `failure_to_test.py`.

> **Note:** The stage list above is a high-level summary. `design-orchestrator.md` is the authoritative source of stage definitions and gate logic.

---

## 🛡️ v1.3 Architectural Upgrades

### The Deterministic Kernel
We have replaced LLM-guessed geometry with strictly deterministic Python engines:
- `geometry_engine.py`: Calculates exact roof pitches, miter cuts, span physics. The AI provides inputs, but never guesses the math.
- `cut_list_engine.py`: Computes exact board foot quantities and waste factors.
- `render_drawings.py`: Deterministically draws SVG files based strictly on `geometry-calculations.json`.
- `structural_physics_validator.py`: Provides empirical formulas for safety verification.

### Validation Layers
| Layer | Script | Purpose | Stage |
|-------|--------|---------|-------|
| **Schema Validation** | `schema_validator.py` | Enforces strict JSON contracts (required fields, types) | 4 |
| **Physics Validation** | `structural_physics_validator.py` | Validates L/d slenderness, L/240 beam deflection, caisson bearing | 4 |
| **Geometry Integrity**| `svg_validator.py` | Validates SVG output matches `geometry-calculations.json` exactly | 6.5 |
| **Drawing Content**   | `drawing_content_validator.py` | Adversarially validates SVG builder-usefulness: dimensions, IDs, title blocks, component panels | 5.75 |
| **Drawing Red-Team**  | `run_drawing_red_team.py` | Executable launcher: runs both validators, writes `drawing-red-team-report.json`, sets `may_claim_success` | 5.75 |
| **Consistency** | `cross_artifact_validator.py` | Ensures values like total BF or beam miters match across docs | 5 |
| **Package Consistency**| `package_consistency_validator.py` | Enforces output generation, date parity, and title block parity | 7 |
| **Assembly Guide** | `assembly_guide_validator.py` | Enforces tripod-first assembly sequences | 7 |

### Integrity Chain
- `source_hash` flows through all derived artifacts: `structural-model.json` → `geometry-calculations.json` → `SVG/MD` outputs.
- A composite dependency manifest ensures that any change correctly bubbles up through the graph via `manifest_utils.py`.

### State Management & Locking
- **Immutability rules**: The `structural-model.json` is locked after Stage 2. No subsequent skill may mutate it.
- **Bracing-model separation**: Bracing parameters have been extracted to their own model to prevent contaminating the core structure.

### Self-Healing & Learning
- **Learning Registry**: Found in `context/staging/learning-registry.json`. Failed runs result in permanent lessons classified by risk.
- **Failure→Improvement Loop**: Validators surface drift, Stage 8 captures the feedback, and Stage 0 actively injects applicable lessons into the next run.
- **Regression Scaffold**: `failure_to_test.py` takes novel drift reports and scaffolds pytest regressions automatically.

### Reference Values
- Always utilize standardized building code defaults unless directed otherwise.
- For a Hexagonal layout at a 4:12 pitch, the verified beam ring miter is exactly `30.0°`. Use this regression anchor to verify assumptions.

---

## Behavior & Judgment (Karpathy Principles)

### 1. Think Before Acting
Always clarify the user's location/jurisdiction before beginning structural computations, as wind/snow loads are non-negotiable inputs. Verify the safety implications of design requests before execution.

### 2. Simplicity First
Follow loose coupling strictly. Each skill or agent should strictly read from `context/staging/` and write its outputs there. Do not create complex direct agent-to-agent interactions; rely on the orchestrator.

### 3. Surgical Changes
When updating an existing skill, agent, or document, only modify the specific section required. Structural physics calculations must override user style preferences without altering unrelated design parameters.

### 4. Goal-Driven Execution
The ultimate goal is generating a professional-grade structural construction PDF packet. Ensure that all validations (e.g., `validation-agent` red-team physics check) pass completely before proceeding to the document compilation stage.

### 5. Self-Evolution & Error Recovery
When a tool, script, or verification step fails, treat it as an evolution event as defined in `.agent/rules/self-evolution-policy.md`. Keep edits within boundaries, classify the failure tier (Gap, Failure, Regression), limit fixes to a maximum of 3 attempts, and record every patch in `evolution-log.md`.

### 6. Test-Driven Development (TDD)
Enforce the strict iron law from `.agent/rules/test-driven-development.md`: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST. Never write implementation code before a failing unit or integration test exists. Place tests in `plugins/<plugin>/tests/` and run the suite before committing.

### 7. Data-Driven & Declarative Architecture
Enforce the strict engineering policy from `.agent/rules/data-driven-declarative.md`: all CAD engine dimensions, framing member counts, offsets, and fabrication cut lists must dynamically resolve from staging `structure.json`. Hardcoding geometry layouts and constants in python scripts is strictly prohibited.

---

## Updated Coding Rules
- **Safety over aesthetics**: Structural physics calculations always override user style preferences.
- **Semantic SVGs**: Use `data-role` tags on all drawn elements rather than relying solely on stroke colors for topology.
- **Precision**: Enforce exactly two-decimal angles (`30.00°`) in all artifacts.
- **Provenance Blocks**: Maintain `<!-- SAW_SETTINGS -->` comment blocks in SVGs for machine verification.
- **Test-cut warnings**: Always append physical "test-cut" warnings on compound cuts for carpenters.
- **Jurisdiction-aware**: Always capture user location (e.g., BC Building Code) before any structural computation.
- **Platform agnostic**: No external framework dependencies; must work across Claude Cowork, Antigravity, Gemini CLI, Copilot CLI.

---

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

---

## Independent Adversarial Drawing Review
Agents may not claim their own drawing outputs are successful.

Every drawing-generation run must be reviewed by the independent `drawing-red-team-agent` (or the `adversarial-drawing-reviewer` skill) before success can be claimed.

The reviewer must be skeptical and must reject:
- placeholder drawings;
- mostly blank SVGs;
- tiny top-left sketches;
- rows of rectangles;
- missing dimensions;
- missing title blocks;
- missing component details;
- drawings that would not be useful to a builder.

If the adversarial report (`context/staging/drawing-red-team-report.json`) does not explicitly set `may_claim_success: true`, the final package status must not be `PASS`.

---

## Skill/Component Standards
- **Agents** live in `plugins/<plugin-name>/agents/<name>/AGENT.md` with YAML frontmatter (`name`, `description`, `allowed-tools`).
- **Skills** live in `plugins/<plugin-name>/skills/<name>/SKILL.md` with the same frontmatter pattern.
- Skills use `create-skill`, `create-sub-agent`, and `create-plugin` meta-skills for consistent authoring.

---

## Deterministic Package Completion Standard (v1.3.1)

A garden-structure-designer task is **not complete** merely because Markdown files, render prompts, or photorealistic images were updated.

The authoritative construction package consists of validated deterministic artifacts:
```
context/staging/design-spec.json          context/staging/structural-model.json
context/staging/geometry-calculations.json
outputs/*.svg                              outputs/shop-blueprint/SB01-cut-list.json
outputs/quality-dashboard.md              outputs/run-insights.json
```

All geometry, dimensions, angles, cut lengths, and validation claims must trace back to JSON/SVG artifacts generated or validated by scripts. Photorealistic images are presentation references only.

Before claiming success, agents must report:
- deterministic artifacts regenerated or revalidated;
- validators run and their exit results;
- remaining warnings;
- status: **PASS**, **PARTIAL**, **BLOCKED**, or **DRAFT ONLY**.