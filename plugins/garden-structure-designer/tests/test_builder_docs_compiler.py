"""Builder docs derive from structure.json + outputs/fabrication/cut-list.json (no legacy SB01 cut list, no silent defaults)."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from builder_docs_compiler import (  # type: ignore[import]  # noqa: E402
    generate_assembly_guide,
    generate_budget_estimate,
    generate_builder_docs,
    generate_lumber_purchase_list,
)


def _structure(sides: int = 6, braces: bool = True) -> dict:
    return {
        "intent": {"jurisdiction": "BC_Vancouver_Island"},
        "structure": {"type": "pergola", "sides": sides},
        "layout": {"shape": "hexagon" if sides == 6 else "polygon", "post_count": sides},
        "members": {
            "posts": {"nominal_size": "6x6", "actual_width_in": 5.5, "actual_depth_in": 5.5, "cut_length_ft": 8.0},
            "beams": {"nominal_size": "6x12", "actual_width_in": 5.5, "actual_depth_in": 11.25, "cut_length_ft": 10.0},
        },
        "roof": {"primary_rafters": {"nominal_size": "4x6", "actual_width_in": 3.5, "actual_depth_in": 5.5}},
        "hub": {"type": "hexagonal_prism"},
        "footings": {"diameter_in": 12, "depth_in": 24, "concrete_grade": "20MPa"},
        "bracing": {
            "enabled": braces,
            "brace": {"nominal_size": "4x4", "actual_width_in": 3.5, "actual_depth_in": 3.5, "count_per_post": 2},
        },
        "geometry": {
            "compound_cut": {"miter_deg": 28.71, "bevel_deg": 9.10},
            "beam_ring": {"beam_miter_deg": 30.0},
        },
    }


def _cut_list(sides: int = 6, braces: bool = True) -> dict:
    def member(mid, role, cut, order):
        return {"id": mid, "role": role, "stock": {"cut_length_ft": cut, "order_length_ft": order}}

    members = [member(f"P{i}", "post", 8.0, 10) for i in range(1, sides + 1)]
    members += [member(f"B{i}", "beam", 10.0, 12) for i in range(1, sides + 1)]
    members += [member(f"R{i}", "rafter_primary", 8.5, 10) for i in range(1, sides + 1)]
    if braces:
        members += [member(f"Brace{i}{s}", "brace", 2.2, 8) for i in range(1, sides + 1) for s in "ab"]
    return {"schema": "garden-structure-designer/fabrication-cut-list/1.0", "members": members}


@pytest.fixture
def workspace(tmp_path):
    staging, outputs = tmp_path / "context" / "staging", tmp_path / "outputs"
    (outputs / "fabrication").mkdir(parents=True)
    staging.mkdir(parents=True)
    (staging / "structure.json").write_text(json.dumps(_structure()))
    (outputs / "fabrication" / "cut-list.json").write_text(json.dumps(_cut_list()))
    return tmp_path


def _run(root: Path) -> dict:
    return generate_builder_docs(staging_dir=root / "context" / "staging", outputs_dir=root / "outputs")


def _edit_structure(root: Path, mutate) -> None:
    path = root / "context" / "staging" / "structure.json"
    data = json.loads(path.read_text())
    mutate(data)
    path.write_text(json.dumps(data))


def test_missing_cut_list_fails(workspace):
    (workspace / "outputs" / "fabrication" / "cut-list.json").unlink()
    result = _run(workspace)
    assert result["status"] == "FAIL"
    assert "cut-list.json missing" in result["reason"]


def test_generate_builder_docs_success(workspace):
    result = _run(workspace)
    assert result["status"] == "COMPLETE"
    outputs = workspace / "outputs"
    guide = (outputs / "assembly-guide.md").read_text(encoding="utf-8")
    assert "Phase 4.3 — Tripod-First Hub and Rafter Hoisting" in guide
    assert "28.71°" in guide
    assert "three alternating" in guide
    assert (outputs / "budget-estimate.md").exists() and (outputs / "lumber-purchase-list.md").exists()


def test_board_feet_derived_from_section_and_cut_list(workspace):
    _run(workspace)
    text = (workspace / "outputs" / "lumber-purchase-list.md").read_text(encoding="utf-8")
    # 6 posts: (5.5*5.5/12)*8.0 = 20.17 BF each -> 121.00 BF
    assert "| Posts | 6x6 | 6 | 8.00' | 10.0' | 121.00 |" in text
    assert "| Knee Braces | 4x4 | 12 |" in text
    assert "Total Board Feet" in text


@pytest.mark.parametrize(
    "mutate,needle",
    [
        (lambda d: d["geometry"].pop("compound_cut"), "geometry.compound_cut"),
        (lambda d: d["geometry"]["beam_ring"].pop("beam_miter_deg"), "geometry.beam_ring.beam_miter_deg"),
        (lambda d: d["intent"].pop("jurisdiction"), "intent.jurisdiction"),
        (lambda d: d["structure"].pop("sides"), "structure.sides"),
        (lambda d: d["members"]["posts"].pop("nominal_size"), "members.posts.nominal_size"),
        (lambda d: d["roof"]["primary_rafters"].pop("actual_depth_in"), "roof.primary_rafters.actual_depth_in"),
    ],
)
def test_missing_structural_inputs_fail_closed(workspace, mutate, needle):
    """No silent structural defaults (AGENTS data-driven rule)."""
    _edit_structure(workspace, mutate)
    result = _run(workspace)
    assert result["status"] == "FAIL"
    assert needle in result["reason"]


def test_enabled_bracing_without_brace_members_fails(tmp_path):
    staging, outputs = tmp_path / "context" / "staging", tmp_path / "outputs"
    (outputs / "fabrication").mkdir(parents=True)
    staging.mkdir(parents=True)
    (staging / "structure.json").write_text(json.dumps(_structure(braces=True)))
    (outputs / "fabrication" / "cut-list.json").write_text(json.dumps(_cut_list(braces=False)))
    result = generate_builder_docs(staging_dir=staging, outputs_dir=outputs)
    assert result["status"] == "FAIL" and "brace" in result["reason"]


def test_assembly_guide_rafter_count_follows_sides():
    guide = generate_assembly_guide(_structure(sides=9), _cut_list(sides=9))
    assert "all 9 rafters" in guide and "six" not in guide.lower()


def test_assembly_guide_tripod_only_when_sides_divisible_by_three():
    guide = generate_assembly_guide(_structure(sides=8), _cut_list(sides=8))
    assert "Tripod-First" not in guide
    assert "Phase 4.3 — Balanced Hub and Rafter Hoisting" in guide


def test_budget_discloses_rate_assumptions():
    text = generate_budget_estimate(_structure(), _cut_list())
    assert "LABOR EXCLUSION" in text and "Default Rate Basis" in text


def test_lumber_list_hardware_counts_follow_cut_list():
    text = generate_lumber_purchase_list(_structure(sides=8), _cut_list(sides=8))
    assert "(Qty: 8)" in text


def test_lumber_list_uses_schema_jurisdiction_and_declared_footing_size():
    text = generate_lumber_purchase_list(_structure(), _cut_list())
    assert "BC_Vancouver_Island" in text
    assert '12" diameter' in text
    assert '18" diameter' not in text
