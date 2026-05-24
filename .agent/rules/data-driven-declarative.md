---
description: Rule enforcing a 100% data-driven, schema-validated declarative architecture across all CAD, drawing, and fabrication engines.
globs: ["plugins/**/*.py", "plugins/**/*.json", "context/**/*.json"]
---

## 🗄️ Data-Driven & Declarative Architecture Policy

This policy governs the absolute separation of geometry parameters from algorithmic execution. All CAD engines, 2D SVG layout renderers, 3D solid modelers, and fabrication cut compilers must be driven dynamically by JSON data contracts, preventing logic changes when design dimensions or layout preferences evolve.

### Non-Negotiables

1. **Zero Hardcoded Design Constants**:
   No structural coordinates, board-foot sizing multipliers, framing counts, pitch slopes, secondary rafter division fractions, post offset spacing, bracing clearance margins, or joinery parameters may be hardcoded as magic numbers inside Python files (`*.py`).
   * **Violation**: `s_purlin = 0.55` or `fractions = [1/3, 2/3]` inside model generators.
   * **Compliant**: `s_purlin = structure_data.get("members", {}).get("purlins", {}).get("height_fraction", 0.55)` and computing intermediate rafter fractions dynamically from `structure_data.get("roof", {}).get("secondary_rafters", {}).get("count_per_side", 2)`.

2. **Single Staging Source of Truth (`structure.json`)**:
   All pipeline steps must consume and write back to `context/staging/structure.json` as the unified data bus. Passing state via file-system shims, shell arguments, or concurrent global variables is strictly prohibited. The 3D build123d compiler, 2D SVG renderer, and fabrication compiler must read from the exact same JSON file to maintain mathematical parity across all views.

3. **Defensive Schema Parsing**:
   Always parse JSON keys using `.get()` with safe, building-code compliant fallbacks. Never assume keys are present, and never allow missing JSON properties to crash the CAD compiler.
   ```python
   # Recommended Pattern
   roof_spec = structure_data.get("roof", {})
   secondary_spec = roof_spec.get("secondary_rafters", {})
   count = secondary_spec.get("count_per_side", 2)
   ```

4. **Bi-Directional Schema Alignment**:
   Any new structural framing member, attachment hardware, or custom geometry added to the CAD engine must first have its parameter schema defined in `generate_real_schemas.py` or the appropriate JSON Schema contract. The database schema, data model, and compilation scripts must remain in lockstep.

5. **TDD Data-Driven Verification**:
   Write integration tests that load modified JSON structure specs (e.g. changing the number of jack rafters from `2` to `4` or changing purlin heights) and verify that the derived geometry and cut lists scale dynamically without logic modifications.
