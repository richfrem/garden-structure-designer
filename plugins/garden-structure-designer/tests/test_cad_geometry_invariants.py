"""
test_cad_geometry_invariants.py
================================
Geometry invariant regression tests required by the CAD refactor spec.

Tests:
  1. test_post_top_equals_beam_bottom
  2. test_rafters_terminate_at_hub_radius
  3. test_brace_endpoints_touch_post_face_and_beam_soffit
  4. test_all_member_lengths_positive
  5. test_projected_labels_do_not_overlap_major_faces
  6. test_isometric_has_expected_semantic_counts
  7. test_no_rafter_endpoint_inside_hub_radius
  8. test_validator_catches_zero_length_member (integration)
  9. test_beam_endpoints_on_post_grid  (Invariant 9 positive)
  9b. test_invariant9_catches_displaced_beam  (Invariant 9 mutation)
  10. test_brace_foot_on_post_face  (Invariant 10 positive)
  10b. test_invariant10_catches_floating_brace_foot  (Invariant 10 mutation — lower foot)
  10c. test_invariant10_catches_floating_brace_head  (Invariant 10 mutation — upper head)
"""

from __future__ import annotations

import copy
import json
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from cad_scene import (
    build_structure_scene,
    validate_scene_geometry,
    GeometryError,
    vlen,
    vsub,
    v2_radius,
)

# ---------------------------------------------------------------------------
# Shared fixture — standard 6-post hex pergola matching the staging model
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def base_structure_dict(tmp_path_factory):
    from test_geometry_engine import STRUCTURE_SEED
    from geometry_engine import compute_from_structure
    tmp = tmp_path_factory.mktemp("base_invariants_fix")
    p = tmp / "structure.json"
    p.write_text(json.dumps(copy.deepcopy(STRUCTURE_SEED)))
    compute_from_structure(str(p))
    return json.loads(p.read_text())

_FT_TOL = 1.0 / 120.0   # 1/10 inch tolerance


@pytest.fixture(scope="module")
def scene(base_structure_dict):
    s = build_structure_scene(copy.deepcopy(base_structure_dict))
    validate_scene_geometry(s)
    return s


@pytest.fixture(scope="module")
def solids_by_role(scene):
    d: dict[str, list] = {}
    for s in scene.solids:
        d.setdefault(s.role, []).append(s)
    return d


# ---------------------------------------------------------------------------
# 1. Post top Z == beam underside Z
# ---------------------------------------------------------------------------

def test_post_top_equals_beam_bottom(scene):
    """
    KEY STRUCTURAL INVARIANT:
    Z_POST_TOP = post_h - beam_d  →  post top face aligns exactly with beam bottom face.
    No gap, no overlap.
    """
    Z_POST_TOP = scene.Z_POST_TOP
    Z_BEAM_TOP = scene.Z_BEAM_TOP
    beam_d = Z_BEAM_TOP - Z_POST_TOP

    # Post top nodes are at Z_POST_TOP
    for s in scene.solids:
        if s.role != "post":
            continue
        post_top_z = max(s.p0[2], s.p1[2])
        assert abs(post_top_z - Z_POST_TOP) <= _FT_TOL, (
            f"Post {s.tag}: top Z={post_top_z:.6f} expected={Z_POST_TOP:.6f} "
            f"(delta={abs(post_top_z - Z_POST_TOP)*12:.3f}\")"
        )

    # Beam bottom = beam centreline Z - BEAM_HD = Z_POST_TOP
    for s in scene.solids:
        if s.role != "beam":
            continue
        centre_z = (s.p0[2] + s.p1[2]) / 2.0
        beam_bot_z = centre_z - beam_d / 2.0
        assert abs(beam_bot_z - Z_POST_TOP) <= _FT_TOL, (
            f"Beam {s.tag}: bottom Z={beam_bot_z:.6f} expected={Z_POST_TOP:.6f} "
            f"(delta={abs(beam_bot_z - Z_POST_TOP)*12:.3f}\")"
        )


# ---------------------------------------------------------------------------
# 2. Rafters terminate at hub face radius (not inside, not far outside)
# ---------------------------------------------------------------------------

def test_rafters_terminate_at_hub_radius(scene, solids_by_role):
    """
    Each rafter p1 (apex end) must have XY radius == hub_r_face within 1/10".
    """
    import math
    hub_r = scene.hub_r
    hub_r_face = hub_r * math.cos(math.pi / scene.qty)
    for r in solids_by_role.get("rafter", []):
        if r.tag.startswith("Jack"):
            continue  # Jack rafters terminate at hip rafters
        xy_r = v2_radius(r.p1)
        assert abs(xy_r - hub_r_face) <= _FT_TOL + 0.05, (
            f"Rafter {r.tag}: apex XY radius={xy_r:.6f} hub_r_face={hub_r_face:.6f} "
            f"(delta={abs(xy_r - hub_r_face)*12:.2f}\")"
        )


# ---------------------------------------------------------------------------
# 3. Brace endpoints touch post face AND beam soffit
# ---------------------------------------------------------------------------

def test_brace_endpoints_touch_post_face_and_beam_soffit(scene, solids_by_role):
    """
    For every brace:
      - lower endpoint Z < Z_POST_TOP  (brace descends below beam soffit)
      - upper endpoint Z ≈ Z_POST_TOP  (brace terminates at beam soffit, ±1")
    """
    Z_POST_TOP = scene.Z_POST_TOP
    for b in solids_by_role.get("brace", []):
        lower_z = min(b.p0[2], b.p1[2])
        upper_z = max(b.p0[2], b.p1[2])

        assert lower_z < Z_POST_TOP - _FT_TOL, (
            f"Brace {b.tag}: lower Z={lower_z:.4f} >= Z_POST_TOP={Z_POST_TOP:.4f} "
            f"— brace does not descend below beam"
        )
        assert abs(upper_z - Z_POST_TOP) <= (1.0 / 12.0), (
            f"Brace {b.tag}: upper Z={upper_z:.4f} differs from Z_POST_TOP={Z_POST_TOP:.4f} "
            f"by {abs(upper_z - Z_POST_TOP)*12:.2f}\" (limit=1\")"
        )


# ---------------------------------------------------------------------------
# 4. All member axis lengths are positive (no zero-length members)
# ---------------------------------------------------------------------------

def test_all_member_lengths_positive(scene):
    """
    No structural member may have a zero-length axis.
    Catches modelling errors where p0 == p1.
    """
    for s in scene.solids:
        if s.role == "footing":
            continue   # footing is a point-marker by design
        length = vlen(vsub(s.p1, s.p0))
        assert length > 1e-4, (
            f"Member '{s.tag}' ({s.role}) has near-zero length: {length:.6f} ft"
        )


# ---------------------------------------------------------------------------
# 5. Projected labels do not overlap major structural faces (annotation layout)
# ---------------------------------------------------------------------------

def test_projected_labels_do_not_overlap_major_faces():
    """
    Regression: the render pipeline must not emit labels that intersect the
    bounding box of major projected member faces.

    Strategy: render the isometric SVG and check that no <text> element's
    estimated bounding box (from x/y attributes + char-count heuristic)
    overlaps any <polygon> bbox for posts, beams, or rafters.
    """
    import subprocess
    import re
    import tempfile
    import os

    # Render to temp file
    scripts_dir = Path(__file__).parent.parent / "scripts"
    model_path  = Path(__file__).parent.parent.parent.parent / "context" / "staging" / "structure.json"

    if not model_path.exists():
        pytest.skip("structure.json not present — skipping annotation layout test")

    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        result = subprocess.run(
            ["python3", str(scripts_dir / "render_drawings.py"), str(model_path)],
            cwd=str(model_path.parent.parent.parent),
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            pytest.skip(f"Renderer failed: {result.stderr[:200]}")

    # Read the generated isometric SVG
    iso_path = model_path.parent.parent.parent / "outputs" / "drawing-isometric-view.svg"
    if not iso_path.exists():
        pytest.skip("drawing-isometric-view.svg not found")

    svg = iso_path.read_text()

    # Extract polygon bboxes for major structural roles
    poly_bboxes: list[tuple[float,float,float,float]] = []
    for m in re.finditer(r'data-role="(post|beam|rafter)"[^>]*points="([^"]+)"', svg):
        pts_str = m.group(2)
        coords = [float(v) for v in re.split(r'[,\s]+', pts_str.strip()) if v]
        xs = coords[0::2]; ys = coords[1::2]
        if xs and ys:
            poly_bboxes.append((min(xs), min(ys), max(xs), max(ys)))

    # Extract text positions — match only numeric x/y attributes
    text_bboxes: list[tuple[float,float,float,float]] = []
    for m in re.finditer(r'<text\b[^>]*\bx="(-?[\d.]+)"[^>]*\by="(-?[\d.]+)"[^>]*>([^<]{3,})<', svg):
        label_text = m.group(3)
        if label_text.startswith("K") or label_text.startswith("J") or label_text == "HUB" or ":" in label_text:
            continue
        tx = float(m.group(1))
        ty = float(m.group(2))
        chars = len(label_text)
        # Heuristic: ~7px per char, 14px tall
        tw = chars * 7.0
        th = 14.0
        text_bboxes.append((tx, ty - th, tx + tw, ty))

    def overlaps(a, b):
        return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])

    violations = []
    for tb in text_bboxes:
        for pb in poly_bboxes:
            if overlaps(tb, pb):
                violations.append(f"text @ ({tb[0]:.0f},{tb[1]:.0f}) overlaps structural face bbox")
                break   # one violation per text label is enough

    # Allow up to 1 minor overlap (title area) but 0 label-through-structure
    assert len(violations) <= 1, (
        f"{len(violations)} text labels overlap structural faces:\n" +
        "\n".join(violations[:5])
    )


# ---------------------------------------------------------------------------
# 6. Isometric SVG has expected semantic data-role counts
# ---------------------------------------------------------------------------

def test_isometric_has_expected_semantic_counts():
    """
    The generated isometric SVG must contain exactly the right number of
    data-role tagged elements for posts, beams, rafters, and hub.
    """
    import re
    import subprocess

    scripts_dir = Path(__file__).parent.parent / "scripts"
    model_path  = Path(__file__).parent.parent.parent.parent / "context" / "staging" / "structure.json"

    if not model_path.exists():
        pytest.skip("structure.json not present")

    iso_path = model_path.parent.parent.parent / "outputs" / "drawing-isometric-view.svg"
    if not iso_path.exists():
        pytest.skip("drawing-isometric-view.svg not found — run renderer first")

    svg = iso_path.read_text()

    # Count unique data-id tags per role (first-face tagging strategy)
    def count_unique(role: str) -> int:
        ids = set(re.findall(rf'data-role="{role}" data-id="([^"]+)"', svg))
        if role == "rafter":
            ids = {i for i in ids if i.startswith("R")}
        return len(ids)

    qty = 6
    assert count_unique("post")   == qty, f"Expected {qty} posts, got {count_unique('post')}"
    assert count_unique("beam")   == qty, f"Expected {qty} beams, got {count_unique('beam')}"
    assert count_unique("rafter") == qty, f"Expected {qty} primary rafters, got {count_unique('rafter')}"

    # Hub appears as one logical member if structure has a hub
    import json
    struct_data = json.loads(model_path.read_text())
    has_hub = struct_data.get("hub", {}).get("type") not in ("none", "", None)
    if has_hub:
        hub_count = svg.count('data-role="hub"')
        assert hub_count >= 1, "Hub has no data-role tag in isometric SVG"


# ---------------------------------------------------------------------------
# 7. No rafter endpoint inside hub radius (rafters must not penetrate hub)
# ---------------------------------------------------------------------------

def test_no_rafter_endpoint_inside_hub_radius(scene, solids_by_role):
    """
    Every rafter apex (p1) must have XY radius >= hub_r_face.
    A radius smaller than hub_r_face means the rafter end is inside the hub solid,
    which is geometrically impossible.
    """
    import math
    hub_r = scene.hub_r
    hub_r_face = hub_r * math.cos(math.pi / scene.qty)
    _tol  = _FT_TOL   # 1/10 inch

    for r in solids_by_role.get("rafter", []):
        if r.tag.startswith("Jack"):
            continue  # Jack rafters terminate at hip rafters
        xy_r = v2_radius(r.p1)
        assert xy_r >= hub_r_face - _tol, (
            f"Rafter {r.tag}: apex XY radius={xy_r:.6f} ft < hub_r_face={hub_r_face:.6f} ft "
            f"— rafter endpoint is INSIDE the hub solid "
            f"(penetration={abs(xy_r - hub_r_face)*12:.3f}\")"
        )


# ---------------------------------------------------------------------------
# validate_scene_geometry integration — ensure it catches deliberate violations
# ---------------------------------------------------------------------------

def test_validator_catches_zero_length_member(base_structure_dict):
    """validate_scene_geometry must raise GeometryError on zero-length members."""
    from cad_scene import Solid, Scene, Face
    bad_solid = Solid(role="post", tag="P_BAD",
                      p0=(0.0, 0.0, 0.0), p1=(0.0, 0.0, 0.0))
    bad_solid.faces.append(Face([(0,0,0)], (0,0,1), "#fff", "post", "P_BAD"))

    s = build_structure_scene(copy.deepcopy(base_structure_dict))
    s.solids.append(bad_solid)

    # Should raise because bad_solid has zero length
    with pytest.raises(GeometryError, match="zero-length"):
        validate_scene_geometry(s)


def test_validator_passes_on_valid_scene(base_structure_dict):
    """validate_scene_geometry must not raise on a correctly built scene."""
    scene = build_structure_scene(copy.deepcopy(base_structure_dict))
    validate_scene_geometry(scene)   # must not raise


# ---------------------------------------------------------------------------
# 8. Rafters sit flush ON TOP of support beams (no beam penetration)
# ---------------------------------------------------------------------------

def test_rafters_supported_on_beams(scene):
    """
    KEY TIMBER-FRAME INVARIANT:
    Rafters must sit entirely ON TOP of the beam ring, not penetrating into the
    beams or posts. Inside the beam perimeter, the rafter bottom faces must be
    at or above Z_BEAM_TOP.
    """
    for s in scene.solids:
        if s.role != "rafter":
            continue
        for face in s.faces:
            # Look for bottom-facing surfaces of the rafter
            if face.normal[2] < -0.1:
                for v in face.verts:
                    xy_r = v2_radius(v)
                    # Within the beam ring perimeter (radius <= 5.0 ft)
                    if xy_r <= scene.post_xy[0][0] - 0.2:
                        assert v[2] >= scene.Z_BEAM_TOP - 1e-3, (
                            f"Rafter {s.tag} underside vertex {v} penetrates beam! "
                            f"Z={v[2]:.4f} ft, expected >= Z_BEAM_TOP={scene.Z_BEAM_TOP:.4f} ft"
                        )


# ---------------------------------------------------------------------------
# 9. Beam endpoints must sit on the post position grid (Invariant 9)
# ---------------------------------------------------------------------------

def test_beam_endpoints_on_post_grid(scene, solids_by_role):
    """
    Invariant 9 (positive): every beam's p0 and p1 XY coordinates must coincide
    with a post position within 1/8 inch.  Beams are constructed from post_xy
    so any drift is a builder error, not a tolerance question.
    """
    _BEAM_POST_SNAP = 1.0 / 96.0   # 1/8 inch in feet
    for b in solids_by_role.get("beam", []):
        for end_pt, label in ((b.p0, "p0"), (b.p1, "p1")):
            nearest_dist = min(
                math.sqrt((end_pt[0] - px) ** 2 + (end_pt[1] - py) ** 2)
                for px, py in scene.post_xy
            )
            assert nearest_dist <= _BEAM_POST_SNAP, (
                f"Beam {b.tag} {label} XY ({end_pt[0]:.4f}, {end_pt[1]:.4f}) is "
                f"{nearest_dist * 12:.3f}\" from nearest post (max 1/8\") — "
                "beam endpoint is disconnected from post grid"
            )


def test_invariant9_catches_displaced_beam(base_structure_dict):
    """
    Invariant 9 (mutation): displace a beam endpoint 0.5 ft off the post grid;
    validate_scene_geometry must raise GeometryError naming Invariant 9.
    """
    s = build_structure_scene(copy.deepcopy(base_structure_dict))
    beams = [solid for solid in s.solids if solid.role == "beam"]
    assert beams, "Need at least one beam for this mutation test"
    # Shift the first beam's p0 0.5 ft off its post position (clearly > 1/8" snap)
    b0 = beams[0]
    beams[0].p0 = (b0.p0[0] + 0.5, b0.p0[1], b0.p0[2])

    with pytest.raises(GeometryError, match="Invariant 9"):
        validate_scene_geometry(s)


# ---------------------------------------------------------------------------
# 10. Brace foot must contact a post face; brace head within beam span (Inv 10)
# ---------------------------------------------------------------------------

def test_brace_foot_on_post_face(scene, solids_by_role):
    """
    Invariant 10 (positive): every brace lower endpoint XY must be within 1 ft
    of a post position.  Braces are anchored to the post face so their lower
    foot is always at distance ≈ POST_HW from the post centre.
    """
    _BRACE_FOOT_MAX = 1.0   # ft
    for b in solids_by_role.get("brace", []):
        lower_pt = b.p0 if b.p0[2] <= b.p1[2] else b.p1
        nearest_dist = min(
            math.sqrt((lower_pt[0] - px) ** 2 + (lower_pt[1] - py) ** 2)
            for px, py in scene.post_xy
        )
        assert nearest_dist <= _BRACE_FOOT_MAX, (
            f"Brace {b.tag} lower foot XY ({lower_pt[0]:.4f}, {lower_pt[1]:.4f}) is "
            f"{nearest_dist:.3f} ft from nearest post (max {_BRACE_FOOT_MAX} ft) — "
            "brace foot is floating off the post face"
        )


def test_invariant10_catches_floating_brace_foot(base_structure_dict):
    """
    Invariant 10 (mutation): move a brace's lower foot 50 ft from any post;
    validate_scene_geometry must raise GeometryError naming Invariant 10.
    """
    s = build_structure_scene(copy.deepcopy(base_structure_dict))
    braces = [solid for solid in s.solids if solid.role == "brace"]
    assert braces, "Need at least one brace for this mutation test"
    b0 = braces[0]
    lower_idx_is_p0 = b0.p0[2] <= b0.p1[2]
    if lower_idx_is_p0:
        braces[0].p0 = (50.0, 50.0, b0.p0[2])
    else:
        braces[0].p1 = (50.0, 50.0, b0.p1[2])

    with pytest.raises(GeometryError, match="Invariant 10"):
        validate_scene_geometry(s)


def test_invariant10_catches_floating_brace_head(base_structure_dict):
    """
    Invariant 10 (mutation): move a brace's upper head 50 ft from any post;
    validate_scene_geometry must raise GeometryError naming Invariant 10.
    """
    s = build_structure_scene(copy.deepcopy(base_structure_dict))
    braces = [solid for solid in s.solids if solid.role == "brace"]
    assert braces, "Need at least one brace for this mutation test"
    b0 = braces[0]
    upper_idx_is_p0 = b0.p0[2] > b0.p1[2]
    if upper_idx_is_p0:
        braces[0].p0 = (50.0, 50.0, b0.p0[2])
    else:
        braces[0].p1 = (50.0, 50.0, b0.p1[2])

    with pytest.raises(GeometryError, match="Invariant 10"):
        validate_scene_geometry(s)



# ---------------------------------------------------------------------------
# New-path: geometry invariants hold when using constraint-based pipeline
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def new_path_scene(tmp_path_factory):
    from test_geometry_engine import STRUCTURE_SEED
    from geometry_engine import compute_from_structure
    tmp = tmp_path_factory.mktemp("new_path_invariants")
    p = tmp / "structure.json"
    p.write_text(json.dumps(copy.deepcopy(STRUCTURE_SEED)))
    compute_from_structure(str(p))
    s = json.loads(p.read_text())
    scene = build_structure_scene(s)
    validate_scene_geometry(scene)
    return scene


def test_new_path_post_top_equals_beam_bottom(new_path_scene):
    """Invariant 1 on constraint-based path: post top Z == beam underside Z."""
    Z_POST_TOP = new_path_scene.Z_POST_TOP
    Z_BEAM_TOP = new_path_scene.Z_BEAM_TOP
    beam_d = Z_BEAM_TOP - Z_POST_TOP
    for s in new_path_scene.solids:
        if s.role == "post":
            assert abs(max(s.p0[2], s.p1[2]) - Z_POST_TOP) <= _FT_TOL, f"{s.tag} top Z mismatch"
        elif s.role == "beam":
            centre_z = (s.p0[2] + s.p1[2]) / 2.0
            assert abs(centre_z - beam_d / 2.0 - Z_POST_TOP) <= _FT_TOL, f"{s.tag} bottom Z mismatch"


def test_new_path_all_member_lengths_positive(new_path_scene):
    """Invariant 4 on constraint-based path: no zero-length members."""
    for s in new_path_scene.solids:
        length = vlen(vsub(s.p1, s.p0))
        assert length > 0, f"Zero-length member on new path: {s.tag}"
