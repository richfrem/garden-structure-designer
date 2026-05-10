#!/usr/bin/env python3
"""
error_classifier.py
=====================================
Purpose:
    Core logic for error_classifier.py functionality within garden-structure-designer pipeline.
Layer: Execution
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
    "unknown"
}

def classify_failure(failure: Dict[str, Any] | str) -> Dict[str, Any]:
    """Classifies a drift/failure axis into standard taxonomy."""
    text = str(failure)
    
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
