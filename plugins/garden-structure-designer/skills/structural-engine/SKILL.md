---
name: structural-engine
description: Generates the structural system based on limits. Computes post placement, beam spans, and rafter geometry. Enforces real-world build constraints by validating spans against safe load paths. Writes geometry section inside structure.json via geometry_engine.py — NEVER derives math mentally.
allowed-tools: Read, Write, Bash
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - context/staging/structure.json  # enriched with members, roof, hub, footings, code, invariants, geometry sections
    validators:
      - plugins/garden-structure-designer/scripts/schema_validator.py
    repair_axes:
      - geometry_warning
      - source_hash_mismatch
---

## Expected Inputs
`context/staging/structure.json` (output from intake-normalizer)
`context/staging/building-code.json` (output from building-code-validator)

## Behavior

1. Calculate minimum safe timber dimensions for:
   - Corner and intermediate posts based on roof area and jurisdiction snow/wind loads.
   - Beams based on post-to-post span, tributary width, and species/grade.
   - Rafters based on roof span, pitch, and specified spacing.
2. Write structural parameters into `context/staging/structure.json` (members, roof, hub, footings sections).
3. **MANDATORY — Run the Geometry Engine:**
   ```bash
   python3 scripts/geometry_engine.py \
       context/staging/structure.json
   ```
   This enriches `context/staging/structure.json` with the geometry section. All compound cut angles, SVG pixel coordinates, rafter lengths, and total height values MUST be read from this file. **You are forbidden from computing these values internally.**

4. Verify the `structure.json` geometry section contains no warnings array entries. If `warnings` is non-empty, re-adjust post cut length or pitch to resolve the height constraint violation before proceeding.

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

## Output Schema (`structure.json` — members section)

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

## Gotchas

- **Pitch angle ≠ miter angle.** For a hexagonal hip rafter at 4:12 pitch, the pitch angle is 18.43° but the compound miter is 28.71°. Using the pitch angle directly produces cuts that won't close at the hub. The geometry engine prevents this — never bypass it.
- **Post cut length ≠ finished post height.** The geometry engine computes `cutLength_ft` accounting for the post base standoff. If you substitute the desired above-grade height directly, every post will stand too tall.
- **`warnings` array is a hard stop.** A non-empty `warnings` array from geometry_engine.py means a height or geometry constraint is violated. Do not forward `structure.json` with warnings to drawing-generator under any circumstances.
- **Locking is one-way without a reset.** Once `_locked: true` is written, any upstream skill (bracing-system-designer updating coordinates, for example) must explicitly reset the lock before writing and re-run the geometry engine before re-locking.
- **Geometry engine must be invoked as a subprocess.** The structural engine is explicitly forbidden from computing compound angles, rafter lengths, or SVG coordinates internally — even as a cross-check. All math must flow through `geometry_engine.py`.

## Smoke Test

1. **Standard hexagon:** Given hex-6, 4:12 pitch, 14ft outer span with no height constraint: `structure.json` geometry section exists, `warnings = []`, `miter_deg ≈ 28.71`, `bevel_deg ≈ 9.10`, `structure.json._locked = true`. ✓
2. **Height violation detection:** Given an 8ft post with a strict 10ft total height limit that the roof rise would breach: geometry engine populates `warnings` with a height constraint message, structural engine halts and does not lock the model. ✓
3. **Lock integrity:** Re-invoking structural engine on an already-locked model without a prior lock reset: skill halts and reports the locked state rather than overwriting. ✓

## Completion: HANDOFF_BLOCK

On successful completion emit this block so the design-orchestrator can gate Stage 2:

```json
{
  "stage": "structural-engine",
  "status": "COMPLETE",
  "outputs": [
    "context/staging/structure.json"
  ],
  "locked": true,
  "warnings_count": 0,
  "next_stage": "joinery-designer"
}
```

If any warning or lock failure occurred, set `"status": "FAIL"` and populate `"failure_reason"` before returning to the orchestrator.
