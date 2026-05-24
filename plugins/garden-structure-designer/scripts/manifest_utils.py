#!/usr/bin/env python3
"""
manifest_utils.py (CLI)
=====================================

Purpose:
    manifest_utils.py (CLI) =====================================

Layer: Execution

Usage Examples:
    python manifest_utils.py [args]

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
import os
import json
import hashlib

def compute_dependency_hash(paths):
    h = hashlib.sha256()
    for path in sorted(paths):
        if not os.path.exists(path):
            continue
        with open(path, 'rb') as f:
            content = f.read()
        if path.endswith('.json'):
            # Canonicalize JSON for stable hashing
            try:
                obj = json.loads(content)
                content = json.dumps(obj, sort_keys=True, separators=(",",":")).encode()
            except json.JSONDecodeError:
                pass # If it's malformed JSON, just hash the raw bytes
        h.update(content)
    return h.hexdigest()
