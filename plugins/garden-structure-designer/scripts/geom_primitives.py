"""
geom_primitives.py
==================
Shared 3D geometry primitives for line-plane intersections and vector ops.
"""
from __future__ import annotations
import math

V3 = tuple[float, float, float]

def vdot(a: V3, b: V3) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def vsub(a: V3, b: V3) -> V3:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def vadd(a: V3, b: V3) -> V3:
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def vmul(a: V3, s: float) -> V3:
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
