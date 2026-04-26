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

## Gotchas

- **Snow load is city-level, not province-level.** BC coastal (Richmond) = 24 psf; BC interior (Kelowna) = 48+ psf. Using the provincial average produces a structurally under-designed system. Always look up the specific municipality.
- **Permit threshold is NOT in scope.** This skill outputs design loads only. Whether the project requires a building permit (e.g. > 10 m² in BC triggers permit) is a separate determination — do not include permit guidance in building-code.json or this skill will be conflated with legal advice.
- **Unknown jurisdiction must be flagged, not silently defaulted.** If jurisdiction cannot be resolved, output `"jurisdiction_resolved": false` and a `"jurisdiction_warning"` field. Never silently fall back to a generic load without indicating the assumption.
- **Wind loads compound with snow loads.** High-wind coastal zones may have lower snow but higher uplift requirements. Ensure both snow and wind load fields are populated in building-code.json.

## Smoke Test

1. **Interior BC lookup:** Given `design-spec.json` with `jurisdiction=BC-Interior` (Kelowna): outputs `building-code.json` with `snow_load_psf ≥ 40`, `jurisdiction_resolved: true`. ✓
2. **Coastal BC lookup:** Given `jurisdiction=BC-Coastal` (Richmond): outputs `snow_load_psf ≤ 25`. ✓
3. **Unknown jurisdiction:** Given `jurisdiction=Unknown`: outputs `building-code.json` with `jurisdiction_resolved: false` and a non-empty `jurisdiction_warning`. ✓
