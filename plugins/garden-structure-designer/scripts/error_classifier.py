#!/usr/bin/env python3
"""
error_classifier.py
===================

Purpose:
    Maps a failure (free text, a drift axis, or a structured v1.5 error code such as
    TOPOLOGY_CARDINALITY_MISMATCH, STALE_REVISION, RECOVERY_REQUIRED, MISSING_INPUT, MISSING_DXF,
    REVISION_MISMATCH) to the standard repair taxonomy: classification, severity, retryability,
    repair axis, repair stage and whether a human review is required. Structured codes win over
    the legacy free-text heuristics.

Layer: Execution / Self-Healing Support

Key Input Dependencies:
    - none (pure function); consumed by repair_orchestrator.py and failure_to_test.py

Key Functions / Data:
    classify_failure(failure) -> dict
    CLASSES (set of valid classifications), STRUCTURED_CODES (v1.5 code routing table)

Usage Examples:
    python3 error_classifier.py "TOPOLOGY_CARDINALITY_MISMATCH: expected 6 beams"
"""
import json
import logging
from typing import Dict, Any, Optional

CLASSES = {
    "schema_error", "missing_artifact", "stale_artifact", "source_hash_mismatch",
    "geometry_warning", "svg_xml_invalid", "svg_topology_mismatch",
    "svg_coordinate_drift", "svg_viewbox_overflow", "compound_cut_mismatch",
    "beam_miter_mismatch", "assembly_sequence_missing", "path_resolution_error",
    "independent_qa_unavailable", "safety_review_required", "jurisdiction_review_required",
    "topology_error", "stale_revision", "recovery_required", "missing_input", "cad_artifact_invalid",
    "unknown"
}

# Structured v1.5 error codes (spec C2/C4/C5), checked before the free-text heuristics:
# (code prefix, classification, repair_stage, severity, retryable, requires_human_review)
STRUCTURED_CODES = (
    ("TOPOLOGY_NOT_IMPLEMENTED", "topology_error", "interactive-designer", "high", False, True),
    ("TOPOLOGY_CARDINALITY_MISMATCH", "topology_error", "structural-engine", "high", False, False),
    ("DUPLICATE_MEMBER_ID", "topology_error", "structural-engine", "high", False, False),
    ("DANGLING_CONNECTION_ENDPOINT", "topology_error", "structural-engine", "high", False, False),
    ("ATTACHMENT_GEOMETRY_MISMATCH", "topology_error", "structural-engine", "high", False, False),
    ("UNKNOWN_TOPOLOGY_FAMILY", "topology_error", "interactive-designer", "high", False, False),
    ("HUB_TYPE_MISMATCH", "topology_error", "interactive-designer", "high", False, False),
    ("STALE_REVISION", "stale_revision", "design-orchestrator", "medium", True, False),
    ("RECOVERY_REQUIRED", "recovery_required", "design-orchestrator", "critical", False, True),
    ("MISSING_INPUT", "missing_input", "intake-normalizer", "high", False, False),
    ("MISSING_DXF", "cad_artifact_invalid", "drawing-generator", "high", True, False),
    ("REVISION_MISMATCH", "stale_artifact", "design-orchestrator", "high", True, False),
    ("REVISION_HASH_MISMATCH", "stale_artifact", "design-orchestrator", "high", True, False),
)

def classify_failure(failure: Dict[str, Any] | str) -> Dict[str, Any]:
    """Classifies a drift/failure axis into standard taxonomy."""
    text = str(failure)

    for code, cls, stage, severity, retryable, human in STRUCTURED_CODES:
        if code in text:
            return {
                "classification": cls,
                "severity": severity,
                "retryable": retryable,
                "repair_axis": code.lower(),
                "repair_stage": stage,
                "requires_human_review": human,
            }

    classification = "unknown"
    severity = "medium"
    retryable = True
    repair_axis = "unknown"
    repair_stage = "unknown"
    requires_human_review = False
    
    if "schema" in text.lower():
        classification = "schema_error"
        repair_axis = "schema_error"
        repair_stage = "validation"
    elif "svg_coordinate" in text.lower():
        classification = "svg_coordinate_drift"
        repair_axis = "svg_coordinate_drift"
        repair_stage = "drawing-generator"
    elif "miter" in text.lower() and "beam" in text.lower():
        classification = "beam_miter_mismatch"
        repair_axis = "beam_miter_mismatch"
        repair_stage = "structural-engine"
    elif "safety" in text.lower() or "deflection" in text.lower():
        classification = "safety_review_required"
        severity = "critical"
        retryable = False
        requires_human_review = True
    elif "hash" in text.lower():
        classification = "source_hash_mismatch"
        repair_axis = "source_hash_mismatch"
        repair_stage = "structural-engine"
        
    return {
        "classification": classification,
        "severity": severity,
        "retryable": retryable,
        "repair_axis": repair_axis,
        "repair_stage": repair_stage,
        "requires_human_review": requires_human_review
    }

if __name__ == "__main__":
    import sys
    inp = sys.argv[1] if len(sys.argv) > 1 else "schema error in member definitions"
    res = classify_failure(inp)
    print(json.dumps(res, indent=2))
