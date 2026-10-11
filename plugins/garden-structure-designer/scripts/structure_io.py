#!/usr/bin/env python3
"""
structure_io.py
===============

Purpose:
    Single reader/writer for ``context/staging/structure.json`` and the C5
    transaction authority: portable interprocess locking, compare-and-swap on the
    revision hash, a durable commit journal, crash recovery, and purge of derived
    artifacts when a new revision is committed.

Layer: Core / Transaction Authority

Key Input Dependencies:
    - context/staging/structure.json (canonical staging bus; <root>/context/staging layout)
    - constants.py (C5_PURGE_GLOBS, C5_PURGE_ROOTS, ERROR_STALE_REVISION)
    - revision_identity.py (gsd-json-v1 hashing, stamp_revision)

Key Functions / Classes:
    load_structure(path) -> dict
    save_structure(data, path) -> None                 (atomic; legacy direct-write path)
    seal_section(data, section) -> None
    assert_not_sealed(data, section) -> None
    compute_source_hash(data) -> str
    StaleRevisionError / RecoveryRequiredError         (error_code STALE_REVISION / RECOVERY_REQUIRED)
    Transaction                                        (txn_id, canonical_path, base_revision_hash, candidate_path)
    begin_transaction(canonical_path, base_revision_hash) -> Transaction
    commit_transaction(txn) -> None
    recover_journals(canonical_path) -> None           (resolve COMMITTING journals under the lock)
    _project_root(canonical_path) -> Path              _journal_path(canonical_path, txn_id) -> Path
    _FileLock(canonical_path)                          (fcntl on POSIX, msvcrt on Windows)
    _write_json_durably(path, payload) -> None         _record_journal(canonical_path, txn_id, entry) -> None
    _assert_canonical_matches(canonical_path, base_revision_hash) -> dict
    _inside_allowed_roots(path, project_root) -> bool  _purge_inventory(project_root) -> list[Path]
    _purge_relative_paths(project_root, relative_paths) -> None
    _recover_locked(canonical_path) -> None

Usage Examples:
    txn = begin_transaction("context/staging/structure.json", base_revision_hash)
    # ... edit txn.candidate_path ...
    commit_transaction(txn)    # raises StaleRevisionError if canonical moved
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

try:
    import fcntl
except ImportError:  # Windows: no fcntl; use msvcrt byte-range locking
    fcntl = None
    import msvcrt

from constants import C5_PURGE_GLOBS, C5_PURGE_ROOTS, ERROR_RECOVERY_REQUIRED, ERROR_STALE_REVISION
from revision_identity import compute_revision_hash, stamp_revision

INPUT_SECTIONS = {
    "intent", "structure", "layout", "members", "roof",
    "hub", "bracing", "footings", "joinery"
}


def load_structure(path: str | Path) -> dict[str, Any]:
    """Reads and parses a structure.json file."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_structure(data: dict[str, Any], path: str | Path) -> None:
    """Stamps meta.updated_at and writes ``data`` atomically (legacy direct-write path)."""
    data["meta"]["updated_at"] = datetime.now(timezone.utc).isoformat()
    _write_json_durably(Path(path), data)


def seal_section(data: dict[str, Any], section: str) -> None:
    """Marks a section as sealed so downstream stages cannot mutate it."""
    if section not in data:
        raise KeyError(f"Section '{section}' not found in structure")
    data[section]["_sealed"] = True


def assert_not_sealed(data: dict[str, Any], section: str) -> None:
    """Raises RuntimeError when ``section`` is already sealed."""
    if data.get(section, {}).get("_sealed"):
        raise RuntimeError(
            f"Section '{section}' is sealed — cannot overwrite. "
            "Downstream stages must not mutate upstream sections."
        )


def compute_source_hash(data: dict[str, Any]) -> str:
    """Hashes the input sections only (meta.source_hash semantics; not a concurrency token)."""
    payload = {k: data[k] for k in sorted(INPUT_SECTIONS) if k in data}
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


# --- C5 transaction authority ---


class StaleRevisionError(RuntimeError):
    """Raised when the canonical revision no longer matches the transaction base."""

    error_code = ERROR_STALE_REVISION


class RecoveryRequiredError(RuntimeError):
    """Raised when a journal cannot be reconciled with canonical state; downstream work is blocked."""

    error_code = ERROR_RECOVERY_REQUIRED


@dataclass(frozen=True)
class Transaction:
    """Handle for one open transaction: candidate workspace plus the CAS base hash."""

    txn_id: str
    canonical_path: Path
    base_revision_hash: str
    candidate_path: Path

    @property
    def project_root(self) -> Path:
        """Project root derived from the canonical path."""
        return _project_root(self.canonical_path)


def _project_root(canonical_path: Path) -> Path:
    """Canonical lives at <root>/context/staging/structure.json."""
    return canonical_path.parents[2]


def _journal_path(canonical_path: Path, txn_id: str) -> Path:
    """Returns the journal file path for a transaction id."""
    return canonical_path.parent / "journal" / f"{txn_id}.json"


def _lock_handle(handle: Any) -> None:
    """Acquires an exclusive lock on an open lock-file handle (blocking)."""
    if fcntl is not None:
        fcntl.flock(handle, fcntl.LOCK_EX)
        return
    handle.seek(0)
    while True:  # msvcrt.LK_LOCK gives up after ~10s; keep waiting like flock does
        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            return
        except OSError:
            continue


def _unlock_handle(handle: Any) -> None:
    """Releases the exclusive lock taken by ``_lock_handle``."""
    if fcntl is not None:
        fcntl.flock(handle, fcntl.LOCK_UN)
        return
    handle.seek(0)
    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)


@contextmanager
def _FileLock(canonical_path: Path) -> Iterator[None]:
    """Exclusive interprocess lock keyed to the canonical structure path."""
    lock_path = canonical_path.with_name(canonical_path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "a+") as handle:
        _lock_handle(handle)
        try:
            yield
        finally:
            _unlock_handle(handle)


def _write_json_durably(path: Path, payload: dict[str, Any]) -> None:
    """Writes JSON to a temp file, fsyncs, and atomically replaces ``path``; cleans up on failure."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(path.name + ".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def _record_journal(canonical_path: Path, txn_id: str, entry: dict[str, Any]) -> None:
    """Durably writes a journal entry for a transaction."""
    _write_json_durably(_journal_path(canonical_path, txn_id), entry)


def _assert_canonical_matches(canonical_path: Path, base_revision_hash: str) -> dict[str, Any]:
    """Re-reads canonical and raises StaleRevisionError unless its hash equals the base hash."""
    data = load_structure(canonical_path)
    current_hash = compute_revision_hash(data)
    if current_hash != base_revision_hash:
        raise StaleRevisionError(
            f"Canonical revision {current_hash} != base {base_revision_hash}"
        )
    return data


def _inside_allowed_roots(path: Path, project_root: Path) -> bool:
    """True when ``path``'s resolved parent sits inside an allowlisted purge root."""
    allowed_roots = [(project_root / rel).resolve() for rel in C5_PURGE_ROOTS]
    # Resolve the parent only: a symlink is removed itself, never its target.
    parent = path.parent.resolve()
    return any(parent == root or root in parent.parents for root in allowed_roots)


def _purge_inventory(project_root: Path) -> list[Path]:
    """Enumerate generator-owned derived files inside allowlisted roots."""
    targets: list[Path] = []
    for pattern in C5_PURGE_GLOBS:
        for path in project_root.glob(pattern):
            if (path.is_file() or path.is_symlink()) and _inside_allowed_roots(path, project_root):
                targets.append(path)
    return sorted(set(targets))


def _purge_relative_paths(project_root: Path, relative_paths: list[str]) -> None:
    """Deletes journaled derived files; refuses every path outside the allowlisted roots (all-or-nothing)."""
    targets = [project_root / rel for rel in relative_paths]
    escaped = [str(t) for t in targets if not _inside_allowed_roots(t, project_root)]
    if escaped:
        raise RecoveryRequiredError(f"Journal inventory escapes allowlisted roots: {escaped}")
    for target in targets:
        target.unlink(missing_ok=True)


def _recover_locked(canonical_path: Path) -> None:
    """Resolves COMMITTING journals (caller holds the lock).

    canonical == new hash: finish the purge idempotently and mark COMMITTED.
    canonical == old hash: the replace never happened, nothing was purged; mark ROLLED_BACK.
    neither: corruption; fail closed with RecoveryRequiredError.
    """
    journal_dir = canonical_path.parent / "journal"
    if not journal_dir.is_dir():
        return
    for journal_file in sorted(journal_dir.glob("*.json")):
        entry = json.loads(journal_file.read_text(encoding="utf-8"))
        if entry.get("state") != "COMMITTING":
            continue
        current = compute_revision_hash(load_structure(canonical_path))
        if current == entry["new_hash"]:
            _purge_relative_paths(_project_root(canonical_path), entry["invalidation_inventory"])
            _record_journal(canonical_path, entry["txn_id"], {**entry, "state": "COMMITTED"})
        elif current == entry["old_hash"]:
            _record_journal(canonical_path, entry["txn_id"], {**entry, "state": "ROLLED_BACK"})
        else:
            raise RecoveryRequiredError(
                f"Journal {entry['txn_id']} matches neither old nor new revision (canonical {current})"
            )


def recover_journals(canonical_path: str | Path) -> None:
    """Public entry point for readers/packagers: resolve unfinished journals under the lock."""
    canonical = Path(canonical_path)
    with _FileLock(canonical):
        _recover_locked(canonical)


def begin_transaction(canonical_path: str | Path, base_revision_hash: str) -> Transaction:
    """Recovers first, verifies the base hash under the lock, and opens a candidate workspace."""
    canonical = Path(canonical_path)
    with _FileLock(canonical):
        _recover_locked(canonical)
        data = _assert_canonical_matches(canonical, base_revision_hash)
        txn_id = str(uuid.uuid4())
        workspace = canonical.parent / "candidates" / txn_id
        workspace.mkdir(parents=True, exist_ok=False)
        candidate = workspace / "structure.json"
        _write_json_durably(candidate, data)
    return Transaction(txn_id, canonical, base_revision_hash, candidate)


def commit_transaction(txn: Transaction) -> None:
    """Commit-time CAS, journaled atomic replace of canonical, then purge of derived artifacts."""
    canonical = txn.canonical_path
    root = txn.project_root
    with _FileLock(canonical):
        _recover_locked(canonical)
        _assert_canonical_matches(canonical, txn.base_revision_hash)

        candidate = stamp_revision(load_structure(txn.candidate_path))
        _write_json_durably(txn.candidate_path, candidate)
        digest = hashlib.sha256(txn.candidate_path.read_bytes()).hexdigest()

        inventory = _purge_inventory(root)
        journal = {
            "txn_id": txn.txn_id,
            "state": "COMMITTING",
            "old_hash": txn.base_revision_hash,
            "new_hash": compute_revision_hash(candidate),
            "candidate_digest": digest,
            "invalidation_inventory": [str(p.relative_to(root)) for p in inventory],
        }
        _record_journal(canonical, txn.txn_id, journal)

        os.replace(txn.candidate_path, canonical)

        for path in inventory:
            path.unlink(missing_ok=True)

        _record_journal(canonical, txn.txn_id, {**journal, "state": "COMMITTED"})
        shutil.rmtree(txn.candidate_path.parent, ignore_errors=True)
