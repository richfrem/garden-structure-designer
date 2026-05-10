
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from run_history import should_halt

def test_repair_logic():
    # Test that repeated identical failures halt
    assert not should_halt("test_script.py", "unknown_axis", 3)
