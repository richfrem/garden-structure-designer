# Dispatch Strategy (model and CLI selection for independent validation)

Single place for the model names used to launch the independent validators (Stage 3 and Stage 4.5) so agent documents do not hardcode them.

Read `**Dispatch Strategy:**` from `context/design-dashboard.md` and invoke the independent validation agent accordingly:
   - `copilot-cli` → `gh copilot suggest` with claude-sonnet-4.6
   - `gemini-cli` → `gemini` with gemini-3.1-pro-preview
   - `claude-subagents` → Claude `Agent` tool with `model: "claude-sonnet-4-5"`
   - `direct` → self-review within this session (no external CLI)

If the chosen independent validator is unavailable, the run is `BLOCKED` unless the user explicitly overrides (see `agents/validation-agent.md`, which stamps overridden outputs `DRAFT - INDEPENDENT QA NOT COMPLETED - NOT FOR CONSTRUCTION`).
