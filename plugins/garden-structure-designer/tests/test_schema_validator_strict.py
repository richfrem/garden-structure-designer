
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

def test_schema_strict():
    content = open(str(Path(__file__).parent.parent / "scripts" / "schema_validator.py")).read()
    assert "--strict" in content
