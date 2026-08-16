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
## [2026-08-15] Pipeline Scope Alignment & Agent Contract Synchronization

- **Tier**: Tier 1 (Gap)
- **Target**: `design-orchestrator.md`, `validation-agent.md`, `GEMINI.md`
- **Outcome**:
  - Identified gap where orchestrator's Revision Mode and validation gates stopped at Stage 5.75 (drawing red team) without executing Stage 6 (builder documents: budget-estimate, lumber-purchase-list, assembly-guide) and Stage 7 (master PDF compilation via `embed_svgs.py` and `md-to-pdf`).
  - Synchronized `design-orchestrator.md` Revision Mode to mandate full 7-stage deterministic execution.
  - Evolved `validation-agent.md` Revision Completion Gate to explicitly require builder documents and compiled PDF before emitting `READY`.
  - Updated `GEMINI.md` Deterministic Completion Standard to explicitly list `structure.json`, all SVGs, `fabrication/cut-list.json`, builder markdown documents, and compiled `pergola_plan.pdf`.

## [2026-08-15] L5 Adversarial Audit, First-Class CLI Tools & AST Hardcode Elimination

- **Tier**: Tier 2 (Failure / Refactor)
- **Target**: `builder_docs_compiler.py`, `compile_package.py`, `hardcode_guard.py`, full script suite (46 files)
- **Outcome**:
  - Eliminated ad-hoc inline Python scripts by creating first-class CLI utilities: [`builder_docs_compiler.py`](file:///Users/richardfremmerlid/Projects/garden-structure-designer/plugins/garden-structure-designer/scripts/builder_docs_compiler.py) and [`compile_package.py`](file:///Users/richardfremmerlid/Projects/garden-structure-designer/plugins/garden-structure-designer/scripts/compile_package.py) with dedicated unit tests in `tests/test_builder_docs_compiler.py` and `tests/test_compile_package.py`.
  - Implemented and executed AST static scanner [`hardcode_guard.py`](file:///Users/richardfremmerlid/Projects/garden-structure-designer/plugins/garden-structure-designer/scripts/hardcode_guard.py) across all 46 Python scripts, fixing all 18 AST `.get(..., <literal>)` fallback violations to achieve 100% fail-closed data-driven geometry compliance per `.agent/rules/data-driven-declarative.md`.
  - Fixed lifecycle section assertion in `cad_language_translator.py`, CLI defaults in `load_applicable_lessons.py`, `cut_list_engine.py`, and `structural_physics_validator.py`, and unified `structure.json` geometry support in `assembly_guide_validator.py`.
  - Full suite of 139 unit/integration tests passing (100% PASS).
  - Executed full Stages 0–8 pipeline: Physics PASS, Drawing Content PASS, Adversarial Red-Team PASS (`may_claim_success: true`), Assembly Guide PASSED ✓, Master Embedded Document compiled to [`outputs/pergola_plan_embedded.md`](file:///Users/richardfremmerlid/Projects/garden-structure-designer/outputs/pergola_plan_embedded.md), and dynamic [`outputs/quality-dashboard.md`](file:///Users/richardfremmerlid/Projects/garden-structure-designer/outputs/quality-dashboard.md) updated to COMPLETED.---

## [2026-08-16] Multi-Project Archive Isolation & Rectangular Flat Pergola Geometry Evolution
- **Tier**: Tier 2 (Failure / Refactor)
- **Target**: `interactive-designer.md`, `design-orchestrator.md`, `cad_language_translator.py`, `geometry_engine.py`, `render_drawings.py`, `drawing_content_validator.py`, `visual_svg_smoke_test.py`
- **Trigger**: Pipeline claimed completion while drawings and outputs still retained radial/hexagonal roof shapes from a previous project run.
- **Actions Taken**:
  1. Updated `interactive-designer.md` and `design-orchestrator.md` with a mandatory pre-intake archive & clean-slate step that automatically backs up prior project artifacts to `temp/pastoutputs/<project-name>` and empties `outputs/` before new generation.
  2. Extended `cad_language_translator.py` and `geometry_engine.py` with first-class support for `shape: "rectangle"` and non-hub flat pergolas (`hub.type: "none"`), placing posts on orthogonal Cartesian grids and generating parallel cross-rafters.
  3. Made drawing isolation panel generation in `render_drawings.py` and component count assertions in `drawing_content_validator.py` dynamically adapt to non-hub structures.
  4. Updated `visual_svg_smoke_test.py` to suppress hub-crop and radial beam span assertions when `structure.shape == "rectangle"`.
  5. Re-ran complete deterministic pipeline (Stages 0–7) for the 12' × 18' Saanich BC rectangular pergola: 150/150 pytest tests passing, visual smoke tests passing, drawing red-team gate approved (`may_claim_success: true`), and generated the master `outputs/pergola_plan.pdf`.
- **Outcome**: 100% clean outputs with zero cross-project contamination, fully verified rectangular pergola blueprints, and strict prevention of premature completion claims.

