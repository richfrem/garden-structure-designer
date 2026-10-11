"""embed_svgs: assets referenced by the package markdown must exist; missing ones are reported, not hidden."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from embed_svgs import process  # type: ignore[import]  # noqa: E402


def test_process_returns_no_missing_assets_when_all_exist(tmp_path):
    (tmp_path / "a.svg").write_text('<svg width="10" height="10"></svg>')
    (tmp_path / "plan.md").write_text("![A](a.svg)")
    assert process(str(tmp_path / "plan.md"), str(tmp_path / "out.md")) == []
    assert "<svg" in (tmp_path / "out.md").read_text()


def test_process_reports_missing_assets(tmp_path):
    (tmp_path / "plan.md").write_text("![A](gone.svg) ![B](gone.png)")
    missing = process(str(tmp_path / "plan.md"), str(tmp_path / "out.md"))
    assert sorted(Path(m).name for m in missing) == ["gone.png", "gone.svg"]


def test_embedded_svg_keeps_semantic_attributes(tmp_path):
    (tmp_path / "a.svg").write_text('<svg width="10" height="10"><g data-role="post" data-tag="P1"/></svg>')
    (tmp_path / "plan.md").write_text("![A](a.svg)")
    process(str(tmp_path / "plan.md"), str(tmp_path / "out.md"))
    assert 'data-role="post"' in (tmp_path / "out.md").read_text()
