# Visual Smoke Test Report (SVG -> Browser Render)

**Schema:** garden-structure-designer/visual-smoke-report/1.1
**Generated:** 2026-10-12T01:19:59.414906+00:00
**Source Hash:** `intent_10ft_hex_pergola_yellow_cedar_20261011`
**Revision:** `rev-10ft-hex-pergola-20261011-001` (`5d5b3de9609bfa3d06dde79c007a97dd0db1ed3c1dd72817de9196481fb9c773`)
**Structure:** `context/staging/structure.json`
**SVG Dir:** `outputs/10ft-hex-pergola`
**Out Dir:** `outputs/10ft-hex-pergola/visual-smoke`
**Baseline Dir:** `None`
**Mode:** no-baseline

**Run Command:**
`python3 plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py --structure context/staging/structure.json --svg-dir outputs/10ft-hex-pergola`

---

## STATUS: **FAIL**
**may_claim_success:** `False`

### Summary
Visual smoke test failed heuristics.

---

## Overall Failures
- BROWSER_RENDER_BLOCKED: drawing-plan-view.svg
- BROWSER_RENDER_BLOCKED: drawing-elevation-view.svg
- BROWSER_RENDER_BLOCKED: drawing-isometric-view.svg
- BROWSER_RENDER_BLOCKED: drawing-perspective-view.svg
- BROWSER_RENDER_BLOCKED: blueprint-plan.svg
- BROWSER_RENDER_BLOCKED: blueprint-elevation.svg
- BROWSER_RENDER_BLOCKED: blueprint-isometric.svg
- BROWSER_RENDER_BLOCKED: blueprint-component-isolation.svg

## Overall Warnings
- *(none)*

---

# Per-Sheet Results
### drawing-plan-view
**Status:** **FAIL**
**SVG:** `outputs/10ft-hex-pergola/drawing-plan-view.svg`
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/drawing-plan-view.png`

#### Metrics
- non_bg_ratio: `0.0000`
- bbox_fill_ratio: `0.0000`
- top_left_clustered: `False`

#### Failures
- BROWSER_RENDER_BLOCKED

#### Warnings
- *(none)*

---
### drawing-elevation-view
**Status:** **FAIL**
**SVG:** `outputs/10ft-hex-pergola/drawing-elevation-view.svg`
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/drawing-elevation-view.png`

#### Metrics
- non_bg_ratio: `0.0000`
- bbox_fill_ratio: `0.0000`
- top_left_clustered: `False`

#### Failures
- BROWSER_RENDER_BLOCKED

#### Warnings
- *(none)*

---
### drawing-isometric-view
**Status:** **FAIL**
**SVG:** `outputs/10ft-hex-pergola/drawing-isometric-view.svg`
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/drawing-isometric-view.png`

#### Metrics
- non_bg_ratio: `0.0000`
- bbox_fill_ratio: `0.0000`
- top_left_clustered: `False`

#### Failures
- BROWSER_RENDER_BLOCKED

#### Warnings
- *(none)*

---
### drawing-perspective-view
**Status:** **FAIL**
**SVG:** `outputs/10ft-hex-pergola/drawing-perspective-view.svg`
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/drawing-perspective-view.png`

#### Metrics
- non_bg_ratio: `0.0000`
- bbox_fill_ratio: `0.0000`
- top_left_clustered: `False`

#### Failures
- BROWSER_RENDER_BLOCKED

#### Warnings
- *(none)*

---
### blueprint-plan
**Status:** **FAIL**
**SVG:** `outputs/10ft-hex-pergola/blueprint-plan.svg`
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/blueprint-plan.png`

#### Metrics
- non_bg_ratio: `0.0000`
- bbox_fill_ratio: `0.0000`
- top_left_clustered: `False`

#### Failures
- BROWSER_RENDER_BLOCKED

#### Warnings
- *(none)*

---
### blueprint-elevation
**Status:** **FAIL**
**SVG:** `outputs/10ft-hex-pergola/blueprint-elevation.svg`
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/blueprint-elevation.png`

#### Metrics
- non_bg_ratio: `0.0000`
- bbox_fill_ratio: `0.0000`
- top_left_clustered: `False`

#### Failures
- BROWSER_RENDER_BLOCKED

#### Warnings
- *(none)*

---
### blueprint-isometric
**Status:** **FAIL**
**SVG:** `outputs/10ft-hex-pergola/blueprint-isometric.svg`
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/blueprint-isometric.png`

#### Metrics
- non_bg_ratio: `0.0000`
- bbox_fill_ratio: `0.0000`
- top_left_clustered: `False`

#### Failures
- BROWSER_RENDER_BLOCKED

#### Warnings
- *(none)*

---
### blueprint-component-isolation
**Status:** **FAIL**
**SVG:** `outputs/10ft-hex-pergola/blueprint-component-isolation.svg`
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/blueprint-component-isolation.png`

#### Metrics
- non_bg_ratio: `0.0000`
- bbox_fill_ratio: `0.0000`
- top_left_clustered: `False`

#### Failures
- BROWSER_RENDER_BLOCKED

#### Warnings
- *(none)*

---

## Artifacts Produced
- JSON report: `context/staging/visual-smoke-report.json`
- This report: `outputs/visual-smoke-report.md`
- Screenshots: `outputs/10ft-hex-pergola/visual-smoke/<sheet>.png`
