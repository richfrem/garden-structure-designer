"""Shared fail-closed accessor used instead of silent `.get(...) or default` for structural inputs."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from strict_access import MissingInputError, require, require_path  # type: ignore[import]  # noqa: E402


def test_require_returns_present_value_including_zero():
    assert require({"a": 0}, "a", "x") == 0


@pytest.mark.parametrize("mapping", [{}, {"a": None}, {"a": ""}, None, []])
def test_require_raises_with_label_and_key(mapping):
    with pytest.raises(MissingInputError, match=r"MISSING_INPUT: x\.a"):
        require(mapping, "a", "x")


def test_missing_input_error_is_a_value_error():
    assert issubclass(MissingInputError, ValueError)


def test_require_path_walks_nested_mappings_and_names_first_missing_level():
    data = {"members": {"posts": {"cut_length_ft": 8.0}}}
    assert require_path(data, "members", "posts", "cut_length_ft") == 8.0
    with pytest.raises(MissingInputError, match=r"MISSING_INPUT: members\.beams"):
        require_path(data, "members", "beams", "cut_length_ft")
