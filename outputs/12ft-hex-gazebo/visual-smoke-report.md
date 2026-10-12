# Visual Smoke Test Report (SVG -> Browser Render)

**Schema:** garden-structure-designer/visual-smoke-report/1.1  
**Generated:** 2026-10-12T17:43:32.662925+00:00  
**Source Hash:** `intent_12ft_hex_gazebo_western_red_cedar_20261012`  
**Revision:** `3bd88e39-cba8-4a7f-a368-c4ec3e2b28f8` (`aa9201c9ffce1efec3aa94a36f5c86ad8afedc7b25942676a3c0ffc57be79185`)  
**Structure:** `context/staging/structure.json`  
**SVG Dir:** `outputs/12ft-hex-gazebo`  
**Out Dir:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke`  
**Baseline Dir:** `None`  
**Mode:** no-baseline  

**Run Command:**
`python3 plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py --structure context/staging/structure.json --svg-dir outputs/12ft-hex-gazebo`

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
**SVG:** `outputs/12ft-hex-gazebo/drawing-plan-view.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/drawing-plan-view.png`  
**Hub Crop PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/drawing-plan-view.hub.png`  
**Hub Clip (px):** `[660, 440, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.0890`
- bbox_fill_ratio: `0.3691`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `1687`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 3, 'beams': 16, 'rafters': 53}`
- hub_edge_density: `0.0275`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for drawing-plan-view.svg — re-rendered

---
### drawing-elevation-view
**Status:** **PASS**  
**SVG:** `outputs/12ft-hex-gazebo/drawing-elevation-view.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/drawing-elevation-view.png`  

#### Metrics
- non_bg_ratio: `0.1156`
- bbox_fill_ratio: `0.4098`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `499`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 11, 'beams': 10, 'rafters': 18}`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for drawing-elevation-view.svg — re-rendered

---
### drawing-isometric-view
**Status:** **PASS**  
**SVG:** `outputs/12ft-hex-gazebo/drawing-isometric-view.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/drawing-isometric-view.png`  
**Hub Crop PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/drawing-isometric-view.hub.png`  
**Hub Clip (px):** `[660, 398, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.2240`
- bbox_fill_ratio: `0.6006`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2591`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 15, 'beams': 11, 'rafters': 60}`
- hub_edge_density: `0.0537`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for drawing-isometric-view.svg — re-rendered

---
### drawing-perspective-view
**Status:** **PASS**  
**SVG:** `outputs/12ft-hex-gazebo/drawing-perspective-view.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/drawing-perspective-view.png`  
**Hub Crop PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/drawing-perspective-view.hub.png`  
**Hub Clip (px):** `[660, 398, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.0985`
- bbox_fill_ratio: `0.4773`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `2126`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 25, 'beams': 72, 'rafters': 169}`
- hub_edge_density: `0.0241`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for drawing-perspective-view.svg — re-rendered

---
### blueprint-plan
**Status:** **PASS**  
**SVG:** `outputs/12ft-hex-gazebo/blueprint-plan.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/blueprint-plan.png`  
**Hub Crop PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/blueprint-plan.hub.png`  
**Hub Clip (px):** `[660, 440, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.0411`
- bbox_fill_ratio: `0.3710`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `3092`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 6, 'beams': 24, 'rafters': 106}`
- hub_edge_density: `0.0342`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for blueprint-plan.svg — re-rendered

---
### blueprint-elevation
**Status:** **PASS**  
**SVG:** `outputs/12ft-hex-gazebo/blueprint-elevation.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/blueprint-elevation.png`  

#### Metrics
- non_bg_ratio: `0.0362`
- bbox_fill_ratio: `0.4106`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `980`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 21, 'beams': 16, 'rafters': 56}`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for blueprint-elevation.svg — re-rendered

---
### blueprint-isometric
**Status:** **PASS**  
**SVG:** `outputs/12ft-hex-gazebo/blueprint-isometric.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/blueprint-isometric.png`  
**Hub Crop PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/blueprint-isometric.hub.png`  
**Hub Clip (px):** `[660, 398, 280, 280]`  

#### Metrics
- non_bg_ratio: `0.0636`
- bbox_fill_ratio: `0.6040`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `4456`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 32, 'beams': 27, 'rafters': 133}`
- hub_edge_density: `0.1018`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for blueprint-isometric.svg — re-rendered

---
### blueprint-component-isolation
**Status:** **PASS**  
**SVG:** `outputs/12ft-hex-gazebo/blueprint-component-isolation.svg`  
**PNG:** `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/blueprint-component-isolation.png`  

#### Metrics
- non_bg_ratio: `0.0476`
- bbox_fill_ratio: `0.8402`
- top_left_clustered: `False`
- cv_content_ratio: `1.0000`
- cv_hub_density: `221`
- expected_topology: `{'posts': 6, 'beams': 6, 'rafters': 6, 'hub': 1, 'braces': 12}`
- detected_components: `{'posts': 13, 'beams': 72, 'rafters': 10}`

#### Failures
- *(none)*

#### Warnings
- PNG_STALE_OR_MISSING: PNG was older than SVG for blueprint-component-isolation.svg — re-rendered

---

## Artifacts Produced
- JSON report: `context/staging/visual-smoke-report.json`
- This report: `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke-report.md`
- Screenshots: `/Users/richardfremmerlid/Projects/garden-structure-designer/outputs/12ft-hex-gazebo/visual-smoke/<sheet>.png`
