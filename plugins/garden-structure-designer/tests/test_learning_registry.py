
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

def test_registry_structure():
    content = open(str(Path(__file__).parent.parent / "scripts" / "lesson_curator.py")).read()
    assert "active_lessons" in content
