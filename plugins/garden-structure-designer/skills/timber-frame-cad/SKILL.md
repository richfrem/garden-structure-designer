---
name: timber-frame-cad
description: Parametric timber-frame CAD solid modeling and view-projection engine. Builds 3D BREP solids (posts, beams, rafters, braces, footings, hubs) using build123d, runs solid-clearance validations, and projects clean, occlusion-sorted 2D views (presentation, structural, fabrication) to SVG.
allowed-tools: Read, Write, Bash
metadata:
  garden_structure_designer:
    consumes:
      - context/staging/structure.json
    produces:
      - outputs/cad/model.step
      - outputs/cad/model.stl
    validators:
      - plugins/garden-structure-designer/scripts/cad_backend_build123d.py
    repair_axes:
      - cad_geometry_error
      - solid_collision_warning
---

## Expected Inputs
* `context/staging/structure.json` (locked 3D structural specs; includes members, roof, hub, footings, and geometry sections)

## Behavior

1. **3D Solid Modeling & CAD Assembly**
   * **Data-as-Source-of-Truth**: The CAD backend contains absolutely no hardcoded cross-sections or layout constraints. Every dimension, spacing, caisson diameter, footing size, knee brace angle, and rafter thickness is parsed dynamically from `structure.json` to define the 3D model.
   * Uses `build123d` (OpenCascade BREP kernel) as the mathematical geometry authority.
   * Builds parametric solids:
     * **Posts**: vertical boxes from grade Z to beam underside Z (`Z_POST_TOP`), utilizing the post width and depth specs.
     * **Beams**: boxes aligned between post-ring vertices from `Z_POST_TOP` to `Z_BEAM_TOP`, utilizing the beam width and depth specs.
     * **Hip & Jack Rafters**: rectangular prisms resting perfectly flush ON TOP of the beams, shifted vertically by $\Delta z_{\text{vertical}} = \text{RAFTER\_HD} / \cos(\theta)$ to prevent frame penetration, utilizing the rafter width and depth specs.
     * **Hub**: regular polygonal prism (matching post-count) acting as a central compression block/hanging column pendant.
     * **Knee Braces**: diagonal prisms connecting post faces to beam soffits with the brace run calculated dynamically from cut length and angle specifications in the data.
     * **Footings**: square concrete piers extending below grade based on dynamic caisson diameter specifications.

2. **Parametric Geometry Validation**
   * **No Zero-Volume**: Asserts `volume > 0` directly on the OpenCascade BREP shapes.
   * **Component Alignment**: Verifies vertices of posts top out at `Z_POST_TOP`, knee braces touch the beam soffit within 3 inches, and rafter ends terminate perfectly at the hub polygon face radius `hub_r`.
   * **Invariants**: Employs count assertions to guarantee exact component parity with the specification (`visible_posts == qty`, `visible_beams == qty`, `visible_rafters == qty`).

3. **Multi-View Projections & Abstraction**
   * Separates the comprehensive **3D Scene Graph** from **2D Renderings** using three `ViewModes`:
     * **`structural`**: engineering rendering displaying all 3D solid elements (with full/low opacities).
     * **`presentation`**: clean, readable layout matching high-end carpentry guidelines (suppresses background clutter, interior jacks/purlins, and hidden braces).
     * **`fabrication`**: component-level isolation showing dimensions, miters, and bevel coordinates.
   * **Occlusion & Depth Layering**: Employs unbiased, purely physical 3D centroid sorting ($d = x\cdot\text{CAM}_x + y\cdot\text{CAM}_y + z\cdot\text{CAM}_z$) to sort faces back-to-front. Shifting rafters up flush resolves coincident-face rendering artifacts naturally.
   * **Annotation Layout**: Measures bounding boxes of projected elements to guarantee labels are placed safely outside the structure outline (or attached by leader lines) without intersecting primary members.

## Reusable CAD Commands

```bash
# Execute solid modeling, run CAD geometry validations, and export STEP/STL files
python3 plugins/garden-structure-designer/scripts/cad_backend_build123d.py

# Generate all 2D orthographic, plan, isometric, and isolation drawings with clean layering
python3 plugins/garden-structure-designer/scripts/render_drawings.py context/staging/structure.json
```

## Gotchas

* **Direct SVG drafting is not the source of truth.** The 3D solid model must always govern the coordinates. SVGs should only act as the layout/annotation/presentation layer.
* **Avoid monolithic depth-biasing.** Shifts of `+20.0` or more override physical space and cause background rafters to render in front of foreground posts. Foreground layering is cleanly resolved by separating physical timber Z coordinates and using minor, sub-inch ordering offsets.
* **Keep CAD models in sync.** Any mathematical shift inside `cad_scene.py` must be duplicated identically in `cad_backend_build123d.py` (converting feet to millimeters for OpenCascade) to prevent validation mismatches.

## CAD Debuggability Requirement (HARD RULE)

Every solid built by this skill MUST be traceable to a named member in `structure.json`. Anonymous geometry is prohibited.

### Member Tagging
All `Solid` objects MUST carry their stable member ID in `Solid.tag`:
- `Solid(role="post",   tag="P1")` — P1 through P{post_count}
- `Solid(role="beam",   tag="B1")` — B1 through B{post_count}
- `Solid(role="rafter", tag="R1")` — R1 through R{rafter_count}
- `Solid(role="hub",    tag="HUB")`
- `Solid(role="brace",  tag="Brace1a")` — sequential per-post pair
- `Solid(role="footing",tag="FT1")` — FT1 through FT{post_count}

Tags MUST match IDs in `structure.json` exactly. Any mismatch is a traceability failure and the pipeline MUST halt.

### SVG Machine-Readable Attributes
Every projected polygon in SVG output MUST include:
```xml
<polygon data-role="beam" data-tag="B3" ... />
```
Both `data-role` and `data-tag` are required. `data-id` alone is insufficient.

### Validation Failure Messages
If any geometry invariant fails, the error message MUST reference the exact member tag:
```
FAIL: Brace2b → B3  (foot XY 0.45 ft from P2, circumradius=0.32 ft)
FAIL: R4 → HUB  (tip distance 2.3" from nearest hub face plane)
```
Generic messages without member IDs are prohibited.

## Completion: HANDOFF_BLOCK

On successful modeling and rendering, emit the following handoff block:

```json
{
  "stage": "timber-frame-cad",
  "status": "COMPLETE",
  "outputs": [
    "outputs/cad/model.step",
    "outputs/cad/model.stl",
    "outputs/drawing-isometric-view.svg",
    "outputs/blueprint-isometric.svg"
  ],
  "valid_cad": true,
  "zorder_verified": true,
  "next_stage": "builder-docs-generator"
}
```
