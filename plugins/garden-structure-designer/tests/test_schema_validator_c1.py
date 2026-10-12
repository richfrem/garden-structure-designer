"""C1 schema properties (topology family, revision identity) and the schema validator's report binding."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from test_geometry_engine import STRUCTURE_SEED  # type: ignore[import]  # noqa: E402

PLUGIN = Path(__file__).parent.parent
SCHEMA = json.loads((PLUGIN / "assets" / "schemas" / "structure.schema.json").read_text())
SCRIPT = PLUGIN / "scripts" / "schema_validator.py"


def _seed(**meta):
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["meta"].update(meta)
    return seed


def test_seed_is_schema_valid():
    jsonschema.validate(_seed(), SCHEMA)


@pytest.mark.parametrize("family", ["RadialHubTopology", "OrthogonalGridTopology", "HipRidgeTopology"])
def test_known_topology_families_are_accepted(family):
    jsonschema.validate(_seed(topology_family=family), SCHEMA)


def test_unknown_topology_family_is_rejected():
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(_seed(topology_family="Dome"), SCHEMA)


def test_revision_identity_fields_are_typed():
    jsonschema.validate(_seed(revision_id="0b1c2d3e-0000-4000-8000-000000000000", revision_hash="a" * 64), SCHEMA)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(_seed(revision_hash="not-a-hash"), SCHEMA)


def _run(tmp_path, structure, *extra):
    staging = tmp_path / "staging"
    staging.mkdir(exist_ok=True)
    (staging / "structure.json").write_text(json.dumps(structure))
    out = tmp_path / "report.json"
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(staging), str(PLUGIN / "assets" / "schemas"), "--json-output", str(out), *extra],
        capture_output=True, text=True,
    )
    return proc, json.loads(out.read_text())


def test_report_is_bound_to_source_hash_and_revision(tmp_path):
    structure = _seed(revision_id="rev-1", revision_hash="b" * 64)
    proc, report = _run(tmp_path, structure)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert report["source_hash"] == structure["meta"]["source_hash"]
    assert report["revision_id"] == "rev-1" and report["revision_hash"] == "b" * 64


def test_invalid_family_fails_the_run(tmp_path):
    proc, report = _run(tmp_path, _seed(topology_family="Dome"))
    assert proc.returncode == 1 and report["status"] == "FAIL"


def test_member_count_invariant_still_enforced(tmp_path):
    structure = _seed()
    structure["invariants"] = {"member_counts_match_sections": True}
    structure["roof"]["primary_rafters"]["count"] = structure["layout"]["post_count"] + 1
    proc, report = _run(tmp_path, structure)
    assert proc.returncode == 1 and any(f.get("check") == "member_counts_match_sections" for f in report["files"])


def test_unknown_top_level_key_fails_schema_validation(tmp_path):
    """The root schema forbids unknown keys, so this fails before --strict could merely warn."""
    structure = _seed()
    structure["mystery"] = 1
    proc, report = _run(tmp_path, structure, "--strict")
    assert proc.returncode == 1 and report["status"] == "FAIL"
