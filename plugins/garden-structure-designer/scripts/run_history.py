#!/usr/bin/env python3
"""
run_history.py
==============

Purpose:
    Append-only history of script runs (context/staging/script-run-history.jsonl): script, args,
    exit code, failure class and SHA-256 of produced artifacts. Used by the repair loop to halt after
    repeated failures of the same class (should_halt) and to detect repeated identical artifacts
    (repeated_identical_artifact).

Layer: Execution / Learning Loop

Key Input Dependencies:
    - context/staging/script-run-history.jsonl (created on first write), path_utils.py

Key Functions:
    get_history_file() -> Path               artifact_hash(path) -> str
    record_run(script, args, exit_code, failure_class=None, artifact_paths=None) -> None
    get_history() -> list[dict]              recent_failures(script, failure_class, limit=5) -> list[dict]
    should_halt(script, failure_class, max_repeats=3) -> bool
    repeated_identical_artifact(path, repeats=2) -> bool

Usage Examples:
    python3 run_history.py        # prints the last recorded runs
"""
import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from path_utils import staging_dir

def get_history_file() -> Path:
    """Path of the JSON-lines run history."""
    return staging_dir() / "script-run-history.jsonl"

def artifact_hash(path: str | Path) -> str:
    """'sha256:<hex>' of a file's bytes, or '' when the file does not exist."""
    p = Path(path)
    if not p.exists():
        return ""
    hasher = hashlib.sha256()
    with open(p, 'rb') as f:
        hasher.update(f.read())
    return f"sha256:{hasher.hexdigest()}"

def record_run(script: str, args: List[str], exit_code: int, failure_class: Optional[str] = None, artifact_paths: Optional[List[str]] = None) -> None:
    """Appends one run record (with artifact hashes for the existing paths)."""
    history_file = get_history_file()
    
    hashes = {}
    if artifact_paths:
        for p in artifact_paths:
            if Path(p).exists():
                hashes[str(p)] = artifact_hash(p)
                
    entry = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "script": script,
        "args": args,
        "exit_code": exit_code,
        "failure_class": failure_class,
        "artifact_hashes": hashes
    }
    
    with open(history_file, 'a') as f:
        f.write(json.dumps(entry) + "\n")

def get_history() -> List[Dict[str, Any]]:
    """All recorded runs, oldest first."""
    history_file = get_history_file()
    if not history_file.exists():
        return []
    history = []
    with open(history_file, 'r') as f:
        for line in f:
            if line.strip():
                history.append(json.loads(line))
    return history

def recent_failures(script: str, failure_class: str, limit: int = 5) -> List[Dict[str, Any]]:
    """The last limit runs of script that failed with failure_class."""
    history = get_history()
    failures = [h for h in history if h.get("script") == script and h.get("failure_class") == failure_class]
    return failures[-limit:]

def should_halt(script: str, failure_class: str, max_repeats: int = 3) -> bool:
    """True once script has failed with failure_class at least max_repeats times."""
    failures = recent_failures(script, failure_class, limit=max_repeats)
    if len(failures) >= max_repeats:
        return True
    return False

def repeated_identical_artifact(path: str, repeats: int = 2) -> bool:
    """True when the last repeats recorded hashes of path are identical (no progress)."""
    history = get_history()
    hashes = [(h.get("artifact_hashes") or {}).get(path) for h in history if path in (h.get("artifact_hashes") or {})]
    hashes = [h for h in hashes if h]
    if len(hashes) >= repeats and len(set(hashes[-repeats:])) == 1:
        return True
    return False

if __name__ == "__main__":
    hist = get_history()
    print(f"Recorded runs in history: {len(hist)}")
    for h in hist[-5:]:
        print(f"  - {h.get('timestamp')}: {h.get('script')} (exit {h.get('exit_code')})")
