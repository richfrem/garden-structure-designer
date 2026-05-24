import json
import copy
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).parent))

from geometry_engine import compute_from_structure  # type: ignore[import]
from cad_scene import build_structure_scene, validate_scene_geometry  # type: ignore[import]
from test_geometry_engine import STRUCTURE_SEED  # type: ignore[import]


def _seeded_structure(tmp_path):
    p = tmp_path / "structure.json"
    p.write_text(json.dumps(copy.deepcopy(STRUCTURE_SEED)))
    compute_from_structure(str(p))
    return json.loads(p.read_text())


def test_build_creates_correct_post_count(tmp_path):
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    posts = [so for so in scene.solids if so.role == "post"]
    assert len(posts) == s["layout"]["post_count"]


def test_hub_radius_matches_geometry_section(tmp_path):
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    assert abs(scene.hub_r - s["geometry"]["hub_radius_ft"]) < 0.001


def test_validate_scene_passes(tmp_path):
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    validate_scene_geometry(scene)  # must not raise


def test_post_top_equals_beam_bottom(tmp_path):
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    beam_depth_ft = s["members"]["beams"]["actual_depth_in"] / 12.0
    assert abs(scene.Z_POST_TOP - (scene.Z_BEAM_TOP - beam_depth_ft)) < 0.001


def test_no_zero_length_members(tmp_path):
    import math
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    for solid in scene.solids:
        length = math.sqrt(sum((a - b) ** 2 for a, b in zip(solid.p1, solid.p0)))
        assert length > 1e-6, f"Zero-length member: {solid.tag}"


def test_footing_count_matches_post_count(tmp_path):
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    footings = [so for so in scene.solids if so.role == "footing"]
    assert len(footings) == s["layout"]["post_count"]


def test_rafters_trimmed_at_hub(tmp_path):
    """Verify that rafters are correctly trimmed by hub planes."""
    import math
    s = _seeded_structure(tmp_path)
    scene = build_structure_scene(s)
    hub_r = s["geometry"]["hub_radius_ft"]
    # We expect rafters to end at the hub face, which is slightly further than hub_r
    rafters = [so for so in scene.solids if so.role == "rafter" and so.tag.startswith("R")]
    for r in rafters:
        # Distance from center in XY to p1 (apex end)
        dist = math.sqrt(r.p1[0]**2 + r.p1[1]**2)
        # Should be exactly at hub face radius (which is slightly > hub_r for polygon but approx hub_r)
        assert dist >= hub_r - 0.01
        assert dist <= hub_r * 1.2 # Allow for polygon corner
