# Visual Smoke Test Report (SVG -> Browser Render)

**Schema:** garden-structure-designer/visual-smoke-report/1.0  
**Generated:** 2026-08-16T03:50:52.777331+00:00  
**Source Hash:** `a1b2c3d4e5f6`  
**Structure:** `context/staging/structure.json`  
**SVG Dir:** `outputs`  
**Out Dir:** `outputs/visual-smoke`  
**Baseline Dir:** `None`  
**Mode:** no-baseline  

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
- non_bg_ratio: `0.0318`
- bbox_fill_ratio: `0.3538`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1885`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 1, 'beams': 10, 'rafters': 32}`
- hub_edge_density: `0.0676`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for drawing-plan-view.svg — re-rendered

---
### drawing-elevation-view
**Status:** **PASS**  
**SVG:** `outputs/drawing-elevation-view.svg`  
**PNG:** `outputs/visual-smoke/drawing-elevation-view.png`  

#### Metrics
- non_bg_ratio: `0.0505`
- bbox_fill_ratio: `0.3963`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `28`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 15, 'beams': 13, 'rafters': 15}`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for drawing-elevation-view.svg — re-rendered

---
### drawing-isometric-view
**Status:** **PASS**  
**SVG:** `outputs/drawing-isometric-view.svg`  
**PNG:** `outputs/visual-smoke/drawing-isometric-view.png`  
**Hub Crop PNG:** `outputs/visual-smoke/drawing-isometric-view.hub.png`  
**Hub Clip (px):** `[660, 471, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.1319`
- bbox_fill_ratio: `0.6080`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2097`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 29, 'beams': 19, 'rafters': 63}`
- hub_edge_density: `0.1083`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for drawing-isometric-view.svg — re-rendered

---
### drawing-perspective-view
**Status:** **PASS**  
**SVG:** `outputs/drawing-perspective-view.svg`  
**PNG:** `outputs/visual-smoke/drawing-perspective-view.png`  
**Hub Crop PNG:** `outputs/visual-smoke/drawing-perspective-view.hub.png`  
**Hub Clip (px):** `[660, 471, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.1319`
- bbox_fill_ratio: `0.6080`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2097`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 29, 'beams': 19, 'rafters': 63}`
- hub_edge_density: `0.1083`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for drawing-perspective-view.svg — re-rendered

---
### blueprint-plan
**Status:** **PASS**  
**SVG:** `outputs/blueprint-plan.svg`  
**PNG:** `outputs/visual-smoke/blueprint-plan.png`  
**Hub Crop PNG:** `outputs/visual-smoke/blueprint-plan.hub.png`  
**Hub Clip (px):** `[660, 440, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.0349`
- bbox_fill_ratio: `0.3549`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2181`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 1, 'beams': 11, 'rafters': 33}`
- hub_edge_density: `0.0655`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for blueprint-plan.svg — re-rendered

---
### blueprint-elevation
**Status:** **PASS**  
**SVG:** `outputs/blueprint-elevation.svg`  
**PNG:** `outputs/visual-smoke/blueprint-elevation.png`  

#### Metrics
- non_bg_ratio: `0.0218`
- bbox_fill_ratio: `0.3963`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `29`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 17, 'beams': 15, 'rafters': 14}`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for blueprint-elevation.svg — re-rendered

---
### blueprint-isometric
**Status:** **PASS**  
**SVG:** `outputs/blueprint-isometric.svg`  
**PNG:** `outputs/visual-smoke/blueprint-isometric.png`  
**Hub Crop PNG:** `outputs/visual-smoke/blueprint-isometric.hub.png`  
**Hub Clip (px):** `[660, 471, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.1064`
- bbox_fill_ratio: `0.6084`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2161`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 33, 'beams': 24, 'rafters': 82}`
- hub_edge_density: `0.1076`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for blueprint-isometric.svg — re-rendered

---
### blueprint-component-isolation
**Status:** **PASS**  
**SVG:** `outputs/blueprint-component-isolation.svg`  
**PNG:** `outputs/visual-smoke/blueprint-component-isolation.png`  

#### Metrics
- non_bg_ratio: `0.0473`
- bbox_fill_ratio: `0.8402`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `221`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 13, 'beams': 66, 'rafters': 9}`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for blueprint-component-isolation.svg — re-rendered

---

## Artifacts Produced
- JSON report: `context/staging/visual-smoke-report.json`
- This report: `outputs/visual-smoke-report.md`
- Screenshots: `outputs/visual-smoke/<sheet>.png`
