---
name: building-code-validator
description: Validates user location input against localized building code standards (e.g., BC Building Code) to determine required load capacities for snow and wind constraints.
allowed-tools: Read, Write
---

## Expected Inputs
`context/staging/design-spec.json` containing the user's location string.

## Core Operations
1. Load localized logic (e.g. BC Building Code tables for coastal vs interior snow loads).
2. Look up baseline assumptions required for safe structural span sizes.
3. Output the required psf limits to `context/staging/building-code.json` so the structural-engine can read it.
