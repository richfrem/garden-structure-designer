# INIT_AGENTS.md

## Overview & Agent Bootstrap
This document provides bootstrap procedures, operational workflows, and triage steps for agents running inside `garden-structure-designer`.

Canonical constraints, CAD invariants, and non-negotiables live in [`AGENTS.md`](AGENTS.md). Architectural flows live in [`docs/architecture.md`](docs/architecture.md).

## Installation & Commands
```bash
# Initialize CADCraft submodule & compile headless CLI
git submodule update --init --recursive
python3 scripts/build_cadcraft.py

# Antigravity / CLI environments via uvx
uvx --from git+https://github.com/richfrem/agent-plugins-skills plugin-add plugins/ 
uvx --from git+https://github.com/richfrem/agent-plugins-skills plugin-add richfrem/garden-structure-designers

# Claude Code marketplace
/plugin marketplace add richfrem/garden-structure-designer
/plugin install garden-structure-designer
```

## Stop-and-Diagnose Protocol

When a pipeline run produces contradictory, stale, missing, or poor outputs, STOP immediately and diagnose:

### 1. Mandatory Triggers
- Red-team report says `FAIL`, `BLOCKED`, or `may_claim_success: false`.
- Quality dashboard says `COMPLETED` while red-team/content reports say `FAIL`.
- Generated SVGs are visually placeholder-quality or blank.
- Required staging artifacts are missing or path-split.
- Validation succeeds but visible output is unusable.

### 2. Triage Inspection
```bash
pwd
find context plugins/garden-structure-designer/context -maxdepth 4 -type f -name "*.json" | sort
ls -la outputs/
ls -la context/staging/ 2>/dev/null || true

cat context/staging/structural-model.json 2>/dev/null || true
cat context/staging/geometry-calculations.json 2>/dev/null || true
cat context/staging/drawing-red-team-report.json 2>/dev/null || true
cat outputs/quality-dashboard.md 2>/dev/null || true
```

### 3. Obstacle Classification & Resolution
Classify the failure into one category:
`PATH_SPLIT`, `STALE_REPORT`, `RENDERER_PLACEHOLDER_OUTPUT`, `VALIDATOR_TOO_WEAK`, `VALIDATOR_TOO_STRICT`, `MISSING_STAGING_ARTIFACT`, `SOURCE_HASH_MISMATCH`, `DASHBOARD_STALE_OR_WRONG_PATH`, `PRODUCER_SELF_CERTIFICATION`, `SKILL_CONTRACT_INSUFFICIENT`, `RENDERER_IMPLEMENTATION_REQUIRED`, or `HUMAN_REVIEW_REQUIRED`.

- Fix paths/stale dashboards before rewriting generators.
- Never weaken a validator that is correctly catching errors.
- Never claim success if `may_claim_success: false`.
