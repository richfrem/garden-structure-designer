---
name: adversarial-drawing-reviewer
description: Launches an independent adversarial drawing-review sub-agent to evaluate SVG outputs for builder usefulness before success can be claimed.
version: 1.3.2
allowed-tools: Read, Write, Bash, Vision
tags:
  - validation
  - svg
  - drawings
  - red-team
  - quality-gate
metadata:
  garden_structure_designer:
    category: validation
    consumes:
      - outputs/*.svg
      - context/staging/structure.json
    produces:
      - context/staging/drawing-red-team-report.json
      - outputs/drawing-red-team-report.md
    validators:
      - plugins/garden-structure-designer/scripts/hardcode_guard.py
      - plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py
      - plugins/garden-structure-designer/scripts/svg_validator.py
      - plugins/garden-structure-designer/scripts/drawing_content_validator.py
    repair_axes:
      - svg_placeholder_geometry
      - svg_missing_dimensions
      - svg_missing_component_details
      - svg_not_builder_meaningful
      - visual_drift_or_regression
      - static_hardcode_violation
---

# Adversarial Drawing Reviewer Skill

This skill exists to prevent green-check theater.

The drawing generator cannot certify its own success.

This skill runs a strict multi-layered gate (Static Scan, Browser Headless rendering, Computer Vision topology check, and Perceptual Difference audit) of every generated drawing before the package can be marked `PASS`.

## Required Behavior

1. **Static Invariant Guard**: Scan the codebase using `hardcode_guard.py` to ensure no literal scales or silent fallbacks exist.
2. **PNG co-generation (token-efficient)**: `render_drawings.py` produces `outputs/visual-smoke/*.png` inline alongside each SVG using `qlmanage` (macOS) or Playwright fallback — **no separate browser session required**. Inspect the pre-generated PNGs directly with Read/Vision tools:
   - `outputs/visual-smoke/drawing-isometric-view.png`
   - `outputs/visual-smoke/drawing-perspective-view.png`
   - `outputs/visual-smoke/blueprint-*.png`
   
   Only re-run `visual_svg_smoke_test.py` if PNGs are missing or stale relative to the SVGs. Playwright is a last-resort fallback, not the primary rendering path.
3. **Computer Vision Topology Audit**: Execute OpenCV-driven feature line detections on the PNGs using Canny edge filtering and Hough line transforms to verify posts, beams, rafters, and hub densities against the expected model configuration.
4. **Perceptual Image Difference**: Compute structural pHash Perceptual Hashing and Mean Absolute Difference (MAD) against baselines/reference images to detect visual drift.
5. **Multimodal Visual Inspection (Carpenter's Eye Test)**: Open and visually inspect the PNG renders (specifically `outputs/visual-smoke/drawing-isometric-view.png` and `drawing-perspective-view.png`) alongside the reference baseline image `outputs/high-resolution-image/hexagon_pergola_render.png` using vision capabilities. Systematically verify every visible joint and member against this checklist:
   - **Hub Apex Connections**:
     * Rafter ends must terminate flat and flush against the hub vertical faces.
     * Rafters must not visually slice through one another or overlap in the apex region.
     * The hub block must be subtle and integrated, not oversized or projecting as a chimney block above the rafter tops.
     * There must be absolutely **no floating, disconnected primitive blocks** hovering in space near the hub or rafters.
   - **Post-to-Beam Seats**:
     * Beam support ledgers must sit squarely and flush on post tops/notches with zero visual gaps or floating elements.
   - **Knee Braces**:
     * Knee braces must be symmetrically aligned with mitered endpoints seated flush against the post face and beam soffit (underside).
     * Endpoints must not hover in space or display ambiguous alignments.
   - **Secondary Framing Suppression**:
     * Verify presentation views (e.g. `drawing-perspective-view.png`) suppress secondary jack rafters and purlins, showing only clean primary framing.
   - **Occlusion and Z-Order**:
     * Ensure correct front-to-back occlusion rendering (no back-side members drawing in front of front-side members).
   If any visual defect is identified, list its Location, Severity (Cosmetic / Structural / Blocking), and Suggested Fix Category. Hard rule: Do not claim PASS if any structural/clipping visual defect exists.
6. **Traditional SVG Validation**: Run `svg_validator.py` and `drawing_content_validator.py` on the files.
7. **Gate Verdict**: Write `context/staging/drawing-red-team-report.json` and set `may_claim_success: true` only when all layers PASS.

## Mandatory Failure Rule

If drawings are blank, tiny, childish, symbolic, or have visual errors (such as rafters colliding or the central hub sticking up above the roof line), this skill must return `FAIL` or `PARTIAL`.

Do not allow `PASS` merely because XML validation passes.

## Authoritative Commands

### 1. Static & Visual Smoke Gate Command
Runs the AST scan guard, Playwright browser rendering, OpenCV topology, and pHash/MAD baseline verification:
```bash
# Verify no static scale hardcodes exist
python3 plugins/garden-structure-designer/scripts/hardcode_guard.py

# Render and audit browser sheets against expected topology
python3 plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py \
  --structure context/staging/structure.json \
  --svg-dir outputs \
  --out-dir outputs/visual-smoke \
  --report-json context/staging/visual-smoke-report.json \
  --report-md outputs/visual-smoke-report.md \
  --fail-on-regression
```

### 2. Traditional Red-Team Content Command
Enumerates all SVGs, runs the content and scale checks, and builds the composite red-team summary:
```bash
python3 plugins/garden-structure-designer/scripts/run_drawing_red_team.py \
  --svg-dir outputs \
  --model context/staging/structure.json \
  --report-dir context/staging \
  --md-dir outputs
```

## Obstacle Escalation

When the red-team gate fails, the reviewer must distinguish between:

- drawings are bad;
- reports are stale;
- paths are inconsistent;
- required artifacts are missing;
- validators are misconfigured.

The reviewer must not only say "FAIL." The reviewer must identify the likely class of failure and recommend the next control-plane action.

Required output fields in `drawing-red-team-report.json`:

```json
{
  "failure_classification": [
    "RENDERER_PLACEHOLDER_OUTPUT",
    "PATH_SPLIT",
    "STALE_REPORT"
  ],
  "recommended_next_action": "FIX_PATHS_FIRST|RERUN_REPORTS_FIRST|FIX_RENDERER_FIRST|BLOCK_AND_REPORT"
}
```

This writes:
- `context/staging/drawing-content-report.json` — per-sheet content detail
- `context/staging/drawing-red-team-report.json` — gate verdict + `may_claim_success`
- `outputs/drawing-red-team-report.md` — human-readable summary

## Diagnostic Commands (optional supplemental detail)

Individual validator runs for debugging a specific sheet:

```bash
python3 plugins/garden-structure-designer/scripts/svg_validator.py \
  outputs/<sheet>.svg \
  context/staging/structure.json

python3 plugins/garden-structure-designer/scripts/drawing_content_validator.py \
  outputs/<sheet>.svg \
  context/staging/structure.json \
  --json-output context/staging/drawing-content-report.json \
  --append
```

Then perform adversarial review using the `drawing-red-team-agent` rubric.

## Final Gate

The orchestrator must read:

```text
context/staging/drawing-red-team-report.json
```

If:

```json
"may_claim_success": false
```

then the package status must not be `PASS`.

Allowed statuses are:

```text
PARTIAL
BLOCKED
DRAFT ONLY
```

The job is not done until this skill approves the drawings.
