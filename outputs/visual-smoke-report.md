# Visual Smoke Test Report (SVG -> Browser Render)

**Schema:** garden-structure-designer/visual-smoke-report/1.0  
**Generated:** 2026-05-24T18:53:05.325653+00:00  
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
- non_bg_ratio: `0.1474`
- bbox_fill_ratio: `0.9534`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1647`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 6, 'beams': 46, 'rafters': 72}`
- hub_edge_density: `0.0676`

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
- non_bg_ratio: `0.1933`
- bbox_fill_ratio: `0.9534`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1756`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 20, 'beams': 59, 'rafters': 42}`

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
- non_bg_ratio: `0.2200`
- bbox_fill_ratio: `0.9534`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `3250`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 35, 'beams': 67, 'rafters': 66}`
- hub_edge_density: `0.1083`

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
- non_bg_ratio: `0.2325`
- bbox_fill_ratio: `0.9534`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2805`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 30, 'beams': 70, 'rafters': 61}`
- hub_edge_density: `0.1083`

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
- non_bg_ratio: `0.1592`
- bbox_fill_ratio: `0.9551`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1644`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 6, 'beams': 48, 'rafters': 75}`
- hub_edge_density: `0.0655`

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
- non_bg_ratio: `0.1114`
- bbox_fill_ratio: `0.9551`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1923`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 21, 'beams': 53, 'rafters': 45}`

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
- non_bg_ratio: `0.1743`
- bbox_fill_ratio: `0.9551`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `3214`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 31, 'beams': 57, 'rafters': 66}`
- hub_edge_density: `0.1076`

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
- JSON report: `context/staging/visual-smoke-report.json`
- This report: `outputs/visual-smoke-report.md`
- Screenshots: `outputs/visual-smoke/<sheet>.png`
