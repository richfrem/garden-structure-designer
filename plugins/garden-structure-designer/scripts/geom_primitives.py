"""
geom_primitives.py
==================

Purpose:
    Shared 3D vector and line-plane primitives (dot, add, subtract, scale, line/plane intersection,
    signed point-plane distance). Note: no script currently imports this module; geometry_engine.py
    and cad_scene.py carry their own copies (review finding, consolidation proposed).

Layer: Core / Geometry Primitives

Key Input Dependencies:
    Standard library only (math).

Key Functions:
    vdot(a, b) -> float          vsub(a, b) -> V3          vadd(a, b) -> V3          vmul(a, s) -> V3
    intersect_line_plane(p0, d, p_plane, n, eps=1e-8) -> tuple[V3, float]
    point_to_plane_distance(point, plane_point, plane_normal) -> float
"""
from __future__ import annotations
import math

V3 = tuple[float, float, float]

def vdot(a: V3, b: V3) -> float:
    """Dot product of two 3D vectors."""
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def vsub(a: V3, b: V3) -> V3:
    """Component-wise a - b."""
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def vadd(a: V3, b: V3) -> V3:
    """Component-wise a + b."""
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def vmul(a: V3, s: float) -> V3:
    """Scales a 3D vector by s."""
    return (a[0]*s, a[1]*s, a[2]*s)

def intersect_line_plane(p0: V3, d: V3, p_plane: V3, n: V3, eps: float = 1e-8) -> tuple[V3, float]:
    """Return p = p0 + t*d where p lies on plane defined by (p_plane, n)."""
    denom = vdot(d, n)
    if abs(denom) < eps:
        raise ValueError("Line parallel to plane")
    t = vdot(vsub(p_plane, p0), n) / denom
    if t <= 0:
        # In our CAD context, a negative t means the intersection is behind the start point.
        # This usually indicates the jack rafter is facing the wrong way or the plane is behind it.
        raise ValueError(f"Intersection behind start (t={t:.4f})")
    return vadd(p0, vmul(d, t)), t

def point_to_plane_distance(point: V3, plane_point: V3, plane_normal: V3) -> float:
    """Signed distance from point to plane."""
    nl = math.sqrt(vdot(plane_normal, plane_normal))
    norm = vmul(plane_normal, 1.0/nl) if nl > 1e-9 else plane_normal
    return vdot(vsub(point, plane_point), norm)

