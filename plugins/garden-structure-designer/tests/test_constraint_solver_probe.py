"""M2B probe: C3 subprocess hygiene and no unverified claims in the report."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import constraint_solver_probe as probe  # type: ignore[import]  # noqa: E402

CARGO_OUT = "test result: ok. 26 passed; 0 failed\ntest result: ok. 9 passed; 0 failed\n"


def _completed(returncode=0, stdout=CARGO_OUT):
    return subprocess.CompletedProcess([], returncode, stdout=stdout, stderr="")


def test_probe_uses_locked_explicit_cwd_and_no_shell(monkeypatch):
    """C3: argument array, --locked, explicit cwd, shell=False."""
    seen = {}

    def fake_run(argv, **kwargs):
        seen["argv"], seen["kwargs"] = argv, kwargs
        return _completed()

    monkeypatch.setattr(probe.shutil, "which", lambda name: "/usr/bin/cargo")
    monkeypatch.setattr(probe.subprocess, "run", fake_run)
    probe.run_probe()
    assert "--locked" in seen["argv"]
    assert seen["kwargs"].get("cwd") == probe.REPO_ROOT
    assert not seen["kwargs"].get("shell", False)


def test_probe_reports_parsed_pass_count(monkeypatch):
    """The report carries the number of tests cargo actually passed."""
    monkeypatch.setattr(probe.shutil, "which", lambda name: "/usr/bin/cargo")
    monkeypatch.setattr(probe.subprocess, "run", lambda *a, **k: _completed())
    assert probe.run_probe()["tests_passed"] == 35


def test_probe_skips_when_cargo_missing(monkeypatch):
    """A missing toolchain is a SKIPPED result, not a crash."""
    monkeypatch.setattr(probe.shutil, "which", lambda name: None)
    result = probe.run_probe()
    assert result["status"] == "SKIPPED" and "cargo" in result["reason"]


def test_main_makes_no_unverified_solver_claims(monkeypatch, capsys):
    """main() must not assert DOF/stability properties it never measured."""
    monkeypatch.setattr(probe, "run_probe", lambda: {"status": "PASS", "tests_passed": 35})
    assert probe.main() == 0
    out = capsys.readouterr().out
    assert "35" in out
    assert "Levenberg" not in out and "fully constrained" not in out
