"""C5 recovery, portable locking and atomic canonical writes for structure_io.py."""
from __future__ import annotations

import importlib.util
import json
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from test_transaction_gateway import PURGE_FILES, _base_hash, _populate_derived, canonical  # type: ignore[import]  # noqa: E402,F401
import structure_io  # type: ignore[import]  # noqa: E402
from revision_identity import compute_revision_hash  # type: ignore[import]  # noqa: E402

SCRIPTS = Path(__file__).parent.parent / "scripts"


def _write_committing_journal(canonical_path: Path, old_hash: str, new_hash: str, inventory=PURGE_FILES) -> Path:
    journal = canonical_path.parent / "journal" / "crashed-txn.json"
    journal.parent.mkdir(parents=True, exist_ok=True)
    journal.write_text(json.dumps({
        "txn_id": "crashed-txn", "state": "COMMITTING", "old_hash": old_hash, "new_hash": new_hash,
        "candidate_digest": "0" * 64, "invalidation_inventory": list(inventory),
    }))
    return journal


def _state(journal: Path) -> str:
    return json.loads(journal.read_text())["state"]


def test_crash_before_replace_rolls_back_and_keeps_artifacts(canonical):
    _populate_derived(canonical.parents[2])
    old = _base_hash(canonical)
    journal = _write_committing_journal(canonical, old, "f" * 64)
    structure_io.recover_journals(canonical)
    assert _state(journal) == "ROLLED_BACK"
    assert all((canonical.parents[2] / rel).exists() for rel in PURGE_FILES)
    structure_io.begin_transaction(canonical, old)  # canonical is usable again


def test_crash_after_replace_finishes_purge_idempotently(canonical):
    root = canonical.parents[2]
    _populate_derived(root)
    old = _base_hash(canonical)
    data = json.loads(canonical.read_text())
    data["layout"]["post_count"] = 8
    new_data = structure_io.stamp_revision(data)
    canonical.write_text(json.dumps(new_data))
    journal = _write_committing_journal(canonical, old, compute_revision_hash(new_data))
    structure_io.recover_journals(canonical)
    structure_io.recover_journals(canonical)  # idempotent
    assert _state(journal) == "COMMITTED"
    assert not any((root / rel).exists() for rel in PURGE_FILES)


def test_neither_old_nor_new_fails_closed(canonical):
    _populate_derived(canonical.parents[2])
    journal = _write_committing_journal(canonical, "a" * 64, "b" * 64)
    with pytest.raises(structure_io.RecoveryRequiredError):
        structure_io.begin_transaction(canonical, _base_hash(canonical))
    assert _state(journal) == "COMMITTING"
    assert all((canonical.parents[2] / rel).exists() for rel in PURGE_FILES)


def test_recovery_refuses_inventory_path_escape(canonical, tmp_path):
    outside = tmp_path / "outside.txt"
    outside.write_text("keep")
    root = canonical.parents[2]
    old = _base_hash(canonical)
    data = structure_io.stamp_revision(json.loads(canonical.read_text()))
    canonical.write_text(json.dumps(data))
    _write_committing_journal(canonical, old, compute_revision_hash(data), inventory=["../outside.txt"])
    with pytest.raises(structure_io.RecoveryRequiredError):
        structure_io.recover_journals(canonical)
    assert outside.read_text() == "keep" and root.exists()


def test_file_lock_has_windows_implementation_without_fcntl(monkeypatch, tmp_path):
    """C3/C5: the module must import and lock on platforms without fcntl (Windows) via msvcrt."""
    calls = []
    fake = types.SimpleNamespace(LK_LOCK=1, LK_UNLCK=0, locking=lambda fd, mode, nbytes: calls.append(mode))
    monkeypatch.setitem(sys.modules, "fcntl", None)
    monkeypatch.setitem(sys.modules, "msvcrt", fake)
    spec = importlib.util.spec_from_file_location("structure_io_win", SCRIPTS / "structure_io.py")
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, "structure_io_win", module)
    spec.loader.exec_module(module)
    with module._FileLock(tmp_path / "s.json"):
        pass
    assert calls == [1, 0]


def test_save_structure_is_atomic(tmp_path, monkeypatch):
    """A failure while serializing must leave the previous canonical file intact."""
    path = tmp_path / "structure.json"
    path.write_text(json.dumps({"meta": {}, "keep": True}))

    def boom(*args, **kwargs):
        raise RuntimeError("disk full")

    monkeypatch.setattr(structure_io.json, "dump", boom)
    with pytest.raises(RuntimeError):
        structure_io.save_structure({"meta": {}, "keep": False}, path)
    assert json.loads(path.read_text())["keep"] is True
