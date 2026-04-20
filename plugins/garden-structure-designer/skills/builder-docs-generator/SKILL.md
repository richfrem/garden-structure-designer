---
name: builder-docs-generator
description: Produces the three builder-facing documents that make the plugin output immediately usable for site procurement and construction: budget-estimate.md, lumber-purchase-list.md, and assembly-guide.md. Invoke as Step 13 of design-orchestrator after blueprints are validated.
allowed-tools: Read, Write
---

## Expected Inputs
- `context/staging/structural-model.json`
- `context/staging/geometry-calculations.json`
- `context/staging/design-spec.json`
- `output/shop-blueprint/SB01-cut-list.json` (for board-foot totals)

## Outputs

### 1. `outputs/lumber-purchase-list.md`
Organize by member type with:
- Nominal dimension, quantity, standard order length (not cut length — add waste).
- Hardware schedule (post bases, lags, ties, concrete).
- BF subtotals from `structural-model.json`.
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

Use the compound cut values from `geometry-calculations.json` in any assembly note that references saw settings.
