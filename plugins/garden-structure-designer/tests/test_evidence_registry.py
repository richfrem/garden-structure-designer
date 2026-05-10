
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from evidence_registry import add_evidence, load_registry

def test_evidence(tmp_path):
    import evidence_registry
    evidence_registry.get_registry_file = lambda: tmp_path / "ev.json"
    ev_id = add_evidence("test claim", "test.json")
    assert ev_id == "EV-0001"
    reg = load_registry()
    assert reg["evidence"][0]["claim"] == "test claim"
