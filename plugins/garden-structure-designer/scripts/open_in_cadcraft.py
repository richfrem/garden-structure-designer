#!/usr/bin/env python3
"""
open_in_cadcraft.py
===================

Purpose:
    Helper utility to launch and inspect DXF CAD deliverables in the Cadcraft
    desktop application, system CAD viewer, or convert to PNG/PDF on demand.

Layer: Service / Tooling

Key Input Dependencies:
    - outputs/cad/SB01-structure.dxf (or specified DXF path)
    - vendor/cadcraft/ (Rust Cadcraft application workspace)

Key Functions:
    find_cadcraft_binary(repo_root) -> Path | None
    open_in_cadcraft(dxf_path, use_native, dry_run) -> int
    main(argv) -> int

Usage Examples:
    python3 scripts/open_in_cadcraft.py
    python3 scripts/open_in_cadcraft.py outputs/cad/SB02-plan.dxf
    python3 scripts/open_in_cadcraft.py --native
    python3 scripts/open_in_cadcraft.py --pdf
"""
from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PLUGIN_ROOT.parent.parent


def find_cadcraft_binary(repo_root: Path) -> Optional[Path]:
    """Locate built cadcraft GUI binary in target directories."""
    candidates = [
        repo_root / "vendor" / "cadcraft" / "target" / "release" / "cadcraft",
        repo_root / "vendor" / "cadcraft" / "target" / "debug" / "cadcraft",
    ]
    for c in candidates:
        if c.is_file() and os.access(c, os.X_OK):
            return c
    return None


def open_file_native(target_path: Path) -> int:
    """Open a file with the host system default application."""
    system = platform.system()
    if system == "Darwin":
        cmd = ["open", str(target_path)]
    elif system == "Windows":
        cmd = ["cmd", "/c", "start", "", str(target_path)]
    else:
        cmd = ["xdg-open", str(target_path)]
    print(f"Launching native viewer: {' '.join(cmd)}")
    return subprocess.run(cmd).returncode


def open_in_cadcraft(
    dxf_path: Path,
    use_native: bool = False,
    dry_run: bool = False,
) -> int:
    """Launch the DXF file in Cadcraft desktop app or native viewer."""
    if not dxf_path.exists():
        print(f"Error: file not found: {dxf_path}", file=sys.stderr)
        return 1

    if use_native:
        if dry_run:
            print(f"[dry-run] open {dxf_path}")
            return 0
        return open_file_native(dxf_path)

    binary = find_cadcraft_binary(REPO_ROOT)
    if binary:
        cmd = [str(binary), str(dxf_path)]
        print(f"Launching Cadcraft binary: {' '.join(cmd)}")
    else:
        cargo_toml = REPO_ROOT / "vendor" / "cadcraft" / "Cargo.toml"
        if not cargo_toml.exists():
            print(f"Error: Cadcraft not found at {cargo_toml}; falling back to native.", file=sys.stderr)
            return open_file_native(dxf_path)
        cmd = ["cargo", "run", "--manifest-path", str(cargo_toml), "-p", "cadcraft", "--", str(dxf_path)]
        print(f"Launching Cadcraft via Cargo: {' '.join(cmd)}")

    if dry_run:
        print(f"[dry-run] {' '.join(cmd)}")
        return 0

    return subprocess.run(cmd).returncode


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entrypoint for open_in_cadcraft."""
    parser = argparse.ArgumentParser(description="Open DXF, PDF, or PNG in Cadcraft or viewer.")
    parser.add_argument("file", nargs="?", default=None, help="Path to file to open (default: outputs/cad/SB01-structure.dxf)")
    parser.add_argument("--plan", action="store_true", help="Open the SB02 plan DXF")
    parser.add_argument("--pdf", action="store_true", help="Open the SB01 vector PDF")
    parser.add_argument("--png", action="store_true", help="Open the SB01 rendered PNG")
    parser.add_argument("--master-pdf", action="store_true", help="Open outputs/pergola_plan.pdf")
    parser.add_argument("--native", action="store_true", help="Open with macOS default application (Preview/CAD)")
    parser.add_argument("--dry-run", action="store_true", help="Print command without launching")

    args = parser.parse_args(argv)

    cad_dir = REPO_ROOT / "outputs" / "cad"
    if args.master_pdf:
        target = REPO_ROOT / "outputs" / "pergola_plan.pdf"
        return open_file_native(target)
    elif args.pdf:
        target = cad_dir / "SB01-structure.pdf"
        return open_file_native(target)
    elif args.png:
        target = cad_dir / "SB01-structure.png"
        return open_file_native(target)
    elif args.plan:
        target = cad_dir / "SB02-plan.dxf"
    elif args.file:
        target = Path(args.file)
    else:
        target = cad_dir / "SB01-structure.dxf"

    return open_in_cadcraft(target, use_native=args.native, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
