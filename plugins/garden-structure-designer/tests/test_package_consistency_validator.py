import sys
import pytest
from pathlib import Path

# Setup paths
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from package_consistency_validator import validate_package

def test_validate_package_unbound_local_shadowing():
    # Calling validate_package should execute successfully and return a list
    result = validate_package()
    assert isinstance(result, list)
