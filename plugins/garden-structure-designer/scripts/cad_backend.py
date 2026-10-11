#!/usr/bin/env python3
"""
cad_backend.py
==============

Purpose:
    Legacy build123d / CadQuery 3D solid modeling and STEP/SVG export module.
    DEPRECATED: Reads from legacy scene geometry. Use cad_backend_build123d.py
    which consumes authoritative resolved_model from geometry_engine.py.

Layer: Service / CAD Export (Legacy Fallback)

Key Input Dependencies:
    - structure model and calculations dictionaries
    - build123d or cadquery CAD library (optional)

Key Functions:
    backend_available() -> bool
    backend_name() -> str
    build_cad_model(model, calcs) -> object | None
    export_step(cad_model, path) -> bool
    export_svg_projection(cad_model, path, view, width, height) -> str

Usage Examples:
    python3 cad_backend.py
"""
from __future__ import annotations

import math
import sys
import warnings
from pathlib import Path
from typing import Any, List, Optional, Tuple

warnings.warn(
    "cad_backend.py is DEPRECATED. Use cad_backend_build123d.py instead — "
    "it reads from the resolved_model produced by geometry_engine.py.",
    DeprecationWarning,
    stacklevel=2,
)

sys.path.append(str(Path(__file__).parent))
from cad_scene import Scene, build_structure_scene, validate_scene_geometry

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
    """Returns True if build123d or cadquery is installed and available."""
    return BACKEND != "none"


def backend_name() -> str:
    """Returns the name of the active 3D CAD backend engine."""
    return BACKEND


def _b3d_box_between(p0: Tuple[float, float, float], p1: Tuple[float, float, float], w: float, h: float) -> Any:
    """Create a build123d Box solid whose axis runs from p0 to p1."""
    import build123d as b3d

    ft_to_mm = 304.8
    x0, y0, z0 = p0
    x1, y1, z1 = p1

    dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
    length_ft = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length_ft < 1e-6:
        return None

    length_mm = length_ft * ft_to_mm
    w_mm = w * ft_to_mm
    h_mm = h * ft_to_mm

    with b3d.BuildPart() as part:
        b3d.Box(length_mm, w_mm, h_mm, align=(b3d.Align.MIN, b3d.Align.CENTER, b3d.Align.CENTER))

    box = part.part
    axis_vec = b3d.Vector(dx, dy, dz).normalized()
    x_axis = b3d.Vector(1, 0, 0)

    if abs(axis_vec.dot(x_axis)) < 0.9999:
        rot_axis = x_axis.cross(axis_vec)
        rot_angle = math.degrees(math.acos(max(-1.0, min(1.0, x_axis.dot(axis_vec)))))
        box = box.rotate(b3d.Axis(b3d.Vector(0, 0, 0), rot_axis), rot_angle)

    return box.translate(b3d.Vector(x0 * ft_to_mm, y0 * ft_to_mm, z0 * ft_to_mm))


def _b3d_cylinder(cx: float, cy: float, cz: float, r: float, h: float) -> Any:
    """Creates a vertical cylinder at (cx, cy, cz) base with radius r and height h."""
    import build123d as b3d

    ft_to_mm = 304.8
    with b3d.BuildPart() as part:
        b3d.Cylinder(r * ft_to_mm, h * ft_to_mm)
    return part.part.translate(b3d.Vector(cx * ft_to_mm, cy * ft_to_mm, cz * ft_to_mm))


def _build_posts_and_footings(scene: Any, post_hw: float, post_hd: float) -> List[Any]:
    """Generates footing cylinders and post box solids for all scene posts."""
    parts = []
    for px, py in scene.post_xy:
        cyl = _b3d_cylinder(px, py, -1.5, 0.5, 1.5)
        if cyl:
            parts.append(cyl)
        box = _b3d_box_between(
            (px, py, scene.Z_GRADE),
            (px, py, scene.Z_POST_TOP),
            post_hw * 2,
            post_hd * 2,
        )
        if box:
            parts.append(box)
    return parts


def _build_ring_beams(scene: Any, beam_hw: float, beam_d: float) -> List[Any]:
    """Generates horizontal ring beam box solids between adjacent posts."""
    parts = []
    qty = scene.qty
    bz = scene.Z_POST_TOP + (beam_d / 2.0)
    for i in range(qty):
        px1, py1 = scene.post_xy[i]
        px2, py2 = scene.post_xy[(i + 1) % qty]
        box = _b3d_box_between((px1, py1, bz), (px2, py2, bz), beam_hw * 2, beam_d)
        if box:
            parts.append(box)
    return parts


def _build_rafters_and_hub(scene: Any, rafter_hw: float, rafter_hd: float) -> List[Any]:
    """Generates hip rafters and central polygonal hub solids."""
    parts = []
    qty = scene.qty
    rafter_apex_pts = [
        (scene.hub_r * math.cos(2 * math.pi * i / qty), scene.hub_r * math.sin(2 * math.pi * i / qty), scene.Z_APEX)
        for i in range(qty)
    ]
    for i, (px, py) in enumerate(scene.post_xy):
        box = _b3d_box_between((px, py, scene.Z_BEAM_TOP), rafter_apex_pts[i], rafter_hw * 2, rafter_hd * 2)
        if box:
            parts.append(box)

    hub_hd = rafter_hd + 0.05
    hub_ztop = scene.Z_APEX + hub_hd
    hub_zbot = scene.Z_APEX - hub_hd
    hub = _b3d_cylinder(0.0, 0.0, hub_zbot, scene.hub_r, hub_ztop - hub_zbot)
    if hub:
        parts.append(hub)
    return parts


def build_cad_model(model: dict, calcs: dict) -> object | None:
    """Builds a full 3D CAD compound model from model and calcs using build123d."""
    if BACKEND != "build123d":
        return None

    import build123d as b3d

    scene = build_structure_scene(model, calcs)
    validate_scene_geometry(scene)

    beam_d = scene.Z_BEAM_TOP - scene.Z_POST_TOP
    posts_spec = model.get("members", {}).get("posts", {})
    beams_spec = model.get("members", {}).get("beams", {})
    rafters_spec = model.get("members", {}).get("rafters", {})

    post_hw = ((posts_spec.get("width_in") or posts_spec.get("actual_width_in") or 5.5) / 12.0) / 2.0
    post_hd = ((posts_spec.get("depth_in") or posts_spec.get("actual_depth_in") or 5.5) / 12.0) / 2.0
    beam_hw = ((beams_spec.get("width_in") or beams_spec.get("actual_width_in") or 5.5) / 12.0) / 2.0
    rafter_hw = ((rafters_spec.get("width_in") or rafters_spec.get("actual_width_in") or 3.5) / 12.0) / 2.0
    rafter_hd = ((rafters_spec.get("depth_in") or rafters_spec.get("actual_depth_in") or 5.5) / 12.0) / 2.0

    parts: List[Any] = []
    parts.extend(_build_posts_and_footings(scene, post_hw, post_hd))
    parts.extend(_build_ring_beams(scene, beam_hw, beam_d))
    parts.extend(_build_rafters_and_hub(scene, rafter_hw, rafter_hd))

    if not parts:
        return None

    try:
        return b3d.Compound(children=parts)
    except Exception:
        return parts


def export_step(cad_model: object, path: str) -> bool:
    """Exports the CAD model compound to a STEP file on disk."""
    if BACKEND == "none" or cad_model is None:
        return False

    if BACKEND == "build123d":
        import build123d as b3d

        try:
            out = Path(path)
            out.parent.mkdir(parents=True, exist_ok=True)
            compound = b3d.Compound(children=cad_model) if isinstance(cad_model, list) else cad_model
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


def export_svg_projection(
    cad_model: object,
    path: str,
    view: str = "iso",
    width: int = 800,
    height: int = 600,
) -> str:
    """Exports a 2D SVG projection of the CAD model for a designated view orientation."""
    if BACKEND != "build123d" or cad_model is None:
        return ""

    import build123d as b3d

    try:
        compound = b3d.Compound(children=cad_model) if isinstance(cad_model, list) else cad_model
        exporter = b3d.ExportSVG(scale=1.0)
        exporter.add_layer("structural", line_color=(44, 45, 66))
        exporter.add_shape(compound, layer="structural")
        svg_str = exporter.toString()

        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(svg_str, encoding="utf-8")
        return svg_str
    except Exception as e:
        print(f"[cad_backend] SVG projection failed: {e}", file=sys.stderr)
        return ""


if __name__ == "__main__":
    print(f"CAD backend: {BACKEND}")
    if BACKEND == "none":
        print("No CAD library available — install build123d or cadquery")
        sys.exit(1)

    model_demo = {"members": {"posts": {"quantity": 6}}, "dimensions": {"max_diagonal_ft": 10.0}}
    calcs_demo = {"total_height": {"post_ft": 8.33, "beam_depth_ft": 0.604}, "roof_rise": {"rise_ft": 1.667}}

    scene_demo = build_structure_scene(model_demo, calcs_demo)
    validate_scene_geometry(scene_demo)
    cad = build_cad_model(model_demo, calcs_demo)
    if cad is None:
        sys.exit(1)

    out_step_demo = "/tmp/garden_structure_smoke.step"
    ok_step = export_step(cad, out_step_demo)
    print(f"  STEP export: {'OK → ' + out_step_demo if ok_step else 'FAILED'}")
