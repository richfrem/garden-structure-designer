#!/usr/bin/env python3
"""
evidence_registry.py
====================

Purpose:
    Registry of evidence behind design claims: each entry links a claim to an artifact (optionally a
    JSON pointer into it), the producing script, its source hash and the validators that checked it
    (context/staging/evidence-registry.json). validate_evidence_links reports entries whose
    artifact no longer exists. Evidence from an earlier revision must never satisfy a current gate:
    bind entries to source_hash and re-validate after every committed revision.

Layer: Execution / Learning Loop

Key Input Dependencies:
    - context/staging/evidence-registry.json (created on first write), path_utils.py

Key Functions:
    get_registry_file() -> Path             init_registry() -> dict
    load_registry() -> dict                 save_registry(data) -> None
    add_evidence(claim, artifact, json_pointer=None, source_script=None, source_hash=None, validators=None) -> str
    validate_evidence_links() -> list[str]

Usage Examples:
    python3 evidence_registry.py     # verifies every registered artifact still exists (exit 1 if not)
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from path_utils import staging_dir

def get_registry_file() -> Path:
    """Path of the evidence registry file in the staging directory."""
    return staging_dir() / "evidence-registry.json"

def init_registry() -> Dict[str, Any]:
    """A new, empty registry document."""
    return {
        "schema": "garden-structure-designer/evidence-registry/1.0",
        "evidence": []
    }

def load_registry() -> Dict[str, Any]:
    """Loads the registry, or a fresh one when none exists yet."""
    file_path = get_registry_file()
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return init_registry()

def save_registry(data: Dict[str, Any]) -> None:
    """Writes the registry back to disk."""
    with open(get_registry_file(), 'w') as f:
        json.dump(data, f, indent=2)

def add_evidence(claim: str, artifact: str, json_pointer: str = None, source_script: str = None, source_hash: str = None, validators: list = None) -> str:
    """Appends an evidence entry and returns its id (EV-0001, EV-0002, ...)."""
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
    """Returns one message per registered artifact that no longer exists."""
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
