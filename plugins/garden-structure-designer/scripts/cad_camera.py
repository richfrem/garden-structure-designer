#!/usr/bin/env python3
"""
cad_camera.py
=============

Purpose:
    Shared camera, projection, and coordinate transform system for CAD rendering.
    Enforces orthonormal right-handed bases, single Y-inversion on SVG sheets,
    consistent isometric directions (normalize(1, -1, 1)), true perspective depth
    division, and semantic anchor projection.

Layer: Domain / Geometry Projections
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Any, Literal, Optional, Tuple

from cad_render_contracts import Anchor, Vec3


def _vec3_sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _vec3_add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _vec3_scale(v: Vec3, s: float) -> Vec3:
    return (v[0] * s, v[1] * s, v[2] * s)


def _vec3_dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _vec3_cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _vec3_len(v: Vec3) -> float:
    return math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)


def _vec3_norm(v: Vec3) -> Vec3:
    length = _vec3_len(v)
    if length <= 1e-12:
        raise ValueError("Cannot normalize near-zero vector")
    return (v[0] / length, v[1] / length, v[2] / length)


@dataclass(frozen=True)
class CameraSpec:
    """Rigorous camera specification for orthographic and perspective views."""
    camera_id: str
    projection_type: Literal["orthographic", "perspective"]
    target_mm: Vec3
    eye_mm: Vec3
    right: Vec3
    up: Vec3
    outward: Vec3  # Looking along -outward
    near_mm: float = 10.0
    far_mm: float = 100000.0
    fov_y_deg: Optional[float] = None
    aspect_ratio: Optional[float] = None

    @property
    def camera_hash(self) -> str:
        """Deterministic digest of camera orientation and parameters."""
        hasher = hashlib.sha256()
        payload = {
            "id": self.camera_id,
            "type": self.projection_type,
            "target": self.target_mm,
            "eye": self.eye_mm,
            "right": self.right,
            "up": self.up,
            "outward": self.outward,
            "near": self.near_mm,
            "far": self.far_mm,
            "fov": self.fov_y_deg,
            "aspect": self.aspect_ratio,
        }
        hasher.update(json.dumps(payload, sort_keys=True).encode("utf-8"))
        return hasher.hexdigest()


@dataclass(frozen=True)
class SheetTransform:
    """Maps model-space projected 2D coordinates into SVG sheet coordinates."""
    viewport_x: float
    viewport_y: float
    viewport_w: float
    viewport_h: float
    center_x: float
    center_y: float
    scale: float  # pixels per model mm for orthographic views


def create_standard_camera(
    view_type: Literal["plan", "front_elevation", "right_elevation", "isometric"],
    target_mm: Vec3 = (0.0, 0.0, 0.0),
    distance_mm: float = 10000.0,
) -> CameraSpec:
    """Creates a standard orthographic camera with verified right-handed orthonormal basis."""
    if view_type == "plan":
        # Outward = (0, 0, 1), looking down -Z
        # Sheet Right = (1, 0, 0), Sheet Up = (0, 1, 0)
        n = (0.0, 0.0, 1.0)
        r = (1.0, 0.0, 0.0)
        u = (0.0, 1.0, 0.0)
    elif view_type == "front_elevation":
        # Looking from south toward north (-Y to +Y)
        # Outward = (0, -1, 0), Sheet Right = (1, 0, 0), Sheet Up = (0, 0, 1)
        n = (0.0, -1.0, 0.0)
        r = (1.0, 0.0, 0.0)
        u = (0.0, 0.0, 1.0)
    elif view_type == "right_elevation":
        # Looking from east toward west (+X to -X)
        # Outward = (1, 0, 0), Sheet Right = (0, 1, 0), Sheet Up = (0, 0, 1)
        n = (1.0, 0.0, 0.0)
        r = (0.0, 1.0, 0.0)
        u = (0.0, 0.0, 1.0)
    elif view_type == "isometric":
        # Outward along (1, -1, 1) / sqrt(3)
        # Looking along -n
        # k = (0, 0, 1)
        # r = (k x n) / ||k x n|| = (1, 1, 0) / sqrt(2)
        # u = n x r = (-1, 1, 2) / sqrt(6)
        n = _vec3_norm((1.0, -1.0, 1.0))
        k = (0.0, 0.0, 1.0)
        k_cross_n = _vec3_cross(k, n)
        r = _vec3_norm(k_cross_n)
        u = _vec3_norm(_vec3_cross(n, r))
    else:
        raise ValueError(f"Unknown standard view_type: {view_type}")

    eye_mm = _vec3_add(target_mm, _vec3_scale(n, distance_mm))

    return CameraSpec(
        camera_id=f"cam_{view_type}",
        projection_type="orthographic",
        target_mm=target_mm,
        eye_mm=eye_mm,
        right=r,
        up=u,
        outward=n,
    )


def create_perspective_camera(
    eye_mm: Vec3,
    target_mm: Vec3,
    fov_y_deg: float = 60.0,
    aspect_ratio: float = 1.0,
    world_up: Vec3 = (0.0, 0.0, 1.0),
) -> CameraSpec:
    """Creates a true perspective camera."""
    forward = _vec3_sub(target_mm, eye_mm)
    n = _vec3_scale(_vec3_norm(forward), -1.0)  # outward points away from target
    r = _vec3_norm(_vec3_cross(world_up, n))
    u = _vec3_norm(_vec3_cross(n, r))

    dist = _vec3_len(forward)

    return CameraSpec(
        camera_id="cam_perspective",
        projection_type="perspective",
        target_mm=target_mm,
        eye_mm=eye_mm,
        right=r,
        up=u,
        outward=n,
        near_mm=max(10.0, dist * 0.01),
        far_mm=max(50000.0, dist * 10.0),
        fov_y_deg=fov_y_deg,
        aspect_ratio=aspect_ratio,
    )


def project_world(point_mm: Vec3, camera: CameraSpec) -> Vec3:
    """
    Projects a world-space point into camera view coordinates:
    x_v = r . (p - c)
    y_v = u . (p - c)
    z_v = n . (p - c)
    Larger z_v is closer to camera.
    """
    rel = _vec3_sub(point_mm, camera.target_mm)
    x_v = _vec3_dot(camera.right, rel)
    y_v = _vec3_dot(camera.up, rel)
    z_v = _vec3_dot(camera.outward, rel)
    return (x_v, y_v, z_v)


def project_perspective(point_mm: Vec3, camera: CameraSpec) -> Tuple[float, float, float]:
    """
    Projects world point to NDC (-1 to 1) using perspective division:
    x = r . (p - eye)
    y = u . (p - eye)
    d = -n . (p - eye) (depth in front of camera)
    """
    if camera.projection_type != "perspective" or not camera.fov_y_deg or not camera.aspect_ratio:
        raise ValueError("Perspective projection requires perspective camera with fov_y_deg and aspect_ratio")

    rel = _vec3_sub(point_mm, camera.eye_mm)
    x = _vec3_dot(camera.right, rel)
    y = _vec3_dot(camera.up, rel)
    d = -_vec3_dot(camera.outward, rel)

    if d <= 1e-6:
        raise ValueError(f"Point {point_mm} is behind or at camera optical plane (depth {d})")

    theta_rad = math.radians(camera.fov_y_deg)
    tan_half_fov = math.tan(theta_rad / 2.0)

    x_ndc = x / (d * camera.aspect_ratio * tan_half_fov)
    y_ndc = y / (d * tan_half_fov)
    return (x_ndc, y_ndc, d)


def to_sheet(
    projected_xy: Tuple[float, float],
    transform: SheetTransform,
) -> Tuple[float, float]:
    """
    Applies single Y-inversion to map projected 2D coordinates to SVG sheet coordinates:
    x_sheet = viewport_x + viewport_w/2 + s * (x_v - center_x)
    y_sheet = viewport_y + viewport_h/2 - s * (y_v - center_y)
    """
    s = transform.scale
    x_sheet = transform.viewport_x + (transform.viewport_w / 2.0) + s * (projected_xy[0] - transform.center_x)
    y_sheet = transform.viewport_y + (transform.viewport_h / 2.0) - s * (projected_xy[1] - transform.center_y)
    return (x_sheet, y_sheet)


def project_anchor(
    anchor: Anchor,
    camera: CameraSpec,
    transform: SheetTransform,
) -> Tuple[float, float]:
    """Projects a 3D semantic anchor directly into 2D SVG sheet coordinates."""
    if camera.projection_type == "perspective":
        x_ndc, y_ndc, _ = project_perspective(anchor.world_mm, camera)
        # NDC (-1 to 1): (-1, -1) bottom-left, (+1, +1) top-right
        x_sheet = transform.viewport_x + (transform.viewport_w / 2.0) + (x_ndc * (transform.viewport_w / 2.0))
        y_sheet = transform.viewport_y + (transform.viewport_h / 2.0) - (y_ndc * (transform.viewport_h / 2.0))
        return (x_sheet, y_sheet)

    view_coords = project_world(anchor.world_mm, camera)
    return to_sheet((view_coords[0], view_coords[1]), transform)
