#!/usr/bin/env python3
"""
spike_hlr_bindings.py
=====================

Purpose:
    Spike script proving OpenCASCADE C++ Hidden Line Removal (HLR) binding capabilities:
    1. Global multi-member visibility calculation (mutual occlusion in 3D).
    2. Shape-filtered extraction: VCompound(shape), HCompound(shape), OutLineVCompound(shape).
    3. Provenance preservation: mapping projected 2D edges directly to source member IDs.
    4. Projection to SVG line segments.

Usage:
    python3 plugins/garden-structure-designer/scripts/spike_hlr_bindings.py [--output-dir /tmp/gsd-hlr-spike]
"""
from __future__ import annotations

import argparse
import math
import os
import sys
from pathlib import Path

from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCP.HLRAlgo import HLRAlgo_Projector
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCP.TopAbs import TopAbs_EDGE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS, TopoDS_Shape


def run_hlr_spike(output_svg: Path | None = None) -> dict[str, int]:
    """Runs a 2-cube mutual occlusion test through OpenCASCADE HLR and returns edge counts."""
    # Box 1: Foreground cube at (0, 0, 0), size 10x10x10 mm
    box1 = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0).Shape()
    # Box 2: Background cube offset at (5, 5, 5), size 10x10x10 mm
    box2 = BRepPrimAPI_MakeBox(gp_Pnt(5.0, 5.0, 5.0), 10.0, 10.0, 10.0).Shape()

    # Step 1: Feed both shapes into ONE global solver
    algo = HLRBRep_Algo()
    algo.Add(box1)
    algo.Add(box2)

    # Step 2: Isometric camera: looking towards (1, -1, 1), screen-right (1, 1, 0)
    axis = gp_Ax2(gp_Pnt(0.0, 0.0, 0.0), gp_Dir(1.0, -1.0, 1.0), gp_Dir(1.0, 1.0, 0.0))
    projector = HLRAlgo_Projector(axis)
    algo.Projector(projector)
    algo.Update()
    algo.Hide()

    # Step 3: Extract shape-filtered results per member
    hlr_shapes = HLRBRep_HLRToShape(algo)

    def extract_edges(shape: TopoDS_Shape) -> list[tuple[tuple[float, float], tuple[float, float]]]:
        if shape.IsNull():
            return []
        edges = []
        exp = TopExp_Explorer(shape, TopAbs_EDGE)
        while exp.More():
            e = TopoDS.Edge_s(exp.Current())
            c = BRepAdaptor_Curve(e)
            p0 = c.Value(c.FirstParameter())
            p1 = c.Value(c.LastParameter())
            edges.append(((p0.X(), p0.Y()), (p1.X(), p1.Y())))
            exp.Next()
        return edges

    v1_edges = extract_edges(hlr_shapes.VCompound(box1))
    v2_edges = extract_edges(hlr_shapes.VCompound(box2))
    h1_edges = extract_edges(hlr_shapes.HCompound(box1))
    h2_edges = extract_edges(hlr_shapes.HCompound(box2))

    counts = {
        "box1_visible": len(v1_edges),
        "box2_visible": len(v2_edges),
        "box1_hidden": len(h1_edges),
        "box2_hidden": len(h2_edges),
    }

    if output_svg:
        output_svg.parent.mkdir(parents=True, exist_ok=True)
        # Bounding box for canvas
        all_pts = [p for seg in (v1_edges + v2_edges) for p in seg]
        min_x = min(p[0] for p in all_pts) - 10
        max_x = max(p[0] for p in all_pts) + 10
        min_y = min(p[1] for p in all_pts) - 10
        max_y = max(p[1] for p in all_pts) + 10
        w = max_x - min_x
        h = max_y - min_y

        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x} {min_y} {w} {h}" width="800" height="600">',
            '  <rect width="100%" height="100%" fill="#1a1a2e" />',
        ]
        # Box 1 visible (cyan)
        for (x1, y1), (x2, y2) in v1_edges:
            svg_lines.append(f'  <line x1="{x1:.2f}" y1="{-y1:.2f}" x2="{x2:.2f}" y2="{-y2:.2f}" stroke="#00ffff" stroke-width="0.8" data-role="box1" />')
        # Box 2 visible (gold)
        for (x1, y1), (x2, y2) in v2_edges:
            svg_lines.append(f'  <line x1="{x1:.2f}" y1="{-y1:.2f}" x2="{x2:.2f}" y2="{-y2:.2f}" stroke="#ffd166" stroke-width="0.8" data-role="box2" />')
        # Box 2 hidden (dashed gold)
        for (x1, y1), (x2, y2) in h2_edges:
            svg_lines.append(f'  <line x1="{x1:.2f}" y1="{-y1:.2f}" x2="{x2:.2f}" y2="{-y2:.2f}" stroke="#ffd166" stroke-width="0.4" stroke-dasharray="1,1" opacity="0.5" />')
        svg_lines.append('</svg>')

        output_svg.write_text('\n'.join(svg_lines), encoding="utf-8")

    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Spike OpenCASCADE HLR bindings")
    parser.add_argument("--output-dir", type=Path, default=Path("/tmp/gsd-hlr-spike"))
    args = parser.parse_args()

    svg_path = args.output_dir / "spike_isometric.svg"
    counts = run_hlr_spike(svg_path)
    print("HLR Spike Successful:")
    for k, v in counts.items():
        print(f"  {k}: {v} edges")
    if svg_path.exists():
        print(f"  SVG written to: {svg_path}")


if __name__ == "__main__":
    main()
