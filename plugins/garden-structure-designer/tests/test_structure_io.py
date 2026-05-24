import json
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from structure_io import (
    load_structure, save_structure, seal_section,
    assert_not_sealed, compute_source_hash
)

MINIMAL = {
    "meta": {"schema_version": "2.0", "lifecycle": "INTENT",
             "source_hash": "", "created_at": "2026-01-01T00:00:00Z",
             "updated_at": "2026-01-01T00:00:00Z"},
    "intent": {"jurisdiction": "BC_SAANICH"},
    "structure": {"type": "pergola", "shape": "hexagon", "sides": 6},
    "layout": {"post_count": 6, "inscribed_radius_ft": 4.875},
    "geometry": {"_sealed": False},
}

def test_load_structure(tmp_path):
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(MINIMAL))
    data = load_structure(p)
    assert data["meta"]["schema_version"] == "2.0"

def test_save_structure_updates_timestamp(tmp_path):
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(MINIMAL))
    data = load_structure(p)
    old_ts = data["meta"]["updated_at"]
    import time; time.sleep(0.01)
    save_structure(data, p)
    data2 = load_structure(p)
    assert data2["meta"]["updated_at"] != old_ts

def test_seal_section():
    data = json.loads(json.dumps(MINIMAL))
    seal_section(data, "geometry")
    assert data["geometry"]["_sealed"] is True

def test_seal_section_raises_on_missing():
    data = json.loads(json.dumps(MINIMAL))
    with pytest.raises(KeyError):
        seal_section(data, "nonexistent")

def test_assert_not_sealed_passes_on_unsealed():
    data = json.loads(json.dumps(MINIMAL))
    assert_not_sealed(data, "geometry")  # no raise

def test_assert_not_sealed_raises_on_sealed():
    data = json.loads(json.dumps(MINIMAL))
    data["geometry"]["_sealed"] = True
    with pytest.raises(RuntimeError, match="sealed"):
        assert_not_sealed(data, "geometry")

def test_compute_source_hash_is_deterministic():
    data = json.loads(json.dumps(MINIMAL))
    h1 = compute_source_hash(data)
    h2 = compute_source_hash(data)
    assert h1 == h2
    assert len(h1) == 64  # sha256 hex

def test_compute_source_hash_changes_when_input_changes():
    data = json.loads(json.dumps(MINIMAL))
    h1 = compute_source_hash(data)
    data["layout"]["post_count"] = 8
    h2 = compute_source_hash(data)
    assert h1 != h2
