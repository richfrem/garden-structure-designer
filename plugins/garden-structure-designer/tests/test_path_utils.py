
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from path_utils import staging_dir, outputs_dir

def test_path_resolution():
    assert "context/staging" in str(staging_dir()).replace('\\', '/')
    assert "outputs" in str(outputs_dir()).replace('\\', '/')


def test_outputs_dir_subfolder_support(monkeypatch, tmp_path):
    assert "18x12-pergola" in str(outputs_dir(subdir="18x12-pergola")).replace('\\', '/')

    monkeypatch.setenv("GSD_OUTPUT_SUBDIR", "custom-project")
    assert "custom-project" in str(outputs_dir()).replace('\\', '/')

