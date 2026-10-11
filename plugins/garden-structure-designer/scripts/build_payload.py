#!/usr/bin/env python3
"""
build_payload.py
================

Purpose:
    Compiles all sealed design artifacts (structure.json, all 8 SVG sheets,
    and builder documentation markdown files) into a single consolidated
    validation payload markdown file for review and external validation.

Layer: Service / QA Pipeline

Key Input Dependencies:
    - context/staging/structure.json
    - outputs/*.svg (all 8 presentation and technical SVG drawings)
    - outputs/*.md (assembly guide, budget estimate, lumber purchase list)

Key Functions:
    build_payload(output_path: Path | None = None) -> Path

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/build_payload.py [--out target.md]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import outputs_dir, staging_dir


def build_payload(output_path: Path | None = None) -> Path:
    """Concatenates all primary staging and output artifacts into a markdown bundle."""
    s_dir = staging_dir()
    o_dir = outputs_dir()

    files_to_merge = {
        "SEALED MANIFEST (structure.json)": s_dir / "structure.json",
        "GENERATED OUTPUT (drawing-plan-view.svg)": o_dir / "drawing-plan-view.svg",
        "GENERATED OUTPUT (drawing-elevation-view.svg)": o_dir / "drawing-elevation-view.svg",
        "GENERATED OUTPUT (drawing-isometric-view.svg)": o_dir / "drawing-isometric-view.svg",
        "GENERATED OUTPUT (drawing-perspective-view.svg)": o_dir / "drawing-perspective-view.svg",
        "GENERATED OUTPUT (blueprint-plan.svg)": o_dir / "blueprint-plan.svg",
        "GENERATED OUTPUT (blueprint-elevation.svg)": o_dir / "blueprint-elevation.svg",
        "GENERATED OUTPUT (blueprint-isometric.svg)": o_dir / "blueprint-isometric.svg",
        "GENERATED OUTPUT (blueprint-component-isolation.svg)": o_dir / "blueprint-component-isolation.svg",
        "BUILDER DOC (assembly-guide.md)": o_dir / "assembly-guide.md",
        "BUILDER DOC (budget-estimate.md)": o_dir / "budget-estimate.md",
        "BUILDER DOC (lumber-purchase-list.md)": o_dir / "lumber-purchase-list.md",
    }

    target_out = output_path or (s_dir / "validation_payload.md")
    target_out.parent.mkdir(parents=True, exist_ok=True)

    with open(target_out, "w", encoding="utf-8") as out:
        for title, p in files_to_merge.items():
            out.write(f"--- {title} ---\n")
            if p.exists():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        out.write(f.read() + "\n\n")
                except Exception as e:
                    out.write(f"Error reading {p}: {e}\n\n")
            else:
                out.write(f"File not found: {p}\n\n")

    print(f"Created validation payload at: {target_out}")
    return target_out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compile all design artifacts into a consolidated validation payload."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Target markdown file path",
    )
    args = parser.parse_args()
    build_payload(args.out)
