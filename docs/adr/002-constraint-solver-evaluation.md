# ADR-002: Evaluation of CADCraft 2D Planar Constraint Solver (M2B Probe)

## Context
Per specification section C6 and Milestone M2B, we evaluated whether CADCraft's internal 2D geometric constraint solver (`cadcraft-constraints` crate) should be utilized in the primary `garden-structure-designer` framing pipeline or remain an offline capability.

## Evaluation & Probe Results
- **Probe Script**: `scripts/constraint_solver_probe.py`
- **Solver Architecture**: Levenberg-Marquardt (LM) non-linear least squares solver with minimum-norm steps, null-space span tracking, and analytical degrees-of-freedom (`dof.rs`) counting.
- **Test Results**: All 35 tests (26 unit + 9 integration) passed in 0.02s:
  - Robust handling of coincident points, tangency, collinearity, perpendicularity, parallelism, and autoconstrained rectangle chains.
  - Proper detection of over-constrained and inconsistent systems without panics.
- **Framing Feasibility**:
  - `garden-structure-designer`'s primary models (gazebos, pergolas) require 3D spatial geometry, compound bevel/miter cuts, and radial vertex placement, which are currently solved with zero ambiguity and sub-millimeter determinism in Python (`geometry_engine.py`).
  - `cadcraft-constraints` is strictly 2D planar (XY) intended for sketch drafting and profile extrusion sketches.

## Decision
1. **Preserve Current Geometry Authority**: Python remains 100% authoritative over 3D structural geometry, member vertices, and compound cuts.
2. **CADCraft Subprocess Role**: CADCraft remains strictly a downstream drafting/exchange subprocess engine (`ExchangeWriter`), never an alternate geometry authority.
3. **Future Use Case**: The 2D constraint solver is well-suited for future orthogonal grid layout sketches (`OrthogonalGridTopology`, Milestone M5) and custom joint profile drafting.
