#!/usr/bin/env python3
"""
revision_identity.py
=====================================

Purpose:
    Pure, standalone revision identity and hashing utility. Provides deterministic
    revision hashing (algorithm ``gsd-json-v1``) and stage receipt generation /
    binding verification. No locking, no filesystem access.

Layer: Core

Hash Contract (gsd-json-v1):
    - SHA-256 over UTF-8 JSON, keys sorted recursively, compact separators,
      ensure_ascii=False, allow_nan=False.
    - Integral floats are normalized to ints (1.0 -> 1) so numeric spelling
      does not change the hash.
    - Excluded: meta.revision_hash, meta.updated_at (only).
    - Included: everything else, including meta.revision_id and meta.source_hash.

Key Functions:
    compute_revision_hash(data) -> str
    stamp_revision(data, revision_id=None) -> dict
    verify_revision_hash(data) -> bool
    create_stage_receipt(stage, revision_id, revision_hash, status, details=None) -> dict
    verify_receipt_binding(receipt, revision_id, revision_hash) -> bool

Script Dependencies:
    Standard library only (copy, hashlib, json, uuid, datetime).
"""

import copy
import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

HASH_ALGORITHM = "gsd-json-v1"
EXCLUDED_META_FIELDS = ("revision_hash", "updated_at")


def _normalize(value: Any) -> Any:
    """Recursively normalize numerics so equal numbers serialize identically."""
    if isinstance(value, dict):
        return {key: _normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def _hashable_view(data: dict) -> dict:
    """Return a normalized deep copy of data without the excluded meta fields."""
    view = _normalize(data)
    meta = view.get("meta")
    if isinstance(meta, dict):
        for field in EXCLUDED_META_FIELDS:
            meta.pop(field, None)
    return view


def compute_revision_hash(data: dict) -> str:
    """Return the 64-char lowercase hex SHA-256 digest of data under gsd-json-v1."""
    canonical = json.dumps(
        _hashable_view(data),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def stamp_revision(data: dict, revision_id: Optional[str] = None) -> dict:
    """Return a deep copy of data with a fresh meta.revision_id and revision_hash."""
    stamped = copy.deepcopy(data)
    meta = stamped.get("meta")
    if not isinstance(meta, dict):
        meta = {}
        stamped["meta"] = meta
    meta["revision_id"] = revision_id or str(uuid.uuid4())
    meta["revision_hash"] = compute_revision_hash(stamped)
    return stamped


def verify_revision_hash(data: dict) -> bool:
    """Return True iff data['meta']['revision_hash'] matches the recomputed hash."""
    meta = data.get("meta")
    if not isinstance(meta, dict):
        return False
    stored_hash = meta.get("revision_hash")
    if not isinstance(stored_hash, str):
        return False
    return stored_hash == compute_revision_hash(data)


def create_stage_receipt(
    stage: str,
    revision_id: str,
    revision_hash: str,
    status: str,
    details: Optional[dict] = None,
) -> dict:
    """Build a stage PASS/FAIL receipt bound to an exact revision."""
    return {
        "stage": stage,
        "revision_id": revision_id,
        "revision_hash": revision_hash,
        "hash_algorithm": HASH_ALGORITHM,
        "status": status,
        "details": copy.deepcopy(details) if details else {},
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def verify_receipt_binding(receipt: dict, revision_id: str, revision_hash: str) -> bool:
    """Return True iff the receipt binds to exactly this revision_id and revision_hash."""
    return (
        receipt.get("revision_id") == revision_id
        and receipt.get("revision_hash") == revision_hash
        and receipt.get("hash_algorithm") == HASH_ALGORITHM
    )
