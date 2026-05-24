## [2026-05-23] Fabrication-Grade Geometry & Visual Smoke Test

- **Tier**: Tier 1 (Gap)
- **Target**: `geometry_engine.py`, `cad_scene.py`, `visual_svg_smoke_test.py`
- **Outcome**: 
  - Implemented Phase 1 of Fabrication-Grade Geometry: Added `geometry.joints` payload to `geometry_engine.py` using line-plane intersection math for hub termination, brace anchoring, and beam miter planes.
  - Refactored `cad_scene.py` to consume `geometry.joints` nodes directly, removing manual approximations.
  - Implemented `visual_svg_smoke_test.py` using Playwright (Chromium) to perform raster-level heuristic checks (spaghetti hub, blank sheets, clustering).
  - Updated `design-orchestrator.md` to include Stage 5.6 (Visual Smoke Test Gate).
  - Passed full-cycle pipeline run with `may_claim_success: true`.

