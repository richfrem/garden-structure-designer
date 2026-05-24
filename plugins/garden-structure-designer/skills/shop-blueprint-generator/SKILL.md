---
name: shop-blueprint-generator
description: Generates heavily dimensioned, technical orthographic blueprints intended strictly for carpenters and fabricators. Outputs highly detailed line-drawings packed with dimensional arrows, bolt-hole spacing coordinates, exact cut lengths, and pitch angles. All angles are READ from geometry-calculations.json — NEVER derived mentally.
allowed-tools: Read, Write, Bash
---

## Expected Inputs
- `context/staging/structure.json` (produced by structural-engine; includes members, roof, hub, footings, geometry sections)
- `context/staging/joinery-model.json`

## Pre-Flight: Run Geometry Engine If Not Present
```bash
python3 scripts/geometry_engine.py \
    context/staging/structure.json
```

## CRITICAL: Source of Truth for All Angles and Dimensions

**You are FORBIDDEN from computing any angle or dimension internally.**

Read all fabrication values from `context/staging/structure.json` (geometry section):

| Blueprint Field         | JSON Path                                    |
|:------------------------|:---------------------------------------------|
| Miter (saw swing)       | `compound_cut.miter_deg`                     |
| Blade Bevel             | `compound_cut.bevel_deg`                     |
| Pitch angle             | `compound_cut.pitch_angle_deg`               |
| **Beam ring flat miter**| **`beam_ring.beam_miter_deg`**               |
| Rafter length (total)   | `rafter.total_with_overhang_in`              |
| Roof rise               | `roof_rise.rise_in`                          |
| Total building height   | `total_height.total_height_ft`               |
| SVG coordinates         | `svg_coordinates.*`                          |

**Critical angle distinction — the most common drift failure:**
- `beam_ring.beam_miter_deg` = flat cut across beam end (30.00° for hex/4:12) — used for ring beam crosscuts only.
- `compound_cut.miter_deg` = compound saw swing for hip rafters (28.71° for hex/4:12) — NOT the same value.
- Never use the rafter miter as the beam miter or vice versa.

**The most common hallucination:** Using the pitch angle (e.g. 18.43°) as the compound miter setting. The miter angle for a hexagonal hip rafter at 4:12 pitch is **28.71°**, not 18.43°. The geometry engine calculates this correctly — use it.

## Shop Blueprint Determinism Rule

Shop blueprints are fabrication artifacts, not concept art.

For every revision, all blueprint dimensions, angles, and saw settings MUST be sourced from:
```
context/staging/structure.json
outputs/shop-blueprint/SB01-cut-list.json
```

Do **not** infer, estimate, or copy angles from images, render prompts, or visual references.

If blueprint values differ from `structure.json` (geometry section), **stop and create a drift report** rather than publishing the output. Every blueprint must include a test-cut warning for compound cuts.

## SVG XML Hard Rules (mandatory — same as drawing-generator)

1. Comments: `<!-- ... -->` only. **No `--` inside comment bodies.**
2. Text nodes: escape `&` → `&amp;`, `"` → `&quot;`, `<` → `&lt;`, `>` → `&gt;`
3. **Validate every SVG before writing:**
   ```bash
   python3 -c "import xml.etree.ElementTree as ET; ET.parse('outputs/blueprint-shop.svg'); print('XML OK')"
   ```
4. Then run the full validator:
   ```bash
   python3 scripts/svg_validator.py \
       outputs/<sheet>.svg context/staging/structure.json
   ```

## Behavior

Produce output files:
- `outputs/blueprint-plan.svg` — Footprint with post coordinates, beam ring, diagonal.
- `outputs/blueprint-elevation.svg` — Dimensioned elevation with all critical labels.
- `outputs/blueprint-isometric.svg` — Mathematically projected parallel wireframe. **NO AI image generation.** Use exact SVG polygon paths derived from the coordinate map.
- `outputs/blueprint-component-isolation.svg` — Isolated detail for compound cut geometry (rafter top/bottom, bird's mouth, hub bolt placement).

## Cut List Rules

When generating the cut list table:
- Copy `miter_deg` and `bevel_deg` verbatim from `structure.json` (geometry section).
- Format as: `Miter: XX.X° / Bevel: X.X°`
- Include a note: `⚠ Test cut on scrap before cutting all [N] pieces.`
- Never include a "Derived by" note — all values come from the geometry engine.

Always prioritize fabrication clarity over visual aesthetics. Dense dimensions, bold callout arrows, and explicit warnings are preferred.

## Gotchas

- **Miter angle ≠ pitch angle — the most common failure mode.** For a hexagonal hip rafter at 4:12, pitch_angle=18.43° but miter_deg=28.71°. Any blueprint showing miter ≈ pitch angle will produce cuts that fail at the hub. Copy `miter_deg` verbatim from `structure.json` (geometry section) every time.
- **"Test cut on scrap" warning is non-negotiable.** It must appear in every cut list that includes compound angles. Omitting it exposes the builder to waste on an expensive timber run.
- **Isometric is parallel projection, not perspective.** No foreshortening, no vanishing points. Compute SVG polygon paths from the coordinate map. Any visual foreshortening indicates a calculation error.
- **SB01-cut-list.json must be written as a build artifact.** builder-docs-generator reads board-foot totals from this file to generate the budget estimate. If the JSON is not written, the downstream builder documents will be incomplete.
- **Component isolation sheet must show the bird's-mouth cut geometry.** This is the most referenced detail at the job site. Missing or vague bird's-mouth dimensions are the leading cause of builder callbacks.

## Smoke Test

1. **Angle accuracy gate:** Given `structure.json` geometry section with miter_deg=28.71: all blueprint text labels show miter=28.71° exactly; no sheet shows miter≈18.43°. ✓
2. **SB01-cut-list.json presence:** After skill completes: `outputs/shop-blueprint/SB01-cut-list.json` exists with board-foot totals populated. ✓
3. **Validator gate:** All four output SVGs pass `svg_validator.py` before skill signals completion. ✓

## Completion: HANDOFF_BLOCK

On successful SVG and cut-list generation, emit this block so the design-orchestrator can proceed to Stage 5 (Blueprint QA):

```json
{
  "stage": "shop-blueprint-generator",
  "status": "COMPLETE",
  "outputs": [
    "outputs/blueprint-plan.svg",
    "outputs/blueprint-elevation.svg",
    "outputs/blueprint-isometric.svg",
    "outputs/blueprint-component-isolation.svg",
    "outputs/shop-blueprint/SB01-cut-list.json"
  ],
  "sheets_validated": 4,
  "next_stage": "validation-agent (Stage 5 Blueprint QA) → Stage 5.75 Drawing Red-Team Gate"
}
```

If any sheet fails validation or SB01-cut-list.json was not written, set `"status": "FAIL"` and list the blocking issues.

## 🚨 Drawing Red-Team Gate — Embedded Enforcement

**This skill MUST NOT claim its own SVG outputs are complete or "builder-meaningful."**

Blueprint generation ends at SVG + cut-list production. The stage is NOT complete until:

1. The adversarial gate has run independently:
   ```bash
   python3 plugins/garden-structure-designer/scripts/run_drawing_red_team.py \
     --svg-dir outputs \
     --model context/staging/structure.json \
     --report-dir context/staging \
     --md-dir outputs
   ```
2. `context/staging/drawing-red-team-report.json` exists with `may_claim_success: true`.

Do NOT set package status to `PASS`, `READY`, or `DESIGN COMPLETE` from within this skill.
Passing `svg_validator.py` is necessary but not sufficient — the red-team gate is the authoritative final check.

## Stop-and-Diagnose Before Renderer Rewrite

If generated SVGs fail the red-team gate, this skill must not immediately rewrite drawing logic.

First determine whether the failure is caused by:

- path split between `context/staging` and `plugins/garden-structure-designer/context/staging`;
- stale quality dashboard;
- missing geometry section in `structure.json`;
- missing `schema-validation-report.json`;
- missing `physics-validation-report.json`;
- red-team/content validator correctly rejecting placeholder drawings;
- renderer genuinely lacking required drawing content.

Only rewrite `render_drawings.py` after confirming:

1. the active staging path is known;
2. `structure.json` is current and its geometry section is populated;
3. the quality dashboard reads the same staging path;
4. the red-team/content validator is running against current SVGs;
5. the failure is genuinely renderer output quality.

If the failure is a path/reporting problem, fix the path/reporting problem first.

