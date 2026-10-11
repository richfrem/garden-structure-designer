# CADCraft Integration — Task Tracker v1.5

**Status**: Ready for Implementation (Multi-Model Aligned: Opus 5.5 + Astra)  
**Target Branch**: `feat/cadcraft-integration`  
**Parent Epic**: Infuse deterministic CAD & Drafting capabilities into `garden-structure-designer`  
**Normative Contract**: `cadcraft_v1.5_spec.md` (C1–C6) and root `architecture.md`

---

## 1. Upstream Submodule & Build Setup

- [x] **TASK-SUB-001**: Move `temp/repos/cadcraft` into canonical pinned submodule `vendor/cadcraft` tracking `https://github.com/storytold/cadcraft` at commit `54ea5e743a29acd8f3178cfaa82fb74a38c2de72`. Remove `temp/repos/cadcraft`.
- [x] **TASK-SUB-002**: Author portable, cross-platform build script `scripts/build_cadcraft.py` to compile `cargo build --locked --release -p cadcraft-cli --manifest-path vendor/cadcraft/Cargo.toml`.

---

## 2. Milestone Progress Checklist

### M0 — Pure Revision Hashing, Defect Reproduction & Two-Stage Topology Gates (C1–C2, C5)
- [x] **TASK-000**: Implement pure revision utility `plugins/garden-structure-designer/scripts/revision_identity.py` (canonical `gsd-json-v1` SHA-256 hash calculation, receipt schema generator, in-process receipt validator).
- [x] **TASK-001**: Author failing reproduction tests in `plugins/garden-structure-designer/tests/test_topology_invariants.py`:
  - Name and utilize pipeline seam `plugins/garden-structure-designer/scripts/pipeline_runner.py:run_pipeline(structure_path, stages=...)`.
  - Assert Stage 0.5 fail-closed with `TOPOLOGY_CARDINALITY_MISMATCH` on mismatched intent (e.g. 5 or 8 declared posts for 6-sided gazebo).
  - Assert Stage 2 fail-closed with `TOPOLOGY_CARDINALITY_MISMATCH` on valid 6-post intent producing 5 or 8 actual solved posts.
  - Assert Stage 2 fail-closed on duplicate member IDs (`DUPLICATE_MEMBER_ID`), dangling references (`DANGLING_CONNECTION_ENDPOINT`), or missing hub face connections.
  - Assert Stage 0.5 & Stage 2 fail-closed with `TOPOLOGY_NOT_IMPLEMENTED` on reserved families (`OrthogonalGridTopology`, `HipRidgeTopology`).
  - Verify downstream renderers, CAD adapters, and package compilers are strictly NOT called after Stage 2 rejection.
- [x] **TASK-002**: Implement Stage 0.5 `plugins/garden-structure-designer/scripts/validate_topology_intent.py` and update `schemas/structure.schema.json`.
- [x] **TASK-003**: Harden Stage 2 `plugins/garden-structure-designer/scripts/topology_compiler.py` to validate source arrays before graph construction; enforce in-process validation for downstream consumers.
- [x] **TASK-004**: Record baseline evidence (observed paths, precision limits) per plan TASK-004 without asserting unverified license claims (documented in `ATTRIBUTION.md` and ADR `002-constraint-solver-evaluation.md`).

---

### M1A — Upstream Headless CLI Feasibility & ExchangeWriter Port (C3)
- [x] **TASK-101**: Audit `vendor/cadcraft` license inventory, transitive dependencies, and API surface; author `ATTRIBUTION.md` based on verified evidence.
- [x] **TASK-102**: Compile release binary with `scripts/build_cadcraft.py` and record binary hash.
- [x] **TASK-103**: Write smoke test `plugins/garden-structure-designer/tests/test_cadcraft_cli_smoke.py`.
- [x] **TASK-104**: Implement `ExchangeWriter` port with `CadcraftAdapter` and fallback `EzdxfAdapter`. Export single-member INSERT block with registered GSD XDATA and verify round-trip with `ezdxf`.

---

### M1B — Production Multi-Sheet DXF Export & Parsed Acceptance (C3–C4)
- [x] **TASK-105**: Author typed adapter `plugins/garden-structure-designer/scripts/cadcraft_adapter.py` with 15s subprocess timeout and error captures.
- [x] **TASK-106**: Implement `plugins/garden-structure-designer/scripts/export_cad.py`:
  - `outputs/cad/SB01-structure.dxf`: Full-scale 3D wireframe framing model.
  - `outputs/cad/SB02-plan.dxf`: Full-scale 2D planar projection.
  - Layer mappings: `FRAMING_POSTS`, `FRAMING_BEAMS`, `FRAMING_RAFTERS`, `FRAMING_HUBS`, `FRAMING_BRACES`, `FOOTINGS_PIERS`.
- [x] **TASK-107**: Wire pipeline lifecycle stages in verified order: Stage 4 (Renderings/DXF) → Stage 5.5 (Parsed DXF & dimensions) → Stage 5.6 (Visual smoke) → Stage 6 (Cut lists & BOM) → Stage 5 (Independent Red-Team approval across ALL artifacts including cut lists) → Stage 7 (Package compilation in `compile_package.py`).
- [x] **TASK-108**: Implement parsed DXF validation in `plugins/garden-structure-designer/scripts/cross_artifact_validator.py` (parsed entity counts, 1:1 member ID xdata parity, 3D bounds for SB01, 2D projected XY bounds for SB02).
- [x] **TASK-109**: Author integration test `plugins/garden-structure-designer/tests/test_dxf_export_pipeline.py`.

---

### M2A — Unified Architectural Drafting Standards (C4)
- [x] **TASK-201**: Consolidate lineweights, architectural tick offsets, and dimension standards in `control_plane/constants.py`.
- [x] **TASK-202**: Align SVG blueprint generators (`render_drawings.py`, `shop-blueprint-generator`) with drafting constants.
- [x] **TASK-203**: Add numerical dimension cross-checks between SVG and DXF in `cross_artifact_validator.py`.

---

### M2B — 2D Planar Constraint Solver Feasibility Gate (Optional Research)
- [x] **TASK-204**: Author `scripts/constraint_solver_probe.py` testing CADCraft `crates/constraints`.
- [x] **TASK-205**: Document solve stability and degrees of freedom; record research decision record.

---

### M3 — Transactional CAS in structure_io.py & Cache Purge (C5)
- [x] **TASK-301**: Implement transaction authority in `plugins/garden-structure-designer/scripts/structure_io.py`.
- [x] **TASK-302**: Enforce atomic commit-time compare-and-swap on `meta.revision_hash`.
- [x] **TASK-303**: Isolate mutation sessions in `context/staging/candidates/<txn_id>/` and write deliverables to `outputs/.rev/<revision_id>/`.
- [x] **TASK-304**: Purge the complete C5 five-family inventory upon candidate commit (solved staging mirrors, drawings/DXFs, cut lists, compiled PDFs/docs, QA/approval reports).
- [x] **TASK-305**: Author concurrency, TTL expiration for orphaned `PREPARED` entries, and crash recovery tests in `plugins/garden-structure-designer/tests/test_transaction_gateway.py`.

---

### M4 — Initial Radial Production Acceptance (C1–C6)
- [x] **TASK-401**: Run complete end-to-end radial test suite across all regular polygons $N \ge 5$ on supported platforms (`test_radial_production_acceptance.py` covering $N \in \{5, 6, 8, 10, 12\}$).
- [x] **TASK-402**: Validate `outputs/package-manifest.json` against all artifact SHA-256 digests (`compile_package.py` and `test_compile_package.py`).
- [x] **TASK-403**: Verify C1–C6 byte-for-byte synchronization between `architecture.md` and `cadcraft_v1.5_spec.md` (verified 100% identical).
- [x] **TASK-404**: Pass independent `drawing-red-team-agent` gate (`may_claim_success: true`).
- [x] **TASK-405**: Link Mermaid architecture diagrams in root `README.md`.

---

### M5 — Orthogonal Grid Pergola & Plugin/Skill Alignment (Future Epic)
- [ ] **TASK-501 (Skill & Agent Documentation Alignment)**:
  - Update `plugins/garden-structure-designer/skills/document-compiler/SKILL.md` to document CAD DXF deliverables (`SB01`, `SB02`) and `package-manifest.json`.
  - Update `plugins/garden-structure-designer/skills/drawing-generator/SKILL.md` and `timber-frame-cad/SKILL.md` with ExchangeWriter port details.
  - Lightly align `plugins/garden-structure-designer/agents/design-orchestrator.md` Stage 7 documentation with CAD deliverables.
- [ ] **TASK-502 (OrthogonalGridTopology Intent & Geometry)**:
  - Implement Stage 0.5 unsealed intent support for `OrthogonalGridTopology` (4 sides, `rows * cols` posts, longitudinal headers, transverse joists).
  - Implement Stage 1 rectangular geometry math in `geometry_engine.py` for arbitrary $M \times N$ orthogonal post grids.
- [ ] **TASK-503 (Orthogonal Topology Compiler)**:
  - Implement Stage 2 sealed graph compilation for rectangular framing (posts $P_1..P_K$, perimeter beams, intermediate joists/ties, post-to-beam tenons/connections).
- [ ] **TASK-504 (Orthogonal Multi-Sheet DXF & Blueprint Projection)**:
  - Extend `export_cad.py` and `render_drawings.py` to project 3D wireframe (`SB01`) and 2D planar plan (`SB02`) for orthogonal grid structures with 1:1 member ID parity.
- [ ] **TASK-505 (End-to-End Claude CLI E2E Verification)**:
  - Prompt Claude CLI (`claude-cli-agent`) to design a 6-post rectangular pergola ($3 \times 2$ post grid, e.g. 18ft $\times$ 12ft) using the plugin skills and scripts.
  - Assert full Stage 0.5 $\rightarrow$ Stage 7 execution producing valid `structure.json`, 8 SVGs, 2 DXFs, fabrication cut list, and compiled PDF package.

---

## 3. Milestone Quality Gates
- **Gate 0 (Topology)**: Both Stage 0.5 (intent) and Stage 2 (sealed graph) pass with 100% of invalid member counts or broken connections failing closed before rendering.
- **Gate 1A (CLI Slice & Port)**: `ExchangeWriter` port proven with `CadcraftAdapter` or fallback `EzdxfAdapter`.
- **Gate 1B (Production DXF)**: Construction package contains parsed-valid multi-layer `.dxf` deliverables with 1:1 ID parity to `structure.json`.
- **Gate 2A (Drafting)**: SVG and DXF dimensions match 100% numerically.
- **Gate 3 (Transactional CAS)**: Atomic commit-time compare-and-swap prevents race conditions and invalidates stale caches.
- **Gate 4 (Production Sign-Off)**: Independent red team approval over all generated deliverables.
- **Gate 5 (Orthogonal Grid Sign-Off)**: 6-post rectangular pergola designed via Claude CLI and verified with 100% test passes across all stages.

