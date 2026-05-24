---
description: Rule enforcing a 100% data-driven, schema-validated declarative architecture across all CAD, drawing, and fabrication engines.
globs: ["plugins/**/*.py", "plugins/**/*.json", "context/**/*.json"]
---

## 🗄️ Data-Driven & Declarative Architecture Policy

This policy governs the absolute separation of geometry parameters from algorithmic execution. All CAD engines, 2D SVG layout renderers, 3D solid modelers, and fabrication cut compilers must be driven dynamically by JSON data contracts, preventing logic changes when design dimensions or layout preferences evolve.

### Non-Negotiables

1. **Zero Hardcoded Design Constants**:
   No structural coordinates, board-foot sizing multipliers, framing counts, pitch slopes, secondary rafter division fractions, post offset spacing, bracing clearance margins, or joinery parameters may be hardcoded as magic numbers inside Python files (`*.py`). Scale factors, margins, viewport parameters, and view coordinates must be driven dynamically by `structure.json`.
   * **Violation**: `scale = 80.0` or `scale = 55.0` or `s_purlin = 0.55` inside rendering scripts.
   * **Compliant**: Calculating scales dynamically based on bounding box or using coordinates from `structure.json`.

2. **Single Staging Source of Truth (`structure.json`)**:
   All pipeline steps must consume and write back to `context/staging/structure.json` as the unified data bus. Passing state via file-system shims, shell arguments, or concurrent global variables is strictly prohibited. The 3D build123d compiler, 2D SVG renderer, and fabrication compiler must read from the exact same JSON file to maintain mathematical parity across all views.

3. **Explicit Fail-Closed Parsing (No Silent Fallbacks)**:
   Silent fallbacks are FORBIDDEN in geometry, rendering, or presentation logic. All required geometry parameters and critical configurations must be explicitly checked. If a configuration or geometry field is missing, fail immediately by raising a `ValueError`.
   * **Violation**: `scale = coords.get("scale_px_per_ft", 55.0)` or `key = structure.get("presentation", {}).get("palette", "cedar_warm")`.
   * **Compliant**:
     ```python
     if "presentation" not in structure or "palette" not in structure["presentation"]:
         raise ValueError("MISSING_REQUIRED_CONFIG: presentation.palette")
     key = structure["presentation"]["palette"]
     ```

4. **Bi-Directional Schema Alignment**:
   Any new structural framing member, attachment hardware, or custom geometry added to the CAD engine must first have its parameter schema defined in `generate_real_schemas.py` or the appropriate JSON Schema contract. The database schema, data model, and compilation scripts must remain in lockstep.

5. **TDD Data-Driven Verification**:
   Write integration tests that load modified JSON structure specs (e.g. changing the number of jack rafters from `2` to `4` or changing purlin heights) and verify that the derived geometry and cut lists scale dynamically without logic modifications.
