# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

This is an **AI-native plugin** called `garden-structure-designer` — a multi-agent design pipeline that converts non-technical user descriptions of garden structures (pergolas, gazebos, pavilions) into professional-grade structural construction PDF packages. It is installed into agentic environments (Claude Cowork, Antigravity, Gemini CLI) via the plugin marketplace system.

## Installation

```bash
# Install via uvx (Antigravity / CLI environments)
uvx --from git+https://github.com/richfrem/garden-structure-designer plugin-add richfrem/garden-structure-designer

# Install via Claude Code marketplace
/plugin marketplace add richfrem/garden-structure-designer
/plugin install garden-structure-designer
```

## Repository Layout

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

## Agent Pipeline Data Flow

The pipeline uses `context/staging/` as the shared data bus between skills:

1. `interactive-designer` → user interview → calls `intake-normalizer`
2. `intake-normalizer` → writes `context/staging/design-spec.json`
3. `design-orchestrator` → reads `design-spec.json`, runs sequentially:
   - `building-code-validator` → writes `context/staging/building-code.json`
   - `structural-engine` → reads both JSONs → writes `context/staging/structural-model.json`
   - `joinery-designer` → reads structural model → writes joinery map
   - `bracing-system-designer` → writes bracing spec
   - `validation-agent` → red-team check on physics before output
   - `drawing-generator` → produces SVG/PNG views
   - `document-compiler` → assembles final PDF packet

## Plugin/Skill File Conventions

- **Agents** live in `plugins/<plugin-name>/agents/<name>/AGENT.md` with YAML frontmatter (`name`, `description`, `allowed-tools`)
- **Skills** live in `plugins/<plugin-name>/skills/<name>/SKILL.md` with the same frontmatter pattern
- Skills use `create-skill`, `create-sub-agent`, and `create-plugin` meta-skills for consistent authoring

## Core Design Constraints

- **Safety over aesthetics**: Structural physics calculations always override user style preferences
- **Jurisdiction-aware**: Always capture user location (e.g., BC Building Code) before any structural computation; wind/snow loads are non-negotiable inputs
- **Loose coupling**: Each skill/agent reads its inputs from `context/staging/` and writes its outputs there — no direct agent-to-agent calls except through the orchestrator
- **Platform agnostic**: No external framework dependencies; must work across Claude Cowork, Antigravity, Gemini CLI, Copilot CLI