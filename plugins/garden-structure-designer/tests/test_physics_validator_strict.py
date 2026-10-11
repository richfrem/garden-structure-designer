"""Stage 3 screening validator: required inputs, no invented defaults, provenance and revision binding in the report."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from structural_physics_validator import validate  # type: ignore[import]  # noqa: E402

SCRIPTS = Path(__file__).parent.parent / "scripts"

MODEL = {
    "meta": {"schema_version": "2.0", "source_hash": "src-1", "revision_id": "rev-1", "revision_hash": "hash-1"},
    "layout": {"inscribed_radius_ft": 4.0},
    "members": {
        "posts": {"cut_length_ft": 8.0, "actual_width_in": 5.5, "actual_depth_in": 5.5},
        "beams": {"actual_width_in": 5.5, "actual_depth_in": 11.25},
    },
    "footings": {"diameter_in": 18},
    "roof": {},
}


def test_valid_model_passes_and_is_bound_to_the_revision():
    report = validate(MODEL)
    assert report["status"] == "PASS"
    assert (report["source_hash"], report["revision_id"], report["revision_hash"]) == ("src-1", "rev-1", "hash-1")
    assert {c["name"] for c in report["checks"]} == {"post_slenderness", "beam_deflection", "caisson_bearing"}


def test_inputs_used_are_recorded_for_provenance():
    inputs = validate(MODEL)["inputs"]
    assert inputs["post_length_in"] == 96.0 and inputs["caisson_diameter_in"] == 18.0 and inputs["span_ft"] == 4.0


@pytest.mark.parametrize(
    "path",
    [("footings", "diameter_in"), ("members", "posts", "cut_length_ft"), ("members", "posts", "actual_width_in"),
     ("members", "beams", "actual_depth_in"), ("layout", "inscribed_radius_ft")],
)
def test_missing_required_input_blocks_instead_of_defaulting(path):
    model = copy.deepcopy(MODEL)
    node = model
    for key in path[:-1]:
        node = node[key]
    del node[path[-1]]
    report = validate(model)
    assert report["status"] == "BLOCKED"
    assert report["checks"] == []
    assert ".".join(path) in " ".join(report["missing_inputs"])


def test_slender_post_fails():
    model = copy.deepcopy(MODEL)
    model["members"]["posts"]["cut_length_ft"] = 30.0  # 360 in / 5.5 in = 65 > 50
    report = validate(model)
    assert report["status"] == "FAIL"
    assert next(c for c in report["checks"] if c["name"] == "post_slenderness")["status"] == "FAIL"


def test_post_larger_than_caisson_fails_bearing():
    model = copy.deepcopy(MODEL)
    model["footings"]["diameter_in"] = 4
    assert next(c for c in validate(model)["checks"] if c["name"] == "caisson_bearing")["status"] == "FAIL"


def test_defaulted_pitch_requires_engineer_review():
    model = copy.deepcopy(MODEL)
    model["roof"]["pitch_defaulted"] = True
    report = validate(model)
    assert report["status"] == "REQUIRES_ENGINEER_REVIEW" and report["assumptions"]


def test_cli_exit_codes_and_report_file(tmp_path):
    path = tmp_path / "structure.json"
    path.write_text(json.dumps(MODEL))
    ok = subprocess.run([sys.executable, str(SCRIPTS / "structural_physics_validator.py"), str(path)], capture_output=True, text=True)
    assert ok.returncode == 0 and json.loads((tmp_path / "physics-validation-report.json").read_text())["status"] == "PASS"
    broken = copy.deepcopy(MODEL)
    del broken["footings"]
    path.write_text(json.dumps(broken))
    bad = subprocess.run([sys.executable, str(SCRIPTS / "structural_physics_validator.py"), str(path)], capture_output=True, text=True)
    assert bad.returncode == 1
