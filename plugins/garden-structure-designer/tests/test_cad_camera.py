"""Tests for cad_camera.py: camera contracts, basis orthonormalization, and sheet transforms."""

from __future__ import annotations

import math
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import cad_camera as cam  # type: ignore[import]  # noqa: E402
from cad_render_contracts import Anchor  # type: ignore[import]  # noqa: E402


def test_orthonormal_basis():
    """Verify camera basis vectors are mutually orthogonal, unit-length, and form a right-handed system."""
    for view_type in ["plan", "front_elevation", "right_elevation", "isometric"]:
        spec = cam.create_standard_camera(view_type=view_type, target_mm=(0.0, 0.0, 0.0))

        r = spec.right
        u = spec.up
        n = spec.outward

        # Unit length
        assert math.isclose(math.sqrt(r[0]**2 + r[1]**2 + r[2]**2), 1.0, abs_tol=1e-6)
        assert math.isclose(math.sqrt(u[0]**2 + u[1]**2 + u[2]**2), 1.0, abs_tol=1e-6)
        assert math.isclose(math.sqrt(n[0]**2 + n[1]**2 + n[2]**2), 1.0, abs_tol=1e-6)

        # Mutually orthogonal (dot products == 0)
        dot_ru = r[0]*u[0] + r[1]*u[1] + r[2]*u[2]
        dot_rn = r[0]*n[0] + r[1]*n[1] + r[2]*n[2]
        dot_un = u[0]*n[0] + u[1]*n[1] + u[2]*n[2]
        assert math.isclose(dot_ru, 0.0, abs_tol=1e-6)
        assert math.isclose(dot_rn, 0.0, abs_tol=1e-6)
        assert math.isclose(dot_un, 0.0, abs_tol=1e-6)

        # Right-handed cross product r x u = n
        cross_ru = (
            r[1]*u[2] - r[2]*u[1],
            r[2]*u[0] - r[0]*u[2],
            r[0]*u[1] - r[1]*u[0],
        )
        assert math.isclose(cross_ru[0], n[0], abs_tol=1e-6)
        assert math.isclose(cross_ru[1], n[1], abs_tol=1e-6)
        assert math.isclose(cross_ru[2], n[2], abs_tol=1e-6)


def test_isometric_projection_asymmetric_point():
    """Verify asymmetric point projects to exact theoretical values without axis swaps or mirroring."""
    spec = cam.create_standard_camera(view_type="isometric", target_mm=(0.0, 0.0, 0.0))

    # Point p = (1000.0, 2000.0, 3000.0)
    p = (1000.0, 2000.0, 3000.0)
    proj = cam.project_world(p, spec)
    # Theoretical:
    # r = (1, 1, 0) / sqrt(2) -> r . p = (1000 + 2000) / sqrt(2) = 3000 / sqrt(2)
    # u = (-1, 1, 2) / sqrt(6) -> u . p = (-1000 + 2000 + 6000) / sqrt(6) = 7000 / sqrt(6)
    # n = (1, -1, 1) / sqrt(3) -> n . p = (1000 - 2000 + 3000) / sqrt(3) = 2000 / sqrt(3)
    expected_x = 3000.0 / math.sqrt(2)
    expected_y = 7000.0 / math.sqrt(6)
    expected_z = 2000.0 / math.sqrt(3)

    assert math.isclose(proj[0], expected_x, abs_tol=1e-5)
    assert math.isclose(proj[1], expected_y, abs_tol=1e-5)
    assert math.isclose(proj[2], expected_z, abs_tol=1e-5)


def test_sheet_transform_single_y_flip():
    """Verify sheet transform correctly flips Y once and centers within viewport."""
    transform = cam.SheetTransform(
        viewport_x=100.0,
        viewport_y=150.0,
        viewport_w=800.0,
        viewport_h=600.0,
        center_x=0.0,
        center_y=0.0,
        scale=0.1,  # 0.1 px per mm
    )

    # Center point (0, 0) should map to center of viewport
    sheet_center = cam.to_sheet((0.0, 0.0), transform)
    assert math.isclose(sheet_center[0], 100.0 + 400.0)
    assert math.isclose(sheet_center[1], 150.0 + 300.0)

    # Up in model (+Y) should go DOWN in SVG coordinates (-Y in sheet space)
    sheet_up = cam.to_sheet((0.0, 1000.0), transform)
    assert math.isclose(sheet_up[0], 500.0)
    assert math.isclose(sheet_up[1], 450.0 - 0.1 * 1000.0)  # 350.0

    # Right in model (+X) should go RIGHT in SVG (+X in sheet space)
    sheet_right = cam.to_sheet((1000.0, 0.0), transform)
    assert math.isclose(sheet_right[0], 500.0 + 0.1 * 1000.0)  # 600.0
    assert math.isclose(sheet_right[1], 450.0)


def test_perspective_projection():
    """Verify perspective camera divides by depth along the optical axis."""
    spec = cam.create_perspective_camera(
        eye_mm=(0.0, -5000.0, 2000.0),
        target_mm=(0.0, 0.0, 2000.0),
        fov_y_deg=60.0,
        aspect_ratio=1.0,
    )

    # Near point at target
    p_target = (0.0, 0.0, 2000.0)
    ndc_target = cam.project_perspective(p_target, spec)
    assert math.isclose(ndc_target[0], 0.0, abs_tol=1e-5)
    assert math.isclose(ndc_target[1], 0.0, abs_tol=1e-5)

    # Point offset by 1000mm in X at target depth
    p_offset = (1000.0, 0.0, 2000.0)
    ndc_offset = cam.project_perspective(p_offset, spec)

    # Far point twice as far away with same X offset should have half NDC offset
    p_far = (1000.0, 5000.0, 2000.0)
    ndc_far = cam.project_perspective(p_far, spec)

    assert ndc_far[0] < ndc_offset[0]
    assert math.isclose(ndc_far[0] * 2.0, ndc_offset[0], rel_tol=1e-4)


def test_project_anchor():
    """Verify semantic anchor projects directly to sheet coordinates."""
    anchor = Anchor(
        anchor_id="P1_MID",
        member_id="P1",
        kind="midpoint",
        world_mm=(1000.0, 2000.0, 3000.0),
        source_ref="members.P1",
    )
    cam_spec = cam.create_standard_camera(view_type="isometric", target_mm=(0.0, 0.0, 0.0))
    sheet_tf = cam.SheetTransform(
        viewport_x=0.0,
        viewport_y=0.0,
        viewport_w=1000.0,
        viewport_h=1000.0,
        center_x=0.0,
        center_y=0.0,
        scale=0.05,
    )

    pt_sheet = cam.project_anchor(anchor, cam_spec, sheet_tf)
    assert isinstance(pt_sheet, tuple)
    assert len(pt_sheet) == 2
    assert math.isfinite(pt_sheet[0]) and math.isfinite(pt_sheet[1])
