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
SCHEMAS = Path(__file__).parent.parent / "schemas"


def test_validates_valid_structure(tmp_path):
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(copy.deepcopy(STRUCTURE_SEED)))
    compute_from_structure(str(p))
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "schema_validator.py"),
         str(tmp_path), str(SCHEMAS), "--strict"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr + result.stdout


def test_rejects_missing_required_field(tmp_path):
    seed = {"meta": {"schema_version": "2.0", "lifecycle": "INTENT", "source_hash": "x"}}
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(seed))
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "schema_validator.py"),
         str(tmp_path), str(SCHEMAS), "--strict"],
        capture_output=True, text=True
    )
    assert result.returncode != 0 or "FAIL" in result.stdout


def test_member_counts_match_sections(tmp_path):
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(copy.deepcopy(STRUCTURE_SEED)))
    compute_from_structure(str(p))
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "schema_validator.py"),
         str(tmp_path), str(SCHEMAS), "--strict"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
