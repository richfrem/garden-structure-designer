# GEMINI.md

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
   - **Stage 2 (Deterministic Engineering)**: `structural-engine` runs `geometry_engine.py` (not an LLM guess) to compute explicit dimensions, spans, and pitches.
   - **Stage 3 (Connections)**: `joinery-designer` & `bracing-system-designer` create the load-path connections.
   - **Stage 4 (Draft Validation)**: Schema and physics validation using `schema_validator.py` and `structural_physics_validator.py`.
   - **Stage 5 (Cross-Artifact)**: `cross_artifact_validator.py` ensures blueprint vs. model consistency.
   - **Stage 6 (Generation)**: `drawing-generator` & `cut_list_engine.py` produce final outputs.
   - **Stage 7 (Red-Team)**: `validation-agent` blocks execution if `drift_report.json` flags mismatch.
   - **Stage 8 (Repair)**: Repeated failures scaffold PyTest regressions via `failure_to_test.py`.

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

## Skill/Component Standards
- **Agents** live in `plugins/<plugin-name>/agents/<name>/AGENT.md` with YAML frontmatter (`name`, `description`, `allowed-tools`).
- **Skills** live in `plugins/<plugin-name>/skills/<name>/SKILL.md` with the same frontmatter pattern.
- Skills use `create-skill`, `create-sub-agent`, and `create-plugin` meta-skills for consistent authoring.
## Gemini CLI Tool Mapping

| Claude Code | Gemini CLI equivalent |
|:------------|:----------------------|
| `Read`      | `read_file`           |
| `Write`     | `write_file`          |
| `Edit`      | `replace_in_file`     |
| `Bash`      | `run_shell_command`   |
| `Glob`      | `glob`                |
| `Grep`      | `grep`                |

Skills in `.agents/skills/` use Claude Code tool names in their SKILL.md files.
When executing skills via Gemini, translate tool references using the table above.

---

## Deterministic Package Completion Standard (v1.3.1)

A garden-structure-designer task is **not complete** merely because Markdown files, render prompts, or photorealistic images were updated.

The authoritative construction package consists of validated deterministic artifacts:
- `context/staging/design-spec.json` / `structural-model.json` / `geometry-calculations.json`
- `outputs/*.svg` and `outputs/shop-blueprint/SB01-cut-list.json`
- `outputs/quality-dashboard.md` and `outputs/run-insights.json`

All geometry, dimensions, angles, and cut lengths must trace back to JSON/SVG artifacts generated by scripts. Photorealistic images are presentation references only. Before claiming success, report: artifacts regenerated or revalidated · validators run · remaining warnings · status: PASS / PARTIAL / BLOCKED / DRAFT ONLY.
