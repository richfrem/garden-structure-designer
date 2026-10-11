"""Tests for the C5 transaction authority in structure_io.py (TASK-M3)."""
import json
import multiprocessing
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from revision_identity import compute_revision_hash, stamp_revision  # type: ignore[import]  # noqa: E402
from structure_io import (  # type: ignore[import]  # noqa: E402
    StaleRevisionError,
    begin_transaction,
    commit_transaction,
)

BASE = {
    "meta": {"schema_version": "2.0", "lifecycle": "INTENT"},
    "layout": {"post_count": 6},
}

PURGE_FILES = [
    "context/staging/structural-model.json",
    "context/staging/geometry-calculations.json",
    "context/staging/drawing-red-team-report.json",
    "outputs/drawing-plan.svg",
    "outputs/blueprint-elevation.svg",
    "outputs/cad/SB01.dxf",
    "outputs/cad/SB02.dxf",
    "outputs/fabrication/cut-list.json",
    "outputs/pergola_plan.md",
    "outputs/pergola_plan.pdf",
    "outputs/quality-dashboard.md",
    # C5 families that were missing from the inventory
    "context/staging/physics-validation-report.json",
    "context/staging/visual-smoke-report.json",
    "context/staging/drawing-content-report.json",
    "context/staging/schema-validation-report.json",
    "outputs/assembly-guide.md",
    "outputs/budget-estimate.md",
    "outputs/lumber-purchase-list.md",
    "outputs/pergola_plan_embedded.md",
    "outputs/pergola_plan_embedded.pdf",
    "outputs/package-manifest.json",
    "outputs/drawing-red-team-report.md",
    "outputs/visual-smoke-report.md",
    "outputs/shop-blueprint/SB01-cut-list.json",
    "outputs/visual-smoke/plan.png",
    "outputs/high-resolution-image/pergola_render_1.png",
]
KEEP_FILES = ["outputs/run-insights.json"]  # archived audit evidence is never purged


@pytest.fixture
def canonical(tmp_path):
    path = tmp_path / "context" / "staging" / "structure.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(stamp_revision(BASE)))
    return path


def _populate_derived(root: Path) -> None:
    for rel in PURGE_FILES:
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("stale")


def _base_hash(path: Path) -> str:
    return compute_revision_hash(json.loads(path.read_text()))


def _edit_candidate(txn, post_count: int) -> None:
    data = json.loads(txn.candidate_path.read_text())
    data["layout"]["post_count"] = post_count
    txn.candidate_path.write_text(json.dumps(data))


def test_begin_validate_commit_success(canonical):
    old_hash = _base_hash(canonical)
    txn = begin_transaction(canonical, old_hash)

    assert txn.candidate_path.parent.name == txn.txn_id
    assert txn.candidate_path.parent.parent.name == "candidates"
    assert txn.candidate_path.exists()

    _edit_candidate(txn, 8)
    commit_transaction(txn)

    committed = json.loads(canonical.read_text())
    assert committed["layout"]["post_count"] == 8
    assert committed["meta"]["revision_id"] != json.loads(
        json.dumps(stamp_revision(BASE))
    )["meta"]["revision_id"]
    assert _base_hash(canonical) != old_hash
    assert not txn.candidate_path.parent.exists()


def test_commit_journal_marked_committed(canonical):
    txn = begin_transaction(canonical, _base_hash(canonical))
    commit_transaction(txn)
    journals = list((canonical.parent / "journal").glob("*.json"))
    assert len(journals) == 1
    entry = json.loads(journals[0].read_text())
    assert entry["state"] == "COMMITTED"
    assert entry["txn_id"] == txn.txn_id
    assert len(entry["candidate_digest"]) == 64
    assert entry["old_hash"] != entry["new_hash"]


def test_begin_rejects_stale_base_hash(canonical):
    with pytest.raises(StaleRevisionError) as exc:
        begin_transaction(canonical, "0" * 64)
    assert exc.value.error_code == "STALE_REVISION"


def test_commit_rejects_when_canonical_changed(canonical):
    txn = begin_transaction(canonical, _base_hash(canonical))
    canonical.write_text(json.dumps(stamp_revision({**BASE, "layout": {"post_count": 4}})))
    before = canonical.read_text()

    with pytest.raises(StaleRevisionError) as exc:
        commit_transaction(txn)
    assert exc.value.error_code == "STALE_REVISION"
    assert canonical.read_text() == before


def test_two_writers_second_gets_stale_revision(canonical):
    base = _base_hash(canonical)
    txn_a = begin_transaction(canonical, base)
    txn_b = begin_transaction(canonical, base)
    _edit_candidate(txn_a, 8)
    _edit_candidate(txn_b, 10)

    commit_transaction(txn_a)
    winner = canonical.read_text()
    with pytest.raises(StaleRevisionError) as exc:
        commit_transaction(txn_b)
    assert exc.value.error_code == "STALE_REVISION"
    assert canonical.read_text() == winner
    assert json.loads(winner)["layout"]["post_count"] == 8


def test_failed_commit_does_not_purge_current_artifacts(canonical):
    base = _base_hash(canonical)
    txn_a = begin_transaction(canonical, base)
    txn_b = begin_transaction(canonical, base)
    commit_transaction(txn_a)
    _populate_derived(canonical.parents[2])

    with pytest.raises(StaleRevisionError):
        commit_transaction(txn_b)
    for rel in PURGE_FILES:
        assert (canonical.parents[2] / rel).exists(), rel


def test_commit_purges_full_c5_inventory(canonical):
    root = canonical.parents[2]
    _populate_derived(root)
    keep_input = root / "context" / "staging" / "notes.txt"
    keep_input.write_text("user input")
    for rel in KEEP_FILES:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text("archived evidence")

    txn = begin_transaction(canonical, _base_hash(canonical))
    commit_transaction(txn)

    for rel in PURGE_FILES:
        assert not (root / rel).exists(), rel
    assert all((root / rel).exists() for rel in KEEP_FILES)
    assert canonical.exists()
    assert keep_input.exists()


def test_purge_does_not_follow_symlinks_out_of_roots(canonical, tmp_path_factory):
    root = canonical.parents[2]
    outside = tmp_path_factory.mktemp("outside") / "victim.svg"
    outside.write_text("precious")
    (root / "outputs").mkdir()
    (root / "outputs" / "escape.svg").symlink_to(outside)

    commit_transaction(begin_transaction(canonical, _base_hash(canonical)))
    assert outside.read_text() == "precious"


def _race_worker(canonical_str, base_hash, post_count, queue):
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    from structure_io import StaleRevisionError as Stale, begin_transaction as begin, commit_transaction as commit

    try:
        txn = begin(canonical_str, base_hash)
        data = json.loads(txn.candidate_path.read_text())
        data["layout"]["post_count"] = post_count
        txn.candidate_path.write_text(json.dumps(data))
        commit(txn)
        queue.put("OK")
    except Stale as exc:
        queue.put(exc.error_code)


def test_multiprocess_race_exactly_one_winner(canonical):
    ctx = multiprocessing.get_context("spawn")
    queue = ctx.Queue()
    base = _base_hash(canonical)
    procs = [
        ctx.Process(target=_race_worker, args=(str(canonical), base, n, queue))
        for n in (8, 10)
    ]
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join(30)
    results = sorted(queue.get(timeout=5) for _ in procs)
    assert results == ["OK", "STALE_REVISION"]
