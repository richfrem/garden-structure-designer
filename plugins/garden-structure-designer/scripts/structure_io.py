import fcntl
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

from constants import C5_PURGE_GLOBS, C5_PURGE_ROOTS, ERROR_STALE_REVISION
from revision_identity import compute_revision_hash, stamp_revision

INPUT_SECTIONS = {
    "intent", "structure", "layout", "members", "roof",
    "hub", "bracing", "footings", "joinery"
}


def load_structure(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_structure(data: dict[str, Any], path: str | Path) -> None:
    data["meta"]["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def seal_section(data: dict[str, Any], section: str) -> None:
    if section not in data:
        raise KeyError(f"Section '{section}' not found in structure")
    data[section]["_sealed"] = True


def assert_not_sealed(data: dict[str, Any], section: str) -> None:
    if data.get(section, {}).get("_sealed"):
        raise RuntimeError(
            f"Section '{section}' is sealed — cannot overwrite. "
            "Downstream stages must not mutate upstream sections."
        )


def compute_source_hash(data: dict[str, Any]) -> str:
    payload = {k: data[k] for k in sorted(INPUT_SECTIONS) if k in data}
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


# --- C5 transaction authority ---


class StaleRevisionError(RuntimeError):
    """Raised when the canonical revision no longer matches the transaction base."""

    error_code = ERROR_STALE_REVISION


@dataclass(frozen=True)
class Transaction:
    txn_id: str
    canonical_path: Path
    base_revision_hash: str
    candidate_path: Path

    @property
    def project_root(self) -> Path:
        return _project_root(self.canonical_path)


def _project_root(canonical_path: Path) -> Path:
    """Canonical lives at <root>/context/staging/structure.json."""
    return canonical_path.parents[2]


def _journal_path(canonical_path: Path, txn_id: str) -> Path:
    return canonical_path.parent / "journal" / f"{txn_id}.json"


@contextmanager
def _FileLock(canonical_path: Path) -> Iterator[None]:
    """Exclusive interprocess lock keyed to the canonical structure path."""
    lock_path = canonical_path.with_name(canonical_path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "a+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def _write_json_durably(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(path.name + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)


def _record_journal(canonical_path: Path, txn_id: str, entry: dict[str, Any]) -> None:
    _write_json_durably(_journal_path(canonical_path, txn_id), entry)


def _assert_canonical_matches(canonical_path: Path, base_revision_hash: str) -> dict[str, Any]:
    data = load_structure(canonical_path)
    current_hash = compute_revision_hash(data)
    if current_hash != base_revision_hash:
        raise StaleRevisionError(
            f"Canonical revision {current_hash} != base {base_revision_hash}"
        )
    return data


def _purge_inventory(project_root: Path) -> list[Path]:
    """Enumerate generator-owned derived files inside allowlisted roots."""
    allowed_roots = [(project_root / rel).resolve() for rel in C5_PURGE_ROOTS]
    targets: list[Path] = []
    for pattern in C5_PURGE_GLOBS:
        for path in project_root.glob(pattern):
            if not (path.is_file() or path.is_symlink()):
                continue
            # Resolve the parent only: a symlink is removed itself, never its target.
            parent = path.parent.resolve()
            if any(parent == root or root in parent.parents for root in allowed_roots):
                targets.append(path)
    return sorted(set(targets))


def begin_transaction(canonical_path: str | Path, base_revision_hash: str) -> Transaction:
    canonical = Path(canonical_path)
    with _FileLock(canonical):
        data = _assert_canonical_matches(canonical, base_revision_hash)
        txn_id = str(uuid.uuid4())
        workspace = canonical.parent / "candidates" / txn_id
        workspace.mkdir(parents=True, exist_ok=False)
        candidate = workspace / "structure.json"
        _write_json_durably(candidate, data)
    return Transaction(txn_id, canonical, base_revision_hash, candidate)


def commit_transaction(txn: Transaction) -> None:
    canonical = txn.canonical_path
    root = txn.project_root
    with _FileLock(canonical):
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
