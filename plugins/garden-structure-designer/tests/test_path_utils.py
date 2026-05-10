
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from path_utils import staging_dir, outputs_dir

def test_path_resolution():
    assert "context/staging" in str(staging_dir()).replace('\\', '/')
    assert "outputs" in str(outputs_dir()).replace('\\', '/')
