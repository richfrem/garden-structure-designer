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
```
plugins/garden-structure-designer/   # The actual plugin content
  agents/
    interactive-designer/            # Entry point: interviews user, triggers intake-normalizer
    design-orchestrator/             # Pipeline controller: runs the full skill chain
    validation-agent/                # Red-team reviewer of physics before compilation
  skills/
    intake-normalizer/               # Converts conversation → design-spec.json
    building-code-validator/         # Maps jurisdiction → load constraints JSON
    structural-engine/               # Computes post/beam/rafter dimensions
    joinery-designer/                # Assigns connection types (mortise-tenon vs. fasteners)
    bracing-system-designer/         # Anti-racking knee brace geometry
    drawing-generator/               # Orthographic SVG/PNG plan & elevation views
    document-compiler/               # Assembles final PDF construction packet
  .claude-plugin/plugin.json         # Plugin manifest

.claude-plugin/marketplace.json      # Marketplace index (points to plugin + agentic-os-core)
exploration/                         # Discovery artifacts (plans, captures, dashboard)
context/                             # Runtime: events.jsonl + memory/
skills-lock.json                     # Installed skills manifest
```

### Agent Pipeline Data Flow (v1.2 Deterministic)
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

## Coding Rules
- **Safety over aesthetics**: Structural physics calculations always override user style preferences.
- **Jurisdiction-aware**: Always capture user location (e.g., BC Building Code) before any structural computation.
- **Loose coupling**: Each skill/agent reads its inputs from `context/staging/` and writes its outputs there — no direct agent-to-agent calls except through the orchestrator.
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
