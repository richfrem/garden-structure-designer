#!/usr/bin/env python3
"""
manifest_utils.py
=================

Purpose:
    Dependency digest for derived-artifact manifests (spec C5: cache hits require matching
    dependency digests; file existence or mtime is never a cache key). JSON dependencies are
    canonicalized (sorted keys, compact separators) so key order does not change the digest.
    A missing dependency raises ``FileNotFoundError`` instead of being skipped, so a vanished
    input can never produce the same digest as one that was never listed.

Layer: Core / Shared Utility

Key Input Dependencies:
    - the dependency file paths passed in (default: context/staging/structure.json)

Key Functions:
    compute_dependency_hash(paths) -> str

Usage Examples:
    python3 manifest_utils.py context/staging/structure.json outputs/fabrication/cut-list.json
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from typing import Iterable


def compute_dependency_hash(paths: Iterable[str]) -> str:
    """SHA-256 over the sorted dependency files (JSON canonicalized); raises FileNotFoundError if one is missing."""
    h = hashlib.sha256()
    for path in sorted(paths):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dependency not found: {path}")
        with open(path, 'rb') as f:
            content = f.read()
        if path.endswith('.json'):
            # Canonicalize JSON for stable hashing
            try:
                obj = json.loads(content)
                content = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
            except json.JSONDecodeError:
                pass  # If it's malformed JSON, just hash the raw bytes
        h.update(content)
    return h.hexdigest()


if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else ["context/staging/structure.json"]
    print(compute_dependency_hash(files))
