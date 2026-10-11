"""svg_validator enforces member tagging: data-tag present with data-id/data-role members, and only real structure.json member ids."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from svg_validator import _check_member_tags  # type: ignore[import]  # noqa: E402

MODEL = {"geometry": {"joints": {"resolved_model": {"members": [
    {"id": "P1", "role": "post"}, {"id": "B1", "role": "beam"}, {"id": "HUB", "role": "hub"}]}}}}


def _svg(body: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg">{body}</svg>'


def test_tagged_members_pass():
    raw = _svg('<polygon data-role="post" data-id="P1" data-tag="P1" points="0,0"/><text data-label="P1">P1</text>')
    assert _check_member_tags(raw, MODEL) == []


def test_data_id_without_data_tag_is_an_error():
    errors = _check_member_tags(_svg('<polygon data-role="post" data-id="P1" points="0,0"/>'), MODEL)
    assert any(e.startswith("SVG_MEMBER_TAG_MISSING") and "P1" in e for e in errors)


def test_member_role_without_any_tag_is_an_error():
    errors = _check_member_tags(_svg('<polygon data-role="beam" points="0,0"/>'), MODEL)
    assert any(e.startswith("SVG_MEMBER_TAG_MISSING") for e in errors)


def test_unknown_member_tag_is_an_error():
    raw = _svg('<polygon data-role="post" data-id="P9" data-tag="P9" points="0,0"/>')
    assert any(e.startswith("SVG_UNKNOWN_MEMBER_TAG") and "P9" in e for e in _check_member_tags(raw, MODEL))


def test_annotation_roles_need_no_member_tag():
    raw = _svg('<g data-role="dimension"><line/></g><g data-role="title-block"/><g data-role="component"/>')
    assert _check_member_tags(raw, MODEL) == []


def test_decorative_member_role_inside_a_component_panel_is_tolerated():
    raw = _svg('<g data-role="component"><rect data-role="post" data-id="P1" data-tag="P1"/><line data-role="post"/></g>')
    assert _check_member_tags(raw, MODEL) == []


def test_legacy_models_without_a_resolved_model_are_skipped():
    assert _check_member_tags(_svg('<polygon data-role="post" data-id="P1"/>'), {}) == []


# --- stale sheets: the title block must show the current source hash and revision --------------------------------

from svg_validator import _check_stale_sheet  # type: ignore[import]  # noqa: E402,E402

STAMPED = {"meta": {"source_hash": "abcdef0123456789", "revision_id": "11112222-3333-4444-5555-666677778888"}}


def _title(source="abcdef01", revision="11112222"):
    return _svg(f'<g data-role="title-block"><text>SOURCE HASH: {source}</text><text>REVISION: {revision} | SCALE: AUTO</text></g>')


def test_current_sheet_is_not_stale():
    assert _check_stale_sheet(_title(), STAMPED) == []


def test_sheet_from_another_source_hash_is_stale():
    assert any(e.startswith("SVG_STALE_SOURCE_HASH") for e in _check_stale_sheet(_title(source="deadbeef"), STAMPED))


def test_sheet_from_another_revision_is_stale():
    assert any(e.startswith("SVG_STALE_REVISION") for e in _check_stale_sheet(_title(revision="00000000"), STAMPED))


def test_unstamped_models_only_check_the_source_hash():
    model = {"meta": {"source_hash": "abcdef0123456789"}}
    assert _check_stale_sheet(_title(revision="UNSTAMPED"), model) == []


def test_models_without_meta_are_skipped():
    assert _check_stale_sheet(_title(source="whatever"), {}) == []
