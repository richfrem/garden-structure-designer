"""C3: the cadcraft-cli export deadline is 15s, centralized, and timeouts surface as CadcraftError."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import cadcraft_adapter  # type: ignore[import]  # noqa: E402
import constants  # type: ignore[import]  # noqa: E402


def test_export_timeout_is_15_seconds_in_constants():
    """Spec C3 mandates a 15-second export deadline owned by constants.py."""
    assert constants.CAD_EXPORT_TIMEOUT_S == 15
    assert cadcraft_adapter.CAD_EXPORT_TIMEOUT_S is constants.CAD_EXPORT_TIMEOUT_S


def test_run_cli_passes_deadline_to_subprocess(monkeypatch, tmp_path):
    """The subprocess call must carry the centralized deadline."""
    seen = {}
    binary = tmp_path / "cadcraft-cli"
    binary.write_text("")

    def fake_run(argv, **kwargs):
        seen.update(kwargs)
        raise subprocess.TimeoutExpired(argv, kwargs["timeout"])

    monkeypatch.setattr(cadcraft_adapter.subprocess, "run", fake_run)
    with pytest.raises(cadcraft_adapter.CadcraftError, match="timed out"):
        cadcraft_adapter.CadcraftAdapter(binary)._run_cli(["new {}"], tmp_path / "o.dxf")
    assert seen["timeout"] == constants.CAD_EXPORT_TIMEOUT_S


def test_run_cli_wraps_exec_failure(monkeypatch, tmp_path):
    """An unexecutable binary must raise CadcraftError so export_cad can fall back to ezdxf."""
    binary = tmp_path / "cadcraft-cli"
    binary.write_text("")

    def fake_run(argv, **kwargs):
        raise PermissionError("not executable")

    monkeypatch.setattr(cadcraft_adapter.subprocess, "run", fake_run)
    with pytest.raises(cadcraft_adapter.CadcraftError, match="could not be executed"):
        cadcraft_adapter.CadcraftAdapter(binary)._run_cli(["new {}"], tmp_path / "o.dxf")
