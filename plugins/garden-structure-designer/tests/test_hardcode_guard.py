"""hardcode_guard: static detection of silent numeric defaults (.get fallback AND `.get(...) or <number>`) and scale literals."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import hardcode_guard as guard  # type: ignore[import]  # noqa: E402


def _scan(tmp_path, source: str):
    path = tmp_path / "sample.py"
    path.write_text(source)
    return guard.scan_file(path)


def _codes(violations):
    return [v["message"].split(":")[0] for v in violations]


def test_get_with_numeric_fallback_is_flagged(tmp_path):
    assert _codes(_scan(tmp_path, 'x = d.get("a", 5.5)\n')) == ["FORBIDDEN_GET_NUMBER"]


def test_or_numeric_default_after_get_is_flagged(tmp_path):
    assert _codes(_scan(tmp_path, 'x = d.get("a") or 8.0\ny = s.get("b", {}).get("c") or 0\n')) == [
        "FORBIDDEN_OR_NUMBER_DEFAULT", "FORBIDDEN_OR_NUMBER_DEFAULT"]


def test_chained_or_with_number_is_flagged_once(tmp_path):
    assert _codes(_scan(tmp_path, 'x = d.get("a") or d.get("b") or 12.0\n')) == ["FORBIDDEN_OR_NUMBER_DEFAULT"]


@pytest.mark.parametrize("source", [
    'x = d.get("a")\n',
    'x = d.get("a") or "label"\n',          # string display fallback is not a structural number
    'x = a or 3\n',                          # not a dictionary lookup
    'x = d["a"]\n',
    'x = d.get("a") or other\n',
])
def test_clean_patterns_pass(tmp_path, source):
    assert _scan(tmp_path, source) == []


def test_scale_literal_is_flagged(tmp_path):
    assert _codes(_scan(tmp_path, "scale = 55\n")) == ["FORBIDDEN_SCALE_LITERAL"]


def test_violation_reports_location_and_snippet(tmp_path):
    violation = _scan(tmp_path, '\n\nx = d.get("a") or 4\n')[0]
    assert violation["line"] == 3 and "or 4" in violation["snippet"]


def test_hardened_review_modules_are_clean_and_in_the_default_targets():
    hardened = {"fabrication_builder.py", "builder_docs_compiler.py", "cad_backend_build123d.py",
                "structural_physics_validator.py", "strict_access.py", "compile_package.py", "package_consistency_validator.py"}
    assert hardened <= {p.name for p in guard.DEFAULT_TARGETS}
    for path in guard.DEFAULT_TARGETS:
        if path.name in hardened:
            assert guard.scan_file(path) == [], path.name
