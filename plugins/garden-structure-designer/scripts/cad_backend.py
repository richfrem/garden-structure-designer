#!/usr/bin/env python3
"""
cad_backend.py
==============
DEPRECATED: This file uses the old geometry pipeline with hardcoded defaults.
Use cad_backend_build123d.py instead — it reads from the resolved_model produced
by geometry_engine.py and performs zero geometry math of its own.

Optional build123d / CadQuery CAD geometry backend for garden-structure-designer.

Architecture
------------
  When build123d is installed:
    - build_cad_model()  → build123d Compound of all structural members
    - export_step()      → STEP file
    - export_svg_projection() → SVG projection of a named view

  When neither library is installed:
    BACKEND = "none"
    All exported functions return None / empty string gracefully.
    render_drawings.py falls back to the pure-Python cad_scene pipeline.

Layer: Execution (optional dependency layer)
Consumed by: render_drawings.py (perspective + isometric views when available)
"""

from __future__ import annotations

import math
import sys
import warnings
from pathlib import Path

warnings.warn(
    "cad_backend.py is DEPRECATED. Use cad_backend_build123d.py instead — "
    "it reads from the resolved_model produced by geometry_engine.py.",
    DeprecationWarning,
    stacklevel=2,
)

sys.path.append(str(Path(__file__).parent))
from cad_scene import Scene, build_structure_scene, validate_scene_geometry

# ---------------------------------------------------------------------------
# Backend detection
# ---------------------------------------------------------------------------

BACKEND: str = "none"

try:
    import build123d as b3d
    BACKEND = "build123d"
except ImportError:
    pass

if BACKEND == "none":
    try:
        import cadquery as cq
        BACKEND = "cadquery"
    except ImportError:
        pass


def backend_available() -> bool:
    return BACKEND != "none"


def backend_name() -> str:
    return BACKEND


# ---------------------------------------------------------------------------
# build123d helper utilities
# ---------------------------------------------------------------------------

def _b3d_box_between(p0: tuple, p1: tuple, w: float, h: float) -> "b3d.Solid":
    """
    Create a build123d Box solid whose axis runs from p0 to p1.

    w, h are the cross-section dimensions (width × height in feet).
    All units in feet; build123d uses mm by default — we convert.
    """
    import build123d as b3d

    FT_TO_MM = 304.8

    x0, y0, z0 = p0
    x1, y1, z1 = p1

    dx, dy, dz = x1-x0, y1-y0, z1-z0
    length_ft = math.sqrt(dx*dx + dy*dy + dz*dz)
    if length_ft < 1e-6:
        return None

    # Build a box aligned with X axis, then rotate to match axis direction
    length_mm = length_ft * FT_TO_MM
    w_mm = w * FT_TO_MM
    h_mm = h * FT_TO_MM

    with b3d.BuildPart() as part:
        b3d.Box(length_mm, w_mm, h_mm, align=(b3d.Align.MIN, b3d.Align.CENTER, b3d.Align.CENTER))

    box = part.part

    # Rotate to align X-axis with the member axis direction
    axis_vec = b3d.Vector(dx, dy, dz).normalized()
    x_axis   = b3d.Vector(1, 0, 0)

    if abs(axis_vec.dot(x_axis)) < 0.9999:
        rot_axis  = x_axis.cross(axis_vec)
        rot_angle = math.degrees(math.acos(max(-1, min(1, x_axis.dot(axis_vec)))))
        box = box.rotate(b3d.Axis(b3d.Vector(0,0,0), rot_axis), rot_angle)

    # Translate to p0
    box = box.translate(b3d.Vector(x0*FT_TO_MM, y0*FT_TO_MM, z0*FT_TO_MM))
    return box


def _b3d_cylinder(cx: float, cy: float, cz: float,
                  r: float, h: float) -> "b3d.Solid":
    """Vertical cylinder at (cx, cy, cz) base, radius r, height h. All in feet."""
    import build123d as b3d
    FT_TO_MM = 304.8
    with b3d.BuildPart() as part:
        b3d.Cylinder(r * FT_TO_MM, h * FT_TO_MM)
    return part.part.translate(
        b3d.Vector(cx*FT_TO_MM, cy*FT_TO_MM, cz*FT_TO_MM)
    )


# ---------------------------------------------------------------------------
# build_cad_model
# ---------------------------------------------------------------------------

def build_cad_model(model: dict, calcs: dict) -> object | None:
    """
    Build a full 3D CAD model from model + calcs using build123d.

    Returns a build123d Compound (collection of labelled solids), or None if
    no CAD backend is available.

    Each solid is labelled with its semantic role and tag so downstream
    exporters can produce annotated STEP files.
    """
    if BACKEND != "build123d":
        return None

    import build123d as b3d

    scene = build_structure_scene(model, calcs)
    validate_scene_geometry(scene)

    qty    = scene.qty
    r_ft   = math.sqrt(scene.post_xy[0][0]**2 + scene.post_xy[0][1]**2)
    post_h = scene.Z_BEAM_TOP   # beam top
    beam_d = scene.Z_BEAM_TOP - scene.Z_POST_TOP
    hub_r  = scene.hub_r

    posts_spec = model.get("members", {}).get("posts", {})
    beams_spec = model.get("members", {}).get("beams", {})
    rafters_spec = model.get("members", {}).get("rafters", {})

    POST_HW   = ((posts_spec.get("width_in") or posts_spec.get("actual_width_in") or 5.5) / 12.0) / 2.0
    POST_HD   = ((posts_spec.get("depth_in") or posts_spec.get("actual_depth_in") or 5.5) / 12.0) / 2.0
    BEAM_HW   = ((beams_spec.get("width_in") or beams_spec.get("actual_width_in") or 5.5) / 12.0) / 2.0
    RAFTER_HW = ((rafters_spec.get("width_in") or rafters_spec.get("actual_width_in") or 3.5) / 12.0) / 2.0
    RAFTER_HD = ((rafters_spec.get("depth_in") or rafters_spec.get("actual_depth_in") or 5.5) / 12.0) / 2.0

    parts: list = []

    # Footings (concrete cylinders)
    for i, (px, py) in enumerate(scene.post_xy):
        cyl = _b3d_cylinder(px, py, -1.5, 0.5, 1.5)   # 6" dia, 18" deep
        if cyl:
            parts.append(cyl)

    # Posts
    for i, (px, py) in enumerate(scene.post_xy):
        box = _b3d_box_between(
            (px, py, scene.Z_GRADE),
            (px, py, scene.Z_POST_TOP),
            POST_HW*2, POST_HD*2,
        )
        if box:
            parts.append(box)

    # Ring beams
    for i in range(qty):
        px1, py1 = scene.post_xy[i]
        px2, py2 = scene.post_xy[(i+1) % qty]
        bz = scene.Z_POST_TOP + (beam_d / 2.0)
        box = _b3d_box_between(
            (px1, py1, bz), (px2, py2, bz),
            BEAM_HW*2, beam_d,
        )
        if box:
            parts.append(box)

    # Hip rafters
    rafter_apex_pts = [
        (hub_r * math.cos(2*math.pi*i/qty),
         hub_r * math.sin(2*math.pi*i/qty),
         scene.Z_APEX)
        for i in range(qty)
    ]
    for i, (px, py) in enumerate(scene.post_xy):
        box = _b3d_box_between(
            (px, py, scene.Z_BEAM_TOP),
            rafter_apex_pts[i],
            RAFTER_HW*2, RAFTER_HD*2,
        )
        if box:
            parts.append(box)

    # Hub
    hub_hd = RAFTER_HD + 0.05
    hub_ztop = scene.Z_APEX + hub_hd
    hub_zbot = scene.Z_APEX - hub_hd
    hub = _b3d_cylinder(0.0, 0.0, hub_zbot, hub_r, hub_ztop - hub_zbot)
    if hub:
        parts.append(hub)

    if not parts:
        return None

    try:
        compound = b3d.Compound(children=parts)
        return compound
    except Exception:
        # Fallback: return list of parts if Compound fails
        return parts


# ---------------------------------------------------------------------------
# export_step
# ---------------------------------------------------------------------------

def export_step(cad_model: object, path: str) -> bool:
    """
    Export the CAD model to a STEP file.

    Returns True on success, False if backend unavailable or export failed.
    """
    if BACKEND == "none" or cad_model is None:
        return False

    if BACKEND == "build123d":
        import build123d as b3d
        try:
            out = Path(path)
            out.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(cad_model, list):
                compound = b3d.Compound(children=cad_model)
            else:
                compound = cad_model
            # build123d 0.7+ uses module-level export_step(), not a method
            if hasattr(b3d, "export_step"):
                b3d.export_step(compound, str(out))
            elif hasattr(compound, "export_step"):
                compound.export_step(str(out))
            else:
                from build123d import export_step as _exp
                _exp(compound, str(out))
            return True
        except Exception as e:
            print(f"[cad_backend] STEP export failed: {e}", file=sys.stderr)
            return False

    return False


# ---------------------------------------------------------------------------
# export_svg_projection
# ---------------------------------------------------------------------------

def export_svg_projection(
    cad_model: object,
    path: str,
    view: str = "iso",
    width: int = 800,
    height: int = 600,
) -> str:
    """
    Export a 2D SVG projection of the CAD model.

    view: "iso" (30° isometric), "top", "front", "side"

    Returns the SVG string on success, empty string on failure.
    The SVG contains only geometry — no title blocks, annotations,
    or semantic data-role tags. Those are added by render_drawings.py.
    """
    if BACKEND == "none" or cad_model is None:
        return ""

    if BACKEND == "build123d":
        import build123d as b3d

        # Camera directions for each view
        view_dirs = {
            "iso":   b3d.Vector(1, 1, 1).normalized(),
            "top":   b3d.Vector(0, 0, 1),
            "front": b3d.Vector(0, -1, 0),
            "side":  b3d.Vector(1, 0, 0),
        }
        cam = view_dirs.get(view) or view_dirs["iso"]

        try:
            if isinstance(cad_model, list):
                compound = b3d.Compound(children=cad_model)
            else:
                compound = cad_model

            exporter = b3d.ExportSVG(scale=1.0)
            exporter.add_layer("structural", line_color=(44, 45, 66))
            exporter.add_shape(compound, layer="structural")
            svg_str = exporter.toString()

            out = Path(path)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(svg_str)
            return svg_str

        except Exception as e:
            print(f"[cad_backend] SVG projection failed: {e}", file=sys.stderr)
            return ""

    return ""


# ---------------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"CAD backend: {BACKEND}")

    if BACKEND == "none":
        print("No CAD library available — install build123d or cadquery")
        sys.exit(1)

    # Smoke test with a default hex model
    model = {
        "members": {"posts": {"quantity": 6}},
        "dimensions": {"max_diagonal_ft": 10.0},
    }
    calcs = {
        "total_height": {"post_ft": 8.33, "beam_depth_ft": 0.604},
        "roof_rise":    {"rise_ft": 1.667},
    }

    print("Building scene...")
    scene = build_structure_scene(model, calcs)
    validate_scene_geometry(scene)
    print(f"  {len(scene.solids)} solids — geometry valid")

    print("Building CAD model...")
    cad = build_cad_model(model, calcs)
    if cad is None:
        print("  CAD model build returned None")
        sys.exit(1)
    print("  CAD model built OK")

    out_step = "/tmp/garden_structure_smoke.step"
    ok = export_step(cad, out_step)
    print(f"  STEP export: {'OK → ' + out_step if ok else 'FAILED'}")
