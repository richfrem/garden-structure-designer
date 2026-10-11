---
name: building-code-validator
description: Validates user location input against localized building code standards (e.g., BC Building Code) to determine required load capacities for snow and wind constraints.
allowed-tools: Read, Write
---

# Building Code Validator

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Confirms the **jurisdiction** (`intent.jurisdiction`) and the snow/wind inputs with the user before any structural computation (AGENTS.md rule 1).
- `validate_intent.py` rejects a missing or blank jurisdiction. The physics validator is a screening check only; sign-off needs a licensed engineer.
- Jurisdiction-specific design checks (snow/wind loads, member capacity) are not yet implemented (F-20); never present the screening result as a code-compliance approval.

## Quick start
```bash
python3 scripts/validate_intent.py [structure.json]
python3 scripts/structural_physics_validator.py [structure.json]
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: location text from the user.
2. **Execution**: resolve the code edition and load inputs, record them in `intent.jurisdiction` and the `code` section.
3. **Gate**: a status of `BLOCKED`, `FAIL` or `REQUIRES_ENGINEER_REVIEW` stops the pipeline and is reported verbatim.

## Verification
- `pytest tests/test_physics_validator_strict.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
