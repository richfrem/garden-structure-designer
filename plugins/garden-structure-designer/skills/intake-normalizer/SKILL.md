---
name: intake-normalizer
description: Converts conversational input and images from the user into structured parameters. Missing or ambiguous data is never defaulted: it is returned as flags that require clarification. Outputs validated design spec JSON to be ingested by the orchestrator.
allowed-tools: Read, Write
---

# Intake Normalizer

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- **Stage 0 / 0.5.** Turns the conversation into `context/staging/structure.json` intent; it never invents structural values.
- A missing or ambiguous dimension, count, hub type or jurisdiction is returned as a clarification flag. Silent structural defaults are prohibited (AGENTS.md).
- Jurisdiction and load inputs (`intent.jurisdiction`) must be confirmed before any structural computation.
- Initial production release supports only `meta.topology_family = RadialHubTopology` (regular N-gon, N >= 5). Grid and hip/ridge families are reserved and fail closed with `TOPOLOGY_NOT_IMPLEMENTED`.
- All canonical writes go through `structure_io.py` (transactional); never write `structure.json` ad hoc.

## Quick start
```bash
python3 scripts/validate_intent.py [structure.json]
python3 scripts/validate_topology_intent.py [structure.json]
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: user description and images -> normalized intent fields (`structure.sides`, `layout.post_count`, `roof.primary_rafters.count`, `hub.type`, members, footings, `intent.jurisdiction`).
2. **Gate (Stage 0)**: `validate_intent.py` must pass: every field geometry_engine, the physics screen and the drawings read is present, numeric and plausible.
3. **Gate (Stage 0.5)**: `validate_topology_intent.py` checks family, `sides >= 5`, `post_count == sides`, rafter count `== sides`, and `hub.type` vs sides (hexagonal_prism = 6, octagonal_prism = 8, polygonal_cylinder >= 5).
4. Stop and report the error code (`GEOMETRY_INVALID`, `TOPOLOGY_CARDINALITY_MISMATCH`, `HUB_TYPE_MISMATCH`, `UNKNOWN_TOPOLOGY_FAMILY`, `TOPOLOGY_NOT_IMPLEMENTED`); do not continue to geometry.

## Verification
- `pytest tests/test_validate_intent.py tests/test_validate_intent_contract.py tests/test_topology_invariants.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
