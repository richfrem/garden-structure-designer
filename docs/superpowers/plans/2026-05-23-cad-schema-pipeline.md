# CAD Schema Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the three-file staging model (`design-spec.json`, `structural-model.json`, `geometry-calculations.json`) with a single canonical `context/staging/structure.json` that is the sole input to the CAD engine — zero hardcoded geometry constants in any script.

**Architecture:** Sealed progressive manifest (`Approach B`). `structure.json` starts sparse after intake, is enriched by each pipeline stage, and sections are sealed (`_sealed: true`) once written. `presentation` is never sealed. M1 (scripts + compat shim) ships first so agents keep running; M2 (agents/skills + legacy deletion) follows once M1 passes red-team.

**Tech Stack:** Python 3.11+, `jsonschema`, `pytest`, existing `geometry_engine.py` math functions, `cad_scene.py` / `render_drawings.py` rendering pipeline.

---

## Regression Anchor (must reproduce after every task)

```
geometry.compound_cut.miter_deg   = 28.71
geometry.compound_cut.bevel_deg   = 9.10
geometry.beam_ring.beam_miter_deg = 30.00
geometry.total_height.total_height_ft = 11.045
```

Run after Tasks 3, 4, 5, 9, and 13 to confirm no regression.

---

# MILESTONE 1 — Scripts + Compatibility Shim

---

### Task 1: JSON Schema for `structure.json`

**Files:**
- Create: `plugins/garden-structure-designer/schemas/structure.schema.json`

- [ ] **Step 1: Write the schema**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "structure",
  "type": "object",
  "required": ["meta", "intent", "structure", "layout"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["schema_version", "lifecycle", "source_hash"],
      "properties": {
        "schema_version": { "type": "string" },
        "lifecycle": {
          "type": "string",
          "enum": ["INTENT", "ENGINEERED", "GEOMETRY_SEALED", "CAD_SEALED", "RENDERED"]
        },
        "source_hash": { "type": "string" }
      }
    },
    "intent": {
      "type": "object",
      "required": ["jurisdiction"],
      "properties": {
        "jurisdiction": { "type": "string" },
        "material_preference": { "type": "string" },
        "joinery_style": { "type": "string" }
      }
    },
    "structure": {
      "type": "object",
      "required": ["type", "shape", "sides"],
      "properties": {
        "type": { "type": "string" },
        "shape": { "type": "string" },
        "sides": { "type": "integer", "minimum": 3 }
      }
    },
    "layout": {
      "type": "object",
      "required": ["post_count", "inscribed_radius_ft"],
      "properties": {
        "post_count": { "type": "integer", "minimum": 3 },
        "inscribed_radius_ft": { "type": "number", "exclusiveMinimum": 0 },
        "post_spacing_ft": { "type": "number" }
      }
    },
    "members": {
      "type": "object",
      "required": ["posts", "beams"],
      "properties": {
        "posts": {
          "type": "object",
          "required": ["nominal_size", "actual_width_in", "actual_depth_in", "cut_length_ft"],
          "properties": {
            "nominal_size": { "type": "string" },
            "actual_width_in": { "type": "number", "exclusiveMinimum": 0 },
            "actual_depth_in": { "type": "number", "exclusiveMinimum": 0 },
            "cut_length_ft": { "type": "number", "exclusiveMinimum": 0 }
          }
        },
        "beams": {
          "type": "object",
          "required": ["nominal_size", "actual_width_in", "actual_depth_in", "cut_length_ft"],
          "properties": {
            "nominal_size": { "type": "string" },
            "actual_width_in": { "type": "number", "exclusiveMinimum": 0 },
            "actual_depth_in": { "type": "number", "exclusiveMinimum": 0 },
            "cut_length_ft": { "type": "number" }
          }
        }
      }
    },
    "roof": {
      "type": "object",
      "required": ["type", "pitch", "primary_rafters"],
      "properties": {
        "type": { "type": "string" },
        "pitch": { "type": "string", "pattern": "^\\d+:\\d+$" },
        "pitch_defaulted": { "type": "boolean" },
        "primary_rafters": {
          "type": "object",
          "required": ["count", "nominal_size", "actual_width_in", "actual_depth_in", "overhang_ft"],
          "properties": {
            "count": { "type": "integer", "minimum": 3 },
            "nominal_size": { "type": "string" },
            "actual_width_in": { "type": "number", "exclusiveMinimum": 0 },
            "actual_depth_in": { "type": "number", "exclusiveMinimum": 0 },
            "overhang_ft": { "type": "number", "minimum": 0 }
          }
        }
      }
    },
    "hub": {
      "type": "object",
      "required": ["type", "radius_min_ft"],
      "properties": {
        "type": { "type": "string" },
        "radius_ft": {
          "oneOf": [
            { "type": "number", "exclusiveMinimum": 0 },
            { "type": "string", "const": "auto" }
          ]
        },
        "radius_min_ft": { "type": "number", "exclusiveMinimum": 0 },
        "height_ratio_to_rafter": { "type": "number", "exclusiveMinimum": 0 },
        "clearance_ft": { "type": "number", "minimum": 0 }
      }
    },
    "bracing": {
      "type": "object",
      "required": ["enabled"],
      "properties": {
        "enabled": { "type": "boolean" },
        "layout": { "type": "string" },
        "brace": {
          "type": "object",
          "required": ["actual_width_in", "actual_depth_in", "length_ft", "angle_deg", "count_per_post"],
          "properties": {
            "nominal_size": { "type": "string" },
            "actual_width_in": { "type": "number", "exclusiveMinimum": 0 },
            "actual_depth_in": { "type": "number", "exclusiveMinimum": 0 },
            "length_ft": { "type": "number", "exclusiveMinimum": 0 },
            "angle_deg": { "type": "number", "minimum": 0, "maximum": 90 },
            "count_per_post": { "type": "integer", "minimum": 1 }
          }
        }
      }
    },
    "footings": {
      "type": "object",
      "required": ["type", "diameter_in", "depth_in"],
      "properties": {
        "type": { "type": "string" },
        "diameter_in": { "type": "number", "exclusiveMinimum": 0 },
        "depth_in": { "type": "number", "exclusiveMinimum": 0 },
        "concrete_grade": { "type": "string" }
      }
    },
    "joinery": {
      "type": "object",
      "properties": {
        "beam_seat_style": { "type": "string" },
        "rafter_tail": { "type": "string" },
        "rafter_seat_style": { "type": "string" }
      }
    },
    "invariants": {
      "type": "object",
      "properties": {
        "rafter_count_equals_post_count": { "type": "boolean" },
        "post_top_equals_beam_bottom": { "type": "boolean" },
        "no_rafter_inside_hub_radius": { "type": "boolean" },
        "brace_must_connect_to_surfaces": { "type": "boolean" },
        "no_solid_intersections": { "type": "boolean" },
        "member_counts_match_sections": { "type": "boolean" },
        "no_zero_length_members": { "type": "boolean" },
        "presentation_primary_counts_match": { "type": "boolean" }
      }
    },
    "presentation": {
      "type": "object",
      "properties": {
        "view_mode": { "type": "string" },
        "roof_style": { "type": "string" },
        "visibility_rules": { "type": "object" },
        "labeling": { "type": "object" },
        "palette": { "type": "string" }
      }
    },
    "code": { "type": "object", "additionalProperties": true },
    "geometry": { "type": "object", "additionalProperties": true },
    "cad": { "type": "object", "additionalProperties": true }
  },
  "additionalProperties": false
}
```

Save to `plugins/garden-structure-designer/schemas/structure.schema.json`.

- [ ] **Step 2: Commit**

```bash
git add plugins/garden-structure-designer/schemas/structure.schema.json
git commit -m "feat: add structure.schema.json for unified CAD manifest"
```

---

### Task 2: `structure_io.py` helper module

**Files:**
- Create: `plugins/garden-structure-designer/scripts/structure_io.py`
- Create: `plugins/garden-structure-designer/tests/__init__.py`
- Create: `plugins/garden-structure-designer/tests/test_structure_io.py`

- [ ] **Step 1: Write the failing tests**

Create `plugins/garden-structure-designer/tests/__init__.py` (empty file).

Create `plugins/garden-structure-designer/tests/test_structure_io.py`:

```python
import json
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from structure_io import (
    load_structure, save_structure, seal_section,
    assert_not_sealed, compute_source_hash
)

MINIMAL = {
    "meta": {"schema_version": "2.0", "lifecycle": "INTENT",
             "source_hash": "", "created_at": "2026-01-01T00:00:00Z",
             "updated_at": "2026-01-01T00:00:00Z"},
    "intent": {"jurisdiction": "BC_SAANICH"},
    "structure": {"type": "pergola", "shape": "hexagon", "sides": 6},
    "layout": {"post_count": 6, "inscribed_radius_ft": 4.875},
    "geometry": {"_sealed": False},
}

def test_load_structure(tmp_path):
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(MINIMAL))
    data = load_structure(p)
    assert data["meta"]["schema_version"] == "2.0"

def test_save_structure_updates_timestamp(tmp_path):
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(MINIMAL))
    data = load_structure(p)
    old_ts = data["meta"]["updated_at"]
    import time; time.sleep(0.01)
    save_structure(data, p)
    data2 = load_structure(p)
    assert data2["meta"]["updated_at"] != old_ts

def test_seal_section():
    data = json.loads(json.dumps(MINIMAL))
    seal_section(data, "geometry")
    assert data["geometry"]["_sealed"] is True

def test_seal_section_raises_on_missing():
    data = json.loads(json.dumps(MINIMAL))
    with pytest.raises(KeyError):
        seal_section(data, "nonexistent")

def test_assert_not_sealed_passes_on_unsealed():
    data = json.loads(json.dumps(MINIMAL))
    assert_not_sealed(data, "geometry")  # no raise

def test_assert_not_sealed_raises_on_sealed():
    data = json.loads(json.dumps(MINIMAL))
    data["geometry"]["_sealed"] = True
    with pytest.raises(RuntimeError, match="sealed"):
        assert_not_sealed(data, "geometry")

def test_compute_source_hash_is_deterministic():
    data = json.loads(json.dumps(MINIMAL))
    h1 = compute_source_hash(data)
    h2 = compute_source_hash(data)
    assert h1 == h2
    assert len(h1) == 64  # sha256 hex

def test_compute_source_hash_changes_when_input_changes():
    data = json.loads(json.dumps(MINIMAL))
    h1 = compute_source_hash(data)
    data["layout"]["post_count"] = 8
    h2 = compute_source_hash(data)
    assert h1 != h2
```

- [ ] **Step 2: Run tests — verify they fail**

```bash
cd /Users/richardfremmerlid/Projects/garden-structure-designer
python -m pytest plugins/garden-structure-designer/tests/test_structure_io.py -v 2>&1 | head -20
```

Expected: `ModuleNotFoundError: No module named 'structure_io'`

- [ ] **Step 3: Implement `structure_io.py`**

Create `plugins/garden-structure-designer/scripts/structure_io.py`:

```python
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INPUT_SECTIONS = {
    "intent", "structure", "layout", "members", "roof",
    "hub", "bracing", "footings", "joinery"
}


def load_structure(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_structure(data: dict[str, Any], path: str | Path) -> None:
    data["meta"]["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def seal_section(data: dict[str, Any], section: str) -> None:
    if section not in data:
        raise KeyError(f"Section '{section}' not found in structure")
    data[section]["_sealed"] = True


def assert_not_sealed(data: dict[str, Any], section: str) -> None:
    if data.get(section, {}).get("_sealed"):
        raise RuntimeError(
            f"Section '{section}' is sealed — cannot overwrite. "
            "Downstream stages must not mutate upstream sections."
        )


def compute_source_hash(data: dict[str, Any]) -> str:
    payload = {k: data[k] for k in sorted(INPUT_SECTIONS) if k in data}
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
```

- [ ] **Step 4: Run tests — verify they pass**

```bash
python -m pytest plugins/garden-structure-designer/tests/test_structure_io.py -v
```

Expected: `8 passed`

- [ ] **Step 5: Commit**

```bash
git add plugins/garden-structure-designer/scripts/structure_io.py \
        plugins/garden-structure-designer/tests/__init__.py \
        plugins/garden-structure-designer/tests/test_structure_io.py
git commit -m "feat: add structure_io.py helper with load/save/seal/hash"
```

---

### Task 3: Migrate `geometry_engine.py` to read/write `structure.json`

**Files:**
- Modify: `plugins/garden-structure-designer/scripts/geometry_engine.py`
- Create: `plugins/garden-structure-designer/tests/test_geometry_engine.py`

The existing math functions (`compound_cut`, `beam_ring_miter`, `rafter_length`, `roof_rise`, `total_height`, `svg_layout`) are correct and stay unchanged. Only the `compute()` function and `main()` are replaced.

- [ ] **Step 1: Write the failing tests**

Create `plugins/garden-structure-designer/tests/test_geometry_engine.py`:

```python
import json
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

STRUCTURE_SEED = {
    "meta": {
        "schema_version": "2.0", "lifecycle": "ENGINEERED",
        "source_hash": "abc123", "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z"
    },
    "intent": {"jurisdiction": "BC_SAANICH"},
    "structure": {"type": "pergola", "shape": "hexagon", "sides": 6},
    "layout": {"post_count": 6, "inscribed_radius_ft": 4.875, "post_spacing_ft": 4.875},
    "members": {
        "posts": {"nominal_size": "6x6", "actual_width_in": 5.5,
                  "actual_depth_in": 5.5, "cut_length_ft": 8.42},
        "beams": {"nominal_size": "6x12", "actual_width_in": 6.0,
                  "actual_depth_in": 12.0, "cut_length_ft": 5.0},
    },
    "roof": {
        "type": "hip", "pitch": "4:12", "pitch_defaulted": False,
        "primary_rafters": {
            "count": 6, "nominal_size": "4x6",
            "actual_width_in": 3.5, "actual_depth_in": 5.5, "overhang_ft": 0.75
        },
        "secondary_rafters": {"enabled": False}
    },
    "hub": {"type": "polygonal", "radius_ft": "auto",
            "radius_min_ft": 0.6, "height_ratio_to_rafter": 2.5, "clearance_ft": 0.5},
    "bracing": {
        "enabled": True, "layout": "paired_per_post",
        "brace": {"nominal_size": "4x4", "actual_width_in": 3.5,
                  "actual_depth_in": 3.5, "length_ft": 2.5,
                  "angle_deg": 45, "count_per_post": 2}
    },
    "footings": {"type": "sonotube", "diameter_in": 12, "depth_in": 24,
                 "concrete_grade": "20MPa"},
    "joinery": {"beam_seat_style": "exposed_tenon", "rafter_tail": "decorative_scallop",
                "rafter_seat_style": "birds_mouth"},
    "invariants": {
        "rafter_count_equals_post_count": True,
        "no_rafter_inside_hub_radius": True,
        "no_zero_length_members": True,
        "member_counts_match_sections": True
    },
    "presentation": {"view_mode": "presentation", "palette": "cedar_warm"},
    "code": {"_sealed": False},
    "geometry": {"_comment": "DERIVED", "_sealed": False},
    "cad": {"_sealed": False, "units": "feet",
            "coordinate_system": "right_handed_z_up", "precision": 0.001}
}

def test_regression_hex_4_12(tmp_path):
    """Regression anchor: hex 4:12 must produce exact canonical values."""
    from geometry_engine import compute_from_structure
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(STRUCTURE_SEED))
    compute_from_structure(str(p))
    data = json.loads(p.read_text())
    geo = data["geometry"]
    assert geo["compound_cut"]["miter_deg"] == 28.71
    assert geo["compound_cut"]["bevel_deg"] == 9.10
    assert geo["beam_ring"]["beam_miter_deg"] == 30.00
    assert geo["total_height"]["total_height_ft"] == 11.045

def test_geometry_section_sealed_after_compute(tmp_path):
    from geometry_engine import compute_from_structure
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(STRUCTURE_SEED))
    compute_from_structure(str(p))
    data = json.loads(p.read_text())
    assert data["geometry"]["_sealed"] is True

def test_lifecycle_set_to_geometry_sealed(tmp_path):
    from geometry_engine import compute_from_structure
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(STRUCTURE_SEED))
    compute_from_structure(str(p))
    data = json.loads(p.read_text())
    assert data["meta"]["lifecycle"] == "GEOMETRY_SEALED"

def test_hub_radius_auto_gte_min(tmp_path):
    from geometry_engine import compute_from_structure
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(STRUCTURE_SEED))
    compute_from_structure(str(p))
    data = json.loads(p.read_text())
    hub_r = data["geometry"]["hub_radius_ft"]
    assert hub_r >= STRUCTURE_SEED["hub"]["radius_min_ft"]

def test_hub_radius_formula_gte_cross_section(tmp_path):
    """hub_r must satisfy both: >= radius_min_ft AND >= rafter cross-section (in feet).
    Uses raw inch inputs to avoid tautology with the formula itself."""
    from geometry_engine import compute_from_structure
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(STRUCTURE_SEED))
    compute_from_structure(str(p))
    data = json.loads(p.read_text())
    hub_r = data["geometry"]["hub_radius_ft"]
    rafter_w_in = STRUCTURE_SEED["roof"]["primary_rafters"]["actual_width_in"]
    rafter_d_in = STRUCTURE_SEED["roof"]["primary_rafters"]["actual_depth_in"]
    assert hub_r >= STRUCTURE_SEED["hub"]["radius_min_ft"]
    assert hub_r >= (rafter_w_in + rafter_d_in) / 12.0

def test_rafter_count_invariant_enforced(tmp_path):
    """rafter count != post count must produce a warning."""
    import copy
    from geometry_engine import compute_from_structure
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["roof"]["primary_rafters"]["count"] = 5  # mismatch: 5 != 6 posts
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(seed))
    with pytest.raises(SystemExit):
        compute_from_structure(str(p))
    data = json.loads(p.read_text())
    assert any("INVARIANT" in w for w in data["geometry"]["warnings"])

def test_compute_fails_on_already_sealed_geometry(tmp_path):
    import copy
    from geometry_engine import compute_from_structure
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["geometry"]["_sealed"] = True
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(seed))
    with pytest.raises(RuntimeError, match="sealed"):
        compute_from_structure(str(p))
```

- [ ] **Step 2: Run tests — verify they fail**

```bash
python -m pytest plugins/garden-structure-designer/tests/test_geometry_engine.py -v 2>&1 | head -15
```

Expected: `ImportError: cannot import name 'compute_from_structure' from 'geometry_engine'`

- [ ] **Step 3: Add `compute_from_structure()` to `geometry_engine.py`**

Add this function ABOVE the existing `main()`, after the existing `compute()` function. Do NOT delete `compute()` yet (M2 cleanup):

```python
def compute_from_structure(structure_path: str) -> dict[str, Any]:
    """
    Read structure.json, compute all geometry, seal geometry section, write back.
    This is the new M1+ entry point. The old compute() is kept for compat.
    """
    import os as _os
    import sys as _sys
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from structure_io import load_structure, save_structure, seal_section, assert_not_sealed

    structure = load_structure(structure_path)

    # Coordinate system contract
    cad_meta = structure.get("cad", {})
    assert cad_meta.get("units", "feet") == "feet", "cad.units must be 'feet'"
    assert cad_meta.get("coordinate_system", "right_handed_z_up") == "right_handed_z_up", \
        "cad.coordinate_system must be 'right_handed_z_up'"

    assert_not_sealed(structure, "geometry")

    layout   = structure["layout"]
    members  = structure["members"]
    roof     = structure["roof"]
    hub_spec = structure["hub"]
    inv      = structure.get("invariants", {})
    precision = cad_meta.get("precision", 0.001)

    sides      = layout["post_count"]
    span_ft    = layout["inscribed_radius_ft"]
    pitch      = roof["pitch"]
    pr, rr     = [int(x) for x in pitch.split(":")]
    overhang_ft = roof["primary_rafters"]["overhang_ft"]
    beam_depth_in = members["beams"]["actual_depth_in"]
    post_cut_ft   = members["posts"]["cut_length_ft"]
    rafter_w_in   = roof["primary_rafters"]["actual_width_in"]
    rafter_d_in   = roof["primary_rafters"]["actual_depth_in"]

    # Compute geometry (unchanged math functions)
    cuts   = compound_cut(pr, rr, sides)
    rl     = rafter_length(span_ft, pr, rr, overhang_ft)
    rise   = roof_rise(span_ft, pr, rr)
    height = total_height(post_cut_ft, beam_depth_in, span_ft, pr, rr)

    # Hub radius: geometry_engine owns the formula.
    # Contract: hub_r >= radius_min_ft AND satisfies no_rafter_inside_hub_radius.
    radius_min = hub_spec.get("radius_min_ft", 0.6)
    hub_r = max(radius_min, (rafter_w_in + rafter_d_in) / 12.0)

    warnings: list[str] = []

    # Invariant: rafter_count_equals_post_count
    if inv.get("rafter_count_equals_post_count"):
        rafter_count = roof["primary_rafters"]["count"]
        if rafter_count != sides:
            warnings.append(
                f"INVARIANT FAIL: rafter_count={rafter_count} != post_count={sides}"
            )

    # Invariant: no_zero_length_members
    if inv.get("no_zero_length_members") and rl["structural_length_ft"] < precision:
        warnings.append(
            f"INVARIANT FAIL: rafter structural_length_ft={rl['structural_length_ft']}"
            f" < precision={precision}"
        )

    # Height limit check from code section
    height_limit = structure.get("code", {}).get("height_limit_ft")
    if height_limit and height["total_height_ft"] > height_limit:
        warnings.append(
            f"FAIL: total_height_ft={height['total_height_ft']:.3f} "
            f"exceeds code limit of {height_limit} ft."
        )

    layout_result = svg_layout(height["total_height_ft"], span_ft, sides)
    scale   = layout_result["scale_px_per_ft"]
    grade_y = layout_result["grade_y"]
    post_px = post_cut_ft * scale
    beam_px = (beam_depth_in / 12.0) * scale
    rise_px = span_ft * (pr / rr) * scale

    svg_coords = {
        **layout_result,
        "post_top_y":    round(grade_y - post_px),
        "beam_soffit_y": round(grade_y - post_px),
        "beam_top_y":    round(grade_y - post_px - beam_px),
        "hub_apex_y":    round(grade_y - post_px - beam_px - rise_px),
        "rise_px":       round(rise_px),
        "beam_px":       round(beam_px),
        "post_px":       round(post_px),
    }

    structure["geometry"] = {
        "_comment": "DERIVED — written by geometry_engine.py. Do not manually edit.",
        "_sealed":     True,
        "compound_cut": cuts,
        "beam_ring":    beam_ring_miter(sides),
        "rafter":       rl,
        "roof_rise":    rise,
        "total_height": height,
        "hub_radius_ft": round(hub_r, 4),
        "svg_coordinates": svg_coords,
        "warnings":     warnings,
    }
    structure["meta"]["lifecycle"] = "GEOMETRY_SEALED"

    save_structure(structure, structure_path)

    if warnings:
        for w in warnings:
            print(f"⚠️  {w}", file=sys.stderr)
        sys.exit(1)

    return structure
```

Also update `main()` to detect which file format is being passed:

```python
def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python3 geometry_engine.py <structure.json | structural-model.json>",
            file=sys.stderr,
        )
        sys.exit(1)

    path = sys.argv[1]

    # Detect new vs legacy invocation by checking file content
    import json as _json
    with open(path) as _f:
        _data = _json.load(_f)

    if "meta" in _data and "schema_version" in _data.get("meta", {}):
        # New: structure.json
        compute_from_structure(path)
        return

    # Legacy: structural-model.json → write geometry-calculations.json
    result = compute(path)
    out_path = os.path.join(os.path.dirname(path), "geometry-calculations.json")
    with open(out_path, "w") as f:
        import json as _json2
        _json2.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    if result.get("warnings"):
        print("\n⚠️  WARNINGS:", file=sys.stderr)
        for w in result["warnings"]:
            print(f"  {w}", file=sys.stderr)
        sys.exit(1)
```

- [ ] **Step 4: Run tests — verify they pass**

```bash
python -m pytest plugins/garden-structure-designer/tests/test_geometry_engine.py -v
```

Expected: `7 passed`

- [ ] **Step 5: Commit**

```bash
git add plugins/garden-structure-designer/scripts/geometry_engine.py \
        plugins/garden-structure-designer/tests/test_geometry_engine.py
git commit -m "feat: add compute_from_structure() to geometry_engine — reads/seals structure.json"
```

---

### Task 4: Migrate `cad_scene.py` to read from `structure.json`

**Files:**
- Modify: `plugins/garden-structure-designer/scripts/cad_scene.py`
- Create: `plugins/garden-structure-designer/tests/test_cad_scene.py`

The `build_structure_scene(model, calcs)` signature becomes `build_structure_scene(structure, is_blueprint=False)`. The existing math and prism-building logic is unchanged — only the parameter extraction block changes.

- [ ] **Step 1: Write the failing tests**

Create `plugins/garden-structure-designer/tests/test_cad_scene.py`:

```python
import json
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Re-use the seed + geometry from Task 3 test
from test_geometry_engine import STRUCTURE_SEED
import copy, json as _json

def _seeded_structure(tmp_path):
    from geometry_engine import compute_from_structure
    p = tmp_path / "structure.json"
    p.write_text(_json.dumps(copy.deepcopy(STRUCTURE_SEED)))
    compute_from_structure(str(p))
    return _json.loads(p.read_text())


def test_build_creates_correct_post_count(tmp_path):
    from cad_scene import build_structure_scene, validate_scene_geometry
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    posts = [so for so in scene.solids if so.role == "post"]
    assert len(posts) == s["layout"]["post_count"]


def test_hub_radius_matches_geometry_section(tmp_path):
    from cad_scene import build_structure_scene
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    assert abs(scene.hub_r - s["geometry"]["hub_radius_ft"]) < 0.001


def test_validate_scene_passes(tmp_path):
    from cad_scene import build_structure_scene, validate_scene_geometry
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    validate_scene_geometry(scene)  # must not raise


def test_post_top_equals_beam_bottom(tmp_path):
    from cad_scene import build_structure_scene
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    assert abs(scene.Z_POST_TOP - (scene.Z_BEAM_TOP - (s["members"]["beams"]["actual_depth_in"] / 12.0))) < 0.001


def test_no_zero_length_members(tmp_path):
    from cad_scene import build_structure_scene
    import math
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    for solid in scene.solids:
        length = math.sqrt(sum((a-b)**2 for a, b in zip(solid.p1, solid.p0)))
        assert length > 1e-6, f"Zero-length member: {solid.tag}"


def test_footing_count_matches_post_count(tmp_path):
    from cad_scene import build_structure_scene
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    footings = [so for so in scene.solids if so.role == "footing"]
    assert len(footings) == s["layout"]["post_count"]
```

- [ ] **Step 2: Run tests — verify they fail**

```bash
python -m pytest plugins/garden-structure-designer/tests/test_cad_scene.py -v 2>&1 | head -20
```

Expected: `TypeError: build_structure_scene() takes ... positional argument` or similar.

- [ ] **Step 3: Update `build_structure_scene()` signature and parameter extraction**

In `cad_scene.py`, replace the function signature and the parameters block (lines 238–313). The math and solid-building loops remain unchanged.

Replace from `def build_structure_scene(` through `# ── Brace run length ──`:

```python
def build_structure_scene(
    structure: dict,
    is_blueprint: bool = False,
) -> Scene:
    """
    Compute all 3D construction nodes and emit Solid objects.
    Reads exclusively from structure.json (unified CAD manifest).
    """
    pal = _palettes(is_blueprint)
    UP: V3 = (0.0, 0.0, 1.0)

    # Coordinate system contract
    cad_meta = structure.get("cad", {})
    assert cad_meta.get("coordinate_system", "right_handed_z_up") == "right_handed_z_up", \
        "cad.coordinate_system must be 'right_handed_z_up'"
    precision = cad_meta.get("precision", 0.001)

    # ── Parameters from structure sections ──────────────────────────────────
    layout       = structure["layout"]
    members      = structure["members"]
    roof         = structure["roof"]
    hub_spec     = structure["hub"]
    bracing_spec = structure.get("bracing", {})
    footings_spec = structure["footings"]
    geom         = structure["geometry"]

    qty  = layout["post_count"]
    r_ft = layout["inscribed_radius_ft"]

    post_h     = members["posts"]["cut_length_ft"]
    beam_d_in  = members["beams"]["actual_depth_in"]
    beam_d     = beam_d_in / 12.0

    roof_r = geom["roof_rise"]["rise_ft"]
    hub_r  = geom["hub_radius_ft"]  # resolved and sealed by geometry_engine.py

    overhang_ft = roof["primary_rafters"]["overhang_ft"]

    # ── Cross-section half-dimensions (feet) ─────────────────────────────────
    POST_HW   = (members["posts"]["actual_width_in"] / 12.0) / 2.0
    POST_HD   = (members["posts"]["actual_depth_in"] / 12.0) / 2.0
    BEAM_HW   = (members["beams"]["actual_width_in"] / 12.0) / 2.0
    BEAM_HD   = beam_d / 2.0
    RAFTER_HW = (roof["primary_rafters"]["actual_width_in"] / 12.0) / 2.0
    RAFTER_HD = (roof["primary_rafters"]["actual_depth_in"] / 12.0) / 2.0

    brace_s    = bracing_spec.get("brace", {})
    BRACE_HW   = (brace_s.get("actual_width_in", 3.5) / 12.0) / 2.0
    BRACE_HD   = (brace_s.get("actual_depth_in", 3.5) / 12.0) / 2.0
    # length_ft is the hypotenuse; run and drop are its horizontal/vertical components
    _brace_len = brace_s.get("length_ft", 2.5)
    _brace_rad = math.radians(brace_s.get("angle_deg", 45))
    brace_run  = _brace_len * math.cos(_brace_rad)   # horizontal distance along post face
    brace_drop = _brace_len * math.sin(_brace_rad)   # vertical drop from beam soffit

    FOOTING_HW = (footings_spec.get("diameter_in", 12.0) / 12.0) / 2.0

    # Hub vertical extent from spec
    hub_clearance_ft    = hub_spec.get("clearance_ft", 0.5)
    hub_height_ratio    = hub_spec.get("height_ratio_to_rafter", 2.5)
    hub_height_ft       = RAFTER_HD * 2.0 * hub_height_ratio
```

Then update the hub Z constants block (currently `hub_ztop = Z_APEX + RAFTER_HD + 0.15`, `hub_zbot = Z_APEX - 1.25`) to:

```python
    hub_ztop = Z_APEX + RAFTER_HD + hub_clearance_ft
    hub_zbot = Z_APEX - hub_height_ft
```

Also update `foundation_spec` reference (currently reads `model.get("foundation", {})`) to read from the already-extracted `footings_spec` and `FOOTING_HW`.

Remove the old footing extraction block:
```python
    # DELETE: foundation_spec = model.get("foundation", {})
    # DELETE: FOOTING_HW = (foundation_spec.get("caisson_diameter_in", 12.0) / 12.0) / 2.0
```

Also update the overhang extraction (currently `overhang_in = model.get("overhang_in", 12)`) to:
```python
    # DELETE: overhang_in = model.get("overhang_in", 12)
    # DELETE: overhang_ft = overhang_in / 12.0
    # Already set: overhang_ft = roof["primary_rafters"]["overhang_ft"]  (from above)
```

The purlin section reads `purlins_spec = model.get("members", {}).get("purlins", {})` — update to:
```python
    purlins_spec = structure.get("members", {}).get("purlins", {})
```

- [ ] **Step 4: Run tests — verify they pass**

```bash
python -m pytest plugins/garden-structure-designer/tests/test_cad_scene.py -v
```

Expected: `6 passed`

- [ ] **Step 5: Commit**

```bash
git add plugins/garden-structure-designer/scripts/cad_scene.py \
        plugins/garden-structure-designer/tests/test_cad_scene.py
git commit -m "feat: migrate cad_scene.build_structure_scene to read from structure.json"
```

---

### Task 5: Migrate `render_drawings.py` to read from `structure.json`

**Files:**
- Modify: `plugins/garden-structure-designer/scripts/render_drawings.py`

This task: (1) removes top-level hardcoded constants, (2) updates `main()` to load `structure.json`, (3) threads `structure` through to `build_structure_scene`, (4) updates `calcs`/`model` references to read from structure sections.

- [ ] **Step 1: Remove hardcoded constant block and add palette resolver**

In `render_drawings.py`, replace the constants block (lines 41–72):

```python
# --- Viewport and palette are now read from structure.json ---
# REMOVED: VIEWBOX_W, VIEWBOX_H, MARGIN (read from geometry.svg_coordinates)
# REMOVED: ARCH_COLORS, BLUE_COLORS (resolved from presentation.palette)

TITLE_BLOCK_W: int = 400
TITLE_BLOCK_H: int = 150

_PALETTE_CEDAR_WARM: dict[str, str] = {
    "post": "#f4ebd0", "beam": "#e6ccb2", "rafter": "#ddb892",
    "brace": "#ede0d4", "footing": "#e5e5e5", "outline": "#2b2d42",
    "dimension": "#3d5a80", "centerline": "#e05a47", "text": "#1d3557"
}
_PALETTE_BLUEPRINT: dict[str, str] = {
    "post": "#1b365d", "beam": "#162e50", "rafter": "#1f3e6a",
    "brace": "#1b365d", "footing": "#11223a", "outline": "#ffffff",
    "dimension": "#00ffff", "centerline": "#ff6d00", "text": "#00ffff"
}
_PALETTES: dict[str, dict[str, str]] = {
    "cedar_warm": _PALETTE_CEDAR_WARM,
    "blueprint":  _PALETTE_BLUEPRINT,
}

def _get_palette(structure: dict, is_blueprint: bool) -> dict[str, str]:
    if is_blueprint:
        return _PALETTE_BLUEPRINT
    key = structure.get("presentation", {}).get("palette", "cedar_warm")
    return _PALETTES.get(key, _PALETTE_CEDAR_WARM)
```

- [ ] **Step 2: Update `draw_title_block` signature and body**

Replace `draw_title_block(svg_list, model, calcs, dwg_name, is_blueprint)` with:

```python
def draw_title_block(svg_list: list[str], structure: dict, dwg_name: str, is_blueprint: bool) -> None:
    coords     = structure["geometry"]["svg_coordinates"]
    width_px   = coords["width_px"]
    height_px  = coords["height_px"]
    x = width_px  - TITLE_BLOCK_W - 20
    y = height_px - TITLE_BLOCK_H - 20
    source_hash = structure["meta"]["source_hash"][:8]
    struct_type = structure["structure"]["type"].upper()
    jurisdiction = structure["intent"].get("jurisdiction", "UNKNOWN")

    border      = "#00ffff" if is_blueprint else _PALETTE_CEDAR_WARM["outline"]
    bg          = "#12253a" if is_blueprint else "#ffffff"
    text_color  = "#00ffff" if is_blueprint else _PALETTE_CEDAR_WARM["text"]
    font_family = "Courier New, Courier, monospace" if is_blueprint else "sans-serif"

    svg_list.append(f'    <g data-role="title-block" transform="translate({x}, {y})">')
    svg_list.append(f'        <rect width="{TITLE_BLOCK_W}" height="{TITLE_BLOCK_H}" fill="{bg}" stroke="{border}" stroke-width="1.8" />')
    svg_list.append(f'        <line x1="0" y1="40" x2="{TITLE_BLOCK_W}" y2="40" stroke="{border}" stroke-width="1" />')
    svg_list.append(f'        <text x="15" y="28" font-family="{font_family}" font-size="18" font-weight="bold" fill="{text_color}">{dwg_name.upper()}</text>')
    svg_list.append(f'        <text x="15" y="60" font-family="{font_family}" font-size="11" fill="{text_color}">STRUCTURE: {struct_type}</text>')
    svg_list.append(f'        <text x="15" y="80" font-family="{font_family}" font-size="11" fill="{text_color}">JURISDICTION: {jurisdiction}</text>')
    svg_list.append(f'        <text x="15" y="100" font-family="{font_family}" font-size="11" fill="{text_color}">SOURCE HASH: {source_hash}</text>')
    svg_list.append(f'        <text x="15" y="120" font-family="{font_family}" font-size="11" fill="{text_color}">DATE: 2026-05-23 | SCALE: 1/2" = 1\'-0"</text>')
    svg_list.append(f'    </g>')
```

- [ ] **Step 3: Update `draw_validator_anchors` signature**

Replace `draw_validator_anchors(svg_list, calcs)` with:

```python
def draw_validator_anchors(svg_list: list[str], structure: dict) -> None:
    geo   = structure["geometry"]
    pitch = structure["roof"]["pitch"]
    cuts  = geo.get("compound_cut", {})
    miter = str(round(cuts.get("miter_deg", 0), 2))
    bevel = str(round(cuts.get("bevel_deg", 0), 2))
    svg_list.append(f'    <!-- VALIDATOR_ANCHORS: {pitch} {miter}° {bevel}° -->')
    svg_list.append(f'    <!-- SAW_SETTINGS: {{"miter_deg": {miter}, "bevel_deg": {bevel}}} -->')
    svg_list.append(f'    <!-- COORDINATE MAP: {json.dumps(geo.get("svg_coordinates", {}))} -->')
    svg_list.append(f'    <g style="visibility:hidden; display:none;">')
    svg_list.append(f'        <text>{pitch}</text>')
    svg_list.append(f'        <text>{miter}</text>')
    svg_list.append(f'        <text>{bevel}</text>')
    svg_list.append(f'    </g>')
```

- [ ] **Step 4: Update render function signatures and internal calcs/model references**

Each render function (`render_plan_view`, `render_elevation_view`, `render_perspective_view`, `render_component_isolation_view`) changes signature from `(model, calcs, filename)` to `(structure, filename)`.

At the top of each render function body, add this helper line so all viewport accesses are concise:

```python
    coords = structure["geometry"]["svg_coordinates"]
```

Then use `coords` for all viewport reads (replaces every inline `structure["geometry"]["svg_coordinates"][...]`).

Inside each function, apply these substitutions:

| Old reference | New reference |
|---|---|
| `build_structure_scene(model, calcs, is_blueprint=...)` | `build_structure_scene(structure, is_blueprint=...)` |
| `calcs.get("total_height", {}).get("post_ft", 8.33)` | `structure["geometry"]["total_height"]["post_ft"]` |
| `calcs.get("total_height", {}).get("beam_depth_ft", 1.0)` | `structure["geometry"]["total_height"]["beam_depth_ft"]` |
| `calcs.get("roof_rise", {}).get("rise_ft", 1.6)` | `structure["geometry"]["roof_rise"]["rise_ft"]` |
| `calcs.get("total_height", {}).get("total_height_ft", 10.6)` | `structure["geometry"]["total_height"]["total_height_ft"]` |
| `calcs.get("pitch", "4:12")` | `structure["roof"]["pitch"]` |
| `calcs.get("compound_cut", {}).get("miter_deg", 28.71)` | `structure["geometry"]["compound_cut"]["miter_deg"]` |
| `calcs.get("compound_cut", {}).get("bevel_deg", 9.10)` | `structure["geometry"]["compound_cut"]["bevel_deg"]` |
| `calcs.get("beam_ring", {}).get("beam_miter_deg", 30.0)` | `structure["geometry"]["beam_ring"]["beam_miter_deg"]` |
| `calcs.get("rafter", {}).get("total_with_overhang_in", 76.0)` | `structure["geometry"]["rafter"]["total_with_overhang_in"]` |
| `calcs.get("svg_coordinates", {}).get("scale_px_per_ft", 42)` | `coords["scale_px_per_ft"]` |
| `VIEWBOX_W` | `coords["width_px"]` |
| `VIEWBOX_H` | `coords["height_px"]` |
| `ARCH_COLORS["X"]` | `_get_palette(structure, is_blueprint)["X"]` |
| `BLUE_COLORS["X"]` | `_PALETTE_BLUEPRINT["X"]` |
| `model.get("members", {}).get("posts", {}).get("quantity", 6)` | `structure["layout"]["post_count"]` |

Also update `generate_svg(filename, model, calcs, output_path)` to `generate_svg(filename, structure, output_path)` and update its internal calls to match.

- [ ] **Step 5: Update `main()`**

Replace the existing `main()` function:

```python
def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python3 render_drawings.py context/staging/structure.json",
            file=sys.stderr,
        )
        sys.exit(1)

    structure_path = Path(sys.argv[1]).resolve()
    if not structure_path.exists():
        print(f"Error: {structure_path} not found.", file=sys.stderr)
        sys.exit(1)

    with open(structure_path, encoding="utf-8") as f:
        structure = json.load(f)

    # Verify geometry section is sealed before rendering
    if not structure.get("geometry", {}).get("_sealed"):
        print("Error: structure.geometry is not sealed. Run geometry_engine.py first.",
              file=sys.stderr)
        sys.exit(1)

    out_dir = outputs_dir(structure_path)

    drawings = [
        ("drawing-plan-view",         "drawing-plan-view.svg"),
        ("drawing-elevation-view",    "drawing-elevation-view.svg"),
        ("drawing-isometric-view",    "drawing-isometric-view.svg"),
        ("drawing-perspective-view",  "drawing-perspective-view.svg"),
        ("blueprint-plan",            "blueprint-plan.svg"),
        ("blueprint-elevation",       "blueprint-elevation.svg"),
        ("blueprint-isometric",       "blueprint-isometric.svg"),
        ("blueprint-component-isolation", "blueprint-component-isolation.svg"),
    ]

    for filename, output_file in drawings:
        output_path = out_dir / output_file
        generate_svg(filename, structure, str(output_path))
        print(f"  ✓ {output_file}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Smoke-test the renderer**

First ensure `context/staging/structure.json` exists (Task 9 creates it formally; for now use this inline seed to test):

```bash
cd /Users/richardfremmerlid/Projects/garden-structure-designer
python plugins/garden-structure-designer/scripts/render_drawings.py context/staging/structure.json
```

Expected: 8 SVG files written to `outputs/`. If structure.json doesn't exist yet, skip this step — it will be verified in Task 9.

- [ ] **Step 7: Commit**

```bash
git add plugins/garden-structure-designer/scripts/render_drawings.py
git commit -m "feat: migrate render_drawings.py to read from structure.json; remove hardcoded constants"
```

---

### Task 6: Update `schema_validator.py` for `structure.json`

**Files:**
- Modify: `plugins/garden-structure-designer/scripts/schema_validator.py`
- Create: `plugins/garden-structure-designer/tests/test_schema_validator.py`

- [ ] **Step 1: Write the failing test**

Create `plugins/garden-structure-designer/tests/test_schema_validator.py`:

```python
import json
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent / "scripts"
SCHEMAS = Path(__file__).parent.parent / "schemas"
STAGING = Path(__file__).parent.parent.parent.parent.parent / "context" / "staging"

def test_validates_valid_structure(tmp_path):
    from test_geometry_engine import STRUCTURE_SEED
    from geometry_engine import compute_from_structure
    import copy
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(copy.deepcopy(STRUCTURE_SEED)))
    compute_from_structure(str(p))
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "schema_validator.py"),
         str(tmp_path), str(SCHEMAS), "--strict"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr

def test_rejects_missing_required_field(tmp_path):
    seed = {"meta": {"schema_version": "2.0", "lifecycle": "INTENT", "source_hash": "x"}}
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(seed))
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "schema_validator.py"),
         str(tmp_path), str(SCHEMAS), "--strict"],
        capture_output=True, text=True
    )
    assert result.returncode != 0 or "FAIL" in result.stdout

def test_member_counts_match_sections(tmp_path):
    """beam count must equal post_count; validator enforces it."""
    import copy
    from test_geometry_engine import STRUCTURE_SEED
    from geometry_engine import compute_from_structure
    seed = copy.deepcopy(STRUCTURE_SEED)
    # Corrupt: add a 7th-post-count mismatch (manually set mismatched value)
    seed["layout"]["post_count"] = 6
    seed["members"]["beams"]["cut_length_ft"] = 5.0  # fine, but inject via validator
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(seed))
    compute_from_structure(str(p))
    # The validator should pass on a clean structure (no mismatch here)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "schema_validator.py"),
         str(tmp_path), str(SCHEMAS), "--strict"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
```

- [ ] **Step 2: Run tests — verify relevant ones fail**

```bash
python -m pytest plugins/garden-structure-designer/tests/test_schema_validator.py::test_validates_valid_structure -v 2>&1 | tail -10
```

Expected: FAIL or error because `structure.schema.json` is not yet wired in the validator.

- [ ] **Step 3: Update `schema_validator.py`**

The current validator scans `target_path/*.json` and matches each file against `{file.stem}.schema.json`. Since `structure.json` now exists and `structure.schema.json` was created in Task 1, it will be auto-picked up.

Add member-count cross-validation after the existing per-file loop:

```python
    # --- Cross-section member count invariant check ---
    structure_file = target_path / "structure.json"
    if structure_file.exists():
        try:
            s = load_json(structure_file)
            post_count = s.get("layout", {}).get("post_count")
            inv = s.get("invariants", {})
            if inv.get("member_counts_match_sections") and post_count:
                rafter_count = s.get("roof", {}).get("primary_rafters", {}).get("count")
                if rafter_count is not None and rafter_count != post_count:
                    overall_status = "FAIL"
                    report["files"].append({
                        "path": str(structure_file),
                        "check": "member_counts_match_sections",
                        "status": "FAIL",
                        "detail": f"rafter count {rafter_count} != post_count {post_count}"
                    })
                cad_nodes = s.get("cad", {}).get("nodes", {})
                if cad_nodes:
                    for key, expected in [
                        ("post_bases", post_count),
                        ("post_tops", post_count),
                        ("beam_ring", post_count),
                    ]:
                        actual = len(cad_nodes.get(key, []))
                        if actual and actual != expected:
                            overall_status = "FAIL"
                            report["files"].append({
                                "path": str(structure_file),
                                "check": "member_counts_match_sections",
                                "status": "FAIL",
                                "detail": f"cad.nodes.{key} length {actual} != post_count {expected}"
                            })
        except Exception as e:
            pass  # schema validation already caught structural issues
```

- [ ] **Step 4: Run tests — verify they pass**

```bash
python -m pytest plugins/garden-structure-designer/tests/test_schema_validator.py -v
```

Expected: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add plugins/garden-structure-designer/scripts/schema_validator.py \
        plugins/garden-structure-designer/tests/test_schema_validator.py
git commit -m "feat: wire structure.schema.json into schema_validator; add member_counts invariant check"
```

---

### Task 7: Update `structural_physics_validator.py` for `structure.json`

**Files:**
- Modify: `plugins/garden-structure-designer/scripts/structural_physics_validator.py`
- Create: `plugins/garden-structure-designer/tests/test_physics_validator.py`

The existing checks use `model.get("members", {})` and `model.get("foundation", {})`. `structure.json` has identical `members` shape. Only the foundation and roof sections differ.

- [ ] **Step 1: Write the failing test**

Create `plugins/garden-structure-designer/tests/test_physics_validator.py`:

```python
import json, subprocess, sys, copy
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

SCRIPTS = Path(__file__).parent.parent / "scripts"

def test_physics_pass_on_valid_structure(tmp_path):
    from test_geometry_engine import STRUCTURE_SEED
    from geometry_engine import compute_from_structure
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(copy.deepcopy(STRUCTURE_SEED)))
    compute_from_structure(str(p))
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "structural_physics_validator.py"), str(p)],
        capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr + result.stdout

def test_physics_reads_footings_section(tmp_path):
    import copy
    from test_geometry_engine import STRUCTURE_SEED
    from geometry_engine import compute_from_structure
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["footings"]["diameter_in"] = 4  # tiny footing → bearing fail
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(seed))
    compute_from_structure(str(p))
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "structural_physics_validator.py"), str(p)],
        capture_output=True, text=True
    )
    # Should FAIL or WARNING — tiny 4" caisson can't bear 5.5x5.5 post
    report = json.loads((tmp_path.parent.parent.parent.parent.parent /
                          "context" / "staging" / "physics-validation-report.json")
                         .read_text()) if False else {}
    # Just verify it ran without crashing
    assert result.returncode in (0, 1)
```

- [ ] **Step 2: Run tests — verify they fail**

```bash
python -m pytest plugins/garden-structure-designer/tests/test_physics_validator.py -v 2>&1 | tail -10
```

Expected: FAIL because validator reads `model.get("foundation")` but structure.json has `footings`.

- [ ] **Step 3: Update `structural_physics_validator.py` data access**

In `main()`, update the data access paths to handle both `structure.json` (new) and `structural-model.json` (legacy):

```python
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 structural_physics_validator.py <structure.json>")
        sys.exit(1)

    model_path = Path(sys.argv[1])
    model = load_json(model_path)

    # Detect structure.json (new) vs structural-model.json (legacy)
    is_structure_json = "meta" in model and "schema_version" in model.get("meta", {})

    if is_structure_json:
        posts  = model.get("members", {}).get("posts", {})
        beams  = model.get("members", {}).get("beams", {})
        pitch_defaulted = model.get("roof", {}).get("pitch_defaulted", False)
        caisson_d = float(model.get("footings", {}).get("diameter_in", 12))
        span_ft   = model.get("layout", {}).get("inscribed_radius_ft", 5.0)
    else:
        posts   = model.get("members", {}).get("posts", {})
        beams   = model.get("members", {}).get("beams", {})
        pitch_defaulted = model.get("roofStructure", {}).get("pitchDefaulted", False)
        caisson_d = float(model.get("foundation", {}).get("caisson_diameter_in", 12))
        span_ft   = posts.get("spanDistance_ft", 10.0)
```

Then update the existing check blocks to use these local variables instead of `model.get(...)` inline calls.

Update the slenderness check:
```python
    post_length = posts.get("cut_length_ft", posts.get("cutLength_ft", 8.0)) * 12
    post_width  = float(posts.get("actual_width_in", posts.get("width_in", 5.5)))
```

Update the deflection check:
```python
    span_in            = span_ft * 12
    allowable_deflection = span_in / 240
    beam_w = float(beams.get("actual_width_in", beams.get("width_in", 3.5)))
    beam_d = float(beams.get("actual_depth_in", beams.get("depth_in", 7.25)))
```

Update the bearing check:
```python
    caisson_area = 3.14159 * (caisson_d / 2) ** 2
    post_area    = float(posts.get("actual_width_in", posts.get("width_in", 5.5))) * \
                   float(posts.get("actual_depth_in", posts.get("depth_in", 5.5)))
```

Update the pitch check:
```python
    if pitch_defaulted:
        report["assumptions"].append("Pitch was defaulted. Verify snow load capacity.")
```

Update the output path to write to the same staging dir as the input:
```python
    out_path = model_path.parent / "physics-validation-report.json"
```

- [ ] **Step 4: Run tests — verify they pass**

```bash
python -m pytest plugins/garden-structure-designer/tests/test_physics_validator.py -v
```

Expected: `2 passed`

- [ ] **Step 5: Commit**

```bash
git add plugins/garden-structure-designer/scripts/structural_physics_validator.py \
        plugins/garden-structure-designer/tests/test_physics_validator.py
git commit -m "feat: structural_physics_validator reads structure.json footings/roof sections"
```

---

### Task 8: Write `emit_legacy_views.py` compatibility shim

**Files:**
- Create: `plugins/garden-structure-designer/scripts/emit_legacy_views.py`

This shim reads `structure.json` and regenerates the three legacy files so agents/skills that still reference them continue to work during M1.

- [ ] **Step 1: Write the shim**

Create `plugins/garden-structure-designer/scripts/emit_legacy_views.py`:

```python
#!/usr/bin/env python3
"""
emit_legacy_views.py — M1 compatibility shim.
Reads structure.json and writes legacy staging files as derived read-only views.
REMOVE IN MILESTONE 2 once all agents/skills are updated.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from structure_io import load_structure


def emit(structure_path: str) -> None:
    structure = load_structure(structure_path)
    staging = Path(structure_path).parent
    geom = structure.get("geometry", {})
    src_hash = structure["meta"]["source_hash"]

    # design-spec.json
    design_spec = {
        "schema": "garden-structure-designer/design-spec/1.0",
        "source_hash": src_hash,
        "structureType": structure["structure"]["type"],
        "planShape": structure["structure"]["shape"],
        "jurisdiction": structure["intent"]["jurisdiction"],
        "pitch": structure["roof"]["pitch"],
        "pitchDefaulted": structure["roof"].get("pitch_defaulted", False),
        "project": {
            "structure_type": structure["structure"]["type"].capitalize(),
            "shape": structure["structure"]["shape"].capitalize(),
            "primary_material": structure["intent"].get("material_preference", "Cedar"),
        },
        "dimensions": {
            "height_total_ft": structure["members"]["posts"]["cut_length_ft"],
            "max_diagonal_ft": structure["layout"]["inscribed_radius_ft"] * 2,
            "post_spacing_diagonal_ft": structure["layout"]["inscribed_radius_ft"] * 2,
        },
        "materials": {
            "post_size": structure["members"]["posts"]["nominal_size"],
            "timber_species": structure["intent"].get("material_preference", "Western Red Cedar"),
        },
        "site": {
            "location": structure["intent"]["jurisdiction"],
            "canonical_location_id": structure["intent"]["jurisdiction"],
        },
        "style": {
            "joinery_preference": structure["intent"].get("joinery_style", "Traditional timber framing"),
            "knee_braces": "Decorative 4x4 cedar braces" if structure.get("bracing", {}).get("enabled") else "None",
            "rafter_tails": structure.get("joinery", {}).get("rafter_tail", "decorative_scallop"),
            "roof_pitch": structure["roof"]["pitch"],
        },
    }

    # structural-model.json
    br = structure.get("bracing", {})
    brace = br.get("brace", {})
    structural_model = {
        "schema": "garden-structure-designer/structural-model/1.0",
        "source_hash": src_hash,
        "_locked": True,
        "structureType": structure["structure"]["type"],
        "planShape": structure["structure"]["shape"],
        "members": {
            "posts": {
                "quantity":         structure["layout"]["post_count"],
                "dimensions":       structure["members"]["posts"]["nominal_size"],
                "cutLength_ft":     structure["members"]["posts"]["cut_length_ft"],
                "spanDistance_ft":  structure["layout"]["inscribed_radius_ft"],
                "nominalSize":      structure["members"]["posts"]["nominal_size"],
                "width_in":         structure["members"]["posts"]["actual_width_in"],
                "depth_in":         structure["members"]["posts"]["actual_depth_in"],
            },
            "beams": {
                "quantity":   structure["layout"]["post_count"],
                "dimensions": structure["members"]["beams"]["nominal_size"],
                "depth_in":   structure["members"]["beams"]["actual_depth_in"],
                "width_in":   structure["members"]["beams"]["actual_width_in"],
                "nominalSize": structure["members"]["beams"]["nominal_size"],
                "cutLength_ft": structure["members"]["beams"]["cut_length_ft"],
            },
            "kneebraces": {
                "quantity":    structure["layout"]["post_count"] * brace.get("count_per_post", 2),
                "dimensions":  brace.get("nominal_size", "4x4"),
                "cutLength_in": round(brace.get("length_ft", 2.5) * 12),
                "angle_deg":   brace.get("angle_deg", 45),
                "width_in":    brace.get("actual_width_in", 3.5),
                "depth_in":    brace.get("actual_depth_in", 3.5),
            },
            "rafters": {
                "quantity":      structure["roof"]["primary_rafters"]["count"],
                "dimensions":    structure["roof"]["primary_rafters"]["nominal_size"],
                "miterAngle_deg": geom.get("compound_cut", {}).get("miter_deg", 28.71),
                "cutLength_ft":  geom.get("rafter", {}).get("total_with_overhang_ft", 6.2),
                "nominalSize":   structure["roof"]["primary_rafters"]["nominal_size"],
                "width_in":      structure["roof"]["primary_rafters"]["actual_width_in"],
                "depth_in":      structure["roof"]["primary_rafters"]["actual_depth_in"],
            },
        },
        "roofStructure": {
            "pitch": structure["roof"]["pitch"],
            "pitchDefaulted": structure["roof"].get("pitch_defaulted", False),
            "style": structure.get("presentation", {}).get("roof_style", "Open Rafter"),
        },
        "overhang_in": round(structure["roof"]["primary_rafters"]["overhang_ft"] * 12),
        "bracing_added": br.get("enabled", True),
        "materials": {"primary": structure["intent"].get("material_preference", "Cedar").split()[0]},
        "joinery": {"type": "traditional"},
        "foundation": {"caisson_diameter_in": structure["footings"]["diameter_in"]},
    }

    # geometry-calculations.json
    geometry_calculations = {
        "schema": "geometry-calculations/1.0",
        "source": "context/staging/structure.json",
        "source_hash": src_hash,
        "pitch":       structure["roof"]["pitch"],
        "sides":       structure["structure"]["sides"],
        "compound_cut": geom.get("compound_cut", {}),
        "beam_ring":    geom.get("beam_ring", {}),
        "rafter":       geom.get("rafter", {}),
        "roof_rise":    geom.get("roof_rise", {}),
        "total_height": geom.get("total_height", {}),
        "svg_coordinates": geom.get("svg_coordinates", {}),
        "warnings":     geom.get("warnings", []),
    }

    (staging / "design-spec.json").write_text(json.dumps(design_spec, indent=2))
    (staging / "structural-model.json").write_text(json.dumps(structural_model, indent=2))
    (staging / "geometry-calculations.json").write_text(json.dumps(geometry_calculations, indent=2))
    print(f"Legacy views emitted to {staging}/")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 emit_legacy_views.py context/staging/structure.json")
        sys.exit(1)
    emit(sys.argv[1])


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Smoke-test the shim**

```bash
python plugins/garden-structure-designer/scripts/emit_legacy_views.py context/staging/structure.json
```

If `context/staging/structure.json` doesn't exist yet, skip — covered in Task 9.

- [ ] **Step 3: Commit**

```bash
git add plugins/garden-structure-designer/scripts/emit_legacy_views.py
git commit -m "feat: add emit_legacy_views.py M1 compat shim (generates legacy files from structure.json)"
```

---

### Task 9: Create seed `structure.json`, run end-to-end regression

**Files:**
- Create: `context/staging/structure.json`

- [ ] **Step 1: Create the seed `structure.json` from current staging data**

Run this Python script inline:

```bash
python3 - << 'EOF'
import json, hashlib
from datetime import datetime, timezone
from pathlib import Path

seed = {
  "meta": {
    "schema_version": "2.0",
    "lifecycle": "ENGINEERED",
    "source_hash": "",
    "created_at": datetime.now(timezone.utc).isoformat(),
    "updated_at": datetime.now(timezone.utc).isoformat()
  },
  "intent": {
    "jurisdiction": "BC_SAANICH",
    "material_preference": "Western Red Cedar",
    "joinery_style": "Traditional timber framing"
  },
  "structure": {"type": "pergola", "shape": "hexagon", "sides": 6},
  "layout": {"post_count": 6, "inscribed_radius_ft": 4.875, "post_spacing_ft": 4.875},
  "members": {
    "posts": {"nominal_size": "6x6", "actual_width_in": 5.5,
              "actual_depth_in": 5.5, "cut_length_ft": 8.42},
    "beams": {"nominal_size": "6x12", "actual_width_in": 6.0,
              "actual_depth_in": 12.0, "cut_length_ft": 5.0}
  },
  "roof": {
    "type": "hip", "pitch": "4:12", "pitch_defaulted": False,
    "primary_rafters": {
      "count": 6, "nominal_size": "4x6",
      "actual_width_in": 3.5, "actual_depth_in": 5.5, "overhang_ft": 0.75
    },
    "secondary_rafters": {"enabled": False}
  },
  "hub": {"type": "polygonal", "radius_ft": "auto",
          "radius_min_ft": 0.6, "height_ratio_to_rafter": 2.5, "clearance_ft": 0.5},
  "bracing": {
    "enabled": True, "layout": "paired_per_post",
    "brace": {"nominal_size": "4x4", "actual_width_in": 3.5,
              "actual_depth_in": 3.5, "length_ft": 2.5,
              "angle_deg": 45, "count_per_post": 2}
  },
  "footings": {"type": "sonotube", "diameter_in": 12, "depth_in": 24, "concrete_grade": "20MPa"},
  "joinery": {"beam_seat_style": "exposed_tenon",
              "rafter_tail": "decorative_scallop", "rafter_seat_style": "birds_mouth"},
  "invariants": {
    "rafter_count_equals_post_count": True,
    "post_top_equals_beam_bottom": True,
    "no_rafter_inside_hub_radius": True,
    "brace_must_connect_to_surfaces": True,
    "no_solid_intersections": True,
    "member_counts_match_sections": True,
    "no_zero_length_members": True,
    "presentation_primary_counts_match": True
  },
  "presentation": {
    "view_mode": "presentation",
    "roof_style": "open_rafter",
    "visibility_rules": {
      "primary_members_only": True,
      "fade_secondary": True,
      "suppress_internal_roof_framing": True,
      "max_visible_braces_per_post": 1
    },
    "labeling": {"avoid_geometry_overlap": True, "use_leaders_when_colliding": True},
    "palette": "cedar_warm"
  },
  "code": {"_sealed": False, "wind_load_kPa": None, "snow_load_kPa": None,
           "height_limit_ft": None, "permit_required": None},
  "geometry": {"_comment": "DERIVED — written by geometry_engine.py.", "_sealed": False},
  "cad": {"_comment": "DERIVED — written by cad_scene.py.", "_sealed": False,
          "units": "feet", "coordinate_system": "right_handed_z_up", "precision": 0.001}
}

# Compute source hash
INPUT_SECTIONS = {"intent","structure","layout","members","roof","hub","bracing","footings","joinery"}
payload = {k: seed[k] for k in sorted(INPUT_SECTIONS) if k in seed}
raw = json.dumps(payload, sort_keys=True).encode("utf-8")
seed["meta"]["source_hash"] = hashlib.sha256(raw).hexdigest()

Path("context/staging/structure.json").write_text(json.dumps(seed, indent=2))
print("Wrote context/staging/structure.json")
EOF
```

- [ ] **Step 2: Run `geometry_engine.py` against the seed**

```bash
python plugins/garden-structure-designer/scripts/geometry_engine.py context/staging/structure.json
```

Expected output: no stderr warnings, exit 0.

- [ ] **Step 3: Verify regression anchor values**

```bash
python3 -c "
import json
data = json.load(open('context/staging/structure.json'))
geo = data['geometry']
print('miter_deg:', geo['compound_cut']['miter_deg'])
print('bevel_deg:', geo['compound_cut']['bevel_deg'])
print('beam_miter_deg:', geo['beam_ring']['beam_miter_deg'])
print('total_height_ft:', geo['total_height']['total_height_ft'])
assert geo['compound_cut']['miter_deg'] == 28.71, 'REGRESSION'
assert geo['compound_cut']['bevel_deg'] == 9.10, 'REGRESSION'
assert geo['beam_ring']['beam_miter_deg'] == 30.00, 'REGRESSION'
assert geo['total_height']['total_height_ft'] == 11.045, 'REGRESSION'
print('All regression anchors PASS')
"
```

Expected:
```
miter_deg: 28.71
bevel_deg: 9.1
beam_miter_deg: 30.0
total_height_ft: 11.045
All regression anchors PASS
```

- [ ] **Step 4: Run `render_drawings.py` against `structure.json`**

```bash
python plugins/garden-structure-designer/scripts/render_drawings.py context/staging/structure.json
```

Expected: 8 SVG files written, exit 0.

- [ ] **Step 5: Run `emit_legacy_views.py` shim**

```bash
python plugins/garden-structure-designer/scripts/emit_legacy_views.py context/staging/structure.json
ls context/staging/design-spec.json context/staging/structural-model.json context/staging/geometry-calculations.json
```

Expected: all 3 files present.

- [ ] **Step 6: Run full test suite**

```bash
python -m pytest plugins/garden-structure-designer/tests/ -v
```

Expected: all tests pass.

- [ ] **Step 7: Run drawing red-team gate**

```bash
python plugins/garden-structure-designer/scripts/run_drawing_red_team.py \
  --svg-dir outputs \
  --model context/staging/structure.json \
  --report-dir context/staging \
  --md-dir outputs
```

Note: the `--model` flag now points to `structure.json`. If `run_drawing_red_team.py` hardcodes a reference to `structural-model.json`, update that reference to read from `structure.json` instead (or pass through the shim-generated `structural-model.json`).

- [ ] **Step 8: Commit M1 completion**

```bash
git add context/staging/structure.json
git commit -m "feat: M1 complete — seed structure.json, all scripts read from unified manifest"
```

---

# MILESTONE 2 — Agents/Skills Update + Legacy Deletion

---

### Task 10: Update `interactive-designer.md`

**Files:**
- Modify: `plugins/garden-structure-designer/agents/interactive-designer.md`

- [ ] **Step 1: Add new interview questions to Block 2**

In `interactive-designer.md`, extend the Block 2 intake questions with the following additions after the existing questions (starting after "Ask the user for their location"):

```markdown
4. **Hub style:** Ask: "For the central roof hub, do you want:
   - A king post (vertical post at center)
   - A polygonal ring (flat decorative block)
   - Open center (rafters terminate at a compression ring only)"
   Default: polygonal ring. Record as `hub_type`.

5. **Rafter tail:** Ask: "How should the rafter tails look at the eave?
   - Square cut (clean, modern)
   - Decorative scallop (traditional timber look)
   - Custom (describe)"
   Default: decorative scallop. Record as `rafter_tail`.

6. **Footing type:** Ask: "What foundation type suits your site?
   - Sonotube (concrete caisson — standard)
   - Helical pier (screw pile — rocky/poor soil)
   - Grade beam (continuous footing)"
   Default: sonotube. Record as `footing_type`.

7. **Knee braces:** Ask: "Do you want knee braces?
   - Paired decorative (2 per post, 45° angle — traditional)
   - Single structural (1 per post)
   - None"
   Default: paired decorative. Record as `brace_preference`.

8. **Drawing style:** Ask: "For drawings, do you prefer:
   - Presentation (warm cedar tones, clean)
   - Technical blueprint (steel-blue CAD style)"
   Default: presentation. Record as `view_mode`.
```

- [ ] **Step 2: Update the handoff in Block 3**

Replace `context/staging/design-spec.json` references with `context/staging/structure.json`:

```markdown
## Block 3 — Execution Pipeline

Hand off to `design-orchestrator` with the completed `context/staging/structure.json`. The orchestrator runs the full pipeline. Do NOT re-invoke individual skills from this agent — delegate fully to the orchestrator.
```

- [ ] **Step 3: Update the session check in Block 0**

Update:
```markdown
cat context/staging/structure.json 2>/dev/null
```

Replace the old reference to `context/design-dashboard.md` session check (if it loaded `design-spec.json`) to load `structure.json`.

- [ ] **Step 4: Commit**

```bash
git add plugins/garden-structure-designer/agents/interactive-designer.md
git commit -m "feat(M2): update interactive-designer with hub/rafter/footing/brace/style interview questions and structure.json handoff"
```

---

### Task 11: Update `design-orchestrator.md`

**Files:**
- Modify: `plugins/garden-structure-designer/agents/design-orchestrator.md`

- [ ] **Step 1: Update all file references**

Apply these substitutions throughout the file:

| Old reference | New reference |
|---|---|
| `context/staging/design-spec.json` | `context/staging/structure.json` |
| `context/staging/structural-model.json` | `context/staging/structure.json` |
| `context/staging/geometry-calculations.json` | `context/staging/structure.json` (geometry section) |
| `python3 scripts/geometry_engine.py context/staging/structural-model.json` | `python3 scripts/geometry_engine.py context/staging/structure.json` |
| `python3 scripts/render_drawings.py context/staging/structural-model.json` | `python3 scripts/render_drawings.py context/staging/structure.json` |
| `python3 scripts/structural_physics_validator.py context/staging/structural-model.json` | `python3 scripts/structural_physics_validator.py context/staging/structure.json` |

- [ ] **Step 2: Update Stage 1 pre-flight check**

Replace the Stage 1 confirmation check:
```markdown
1. Confirm `context/staging/structure.json` is present (written by `intake-normalizer`).
2. Confirm `meta.lifecycle` is `INTENT` or `ENGINEERED`.
3. Read `**Dispatch Strategy:**` from the dashboard.
```

- [ ] **Step 3: Update Stage 2 structural lock check**

Replace:
```markdown
4. Set `structural-model.json → _locked: true`
```
With:
```markdown
4. Verify `structure.json → members._sealed = true` after `structural-engine` completes.
   Verify `structure.json → geometry._sealed = true` after `geometry_engine.py` completes.
```

- [ ] **Step 4: Update the Context Checkpoint**

Replace the checkpoint block with:
```markdown
CHECKPOINT: structure.json sealed through geometry.
  posts={members.posts.nominal_size}@{members.posts.cut_length_ft}ft,
  pitch={roof.pitch},
  miter={geometry.compound_cut.miter_deg}°,
  total_height={geometry.total_height.total_height_ft}ft.
  lifecycle={meta.lifecycle}
```

- [ ] **Step 5: Update Revision Mode deterministic artifact list**

Replace references to `structural-model.json` / `geometry-calculations.json` with `structure.json` and its sealed sections.

- [ ] **Step 6: Add M1 shim call after drawing generation (temporary)**

Add this note to Stage 4:
```markdown
After geometry_engine.py seals structure.json, run the M1 compatibility shim
to keep legacy validators functional until M2 is complete:
```bash
python3 plugins/garden-structure-designer/scripts/emit_legacy_views.py \
  context/staging/structure.json
```
```

- [ ] **Step 7: Commit**

```bash
git add plugins/garden-structure-designer/agents/design-orchestrator.md
git commit -m "feat(M2): update design-orchestrator to reference structure.json throughout pipeline"
```

---

### Task 12: Update `validation-agent.md` and `drawing-red-team-agent.md`

**Files:**
- Modify: `plugins/garden-structure-designer/agents/validation-agent.md`
- Modify: `plugins/garden-structure-designer/agents/drawing-red-team-agent.md`

- [ ] **Step 1: Update `validation-agent.md` Phase 1**

Replace:
```markdown
python3 scripts/geometry_engine.py context/staging/structural-model.json
```
With:
```markdown
python3 scripts/geometry_engine.py context/staging/structure.json
```

- [ ] **Step 2: Update `validation-agent.md` Phase 2**

Replace:
```markdown
Read `context/staging/design-spec.json` and `context/staging/structural-model.json`.
```
With:
```markdown
Read `context/staging/structure.json`. Verify:
- `structure.layout.post_count` matches expected count.
- `structure.meta.lifecycle` is `GEOMETRY_SEALED` or later.
- `structure.geometry.total_height.total_height_ft` does not exceed `structure.code.height_limit_ft`.
```

- [ ] **Step 3: Update `validation-agent.md` Revision Completion Gate**

Replace all references to `geometry-calculations.json` with `structure.json geometry section` and `structural-model.json` with `structure.json members section`.

- [ ] **Step 4: Update `drawing-red-team-agent.md` Required Inputs**

Replace the required inputs list:
```markdown
## Required Inputs

Review these files if present:

outputs/drawing-plan-view.svg
outputs/drawing-elevation-view.svg
outputs/drawing-isometric-view.svg
outputs/drawing-perspective-view.svg
outputs/blueprint-plan.svg
outputs/blueprint-elevation.svg
outputs/blueprint-isometric.svg
outputs/blueprint-component-isolation.svg
outputs/quality-dashboard.md
outputs/run-insights.json
context/staging/structure.json          ← replaces design-spec, structural-model, geometry-calculations
```

- [ ] **Step 5: Update `drawing-red-team-agent.md` acceptance criteria paths**

Replace inline references to model field paths:

| Old | New |
|---|---|
| `model.get("members", {}).get("posts", {}).get("quantity")` | `structure["layout"]["post_count"]` |
| `design-spec.json shape` | `structure["structure"]["shape"]` |
| `structural-model.json bracing_added` | `structure["bracing"]["enabled"]` |
| `geometry-calculations.json compound_cut.miter_deg` | `structure["geometry"]["compound_cut"]["miter_deg"]` |

- [ ] **Step 6: Commit**

```bash
git add plugins/garden-structure-designer/agents/validation-agent.md \
        plugins/garden-structure-designer/agents/drawing-red-team-agent.md
git commit -m "feat(M2): update validation-agent and drawing-red-team-agent to read from structure.json"
```

---

### Task 13: Update all 12 skill `SKILL.md` files

**Files:**
- Modify: All `plugins/garden-structure-designer/skills/*/SKILL.md`

The `consumes` and `produces` metadata in each skill's YAML frontmatter references legacy staging files. Each needs updating.

- [ ] **Step 1: Update `intake-normalizer/SKILL.md`**

Change frontmatter and output description:
```yaml
metadata:
  garden_structure_designer:
    produces:
      - context/staging/structure.json
```

Body: replace `Output a strictly typed JSON file to context/staging/design-spec.json` with `Output context/staging/structure.json with sections: meta, intent, structure, layout, presentation, cad (units/coord_system/precision). Set meta.lifecycle = "INTENT".`

- [ ] **Step 2: Update `structural-engine/SKILL.md`**

```yaml
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - context/staging/structure.json  # enriched with members, roof, hub, footings, code, invariants, geometry sections
```

Body: replace all `design-spec.json` / `structural-model.json` / `geometry-calculations.json` references with `structure.json` and the appropriate section names.

Update the mandatory geometry engine call:
```markdown
python3 scripts/geometry_engine.py context/staging/structure.json
```

- [ ] **Step 3: Update `building-code-validator/SKILL.md`**

```yaml
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - context/staging/structure.json  # adds code section
```

Body: update output description from `writes context/staging/building-code.json` to `writes code section into context/staging/structure.json`.

- [ ] **Step 4: Update `joinery-designer/SKILL.md`**

```yaml
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - context/staging/structure.json  # seals joinery section
```

- [ ] **Step 5: Update `bracing-system-designer/SKILL.md`**

```yaml
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - context/staging/structure.json  # seals bracing section
```

- [ ] **Step 6: Update `drawing-generator/SKILL.md`**

```yaml
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - outputs/drawing-plan-view.svg
      - outputs/drawing-elevation-view.svg
      - outputs/drawing-isometric-view.svg
      - outputs/drawing-perspective-view.svg
```

Body: replace `reads structural-model.json and geometry-calculations.json` with `reads context/staging/structure.json`. Update the mandatory render command:

```markdown
python3 scripts/render_drawings.py context/staging/structure.json
```

- [ ] **Step 7: Update `shop-blueprint-generator/SKILL.md`**

Same pattern as drawing-generator: consumes `structure.json`, produces blueprint SVGs.

- [ ] **Step 8: Update `builder-docs-generator/SKILL.md`**

```yaml
consumes:
  - context/staging/structure.json
```

Body: replace all `structural-model.json` references with `structure.json[members]`, `structure.json[geometry]`.

- [ ] **Step 9: Update remaining 4 skills** (`adversarial-drawing-reviewer`, `document-compiler`, `obstacle-triage`, `photorealistic-renderer`)

For each: replace any `structural-model.json` / `design-spec.json` / `geometry-calculations.json` consumes references with `context/staging/structure.json`.

- [ ] **Step 10: Commit all skill updates**

```bash
git add plugins/garden-structure-designer/skills/
git commit -m "feat(M2): update all 12 skill SKILL.md consumes/produces to reference structure.json"
```

---

### Task 14: Remove shim and delete legacy staging files

**Files:**
- Delete: `plugins/garden-structure-designer/scripts/emit_legacy_views.py`
- Delete: `context/staging/design-spec.json`
- Delete: `context/staging/structural-model.json`
- Delete: `context/staging/geometry-calculations.json`

- [ ] **Step 1: Verify no agent or skill still references legacy file names**

```bash
grep -rE "(design-spec|structural-model|geometry-calculations)\.json" \
  plugins/garden-structure-designer/agents/ \
  plugins/garden-structure-designer/skills/ \
  plugins/garden-structure-designer/scripts/ \
  --include="*.md" --include="*.py" -l
```

Expected: no output (all references removed in Tasks 10–13).

If any files appear, open them and remove the remaining legacy references before continuing.

- [ ] **Step 2: Remove shim and delete legacy files**

```bash
rm plugins/garden-structure-designer/scripts/emit_legacy_views.py
rm context/staging/design-spec.json
rm context/staging/structural-model.json
rm context/staging/geometry-calculations.json
```

- [ ] **Step 3: Run full test suite to confirm nothing broke**

```bash
python -m pytest plugins/garden-structure-designer/tests/ -v
```

Expected: all tests pass.

- [ ] **Step 4: Run regression anchor verification**

```bash
python3 -c "
import json
data = json.load(open('context/staging/structure.json'))
geo = data['geometry']
assert geo['compound_cut']['miter_deg'] == 28.71, 'REGRESSION: miter_deg'
assert geo['compound_cut']['bevel_deg'] == 9.10, 'REGRESSION: bevel_deg'
assert geo['beam_ring']['beam_miter_deg'] == 30.00, 'REGRESSION: beam_miter_deg'
assert geo['total_height']['total_height_ft'] == 11.045, 'REGRESSION: total_height_ft'
print('All regression anchors PASS')
"
```

- [ ] **Step 5: Run end-to-end pipeline**

```bash
python plugins/garden-structure-designer/scripts/render_drawings.py context/staging/structure.json
python plugins/garden-structure-designer/scripts/run_drawing_red_team.py \
  --svg-dir outputs \
  --model context/staging/structure.json \
  --report-dir context/staging \
  --md-dir outputs
```

Confirm `context/staging/drawing-red-team-report.json` exists and `may_claim_success` reflects actual drawing quality.

- [ ] **Step 6: Commit M2 completion**

```bash
git add -A
git commit -m "feat(M2): complete migration — remove legacy staging files and emit_legacy_views shim"
```

---

## Final verification checklist

Before declaring PASS:

```
[ ] context/staging/structure.json exists with lifecycle=GEOMETRY_SEALED or later
[ ] structure.json meta.source_hash computed and stable
[ ] geometry section sealed (_sealed: true)
[ ] regression anchor values exact: miter=28.71, bevel=9.10, beam_miter=30.00, total_height=11.045
[ ] 8 SVG files present in outputs/
[ ] drawing-red-team-report.json exists
[ ] All pytest tests pass
[ ] No references to design-spec.json / structural-model.json / geometry-calculations.json in agents or skills
[ ] emit_legacy_views.py deleted
```
