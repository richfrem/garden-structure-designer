# Visual Smoke Test Report (SVG -> Browser Render)

**Schema:** garden-structure-designer/visual-smoke-report/1.0  
**Generated:** 2026-08-16T20:13:07.950489+00:00  
**Source Hash:** `b2c3d4e5f6a1`  
**Structure:** `context/staging/structure.json`  
**SVG Dir:** `outputs`  
**Out Dir:** `outputs/visual-smoke`  
**Baseline Dir:** `None`  
**Mode:** no-baseline  

**Run Command:**
`python3 plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py --structure context/staging/structure.json --svg-dir outputs`

---

## STATUS: **FAIL**
**may_claim_success:** `False`

### Summary
Visual smoke test failed heuristics.

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
- non_bg_ratio: `0.0592`
- bbox_fill_ratio: `0.4859`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `857`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 0, 'braces': 12}`
- detected_components: `{'posts': 13, 'beams': 28, 'rafters': 16}`

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
- non_bg_ratio: `0.0440`
- bbox_fill_ratio: `0.4003`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `102`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 0, 'braces': 12}`
- detected_components: `{'posts': 11, 'beams': 8, 'rafters': 11}`

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
- non_bg_ratio: `0.1598`
- bbox_fill_ratio: `0.8097`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1268`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 0, 'braces': 12}`
- detected_components: `{'posts': 22, 'beams': 6, 'rafters': 93}`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### drawing-perspective-view
**Status:** **PASS**  
**SVG:** `outputs/drawing-perspective-view.svg`  
**PNG:** `outputs/visual-smoke/drawing-perspective-view.png`  

#### Metrics
- non_bg_ratio: `0.1598`
- bbox_fill_ratio: `0.8097`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1268`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 0, 'braces': 12}`
- detected_components: `{'posts': 22, 'beams': 6, 'rafters': 93}`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### blueprint-plan
**Status:** **PASS**  
**SVG:** `outputs/blueprint-plan.svg`  
**PNG:** `outputs/visual-smoke/blueprint-plan.png`  

#### Metrics
- non_bg_ratio: `0.0667`
- bbox_fill_ratio: `0.4868`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `848`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 0, 'braces': 12}`
- detected_components: `{'posts': 15, 'beams': 27, 'rafters': 5}`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---
### blueprint-elevation
**Status:** **FAIL**  
**SVG:** `outputs/blueprint-elevation.svg`  
**PNG:** `outputs/visual-smoke/blueprint-elevation.png`  

#### Metrics
- non_bg_ratio: `0.0182`
- bbox_fill_ratio: `0.4003`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `107`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 0, 'braces': 12}`
- detected_components: `{'posts': 12, 'beams': 11, 'rafters': 12}`

#### Failures
- VISUAL_BLANK

#### Warnings
- *(none)*

---
### blueprint-isometric
**Status:** **PASS**  
**SVG:** `outputs/blueprint-isometric.svg`  
**PNG:** `outputs/visual-smoke/blueprint-isometric.png`  

#### Metrics
- non_bg_ratio: `0.1186`
- bbox_fill_ratio: `0.8116`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1250`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 0, 'braces': 12}`
- detected_components: `{'posts': 23, 'beams': 5, 'rafters': 120}`

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
- non_bg_ratio: `0.0478`
- bbox_fill_ratio: `0.8402`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `221`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 0, 'braces': 12}`
- detected_components: `{'posts': 13, 'beams': 72, 'rafters': 9}`

#### Failures
- *(none)*

#### Warnings
- *(none)*

---

## Artifacts Produced
- JSON report: `context/staging/visual-smoke-report.json`
- This report: `outputs/visual-smoke-report.md`
- Screenshots: `outputs/visual-smoke/<sheet>.png`
