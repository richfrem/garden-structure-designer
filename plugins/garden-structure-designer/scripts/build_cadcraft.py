#!/usr/bin/env python3
"""Build the headless ``cadcraft-cli`` binary from the pinned vendor/cadcraft submodule.

Usage:
    python scripts/build_cadcraft.py [--check-only] [--force]
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = REPO_ROOT / "vendor" / "cadcraft" / "Cargo.toml"
PACKAGE_NAME = "cadcraft-cli"
BINARY_NAME = PACKAGE_NAME + (".exe" if sys.platform == "win32" else "")
SMOKE_FLAGS = ("--help", "--version")
SMOKE_TIMEOUT_SECONDS = 30


class BuildError(RuntimeError):
    """Raised when the cadcraft-cli build or verification fails."""


def find_cargo() -> str:
    cargo = shutil.which("cargo")
    if cargo is None:
        raise BuildError(
            "'cargo' was not found in PATH. Install the Rust toolchain from "
            "https://rustup.rs and re-run this script."
        )
    return cargo


def binary_path() -> Path:
    # Cargo places release artifacts in <workspace root>/target/release.
    return MANIFEST_PATH.parent / "target" / "release" / BINARY_NAME


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binary_responds(binary: Path) -> bool:
    """Return True if the binary exits 0 for --help or --version."""
    for flag in SMOKE_FLAGS:
        try:
            result = subprocess.run(
                [str(binary), flag],
                capture_output=True,
                timeout=SMOKE_TIMEOUT_SECONDS,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if result.returncode == 0:
            return True
    return False


def verify_binary() -> Path:
    binary = binary_path()
    if not binary.is_file():
        raise BuildError(f"Compiled binary not found at {binary}")
    if not binary_responds(binary):
        raise BuildError(f"{binary} did not respond successfully to --help or --version")
    print(f"Binary: {binary}")
    print(f"SHA-256: {sha256_of(binary)}")
    return binary


def build() -> None:
    if not MANIFEST_PATH.is_file():
        raise BuildError(
            f"{MANIFEST_PATH} not found. Run: git submodule update --init vendor/cadcraft"
        )
    command = [
        find_cargo(),
        "build",
        "--locked",
        "--release",
        "-p",
        PACKAGE_NAME,
        "--manifest-path",
        str(MANIFEST_PATH),
    ]
    print("Running:", " ".join(command))
    if subprocess.run(command, cwd=REPO_ROOT).returncode != 0:
        raise BuildError("cargo build failed")


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="verify the pre-compiled binary exists and works, without rebuilding",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="rebuild even if the binary already exists",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.check_only:
            verify_binary()
        else:
            if args.force or not binary_path().is_file():
                build()
            else:
                print(f"Binary already exists; use --force to rebuild: {binary_path()}")
            verify_binary()
    except BuildError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
