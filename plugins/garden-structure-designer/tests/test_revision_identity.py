import re
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from revision_identity import (
    compute_revision_hash,
    create_stage_receipt,
    stamp_revision,
    verify_receipt_binding,
    verify_revision_hash,
)


@pytest.fixture
def structure():
    return {
        "layout": {"shape": "hexagon", "inscribed_radius_ft": 10.0, "post_count": 6},
        "posts": [{"id": "P1", "x": 1.5, "y": 2.0}, {"id": "P2", "x": 3.25, "y": 4.0}],
        "meta": {"updated_at": "2026-01-01T00:00:00Z", "source_hash": "abc"},
    }


def test_hash_is_64_char_lowercase_hex(structure):
    assert re.fullmatch(r"[0-9a-f]{64}", compute_revision_hash(structure))


def test_key_order_does_not_change_hash():
    a = {"a": 1, "b": {"x": 1, "y": [1, 2]}, "meta": {"source_hash": "s"}}
    b = {"meta": {"source_hash": "s"}, "b": {"y": [1, 2], "x": 1}, "a": 1}
    assert compute_revision_hash(a) == compute_revision_hash(b)


def test_integral_float_equals_int():
    assert compute_revision_hash({"x": 1.0}) == compute_revision_hash({"x": 1})


def test_minor_coordinate_change_changes_hash(structure):
    original = compute_revision_hash(structure)
    structure["posts"][0]["x"] = 1.5001
    assert compute_revision_hash(structure) != original


def test_updated_at_excluded(structure):
    original = compute_revision_hash(structure)
    structure["meta"]["updated_at"] = "2030-12-31T23:59:59Z"
    assert compute_revision_hash(structure) == original


def test_revision_hash_field_excluded(structure):
    original = compute_revision_hash(structure)
    structure["meta"]["revision_hash"] = "deadbeef"
    assert compute_revision_hash(structure) == original


def test_revision_id_included(structure):
    structure["meta"]["revision_id"] = "id-1"
    first = compute_revision_hash(structure)
    structure["meta"]["revision_id"] = "id-2"
    assert compute_revision_hash(structure) != first


def test_source_hash_included(structure):
    original = compute_revision_hash(structure)
    structure["meta"]["source_hash"] = "other"
    assert compute_revision_hash(structure) != original


def test_non_excluded_meta_field_included(structure):
    original = compute_revision_hash(structure)
    structure["meta"]["note"] = "x"
    assert compute_revision_hash(structure) != original


def test_nan_rejected():
    with pytest.raises(ValueError):
        compute_revision_hash({"x": float("nan")})


def test_non_ascii_supported():
    assert compute_revision_hash({"name": "pergola é"}) != compute_revision_hash({"name": "pergola e"})


def test_compute_does_not_mutate_input(structure):
    structure["meta"]["revision_hash"] = "h"
    snapshot = repr(structure)
    compute_revision_hash(structure)
    assert repr(structure) == snapshot


def test_stamp_generates_uuid_and_valid_hash(structure):
    stamped = stamp_revision(structure)
    assert re.fullmatch(r"[0-9a-f-]{36}", stamped["meta"]["revision_id"])
    assert verify_revision_hash(stamped)
    assert "revision_hash" not in structure["meta"]  # original untouched


def test_stamp_uses_supplied_revision_id(structure):
    assert stamp_revision(structure, revision_id="rev-1")["meta"]["revision_id"] == "rev-1"


def test_stamp_creates_meta_when_missing():
    stamped = stamp_revision({"a": 1})
    assert verify_revision_hash(stamped)


def test_restamp_changes_revision_id_and_hash(structure):
    first = stamp_revision(structure)
    second = stamp_revision(first)
    assert first["meta"]["revision_id"] != second["meta"]["revision_id"]
    assert first["meta"]["revision_hash"] != second["meta"]["revision_hash"]


def test_verify_survives_updated_at_change(structure):
    stamped = stamp_revision(structure)
    stamped["meta"]["updated_at"] = "2031-01-01T00:00:00Z"
    assert verify_revision_hash(stamped)


def test_verify_detects_tampering(structure):
    stamped = stamp_revision(structure)
    stamped["posts"][1]["y"] = 4.5
    assert not verify_revision_hash(stamped)


def test_verify_detects_revision_id_tampering(structure):
    stamped = stamp_revision(structure)
    stamped["meta"]["revision_id"] = "forged"
    assert not verify_revision_hash(stamped)


def test_verify_false_without_hash_or_meta(structure):
    assert not verify_revision_hash(structure)
    assert not verify_revision_hash({"a": 1})


def test_receipt_fields_and_binding():
    receipt = create_stage_receipt("validate", "rev-1", "h" * 64, "PASS", {"checks": 3})
    assert receipt["stage"] == "validate"
    assert receipt["status"] == "PASS"
    assert receipt["details"] == {"checks": 3}
    assert verify_receipt_binding(receipt, "rev-1", "h" * 64)


def test_receipt_default_details_empty():
    assert create_stage_receipt("s", "r", "h", "FAIL")["details"] == {}


def test_receipt_binding_rejects_mismatch():
    receipt = create_stage_receipt("s", "rev-1", "hash-1", "PASS")
    assert not verify_receipt_binding(receipt, "rev-2", "hash-1")
    assert not verify_receipt_binding(receipt, "rev-1", "hash-2")
    assert not verify_receipt_binding({}, "rev-1", "hash-1")


def test_receipt_binds_to_stamped_revision(structure):
    stamped = stamp_revision(structure)
    meta = stamped["meta"]
    receipt = create_stage_receipt("render", meta["revision_id"], meta["revision_hash"], "PASS")
    assert verify_receipt_binding(receipt, meta["revision_id"], meta["revision_hash"])
    restamped = stamp_revision(stamped)
    assert not verify_receipt_binding(
        receipt, restamped["meta"]["revision_id"], restamped["meta"]["revision_hash"]
    )
