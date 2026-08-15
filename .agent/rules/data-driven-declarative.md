---
description: Rule enforcing a 100% data-driven, schema-validated declarative architecture across all CAD, drawing, and fabrication engines.
globs: ["plugins/**/*.py", "plugins/**/*.json", "context/**/*.json"]
---

# Data-Driven & Declarative Architecture Policy

This policy governs the absolute separation of geometry parameters from algorithmic execution. All CAD engines, 2D SVG layout renderers, 3D solid modelers, and fabrication cut compilers must be driven dynamically by JSON data contracts, preventing logic changes when design dimensions or layout preferences evolve.

---

## 1. Non-Negotiables

### 1. Zero Hardcoded Design Constants
No structural coordinates, board-foot sizing multipliers, framing counts, pitch slopes, secondary rafter division fractions, post offset spacing, bracing clearance margins, or joinery parameters may be hardcoded as magic numbers inside Python files (`*.py`). Scale factors, margins, viewport parameters, and view coordinates must be driven dynamically by `structure.json`.
* **Violation**: `scale = 80.0` or `scale = 55.0` or `s_purlin = 0.55` inside rendering scripts.
* **Compliant**: Calculating scales dynamically based on bounding box or using coordinates from `structure.json`.

### 2. Single Staging Source of Truth (`structure.json`)
All pipeline steps must consume and write back to the unified staging data bus (`context/staging/structure.json`). Passing state via file-system shims, shell arguments, or concurrent global variables is strictly prohibited. The 3D solid compiler, 2D SVG renderer, and fabrication compiler must read from the exact same JSON file to maintain mathematical parity across all views.
* **Path Discipline (SDD 3.3)**: Always resolve the staging path unambiguously relative to the primary workspace root to prevent worktree path-split errors.

### 3. Explicit Fail-Closed Parsing (No Silent Fallbacks)
Silent fallbacks are FORBIDDEN in geometry, rendering, or presentation logic. All required geometry parameters and critical configurations must be explicitly checked. If a configuration or geometry field is missing, fail immediately by raising a `ValueError` with a standardized machine-readable prefix.
* **Violation**: `scale = coords.get("scale_px_per_ft", 55.0)` or `key = structure.get("presentation", {}).get("palette", "cedar_warm")`.
* **Compliant**:
  ```python
  if "presentation" not in structure or "palette" not in structure["presentation"]:
      raise ValueError("SCHEMA_MISSING_FIELD: presentation.palette")
  key = structure["presentation"]["palette"]
  ```

### 4. Spec-Gated Bi-Directional Schema Alignment (SDD Gate 0)
Any new structural framing member, attachment hardware, or custom geometry added to the CAD engine constitutes a **Spec Change (SDD Track B)**. The parameter schema must first be defined and approved in `generate_real_schemas.py` or the JSON Schema contract BEFORE writing engine execution logic. Database schemas, data models, and compilation scripts must remain in lockstep.

### 5. Automated Static Guard Verification
Before committing CAD engine edits or executing rendering pipelines, code MUST pass the automated static scanner guard (e.g., `hardcode_guard.py`) to verify zero silent fallback defaults (`.get()`) or hardcoded numerical scale factors exist in python code.

### 6. TDD Data-Driven Verification
Write integration tests that load modified JSON structure specs (e.g., changing the number of jack rafters from `2` to `4` or changing purlin heights) and verify that derived geometry and cut lists scale dynamically without code logic modifications.

---

## 2. SDD Execution Track Mapping

| Activity | SDD Track | Required Workflow |
|:---------|:----------|:------------------|
| **Parameter Variations** (e.g., 4:12 vs 6:12 pitch using existing schema) | **Track A (Factory)** | Deterministic execution & dynamic rendering using `structure.json` |
| **Schema Expansion** (e.g., adding new joinery fields or tie-beam parameters) | **Track B (Discovery)** | SDD Gate 0 approval on schema definition ➜ plan engine update ➜ implement |
| **Error Handling / Guard Fixes** (e.g., improving `ValueError` diagnostic strings) | **Track C (Micro-Fix)** | Direct implementation with unit test verification |

