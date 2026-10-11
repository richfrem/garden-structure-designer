# AGENTS.md

## Overview
`garden-structure-designer` is an AI-native multi-agent design pipeline that converts colloquial user descriptions of garden structures (pergolas, gazebos, pavilions) into professional-grade structural construction PDF packages. Staging bus is `context/staging/structure.json`.

Detailed architecture and stage definitions live in [`architecture.md`](architecture.md). Operational workflows and triage live in [`INIT_AGENTS.md`](INIT_AGENTS.md).

## On-Demand Skills (Enable / Disable)
Skills, agents, rules and hooks are loaded on demand. Desired state lives in `.agents/ownership/<plugin>.json` (`should_install: true/false`). Run `python3 .agents/skills/plugin-syncer/scripts/sync_with_inventory.py` to synchronize changes. Never toggle components without explicit user authorization.

## Behavioral Guidelines (Karpathy Principles)
1. **Think Before Acting**: MUST clarify location/jurisdiction (wind/snow loads) before structural computations.
2. **Simplicity First**: MUST preserve loose coupling; agents communicate strictly via `context/staging/structure.json`.
3. **Surgical Changes**: MUST touch only target sections. Structural physics always overrides aesthetics.
4. **Goal-Driven Execution**: MUST pass all validation gates before compiling construction PDF packages.

## CAD & Deterministic Invariants (HARD RULES)
1. **Stable Member IDs**: ALL members MUST carry stable IDs (`P1`, `B1`, `R1`, `HUB`, `FT1`, `Brace1a`).
2. **Cross-Layer Traceability**: IDs MUST match across `structure.json`, geometry models, SVG `data-tag`, and QA reports.
3. **Semantic SVGs**: ALL SVG elements MUST embed `data-role` and `data-tag` attributes; anonymous geometry is PROHIBITED.
4. **Visual Labels**: ALL major members MUST render a visible label near their midpoint in every drawing sheet.
5. **Dynamic Derivation**: MUST dynamically derive member counts and geometry from `structure.json`; hardcoding shapes or post counts is PROHIBITED.
6. **Stop-and-Diagnose**: MUST halt and diagnose root cause when reports conflict or outputs fail before touching code.
7. **Adversarial Drawing Gate**: Drawing success MUST NOT be self-certified; `drawing-red-team-agent` approval required (`may_claim_success: true`).
8. **Package Completion**: Construction package MUST include valid `structure.json`, SVGs, cut-lists, and compiled PDF.

## Non-Negotiable Rules
Detailed policy documents live in [`.agent/rules/`](.agent/rules/). Key invariants:

1. **Test-Driven Development**: MUST have a failing test before writing production code. (details: [`.agent/rules/test-driven-development.md`](.agent/rules/test-driven-development.md))
2. **Data-Driven & Declarative**: MUST derive all dimensions from `structure.json`; hardcoded geometry or silent defaults PROHIBITED. (details: [`.agent/rules/data-driven-declarative.md`](.agent/rules/data-driven-declarative.md))
3. **Coding Conventions**: MUST follow naming standards and file headers. (details: [`.agent/rules/coding-conventions.md`](.agent/rules/coding-conventions.md))
4. **Dependency Management**: MUST use `pip-compile`; manual `pip install` is PROHIBITED. (details: [`.agent/rules/dependency-management.md`](.agent/rules/dependency-management.md))
5. **Plugin Architecture**: MUST use `symlink_manager.py`; raw `ln -s` is PROHIBITED. (details: [`.agent/rules/plugin-architecture-policy.md`](.agent/rules/plugin-architecture-policy.md))
6. **Self-Evolution & Map Debt**: MUST run pre-completion gate and record map debt. (details: [`.agent/rules/self-evolution-policy.md`](.agent/rules/self-evolution-policy.md))
7. **Destructive Action Guards**: File and skill deletions are strictly PROHIBITED without explicit user approval. (details: [`.agent/rules/destructive-action-guard.md`](.agent/rules/destructive-action-guard.md))
8. **Git Operations Protocol**: MUST NOT stash, force-push, or commit unrequested files. (details: [`.agent/rules/git-operations.md`](.agent/rules/git-operations.md))
9. **Worktree Isolation**: MUST create an isolated git worktree before multi-file modifications. (details: [`.agent/rules/worktree-lifecycle-management.md`](.agent/rules/worktree-lifecycle-management.md))
10. **Adversarial Reasoning**: MUST challenge assumptions before agreement. (details: [`.agent/rules/adversarial-reasoning-before-agreement-rule.md`](.agent/rules/adversarial-reasoning-before-agreement-rule.md))
11. **Cryptographic Human Gates**: MUST obtain user approval for gated actions. (details: [`.agent/rules/cryptographic-human-gates.md`](.agent/rules/cryptographic-human-gates.md))
12. **Config-Driven Constants**: MUST consolidate constants in `control_plane/constants.py`. (details: [`.agent/rules/config-driven-constants-over-hardcoding.md`](.agent/rules/config-driven-constants-over-hardcoding.md))
