---
name: structural-engine
description: Generates the structural system based on limits. Computes post placement, beam spans, and rafter geometry. Enforces real-world build constraints by validating spans against safe load paths. Writes geometry-calculations.json via geometry_engine.py — NEVER derives math mentally.
allowed-tools: Read, Write, Bash
---

## Expected Inputs
`context/staging/design-spec.json` (output from intake-normalizer)
`context/staging/building-code.json` (output from building-code-validator)

## Behavior

1. Calculate minimum safe timber dimensions for:
   - Corner and intermediate posts based on roof area and jurisdiction snow/wind loads.
   - Beams based on post-to-post span, tributary width, and species/grade.
   - Rafters based on roof span, pitch, and specified spacing.
2. Write structural parameters to `context/staging/structural-model.json`.
3. **MANDATORY — Run the Geometry Engine:**
   ```bash
   python3 scripts/geometry_engine.py \
       context/staging/structural-model.json
   ```
   This produces `context/staging/geometry-calculations.json`. All compound cut angles, SVG pixel coordinates, rafter lengths, and total height values MUST be read from this file. **You are forbidden from computing these values internally.**

4. Verify the `geometry-calculations.json` contains no warnings array entries. If `warnings` is non-empty, re-adjust post cut length or pitch to resolve the height constraint violation before proceeding.

## Compound Cut Reference (read-only — use geometry_engine.py to compute)

For a regular polygon structure with `sides` sides and roof pitch `rise:run`:

```
pitch_angle     = arctan(rise / run)
plan_half_angle = 360 / (2 × sides)          # degrees
Miter           = arctan(cos(pitch_angle) × tan(plan_half_angle))
Bevel           = arcsin(sin(pitch_angle) × sin(plan_half_angle))
```

**Verified Example — Hexagon (sides=6), 4:12 Pitch:**
- pitch_angle = 18.43°, plan_half_angle = 30°
- **Miter = 28.71°** (NOT 18.43°)
- **Bevel = 9.10°** (NOT 15.6°)

Using the raw pitch angle as the miter setting is the most common hallucination. The geometry_engine.py script prevents this entirely.

## Output Schema (`structural-model.json`)

```json
{
  "members": {
    "posts": { "quantity": 6, "dimensions": "6x6", "cutLength_ft": 8.33, "spanDistance_ft": 5.0 },
    "beams": { "quantity": 6, "dimensions": "6x8", "depth_in": 7.25 },
    "hipRafters":  { "quantity": 6, "dimensions": "4x6" }
  },
  "roofStructure": { "pitch": "4:12" },
  "overhang_in": 12,
  "_locked": false
}
```

Set `"_locked": true` once this file has passed validation. Locked files must not be modified without resetting the lock and re-running the geometry engine.
