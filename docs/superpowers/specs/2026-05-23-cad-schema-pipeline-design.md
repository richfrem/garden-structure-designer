# CAD Schema Pipeline Design
**Date:** 2026-05-23  
**Branch:** feature/v1.3.3-cad-roof-footings-fixes  
**Status:** APPROVED — ready for implementation planning

---

## Problem statement

The current pipeline uses three separate JSON files (`design-spec.json`, `structural-model.json`, `geometry-calculations.json`) that do not capture all design parameters. Geometry constants (hub size, footing depth, rafter tail style, view filtering rules) are hardcoded in `render_drawings.py` and `cad_scene.py`. Changing any geometry requires editing Python, not data.

**Goal:** Replace the three-file staging model with a single canonical `context/staging/structure.json` that is the sole input to the CAD engine. Every geometric decision must be derivable from `structure.json`. No fallback constants are allowed in rendering scripts.

---

## Decision

**Approach B — Sealed progressive manifest**, with domain-driven section grouping.

`structure.json` starts sparse after the interview and is progressively enriched by each pipeline stage. Sections are sealed with `_sealed: true` after their owning stage completes. Sealed sections are immutable — any downstream write attempt is a hard pipeline error.

The `presentation` section is **never sealed** — it can be mutated at any time to trigger a re-render without a structural re-run.

---

## Lifecycle states

```
EMPTY → INTENT → ENGINEERED → GEOMETRY_SEALED → CAD_SEALED → RENDERED
```

The `meta.lifecycle` field tracks the current state. Validators enforce that stages do not run out of order.

---

## Canonical schema — `context/staging/structure.json`

```json
{
  "meta": {
    "schema_version": "2.0",
    "lifecycle": "INTENT",
    "source_hash": "<sha256 of intent+structure+layout+members+roof+hub+bracing+footings+joinery>",
    "created_at": "<ISO8601>",
    "updated_at": "<ISO8601>"
  },

  "intent": {
    "jurisdiction": "BC_SAANICH",
    "material_preference": "Western Red Cedar",
    "joinery_style": "Traditional timber framing",
    "session_id": "<uuid>"
  },

  "structure": {
    "type": "pergola",
    "shape": "hexagon",
    "sides": 6
  },

  "layout": {
    "post_count": 6,
    "inscribed_radius_ft": 4.875,
    "post_spacing_ft": 4.875
  },

  "members": {
    "posts": {
      "nominal_size": "6x6",
      "actual_width_in": 5.5,
      "actual_depth_in": 5.5,
      "cut_length_ft": 8.42
    },
    "beams": {
      "nominal_size": "6x12",
      "actual_width_in": 6.0,
      "actual_depth_in": 12.0,
      "cut_length_ft": 5.0
    }
  },

  "roof": {
    "type": "hip",
    "pitch": "4:12",
    "pitch_defaulted": false,
    "primary_rafters": {
      "count": 6,
      "nominal_size": "4x6",
      "actual_width_in": 3.5,
      "actual_depth_in": 5.5,
      "overhang_ft": 0.75
    },
    "secondary_rafters": {
      "enabled": false
    }
  },

  "hub": {
    "type": "polygonal",
    "radius_ft": "auto",
    "radius_min_ft": 0.6,
    "height_ratio_to_rafter": 2.5,
    "clearance_ft": 0.5
  },

  "bracing": {
    "enabled": true,
    "layout": "paired_per_post",
    "brace": {
      "nominal_size": "4x4",
      "actual_width_in": 3.5,
      "actual_depth_in": 3.5,
      "length_ft": 2.5,
      "angle_deg": 45,
      "count_per_post": 2
    }
  },

  "footings": {
    "type": "sonotube",
    "diameter_in": 12,
    "depth_in": 24,
    "concrete_grade": "20MPa"
  },

  "joinery": {
    "beam_seat_style": "exposed_tenon",
    "rafter_tail": "decorative_scallop",
    "rafter_seat_style": "birds_mouth"
  },

  "invariants": {
    "rafter_count_equals_post_count": true,
    "post_top_equals_beam_bottom": true,
    "no_rafter_inside_hub_radius": true,
    "brace_must_connect_to_surfaces": true
  },

  "presentation": {
    "view_mode": "presentation",
    "roof_style": "open_rafter",
    "visibility_rules": {
      "primary_members_only": true,
      "fade_secondary": true,
      "suppress_internal_roof_framing": true,
      "max_visible_braces_per_post": 1
    },
    "labeling": {
      "avoid_geometry_overlap": true,
      "use_leaders_when_colliding": true
    },
    "palette": "cedar_warm"
  },

  "code": {
    "_sealed": false,
    "wind_load_kPa": null,
    "snow_load_kPa": null,
    "height_limit_ft": null,
    "permit_required": null
  },

  "geometry": {
    "_sealed": false
  },

  "cad": {
    "_sealed": false,
    "units": "feet",
    "coordinate_system": "right_handed_z_up",
    "precision": 0.001
  }
}
```

### Hub `radius_ft: "auto"` resolution rule

When `radius_ft` is `"auto"`, `geometry_engine.py` computes:

```
rafter_half_width = actual_width_in / 2 / 12   (ft)
hub_radius = max(radius_min_ft, rafter_half_width * sides * 0.5 / π + tolerance)
```

The resolved value is written into `geometry.hub_radius_ft` (sealed). The `hub.radius_ft = "auto"` marker is preserved in the input section to indicate it was computed, not user-specified.

---

## Section ownership and sealing rules

| Section | Written by | Sealed at | Mutable after seal |
|---|---|---|---|
| `meta` | all stages (lifecycle/timestamp) | **Never** | Yes — `lifecycle` and `updated_at` update each stage; `source_hash` must not change after Stage 1 |
| `intent` | `intake-normalizer` | Stage 1 | No |
| `structure` | `intake-normalizer` | Stage 1 | No |
| `layout` | `intake-normalizer` | Stage 1 | No |
| `members` | `structural-engine` | Stage 2 | No |
| `roof` | `structural-engine` | Stage 2 | No |
| `hub` | `structural-engine` | Stage 2 | No |
| `footings` | `structural-engine` | Stage 2 | No |
| `code` | `building-code-validator` | Stage 2 | No |
| `bracing` | `bracing-system-designer` | Stage 3 | No |
| `joinery` | `joinery-designer` | Stage 3 | No |
| `invariants` | `structural-engine` | Stage 2 | No |
| `geometry` | `geometry_engine.py` | Stage 2 | No |
| `cad` | `intake-normalizer` writes `units/coordinate_system/precision`; `cad_scene.py` writes `nodes` | Stage 4 (after `nodes` written) | No |
| `presentation` | `intake-normalizer` (initial) | **Never** | Yes — triggers re-render only |

---

## `geometry` section — full shape (sealed by `geometry_engine.py`)

```json
"geometry": {
  "_sealed": true,
  "compound_cut": {
    "miter_deg": 28.71,
    "bevel_deg": 9.10,
    "pitch_angle_deg": 18.43,
    "plan_half_angle_deg": 30.0
  },
  "beam_ring": {
    "beam_miter_deg": 30.0,
    "interior_angle_deg": 120.0
  },
  "rafter": {
    "structural_length_ft": 5.139,
    "total_with_overhang_ft": 6.193,
    "total_with_overhang_in": 74.31
  },
  "roof_rise": {
    "rise_ft": 1.625,
    "rise_in": 19.5
  },
  "total_height": {
    "post_ft": 8.42,
    "beam_depth_ft": 1.0,
    "roof_rise_ft": 1.625,
    "total_height_ft": 11.045,
    "total_height_in": 132.54
  },
  "hub_radius_ft": 0.65,
  "svg_coordinates": {
    "viewBox": "0 0 1100 900",
    "width_px": 1100,
    "height_px": 900,
    "grade_y": 780,
    "scale_px_per_ft": 42.0,
    "post_top_y": 426,
    "beam_soffit_y": 426,
    "beam_top_y": 384,
    "hub_apex_y": 316
  },
  "warnings": []
}
```

---

## `cad` section — full shape (sealed by `cad_scene.py`)

```json
"cad": {
  "_sealed": true,
  "units": "feet",
  "coordinate_system": "right_handed_z_up",
  "precision": 0.001,
  "nodes": {
    "post_bases": [[x, y, 0.0], ...],
    "post_tops": [[x, y, post_z], ...],
    "beam_ring": [[x, y, beam_z], ...],
    "hub_center": [0.0, 0.0, hub_z],
    "hub_apex": [0.0, 0.0, apex_z],
    "rafter_roots": [[x, y, beam_z], ...],
    "rafter_tips": [[x, y, beam_z], ...],
    "brace_starts": [[x, y, z], ...],
    "brace_ends": [[x, y, z], ...]
  }
}
```

---

## Script contracts

### `geometry_engine.py`

- **Input:** `context/staging/structure.json`
- **Reads:** `structure`, `layout`, `members`, `roof`, `hub`, `footings`
- **Writes:** `geometry` section into `structure.json`, sets `geometry._sealed = true`
- **Resolves:** `hub.radius_ft: "auto"` → writes resolved value to `geometry.hub_radius_ft`
- **Enforces:** all `invariants` that are checkable at this stage
- **Zero hardcoded geometry constants** — all values derived from input sections
- **Exit 0** with no warnings, or **exit 1** with `geometry.warnings` populated

### `cad_scene.py`

- **Input:** `context/staging/structure.json`
- **Reads:** `structure`, `layout`, `members`, `roof`, `hub`, `bracing`, `footings`, `geometry`
- **Writes:** `cad.nodes` into `structure.json`, sets `cad._sealed = true`
- **Zero hardcoded 3D coordinates** — all node positions derived from `geometry` values
- **Enforces:** `invariants.no_rafter_inside_hub_radius`, `invariants.brace_must_connect_to_surfaces`

### `render_drawings.py`

- **Input:** `context/staging/structure.json`
- **Reads:** ALL sections — uses `geometry` for coordinates, `cad` for 3D nodes, `presentation` for visibility/palette
- **Zero hardcoded geometry constants** — `SCALE_PX_PER_FT`, `GRADE_Y`, hub size, footing depth, brace geometry all come from `structure.json`
- **Zero hardcoded color constants** — palette resolved from `presentation.palette` lookup table
- **Respects `presentation.visibility_rules`** — applies member filtering before rendering any sheet
- **Respects `presentation.labeling`** — runs leader collision detection if `use_leaders_when_colliding: true`

### `schema_validator.py`

- Validates `structure.json` against `plugins/garden-structure-designer/schemas/structure.schema.json` (new file)
- Enforces sealed section immutability across consecutive runs
- Validates lifecycle state transitions

---

## Agent contract updates

### `interactive-designer`

Must capture (in addition to current questions):
- Hub style preference: king post, polygonal ring, open center
- Rafter tail profile: square cut, decorative scallop, custom
- Footing type: sonotube, helical pier, grade beam
- Knee brace preference: decorative paired, structural single, none
- Desired view mode for drawings: presentation vs. technical

All captured values are passed to `intake-normalizer` as part of the session transcript.

### `intake-normalizer`

- **Writes** `meta`, `intent`, `structure`, `layout`, `presentation` into `structure.json`
- **Does not** write `members`, `roof`, `hub`, `bracing`, `footings`, `geometry`, `cad` — those are downstream
- Seals `meta`, `intent`, `structure`, `layout` after writing
- Sets `meta.lifecycle = "INTENT"`

### `structural-engine`

- **Reads** `structure.json` (intent, structure, layout sections)
- **Writes** `members`, `roof`, `hub`, `footings`, `code`, `invariants` into `structure.json`
- **Calls** `geometry_engine.py context/staging/structure.json` which seals `geometry`
- **Does not** write to `geometry` directly — only via the engine
- Sets `meta.lifecycle = "ENGINEERED"` after members are written
- Sets `meta.lifecycle = "GEOMETRY_SEALED"` after `geometry_engine.py` completes

### `design-orchestrator`

All file references updated: `design-spec.json` → `structure.json["intent"]`, `structural-model.json` → `structure.json["members"]`, `geometry-calculations.json` → `structure.json["geometry"]`.

The context checkpoint after Stage 3 reads from `structure.json`:
```
CHECKPOINT: structure.json sealed through geometry.
  posts=6×6@{members.posts.cut_length_ft}ft,
  pitch={roof.pitch},
  miter={geometry.compound_cut.miter_deg}°,
  total_height={geometry.total_height.total_height_ft}ft.
```

### `validation-agent`

- All validation reads from `structure.json`
- Geometry engine verification: `python3 scripts/geometry_engine.py context/staging/structure.json`
- Invariant checks use `structure.invariants` as the specification
- `drift_report.json` references section names from `structure.json` (e.g. `"section": "geometry"`)

### `drawing-red-team-agent`

- Required inputs section updated: reads `structure.json` instead of the three legacy files
- Sheet-specific acceptance criteria reference `structure.json` paths:
  - post count: `structure.layout.post_count`
  - hub type: `structure.hub.type`
  - brace presence: `structure.bracing.enabled`
  - rafter tail style: `structure.joinery.rafter_tail`

---

## Migration plan (hard cutover)

1. Add `structure.schema.json` to `plugins/garden-structure-designer/schemas/`
2. Update `geometry_engine.py` to read/write `structure.json` instead of three files
3. Update `cad_scene.py` to read from `structure.json`
4. Update `render_drawings.py` — remove all hardcoded geometry constants, read from `structure.json`
5. Update `schema_validator.py` to validate the new schema
6. Update `structural_physics_validator.py` to read from `structure.json`
7. Update all 4 agent `.md` files with new file references and new interview questions
8. Update all 12 skill `.md` files with new `consumes`/`produces` metadata pointing to `structure.json`
9. Delete legacy staging artifacts: `design-spec.json`, `structural-model.json`, `geometry-calculations.json`
10. Run full pipeline end-to-end regression test

---

## Invariants enforcement summary

| Invariant | Enforced by | Stage |
|---|---|---|
| `rafter_count_equals_post_count` | `geometry_engine.py` | 2 |
| `post_top_equals_beam_bottom` | `cad_scene.py` | 4 |
| `no_rafter_inside_hub_radius` | `cad_scene.py` | 4 |
| `brace_must_connect_to_surfaces` | `cad_scene.py` | 4 |

---

## Regression anchor

For a Hexagonal structure at 4:12 pitch, these values must be reproduced exactly after migration:

```
geometry.compound_cut.miter_deg    = 28.71°
geometry.compound_cut.bevel_deg    = 9.10°
geometry.beam_ring.beam_miter_deg  = 30.00°
geometry.total_height.total_height_ft = 11.045
```

Any geometry migration that changes these values is a regression.

---

## Files changed in this implementation

**New files:**
- `plugins/garden-structure-designer/schemas/structure.schema.json`

**Modified scripts:**
- `scripts/geometry_engine.py` — reads/writes `structure.json`
- `scripts/cad_scene.py` — reads from `structure.json`
- `scripts/render_drawings.py` — zero hardcoded constants, reads from `structure.json`
- `scripts/schema_validator.py` — validates `structure.json`
- `scripts/structural_physics_validator.py` — reads from `structure.json`

**Modified agents:**
- `agents/interactive-designer.md` — new interview questions
- `agents/design-orchestrator.md` — updated file references
- `agents/validation-agent.md` — updated file references
- `agents/drawing-red-team-agent.md` — updated required inputs

**Modified skills (consumes/produces metadata):**
- All 12 skills in `skills/*/SKILL.md`

**Deleted staging files (after migration validation passes):**
- `context/staging/design-spec.json`
- `context/staging/structural-model.json`
- `context/staging/geometry-calculations.json`
