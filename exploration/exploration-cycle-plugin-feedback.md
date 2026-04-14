# Exploration-Cycle-Plugin Feedback

**Target:** `antigravity-maintainer-agent` (or equivalent orchestrator improver)
**Subject:** Improvements required for `exploration-cycle-plugin` based on the *Garden Structure Designer* Phase 1-3 session.

## Prompt for the Maintainer Agent

> **Maintainer, please review the following feedback gathered from a live run of the `exploration-cycle-plugin` (Greenfield session) and incorporate these fixes into the master plugin definitions:**
> 
> ### 1. Outdated LLM Tooling References
> The orchestrator's `Dispatch Strategy` documentation and internal prompt lists are referencing outdated generation models (such as `gemini-2.5`). Update the documentation to reflect current frontier capabilities (i.e. `gemini-3.1-pro-preview`, `gemini-3.1-flash-lite-preview`, and Copilot `gpt-5-mini`).
> 
> ### 2. Failure to Enforce Tooling & Scaffolder Isolation
> During the **Phase 3 (Build)** cycle, the `subagent-driven-prototyping` instructions were too loose, allowing the orchestrator agent to construct the plugin using raw Bash commands (`mkdir`, raw markdown creation) instead of adopting the standardized ecosystem scaffolding tools (`agent-scaffolders`: `create-skill`, `create-plugin`, etc.). 
> **Action:** Harden the rules engine for Phase 3. Add explicit constraints: *“If building an agentic plugin, you MUST use the localized skills in `.agents/skills` (like `create-plugin` and `create-skill`) to construct your framework, enforcing EVAl harnesses and directory templates.”*
> 
> ### 3. Prototype Destination Ambiguity for Agentic Plugins
> The `exploration-cycle-plugin` assumes a typical software output directory (`exploration/prototype/`). However, building an active Agent Plugin requires building outside of that directory (e.g. `plugins/[plugin-name]`). 
> **Action:** Add a contextual check to the Phase 3 definition: *“If the session is meant to build a Claude Plugin, redirect the build path toward `plugins/` rather than the standard prototyping bucket.”*
> 
> ### 4. Hooks / Dependencies Binding
> In Phase 3, the orchestrator successfully created `AGENTS.md` and `SKILLS.md` but did not instinctively wire them into the `.claude-plugin/plugin.json` lists without direct user intervention. 
> **Action:** Ensure the `create-plugin` scaffolding workflow heavily emphasizes the final binding check in `plugin.json` for any newly generated sub-components.
