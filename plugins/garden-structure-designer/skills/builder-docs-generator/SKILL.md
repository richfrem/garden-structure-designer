---
name: builder-docs-generator
description: Produces the three builder-facing documents that make the plugin output immediately usable for site procurement and construction: budget-estimate.md, lumber-purchase-list.md, and assembly-guide.md. Invoke as Step 13 of design-orchestrator after blueprints are validated.
allowed-tools: Read, Write
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - context/staging/cut-list.json
    validators:
      - plugins/garden-structure-designer/scripts/schema_validator.py
    repair_axes:
      - schema_error
---

## Builder Document Consistency Rule

Builder documents describe the deterministic model. They must not become independent design sources.

When revising any of `outputs/pergola_plan.md`, `outputs/assembly-guide.md`, `outputs/lumber-purchase-list.md`, or `outputs/budget-estimate.md`, cross-check all wording against:
```
context/staging/structure.json
outputs/shop-blueprint/SB01-cut-list.json
```

**Dimension language must specify what the dimension means:** post cut length, beam soffit height, total height, point-to-point diameter, flat-to-flat width, side length, or radius/circumradius. For a regular hexagon, do not conflate radius, point-to-point diameter, flat-to-flat width, and side length — they are different values.

If a dimension is uncertain, write `Dimension pending deterministic verification.` rather than inventing a value from an image.


- `context/staging/structure.json` (members, geometry sections)
- `outputs/shop-blueprint/SB01-cut-list.json` (for board-foot totals)

## Outputs

### 1. `outputs/lumber-purchase-list.md`
Organize by member type with:
- Nominal dimension, quantity, standard order length (not cut length — add waste).
- Hardware schedule (post bases, lags, ties, concrete).
- BF subtotals from `structure.json` (members section).
- Consolidation notes for minimum delivery orders.

### 2. `outputs/budget-estimate.md`
Regional market rates (default: Vancouver Island, BC). Include:
- Lumber cost by member type ($ per BF at current market).
- Hardware subtotal.
- Roofing subtotal.
- Foundation subtotal.
- **Labor exclusion note** with estimated range.
- Tax exclusion note.
- Recommended suppliers for the jurisdiction.

### 3. `outputs/assembly-guide.md`
Phase-by-phase site construction sequence:
- **Phase 1:** Site layout & footing (hexagon string layout, caisson excavation, concrete pour, J-bolt wet-set).
- **Phase 2:** Post & beam ring (standoff bases, erect/plumb/brace posts, fly ring beams).
- **Phase 3:** Hub & rafter assembly (tripod-first hoisting strategy recommended for hexagonal hubs).
- **Phase 4:** Roof decking & shingles.
- QC checkpoint per phase (plumb, pitch, clearance verification steps).

Use the compound cut values from `structure.json` (geometry section) in any assembly note that references saw settings.

## MANDATORY CONSTRAINT — HEXAGONAL HUB ASSEMBLY
For any structure with `planShape = hexagon` and a central hub:

The assembly guide MUST include a section titled exactly:
"Phase 4.3 — Tripod-First Hub and Rafter Hoisting"

The required sequence is:
1. Install three alternating rafters into the hub on the ground.
2. Hoist this tripod assembly onto three alternating beam seats.
3. Temporarily brace the tripod to the beam ring.
4. Install the remaining three rafters one at a time.
5. Confirm hub is centred over the layout stake.
6. Peg only after all six rafters are seated and verified.

This MUST be presented as the PRIMARY method.
Scaffolding and ground pre-assembly may be mentioned as ALTERNATIVES ONLY.

## Gotchas

- **Order length ≠ cut length.** Add a minimum 1ft per piece as waste allowance; add more when multiple cuts come from a single board (e.g. rafters require one cut per piece at the bird's-mouth). Using cut length as order length results in a shortage on-site.
- **Regional pricing defaults to Vancouver Island, BC.** If `structure.json` jurisdiction indicates a different region, override the regional pricing header and note the mismatch explicitly. Never silently apply Vancouver Island rates to an Ontario or Alberta build.
- **SB01-cut-list.json must exist before this skill runs.** Board-foot totals for the budget estimate come from this file. If it is missing, halt and return an error directing the orchestrator to re-run shop-blueprint-generator.
- **Assembly-guide saw settings must reference structure.json values.** Any assembly step that mentions saw settings (miter, bevel) must quote the values verbatim from `structure.json` (geometry section) — not from memory, not approximated.
- **Labor and tax exclusions are mandatory disclosures.** Both must appear as explicit line items in budget-estimate.md. Omitting either makes the estimate appear lower than reality and misleads the client.

## Smoke Test

1. **Prerequisite check:** Given a run with no `outputs/shop-blueprint/SB01-cut-list.json`: skill halts immediately with a diagnostic message rather than producing an incomplete estimate. ✓
2. **Order-length inflation:** Given a hex-6 with rafter cut length = 7.5ft: lumber-purchase-list specifies order length ≥ 9ft (standard stock) per piece, not 7.5ft. ✓
3. **Assembly-guide angle accuracy:** Assembly-guide.md saw settings section reads miter and bevel from `structure.json` (geometry section), matching the blueprint values exactly. ✓

## Completion: HANDOFF_BLOCK

On successful completion emit this block so the design-orchestrator can gate Stage 7 (compilation):

```json
{
  "stage": "builder-docs-generator",
  "status": "COMPLETE",
  "outputs": [
    "outputs/lumber-purchase-list.md",
    "outputs/budget-estimate.md",
    "outputs/assembly-guide.md"
  ],
  "regional_pricing": "<jurisdiction from structure.json>",
  "next_stage": "document-compiler"
}
```

If SB01-cut-list.json was missing or any output file was not written, set `"status": "FAIL"` and specify the blocking reason.
