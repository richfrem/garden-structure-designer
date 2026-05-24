---
name: intake-normalizer
description: Converts conversational input and images from the user into structured parameters. Handles missing or ambiguous data by defining defaults or returning flags for required clarification. Outputs validated design spec JSON to be ingested by the orchestrator.
allowed-tools: Read, Write
---

## Expected Inputs
Raw conversational transcript from the `interactive-designer` agent, and optionally paths to inspiration images.

## Core Responsibilities
1. Parse the conversation transcript for exact structural intent (dimensions, structure type, site jurisdiction).
2. For missing parameters, inject safe structural defaults or mark them as `NEEDS_CLARIFICATION`.
3. Read the explicitly gathered building code jurisdiction (e.g., "British Columbia") and map it to a canonical location ID for the `building-code-validator`.
4. Output `context/staging/structure.json` with sections: meta, intent, structure, layout, presentation, cad. Set `meta.lifecycle = "INTENT"`.

## Gotchas

- **City ≠ jurisdiction.** "Vancouver" could be Vancouver BC (Canadian codes) or Vancouver WA (US IBC). Always include province/state alongside city, or flag for clarification. Never resolve jurisdictions from city name alone.
- **Ambiguous footprints default to square.** "About 12x12" with no shape specified implies a 4-post square structure, not hexagonal. Output the assumed shape explicitly in design-spec.json; do not silently assume.
- **Missing pitch defaults to 4:12** — log this default in the JSON as `"pitch": "4:12", "pitchDefaulted": true` so downstream agents can see the assumption.
- **NEEDS_CLARIFICATION blocks the pipeline.** Any field marked `NEEDS_CLARIFICATION` will cause the structural engine to halt. Do not forward design-spec.json with unresolved clarifications unless the orchestrator has explicitly approved safe defaults.
- **Dimension vs. clear span.** Users often give overall footprint (including post thickness). Structural span is the center-to-center post distance. Clarify which measurement the user intends when in doubt.

## Smoke Test

1. **Complete happy path:** Given transcript "12-foot hexagonal gazebo in Kelowna, BC, 4:12 roof pitch": outputs `structure.json` with `shape=hexagon`, `span_ft=12`, `jurisdiction=BC-Interior`, `pitch=4:12`, zero `NEEDS_CLARIFICATION` fields. ✓
2. **Missing data handling:** Given transcript "I want a pergola, not sure about the size yet": outputs `structure.json` with `NEEDS_CLARIFICATION` on `span_ft`, pipeline does not advance. ✓
3. **Cross-border jurisdiction:** Given "Vancouver" with no province/state: outputs `NEEDS_CLARIFICATION` on jurisdiction rather than assuming BC. ✓
