---
name: structural-engine
description: Generates the structural system based on limits. Computes post placement, beam spans, and rafter geometry. Enforces real-world build constraints by validating spans against safe load paths.
allowed-tools: Read, Write
---

## Expected Inputs
`context/staging/design-spec.json` (output from intake-normalizer) and `context/staging/building-code.json` (output from building-code-validator).

## Behavior
Calculate the minimum safe timber dimensions for:
1. Corner and intermediate posts based on roof area.
2. Beams based on post span span.
3. Rafters based on depth of the structure and specified spacing.

Write exact coordinates and cut-sizes for framing objects into `context/staging/structural-model.json`.
