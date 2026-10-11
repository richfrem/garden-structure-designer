"""Smoke tests for scripts/build_cadcraft.py (--check-only behavior)."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "build_cadcraft.py"


@pytest.fixture(scope="module")
def build_cadcraft():
    spec = importlib.util.spec_from_file_location("build_cadcraft", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_script_importable(build_cadcraft):
    assert callable(build_cadcraft.main)
    assert build_cadcraft.MANIFEST_PATH.name == "Cargo.toml"
    expected = "cadcraft-cli.exe" if sys.platform == "win32" else "cadcraft-cli"
    assert build_cadcraft.BINARY_NAME == expected


def test_check_only_without_binary_fails(build_cadcraft, monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(build_cadcraft, "binary_path", lambda: tmp_path / "missing")
    assert build_cadcraft.main(["--check-only"]) == 1
    assert "not found" in capsys.readouterr().err


def test_check_only_with_working_binary_succeeds(build_cadcraft, monkeypatch, capsys):
    # Use the Python interpreter as a stand-in binary that answers --version.
    monkeypatch.setattr(build_cadcraft, "binary_path", lambda: Path(sys.executable))
    assert build_cadcraft.main(["--check-only"]) == 0
    assert "SHA-256:" in capsys.readouterr().out


def test_check_only_never_invokes_cargo(build_cadcraft, monkeypatch, tmp_path):
    monkeypatch.setattr(build_cadcraft, "binary_path", lambda: tmp_path / "missing")
    monkeypatch.setattr(build_cadcraft, "build", lambda: pytest.fail("build() called"))
    build_cadcraft.main(["--check-only"])


def test_script_runs_as_subprocess():
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "--check-only" in result.stdout and "--force" in result.stdout
