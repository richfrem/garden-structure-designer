# Visual Smoke Test Report (SVG -> Browser Render)

**Schema:** garden-structure-designer/visual-smoke-report/1.1  
**Generated:** 2026-10-12T07:30:23.352331+00:00  
**Source Hash:** `intent_10ft_hex_pergola_yellow_cedar_20261011`  
**Revision:** `8e093b56-d9b0-4f21-93e9-ffb888398d3f` (`77ad42eab043af468317cf65709aba3ffb724b816afedf859c1663330c293862`)  
**Structure:** `context/staging/structure.json`  
**SVG Dir:** `outputs/10ft-hex-pergola`  
**Out Dir:** `outputs/10ft-hex-pergola/visual-smoke`  
**Baseline Dir:** `None`  
**Mode:** no-baseline  

**Run Command:**
`python3 plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py --structure context/staging/structure.json --svg-dir outputs/10ft-hex-pergola`

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
**SVG:** `outputs/10ft-hex-pergola/drawing-plan-view.svg`  
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/drawing-plan-view.png`  
**Hub Crop PNG:** `outputs/10ft-hex-pergola/visual-smoke/drawing-plan-view.hub.png`  
**Hub Clip (px):** `[660, 440, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.0704`
- bbox_fill_ratio: `0.3263`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `951`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 1, 'beams': 9, 'rafters': 20}`
- hub_edge_density: `0.0264`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### drawing-elevation-view
**Status:** **PASS**  
**SVG:** `outputs/10ft-hex-pergola/drawing-elevation-view.svg`  
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/drawing-elevation-view.png`  

#### Metrics
- non_bg_ratio: `0.1262`
- bbox_fill_ratio: `0.4204`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `544`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 9, 'beams': 11, 'rafters': 11}`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### drawing-isometric-view
**Status:** **PASS**  
**SVG:** `outputs/10ft-hex-pergola/drawing-isometric-view.svg`  
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/drawing-isometric-view.png`  
**Hub Crop PNG:** `outputs/10ft-hex-pergola/visual-smoke/drawing-isometric-view.hub.png`  
**Hub Clip (px):** `[660, 482, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.2445`
- bbox_fill_ratio: `0.6388`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2014`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 13, 'beams': 15, 'rafters': 47}`
- hub_edge_density: `0.0446`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### drawing-perspective-view
**Status:** **PASS**  
**SVG:** `outputs/10ft-hex-pergola/drawing-perspective-view.svg`  
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/drawing-perspective-view.png`  
**Hub Crop PNG:** `outputs/10ft-hex-pergola/visual-smoke/drawing-perspective-view.hub.png`  
**Hub Clip (px):** `[660, 482, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.1089`
- bbox_fill_ratio: `0.4533`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1329`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 29, 'beams': 73, 'rafters': 112}`
- hub_edge_density: `0.0473`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### blueprint-plan
**Status:** **PASS**  
**SVG:** `outputs/10ft-hex-pergola/blueprint-plan.svg`  
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/blueprint-plan.png`  
**Hub Crop PNG:** `outputs/10ft-hex-pergola/visual-smoke/blueprint-plan.hub.png`  
**Hub Clip (px):** `[660, 440, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.0257`
- bbox_fill_ratio: `0.3277`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1628`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 1, 'beams': 23, 'rafters': 39}`
- hub_edge_density: `0.0356`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### blueprint-elevation
**Status:** **PASS**  
**SVG:** `outputs/10ft-hex-pergola/blueprint-elevation.svg`  
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/blueprint-elevation.png`  

#### Metrics
- non_bg_ratio: `0.0280`
- bbox_fill_ratio: `0.3959`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `950`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 19, 'beams': 17, 'rafters': 27}`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### blueprint-isometric
**Status:** **PASS**  
**SVG:** `outputs/10ft-hex-pergola/blueprint-isometric.svg`  
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/blueprint-isometric.png`  
**Hub Crop PNG:** `outputs/10ft-hex-pergola/visual-smoke/blueprint-isometric.hub.png`  
**Hub Clip (px):** `[660, 482, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.0585`
- bbox_fill_ratio: `0.6156`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `3015`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 33, 'beams': 34, 'rafters': 95}`
- hub_edge_density: `0.0925`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### blueprint-component-isolation
**Status:** **PASS**  
**SVG:** `outputs/10ft-hex-pergola/blueprint-component-isolation.svg`  
**PNG:** `outputs/10ft-hex-pergola/visual-smoke/blueprint-component-isolation.png`  

#### Metrics
- non_bg_ratio: `0.0473`
- bbox_fill_ratio: `0.8402`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `221`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 14, 'beams': 71, 'rafters': 10}`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---

## Artifacts Produced
- JSON report: `/Users/richardfremmerlid/Projects/garden-structure-designer/context/staging/visual-smoke-report.json`
- This report: `outputs/10ft-hex-pergola/visual-smoke-report.md`
- Screenshots: `outputs/10ft-hex-pergola/visual-smoke/<sheet>.png`
