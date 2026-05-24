## [2026-05-23] Fabrication-Grade Geometry & Visual Smoke Test

- **Tier**: Tier 1 (Gap)
- **Target**: `geometry_engine.py`, `cad_scene.py`, `visual_svg_smoke_test.py`
- **Outcome**: 
  - Implemented Phase 1 of Fabrication-Grade Geometry: Added `geometry.joints` payload to `geometry_engine.py` using line-plane intersection math for hub termination, brace anchoring, and beam miter planes.
  - Refactored `cad_scene.py` to consume `geometry.joints` nodes directly, removing manual approximations.
  - Implemented `visual_svg_smoke_test.py` using Playwright (Chromium) to perform raster-level heuristic checks (spaghetti hub, blank sheets, clustering).
  - Updated `design-orchestrator.md` to include Stage 5.6 (Visual Smoke Test Gate).
  - Passed full-cycle pipeline run with `may_claim_success: true`.

## [2026-05-24] Secondary Rafters & Collar Purlins Pipeline Integration

- **Tier**: Tier 1 (Gap)
- **Target**: `render_drawings.py`, `test_cad_geometry_invariants.py`, `chrome-verification/SKILL.md`
- **Outcome**:
  - Unsealed geometry, configured collar purlins and intermediate rafters in `structure.json` to match high-resolution render.
  - Refactored `render_drawings.py` count invariants check to filter out non-primary (Jack) rafters, resolving the perspective/isometric drawing generation crash.
  - Updated `test_cad_geometry_invariants.py` unit test to properly filter for primary rafters when asserting exact semantic count invariants.
  - Created a first-class `chrome-verification` skill (`SKILL.md`) in the central store to formally govern browser-based visual smoke testing.
  - Verified and passed the full visual smoke test pipeline in headless Chromium with zero warnings and zero failures.


