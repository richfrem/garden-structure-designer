#!/usr/bin/env python3
"""
export_cad.py
=============

Purpose:
    High-level service mapping ``structure.json`` entities to multi-layer DXF
    sheets (SB01 3D structure, SB02 plan) through an ``ExchangeWriter`` adapter.
    ``auto`` prefers cadcraft and falls back to ezdxf if cadcraft is missing or fails.

Layer: Service

Key Input Dependencies:
    structure.json with geometry.joints.resolved_model and meta.revision_id
    (meta.revision_hash is computed via revision_identity when absent).

Key Functions:
    select_writer(name) -> ExchangeWriter
    _revision_identity(structure) -> tuple[str, str]
    export_sheets(structure, output_dir, writer=None) -> list[dict]
    main(argv) -> int

Usage:
    python3 export_cad.py --structure context/staging/structure.json \
        --output-dir outputs/cad [--writer auto|cadcraft|ezdxf]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from cadcraft_adapter import CadcraftAdapter, CadcraftError  # noqa: E402
from constants import SHEET_FILENAMES  # noqa: E402,F401
from exchange_writer import ExchangeWriter  # noqa: E402
from ezdxf_adapter import EzdxfAdapter  # noqa: E402
from revision_identity import compute_revision_hash  # noqa: E402


def select_writer(name: str = "auto") -> ExchangeWriter:
    """Return the writer for ``name`` (``auto`` = cadcraft when built, else ezdxf)."""
    if name == "ezdxf":
        return EzdxfAdapter()
    if name == "cadcraft":
        return CadcraftAdapter()
    if name != "auto":
        raise ValueError(f"Unknown writer {name!r}")
    cadcraft = CadcraftAdapter()
    return cadcraft if cadcraft.is_available() else EzdxfAdapter()


def _revision_identity(structure: dict) -> tuple[str, str]:
    """Return (revision_id, revision_hash) for ``structure``."""
    meta = structure.get("meta", {})
    if not meta.get("revision_id"):
        raise ValueError("structure.meta.revision_id is required for CAD export")
    return meta["revision_id"], meta.get("revision_hash") or compute_revision_hash(structure)


def export_sheets(
    structure: dict, output_dir: Path, writer: ExchangeWriter | None = None, *, fallback: bool = True
) -> list[dict]:
    """Export every sheet to ``output_dir``; returns one metadata dict per sheet.

    With ``fallback`` a CadcraftError switches the remaining sheets to ezdxf.
    """
    writer = writer or select_writer()
    revision_id, revision_hash = _revision_identity(structure)
    results = []
    for sheet_id, filename in SHEET_FILENAMES.items():
        path = Path(output_dir) / filename
        kwargs = {"revision_id": revision_id, "revision_hash": revision_hash}
        try:
            results.append(writer.export_sheet(sheet_id, structure, path, **kwargs))
        except CadcraftError as exc:
            if not fallback:
                raise
            print(f"cadcraft failed ({exc}); falling back to ezdxf", file=sys.stderr)
            writer = EzdxfAdapter()
            results.append(writer.export_sheet(sheet_id, structure, path, **kwargs))
    return results


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Export structure.json to DXF sheets")
    parser.add_argument("--structure", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--writer", choices=["auto", "cadcraft", "ezdxf"], default="auto")
    parser.add_argument("--open", action="store_true", help="Launch exported SB01 DXF in Cadcraft desktop app")
    args = parser.parse_args(argv)
    structure = json.loads(args.structure.read_text(encoding="utf-8"))
    results = export_sheets(structure, args.output_dir, select_writer(args.writer), fallback=args.writer == "auto")
    print(json.dumps(results, indent=2))

    sb01_path = args.output_dir / SHEET_FILENAMES.get("SB01", "SB01-structure.dxf")
    print(f"\nTo open in Cadcraft GUI:\n  python3 scripts/open_in_cadcraft.py {sb01_path}")

    if args.open:
        try:
            from open_in_cadcraft import open_in_cadcraft
            return open_in_cadcraft(sb01_path)
        except ImportError:
            print("Warning: open_in_cadcraft helper not available.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
