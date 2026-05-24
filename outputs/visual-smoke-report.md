# Visual Smoke Test Report (SVG -> Browser Render)

**Schema:** garden-structure-designer/visual-smoke-report/1.0  
**Generated:** 2026-05-24T07:49:33.335074+00:00  
**Source Hash:** `6a3a31093913173981deb71e2e0b9148147dfe6aba97ba5347db7fd1c3ea4d61`  
**Structure:** `context/staging/structure.json`  
**SVG Dir:** `outputs`  
**Out Dir:** `outputs/visual-smoke`  
**Baseline Dir:** `None`  
**Mode:** fail-on-regression  

**Run Command:**
`python3 plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py --structure context/staging/structure.json --svg-dir outputs`

---

## STATUS: **PASS**
**may_claim_success:** `True`

### Summary
All sheets rendered and heuristics passed.

---

## Overall Failures
- *(none)*

## Overall Warnings
- *(none)*

---

# Per-Sheet Results
### drawing-plan-view
**Status:** **PASS**  
**SVG:** `outputs/drawing-plan-view.svg`  
**PNG:** `outputs/visual-smoke/drawing-plan-view.png`  
**Hub Crop PNG:** `outputs/visual-smoke/drawing-plan-view.hub.png`  
**Hub Clip (px):** `[660, 440, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.1523`
- bbox_fill_ratio: `0.9439`
- top_left_clustered: `False`
- hub_edge_density: `0.0582`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### drawing-elevation-view
**Status:** **PASS**  
**SVG:** `outputs/drawing-elevation-view.svg`  
**PNG:** `outputs/visual-smoke/drawing-elevation-view.png`  

#### Metrics
- non_bg_ratio: `0.1628`
- bbox_fill_ratio: `0.9439`
- top_left_clustered: `False`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### drawing-isometric-view
**Status:** **PASS**  
**SVG:** `outputs/drawing-isometric-view.svg`  
**PNG:** `outputs/visual-smoke/drawing-isometric-view.png`  
**Hub Crop PNG:** `outputs/visual-smoke/drawing-isometric-view.hub.png`  
**Hub Clip (px):** `[660, 307, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.2009`
- bbox_fill_ratio: `0.9439`
- top_left_clustered: `False`
- hub_edge_density: `0.1107`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### drawing-perspective-view
**Status:** **PASS**  
**SVG:** `outputs/drawing-perspective-view.svg`  
**PNG:** `outputs/visual-smoke/drawing-perspective-view.png`  
**Hub Crop PNG:** `outputs/visual-smoke/drawing-perspective-view.hub.png`  
**Hub Clip (px):** `[660, 307, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.2010`
- bbox_fill_ratio: `0.9439`
- top_left_clustered: `False`
- hub_edge_density: `0.1107`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### blueprint-plan
**Status:** **PASS**  
**SVG:** `outputs/blueprint-plan.svg`  
**PNG:** `outputs/visual-smoke/blueprint-plan.png`  
**Hub Crop PNG:** `outputs/visual-smoke/blueprint-plan.hub.png`  
**Hub Clip (px):** `[660, 440, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.1567`
- bbox_fill_ratio: `0.9468`
- top_left_clustered: `False`
- hub_edge_density: `0.0714`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### blueprint-elevation
**Status:** **PASS**  
**SVG:** `outputs/blueprint-elevation.svg`  
**PNG:** `outputs/visual-smoke/blueprint-elevation.png`  

#### Metrics
- non_bg_ratio: `0.1001`
- bbox_fill_ratio: `0.9468`
- top_left_clustered: `False`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### blueprint-isometric
**Status:** **PASS**  
**SVG:** `outputs/blueprint-isometric.svg`  
**PNG:** `outputs/visual-smoke/blueprint-isometric.png`  
**Hub Crop PNG:** `outputs/visual-smoke/blueprint-isometric.hub.png`  
**Hub Clip (px):** `[660, 307, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.1533`
- bbox_fill_ratio: `0.9468`
- top_left_clustered: `False`
- hub_edge_density: `0.1107`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### blueprint-component-isolation
**Status:** **PASS**  
**SVG:** `outputs/blueprint-component-isolation.svg`  
**PNG:** `outputs/visual-smoke/blueprint-component-isolation.png`  

#### Metrics
- non_bg_ratio: `0.1013`
- bbox_fill_ratio: `0.9468`
- top_left_clustered: `False`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---

## Artifacts Produced
- JSON report: `context/staging/visual-smoke-report.json`
- This report: `outputs/visual-smoke-report.md`
- Screenshots: `outputs/visual-smoke/<sheet>.png`
