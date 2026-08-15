# Visual Smoke Test Report (SVG -> Browser Render)

**Schema:** garden-structure-designer/visual-smoke-report/1.0  
**Generated:** 2026-08-15T19:43:35.840701+00:00  
**Source Hash:** `6a3a31093913173981deb71e2e0b9148147dfe6aba97ba5347db7fd1c3ea4d61`  
**Structure:** `/Users/richardfremmerlid/Projects/garden-structure-designer/context/staging/structure.json`  
**SVG Dir:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs`  
**Out Dir:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke`  
**Baseline Dir:** `None`  
**Mode:** no-baseline  

**Run Command:**
`python3 plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py --structure /Users/richardfremmerlid/Projects/garden-structure-designer/context/staging/structure.json --svg-dir /Users/richardfremmerlid/Projects/garden-structure-designer/outputs`

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
**SVG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/drawing-plan-view.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/drawing-plan-view.png`  
**Hub Crop PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/drawing-plan-view.hub.png`  
**Hub Clip (px):** `[660, 440, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.0501`
- bbox_fill_ratio: `0.3495`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2736`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 4, 'beams': 15, 'rafters': 67}`
- hub_edge_density: `0.0676`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for drawing-plan-view.svg — re-rendered

---
### drawing-elevation-view
**Status:** **PASS**  
**SVG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/drawing-elevation-view.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/drawing-elevation-view.png`  

#### Metrics
- non_bg_ratio: `0.0597`
- bbox_fill_ratio: `0.4215`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `0`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 15, 'beams': 10, 'rafters': 39}`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for drawing-elevation-view.svg — re-rendered

---
### drawing-isometric-view
**Status:** **PASS**  
**SVG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/drawing-isometric-view.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/drawing-isometric-view.png`  
**Hub Crop PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/drawing-isometric-view.hub.png`  
**Hub Clip (px):** `[660, 438, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.1402`
- bbox_fill_ratio: `0.5774`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2162`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 30, 'beams': 33, 'rafters': 89}`
- hub_edge_density: `0.1083`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for drawing-isometric-view.svg — re-rendered

---
### drawing-perspective-view
**Status:** **PASS**  
**SVG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/drawing-perspective-view.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/drawing-perspective-view.png`  
**Hub Crop PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/drawing-perspective-view.hub.png`  
**Hub Clip (px):** `[660, 438, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.1402`
- bbox_fill_ratio: `0.5774`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2162`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 30, 'beams': 33, 'rafters': 89}`
- hub_edge_density: `0.1083`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for drawing-perspective-view.svg — re-rendered

---
### blueprint-plan
**Status:** **PASS**  
**SVG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/blueprint-plan.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/blueprint-plan.png`  
**Hub Crop PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/blueprint-plan.hub.png`  
**Hub Clip (px):** `[660, 440, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.0544`
- bbox_fill_ratio: `0.3503`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `3160`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 6, 'beams': 17, 'rafters': 68}`
- hub_edge_density: `0.0655`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for blueprint-plan.svg — re-rendered

---
### blueprint-elevation
**Status:** **PASS**  
**SVG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/blueprint-elevation.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/blueprint-elevation.png`  

#### Metrics
- non_bg_ratio: `0.0277`
- bbox_fill_ratio: `0.4220`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `0`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 19, 'beams': 12, 'rafters': 37}`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for blueprint-elevation.svg — re-rendered

---
### blueprint-isometric
**Status:** **PASS**  
**SVG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/blueprint-isometric.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/blueprint-isometric.png`  
**Hub Crop PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/blueprint-isometric.hub.png`  
**Hub Clip (px):** `[660, 438, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.1110`
- bbox_fill_ratio: `0.5778`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2267`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 30, 'beams': 28, 'rafters': 102}`
- hub_edge_density: `0.1076`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for blueprint-isometric.svg — re-rendered

---
### blueprint-component-isolation
**Status:** **PASS**  
**SVG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/blueprint-component-isolation.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/blueprint-component-isolation.png`  

#### Metrics
- non_bg_ratio: `0.1104`
- bbox_fill_ratio: `0.9551`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1690`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 13, 'beams': 97, 'rafters': 17}`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---

## Artifacts Produced
- JSON report: `/Users/richardfremmerlid/Projects/garden-structure-designer/context/staging/visual-smoke-report.json`
- This report: `outputs/visual-smoke-report.md`
- Screenshots: `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/visual-smoke/<sheet>.png`
