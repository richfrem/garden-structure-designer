# Visual Smoke Test Report (SVG -> Browser Render)

**Schema:** garden-structure-designer/visual-smoke-report/1.0  
**Generated:** 2026-05-24T19:29:36.160712+00:00  
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

#### Metrics
- non_bg_ratio: `0.1740`
- bbox_fill_ratio: `0.9534`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2049`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 9, 'beams': 53, 'rafters': 113}`

#### Failures
- *(none)*

#### Warnings
- Could not compute hub crop window.

---
### drawing-elevation-view
**Status:** **PASS**  
**SVG:** `outputs/drawing-elevation-view.svg`  
**PNG:** `outputs/visual-smoke/drawing-elevation-view.png`  

#### Metrics
- non_bg_ratio: `0.1976`
- bbox_fill_ratio: `0.9534`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1756`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 27, 'beams': 53, 'rafters': 60}`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### drawing-isometric-view
**Status:** **PASS**  
**SVG:** `outputs/drawing-isometric-view.svg`  
**PNG:** `outputs/visual-smoke/drawing-isometric-view.png`  

#### Metrics
- non_bg_ratio: `0.2390`
- bbox_fill_ratio: `0.9534`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `3281`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 34, 'beams': 74, 'rafters': 91}`

#### Failures
- *(none)*

#### Warnings
- Could not compute hub crop window.

---
### drawing-perspective-view
**Status:** **PASS**  
**SVG:** `outputs/drawing-perspective-view.svg`  
**PNG:** `outputs/visual-smoke/drawing-perspective-view.png`  

#### Metrics
- non_bg_ratio: `0.2509`
- bbox_fill_ratio: `0.9534`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2774`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 30, 'beams': 73, 'rafters': 92}`

#### Failures
- *(none)*

#### Warnings
- Could not compute hub crop window.

---
### blueprint-plan
**Status:** **PASS**  
**SVG:** `outputs/blueprint-plan.svg`  
**PNG:** `outputs/visual-smoke/blueprint-plan.png`  

#### Metrics
- non_bg_ratio: `0.1866`
- bbox_fill_ratio: `0.9551`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2048`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 9, 'beams': 53, 'rafters': 114}`

#### Failures
- *(none)*

#### Warnings
- Could not compute hub crop window.

---
### blueprint-elevation
**Status:** **PASS**  
**SVG:** `outputs/blueprint-elevation.svg`  
**PNG:** `outputs/visual-smoke/blueprint-elevation.png`  

#### Metrics
- non_bg_ratio: `0.1200`
- bbox_fill_ratio: `0.9551`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1923`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 27, 'beams': 56, 'rafters': 64}`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### blueprint-isometric
**Status:** **PASS**  
**SVG:** `outputs/blueprint-isometric.svg`  
**PNG:** `outputs/visual-smoke/blueprint-isometric.png`  

#### Metrics
- non_bg_ratio: `0.1902`
- bbox_fill_ratio: `0.9551`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `3252`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 32, 'beams': 74, 'rafters': 99}`

#### Failures
- *(none)*

#### Warnings
- Could not compute hub crop window.

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
