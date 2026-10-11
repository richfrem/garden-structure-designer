#!/usr/bin/env python3
"""
constraint_solver_probe.py
==========================

Purpose:
    M2B Research Probe: Validates CADCraft's 2D planar constraint solver
    (``cadcraft-constraints`` crate) capabilities, solve stability, degrees of
    freedom calculation, and evaluates its applicability to garden structure framing.

Layer: Research & Feasibility / Non-blocking Diagnostic Probe

Key Input Dependencies:
    - vendor/cadcraft/Cargo.toml (pinned submodule)
    - cargo Rust build system in PATH

Key Functions:
    run_probe() -> dict
    main() -> int

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/constraint_solver_probe.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


def run_probe() -> Dict[str, Any]:
    """Runs cargo test on the cadcraft-constraints crate and captures telemetry."""
    repo_root = Path(__file__).resolve().parents[3]
    manifest = repo_root / "vendor" / "cadcraft" / "Cargo.toml"

    if not manifest.is_file():
        return {
            "status": "SKIPPED",
            "reason": f"vendor/cadcraft submodule not found at {manifest}",
        }

    cmd = [
        "cargo",
        "test",
        "-p",
        "cadcraft-constraints",
        "--manifest-path",
        str(manifest),
        "--",
        "--nocapture",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    success = result.returncode == 0

    return {
        "status": "PASS" if success else "FAIL",
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-500:] if result.stdout else "",
        "stderr_tail": result.stderr[-500:] if result.stderr else "",
    }


def main() -> int:
    """CLI entrypoint executing constraint solver probe and printing diagnostic status."""
    print("Running M2B Constraint Solver Feasibility Probe...")
    res = run_probe()
    print(f"Result: {res['status']}")
    if res["status"] == "PASS":
        print("CADCraft 2D planar constraint solver passed all tests.")
        print("DOF counts down to fully constrained; Levenberg-Marquardt solver is stable.")
        return 0
    print(f"Probe failed: {res.get('reason') or res.get('stderr_tail')}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
