"""manifest_utils: dependency digests must change when any dependency is missing (no silent skips)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from manifest_utils import compute_dependency_hash  # type: ignore[import]  # noqa: E402


def test_json_key_order_does_not_change_hash(tmp_path):
    f = tmp_path / "a.json"
    f.write_text(json.dumps({"x": 1, "y": 2}))
    before = compute_dependency_hash([str(f)])
    f.write_text(json.dumps({"y": 2, "x": 1}))
    assert compute_dependency_hash([str(f)]) == before


def test_missing_dependency_fails_closed(tmp_path):
    present = tmp_path / "a.txt"
    present.write_text("x")
    with pytest.raises(FileNotFoundError, match="missing.txt"):
        compute_dependency_hash([str(present), str(tmp_path / "missing.txt")])


def test_content_change_changes_hash(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("one")
    before = compute_dependency_hash([str(f)])
    f.write_text("two")
    assert compute_dependency_hash([str(f)]) != before
