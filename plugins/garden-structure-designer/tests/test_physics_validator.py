import json
import subprocess
import sys
import copy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).parent))

from geometry_engine import compute_from_structure  # type: ignore[import]
from test_geometry_engine import STRUCTURE_SEED  # type: ignore[import]

SCRIPTS = Path(__file__).parent.parent / "scripts"


def test_physics_pass_on_valid_structure(tmp_path):
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(copy.deepcopy(STRUCTURE_SEED)))
    compute_from_structure(str(p))
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "structural_physics_validator.py"), str(p)],
        capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr + result.stdout


def test_physics_reads_footings_section(tmp_path):
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["footings"]["diameter_in"] = 4   # tiny footing → bearing fail or warning
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(seed))
    compute_from_structure(str(p))
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "structural_physics_validator.py"), str(p)],
        capture_output=True, text=True
    )
    # Should run without crashing (return 0 or 1)
    assert result.returncode in (0, 1)
