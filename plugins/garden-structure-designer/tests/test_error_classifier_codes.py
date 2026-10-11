"""Structured v1.5 error codes (C2 topology, C5 transaction, C4 CAD artifacts) must route to repair stages, not 'unknown'."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from error_classifier import CLASSES, classify_failure  # type: ignore[import]  # noqa: E402


@pytest.mark.parametrize(
    "text,classification,human",
    [
        ("TOPOLOGY_CARDINALITY_MISMATCH: Expected 6 beam member(s)", "topology_error", False),
        ("DUPLICATE_MEMBER_ID: Duplicate member id 'B1'", "topology_error", False),
        ("DANGLING_CONNECTION_ENDPOINT: beam B6 i1=6", "topology_error", False),
        ("ATTACHMENT_GEOMETRY_MISMATCH", "topology_error", False),
        ("TOPOLOGY_NOT_IMPLEMENTED: reserved family", "topology_error", True),
        ("UNKNOWN_TOPOLOGY_FAMILY: None", "topology_error", False),
        ("STALE_REVISION: Canonical revision != base", "stale_revision", False),
        ("RECOVERY_REQUIRED: journal matches neither", "recovery_required", True),
        ("MISSING_INPUT: geometry.compound_cut", "missing_input", False),
        ("MISSING_DXF: outputs/cad/SB01-structure.dxf not found.", "cad_artifact_invalid", False),
        ("REVISION_MISMATCH: cut-list.json revision_id", "stale_artifact", False),
        ("REVISION_HASH_MISMATCH", "stale_artifact", False),
    ],
)
def test_structured_codes_are_classified(text, classification, human):
    result = classify_failure(text)
    assert result["classification"] == classification
    assert result["classification"] in CLASSES
    assert result["requires_human_review"] is human
    assert result["repair_stage"] != "unknown"


def test_unrelated_text_is_still_unknown():
    assert classify_failure("something odd")["classification"] == "unknown"
