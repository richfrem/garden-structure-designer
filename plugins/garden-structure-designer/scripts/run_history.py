#!/usr/bin/env python3
"""
run_history.py (CLI)
=====================================

Purpose:
    run_history.py =====================================

Layer: Execution

Usage Examples:
    python run_history.py [args]

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
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from path_utils import staging_dir

def get_history_file() -> Path:
    return staging_dir() / "script-run-history.jsonl"

def artifact_hash(path: str | Path) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    hasher = hashlib.sha256()
    with open(p, 'rb') as f:
        hasher.update(f.read())
    return f"sha256:{hasher.hexdigest()}"

def record_run(script: str, args: List[str], exit_code: int, failure_class: Optional[str] = None, artifact_paths: Optional[List[str]] = None) -> None:
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
    history = get_history()
    failures = [h for h in history if h.get("script") == script and h.get("failure_class") == failure_class]
    return failures[-limit:]

def should_halt(script: str, failure_class: str, max_repeats: int = 3) -> bool:
    failures = recent_failures(script, failure_class, limit=max_repeats)
    if len(failures) >= max_repeats:
        return True
    return False

def repeated_identical_artifact(path: str, repeats: int = 2) -> bool:
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
