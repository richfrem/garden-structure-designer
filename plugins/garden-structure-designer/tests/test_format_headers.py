"""format_headers must never rewrite headers on import or by default (it once overwrote every real header with a template)."""
from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

BOILERPLATE = '"""\nx.py (CLI)\n===\nPurpose:\n    x.py\n"""\nprint(1)\n'
REAL = '"""\nx.py\n====\n\nPurpose:\n    Does a real thing.\n\nKey Input Dependencies:\n    - nothing\n"""\nprint(1)\n'


def _load(monkeypatch, cwd: Path):
    monkeypatch.chdir(cwd)
    sys.modules.pop("format_headers", None)
    return importlib.import_module("format_headers")


def test_import_does_not_modify_files(tmp_path, monkeypatch):
    (tmp_path / "x.py").write_text(REAL)
    _load(monkeypatch, tmp_path)
    assert (tmp_path / "x.py").read_text() == REAL


def test_dry_run_is_default(tmp_path, monkeypatch):
    (tmp_path / "x.py").write_text(BOILERPLATE)
    module = _load(monkeypatch, tmp_path)
    module.main([])
    assert (tmp_path / "x.py").read_text() == BOILERPLATE


def test_apply_never_overwrites_a_real_header(tmp_path, monkeypatch):
    (tmp_path / "x.py").write_text(REAL)
    module = _load(monkeypatch, tmp_path)
    module.main(["--apply"])
    assert (tmp_path / "x.py").read_text() == REAL


def test_apply_adds_a_header_to_docstring_less_files(tmp_path, monkeypatch):
    (tmp_path / "y.py").write_text("print(2)\n")
    module = _load(monkeypatch, tmp_path)
    module.main(["--apply"])
    text = (tmp_path / "y.py").read_text()
    assert text.startswith("#!/usr/bin/env python3") and "Key Input Dependencies:" in text and text.rstrip().endswith("print(2)")
