#!/usr/bin/env python3
"""
constraint_solver_probe.py
==========================

Purpose:
    M2B Research Probe: runs the pinned CADCraft 2D planar constraint solver
    crate's own test suite (``cadcraft-constraints``) and reports the real pass
    count. It is a non-blocking diagnostic: it never becomes a geometry authority
    and makes no claim beyond what cargo reports (solve stability and degrees of
    freedom are asserted by the crate's tests, not re-measured here).

Layer: Research & Feasibility / Non-blocking Diagnostic Probe

Key Input Dependencies:
    - vendor/cadcraft/Cargo.toml (pinned submodule)
    - cargo Rust build system in PATH

Key Functions:
    _count_passed(stdout) -> int
    run_probe() -> dict
    main() -> int

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/constraint_solver_probe.py
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKAGE_NAME = "cadcraft-constraints"


def _count_passed(stdout: str) -> int:
    """Sums the ``N passed`` counts from every cargo ``test result`` line."""
    return sum(int(n) for n in re.findall(r"test result: \w+\. (\d+) passed", stdout))


def run_probe() -> Dict[str, Any]:
    """Runs cargo test on the cadcraft-constraints crate and captures telemetry."""
    manifest = REPO_ROOT / "vendor" / "cadcraft" / "Cargo.toml"

    if not manifest.is_file():
        return {
            "status": "SKIPPED",
            "reason": f"vendor/cadcraft submodule not found at {manifest}",
        }
    cargo = shutil.which("cargo")
    if cargo is None:
        return {"status": "SKIPPED", "reason": "'cargo' was not found in PATH"}

    cmd = [
        cargo,
        "test",
        "--locked",
        "-p",
        PACKAGE_NAME,
        "--manifest-path",
        str(manifest),
        "--",
        "--nocapture",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
    success = result.returncode == 0

    return {
        "status": "PASS" if success else "FAIL",
        "returncode": result.returncode,
        "tests_passed": _count_passed(result.stdout or ""),
        "stdout_tail": result.stdout[-500:] if result.stdout else "",
        "stderr_tail": result.stderr[-500:] if result.stderr else "",
    }


def main() -> int:
    """CLI entrypoint executing constraint solver probe and printing diagnostic status."""
    print("Running M2B Constraint Solver Feasibility Probe...")
    res = run_probe()
    print(f"Result: {res['status']}")
    if res["status"] == "PASS":
        print(f"{PACKAGE_NAME}: {res['tests_passed']} tests passed.")
        return 0
    print(f"Probe failed: {res.get('reason') or res.get('stderr_tail')}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
