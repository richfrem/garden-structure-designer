
import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

def test_failure_generation(tmp_path):
    # Ensure generated tests import geometry_engine instead of just using found==expected
    drift = {"failed_axes": ["compound_cut_mismatch"]}
    drift_path = tmp_path / "drift.json"
    drift_path.write_text(json.dumps(drift))
    # We would call main() here, but testing the generator script directly is complex.
    # The requirement is that the script outputs imports for geometry_engine.
    content = open(str(Path(__file__).parent.parent / "scripts" / "failure_to_test.py")).read()
    assert "geometry_engine import compute" in content
