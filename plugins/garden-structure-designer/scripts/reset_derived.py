#!/usr/bin/env python3
"""
reset_derived.py
================

Purpose:
    Unseals the derived sections of structure.json (geometry and/or cad) and resets
    meta.lifecycle. The change is applied as a C5 transaction (structure_io.update_structure):
    compare-and-swap on the revision hash, a new committed revision, and the purge of every
    stale derived artifact (including the legacy shim files) from the C5 inventory.
    Expects the canonical layout <root>/context/staging/structure.json.

Layer: Execution / Maintenance

Key Input Dependencies:
    - context/staging/structure.json (or the path argument)
    - structure_io.py (load_structure, update_structure), path_utils.py

Key Functions:
    needs_reset(data, reset_geom, reset_cad, lifecycle) -> bool
    apply_reset(data, reset_geom, reset_cad, lifecycle) -> None
    main(argv=None) -> None

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/reset_derived.py [structure.json] [--geometry] [--cad] [--lifecycle ENGINEERED]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add script directory to sys.path to allow importing local modules
sys.path.insert(0, str(Path(__file__).parent.absolute()))

from path_utils import staging_dir
from structure_io import load_structure, update_structure


def _targets(data: dict, reset_geom: bool, reset_cad: bool) -> list[str]:
    """Names of the derived sections present in ``data`` that the flags select."""
    return [name for name, wanted in (("geometry", reset_geom), ("cad", reset_cad)) if wanted and name in data]


def needs_reset(data: dict, reset_geom: bool, reset_cad: bool, lifecycle: str) -> bool:
    """True when any selected derived section is still sealed or the lifecycle differs."""
    sealed = any(data[name].get("_sealed") is not False for name in _targets(data, reset_geom, reset_cad))
    return sealed or ("meta" in data and data["meta"].get("lifecycle") != lifecycle)


def apply_reset(data: dict, reset_geom: bool, reset_cad: bool, lifecycle: str) -> None:
    """Unseals the selected derived sections and sets the lifecycle (in place)."""
    for name in _targets(data, reset_geom, reset_cad):
        data[name]["_sealed"] = False
    if "meta" in data:
        data["meta"]["lifecycle"] = lifecycle


def main(argv: Optional[list[str]] = None) -> None:
    """CLI entrypoint: reset derived sections through a committed transaction."""
    parser = argparse.ArgumentParser(description="Reset derived sections of structure.json")
    parser.add_argument("model_path", nargs="?", default=str(staging_dir() / "structure.json"), help="Path to structure.json")
    parser.add_argument("--geometry", action="store_true", help="Reset geometry section")
    parser.add_argument("--cad", action="store_true", help="Reset cad section")
    parser.add_argument("--lifecycle", default="ENGINEERED", help="Reset lifecycle to this state")
    args = parser.parse_args(argv)

    model_path = Path(args.model_path)
    if not model_path.exists():
        print(f"Error: {model_path} not found.")
        sys.exit(1)

    # If neither flag specified, reset both derived sections by default
    reset_all = not args.geometry and not args.cad
    reset_geom, reset_cad = args.geometry or reset_all, args.cad or reset_all

    if not needs_reset(load_structure(model_path), reset_geom, reset_cad, args.lifecycle):
        print("No changes needed. Derived sections already unsealed and lifecycle matches.")
        return
    update_structure(model_path, lambda data: apply_reset(data, reset_geom, reset_cad, args.lifecycle))
    print(f"Reset derived sections in {model_path.name}. Lifecycle set to {args.lifecycle}. Derived artifacts purged (C5).")


if __name__ == "__main__":
    main()
