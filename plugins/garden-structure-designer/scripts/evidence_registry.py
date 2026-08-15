#!/usr/bin/env python3
"""
evidence_registry.py (CLI)
=====================================

Purpose:
    evidence_registry.py =====================================

Layer: Execution

Usage Examples:
    python evidence_registry.py [args]

Supported Object Types:
    JSON, SVG, Markdown

CLI Arguments:
    Varies per script, typically input file paths.

Input Files:
    context/staging/ *.json outputs/ *.svg

Output:
    Validation codes (0 or 1), generated JSON or SVG files.

Key Functions:
    Refer to module docstring or inner functions.

Script Dependencies:
    Standard library json, os, sys, math, hashlib, etc.

Consumed by:
    design-orchestrator, various skills in the pipeline.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from path_utils import staging_dir

def get_registry_file() -> Path:
    return staging_dir() / "evidence-registry.json"

def init_registry() -> Dict[str, Any]:
    return {
        "schema": "garden-structure-designer/evidence-registry/1.0",
        "evidence": []
    }

def load_registry() -> Dict[str, Any]:
    file_path = get_registry_file()
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return init_registry()

def save_registry(data: Dict[str, Any]) -> None:
    with open(get_registry_file(), 'w') as f:
        json.dump(data, f, indent=2)

def add_evidence(claim: str, artifact: str, json_pointer: str = None, source_script: str = None, source_hash: str = None, validators: list = None) -> str:
    data = load_registry()
    evidence_id = f"EV-{len(data['evidence']) + 1:04d}"
    
    entry = {
        "evidence_id": evidence_id,
        "claim": claim,
        "artifact": str(artifact),
        "json_pointer": json_pointer,
        "source_script": str(source_script) if source_script else None,
        "source_hash": source_hash,
        "validated_by": validators or []
    }
    
    data["evidence"].append(entry)
    save_registry(data)
    return evidence_id

def validate_evidence_links() -> List[str]:
    data = load_registry()
    broken = []
    for ev in data.get("evidence", []):
        if not Path(ev["artifact"]).exists():
            broken.append(f"Broken artifact: {ev['artifact']} in {ev['evidence_id']}")
    return broken

if __name__ == "__main__":
    import sys
    broken = validate_evidence_links()
    if broken:
        print(f"EVIDENCE REGISTRY VALIDATION FAILED: {len(broken)} broken links")
        for b in broken:
            print(f"  ✗ {b}")
        sys.exit(1)
    else:
        reg = load_registry()
        print(f"EVIDENCE REGISTRY: {len(reg.get('evidence', []))} valid evidence items recorded ✓")
        sys.exit(0)
