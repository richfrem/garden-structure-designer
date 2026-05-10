
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from error_classifier import classify_failure

def test_classification():
    cls = classify_failure("miter and beam")
    assert cls["classification"] == "beam_miter_mismatch"
    cls2 = classify_failure("schema invalid")
    assert cls2["classification"] == "schema_error"
