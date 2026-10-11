---
name: intake-normalizer
description: Converts conversational input and images from the user into structured parameters. Handles missing or ambiguous data by defining defaults or returning flags for required clarification. Outputs validated design spec JSON to be ingested by the orchestrator.
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
- Strictly follow deterministic execution contracts for intake-normalizer.
- Input parameters must resolve from staging structure.json.

## Quick start


## Workflow
1. **Input Phase**: Load parameters for intake-normalizer.
2. **Execution Phase**: Process and emit deterministic output.
3. **Gate Phase**: Validate schema and physics integrity.

## Verification


## References
- [Acceptance Criteria](references/acceptance-criteria.md)
