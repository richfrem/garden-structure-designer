#!/usr/bin/env python3
"""
validate_connections.py
=======================
Hard pre-render gate: verifies physical surface contact between structural
members using actual 3D geometry from the Scene.

Pipeline position:
    cad_scene.build_structure_scene()  →  Scene
        ↓
    cad_scene.validate_scene_geometry()  →  geometric invariants (p0/p1 range checks)
        ↓
    validate_connections()               →  physical contact (this module)
        ↓
    render_drawings.py  /  svg generation

Why a separate pass (not baked into validate_scene_geometry):
    validate_scene_geometry checks axis ENDPOINTS (p0/p1) and Z-plane ordering.
    validate_connections checks actual rendered SURFACE geometry:
      - beam_soffit_at_post_top: uses face vertex min Z, not p0/p1
      - rafter_tip_on_hub_face:  uses point-to-plane distance to hub face normals
      - brace_foot_on_post_face: checks XY proximity against post circumradius

    If cad_scene.py has a face-construction bug (p0/p1 correct, face verts wrong),
    validate_scene_geometry passes but validate_connections catches it.

Checks:
    1. beam_soffit_at_post_top  — beam bottom face min vertex Z == Z_POST_TOP (1/8" tol)
    2. rafter_tip_on_hub_face   — rafter.p1 distance to nearest hub face plane < 1/8"
    3. brace_foot_on_post_face  — brace lower endpoint XY within post circumradius + 1/8"

Exit codes when used as CLI:
    0 = all checks passed
    1 = one or more physical contact checks failed
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Types (imported from cad_scene at runtime to avoid circular-import risk)
# ---------------------------------------------------------------------------

try:
    from cad_scene import Scene, Solid, vdot, vcent, vsub, vlen, vnorm, vscl  # noqa: F401
    V3 = tuple[float, float, float]
except ImportError:
    pass  # CLI fallback: Scene must be passed pre-built


class ContactError(ValueError):
    """Raised when physical surface contact validation fails."""

# ---------------------------------------------------------------------------
# Tolerances
# ---------------------------------------------------------------------------

_CONTACT_TOL = 1.0 / 96.0   # 1/8 inch in feet — surface contact tolerance


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _dist_point_to_plane(
    pt: "tuple[float, float, float]",
    plane_pt: "tuple[float, float, float]",
    plane_normal: "tuple[float, float, float]",
) -> float:
    """Signed (absolute) distance from pt to plane defined by plane_pt and unit normal."""
    return abs(
        (pt[0] - plane_pt[0]) * plane_normal[0]
        + (pt[1] - plane_pt[1]) * plane_normal[1]
        + (pt[2] - plane_pt[2]) * plane_normal[2]
    )


def _min_z_of_solid(solid: "Solid") -> float:
    """Minimum Z coordinate across all face vertices of a Solid."""
    return min(v[2] for f in solid.faces for v in f.verts)


def _post_circumradius(post: "Solid") -> float:
    """Circumradius of a post's cross-section: max XY distance from axis to any corner."""
    cx, cy = post.p0[0], post.p0[1]
    return max(
        math.sqrt((v[0] - cx) ** 2 + (v[1] - cy) ** 2)
        for f in post.faces
        for v in f.verts
    )


# ---------------------------------------------------------------------------
# Check 1 — Beam soffit at post top
# ---------------------------------------------------------------------------

def _nearest_post_tag(posts: "list[Solid]", xy: "tuple[float, float]") -> str:
    """Tag of the post whose base XY center is closest to xy."""
    return min(
        posts,
        key=lambda p: math.sqrt((p.p0[0] - xy[0]) ** 2 + (p.p0[1] - xy[1]) ** 2),
    ).tag


def _check_beam_soffit_at_post_top(scene: "Scene") -> list[str]:
    """
    Each beam's bottom face min vertex Z must equal Z_POST_TOP within 1/8".
    Distinct from Invariant 6 (which checks p0/p1 range): this checks rendered
    face vertex geometry, catching face-construction drift that p0/p1 would miss.
    """
    errors: list[str] = []
    beams = [s for s in scene.solids if s.role == "beam"]
    posts = [s for s in scene.solids if s.role == "post"]
    for beam in beams:
        soffit_z = _min_z_of_solid(beam)
        delta = abs(soffit_z - scene.Z_POST_TOP)
        if delta > _CONTACT_TOL:
            # Report which posts this beam spans to aid diagnosis
            post_a = _nearest_post_tag(posts, (beam.p0[0], beam.p0[1])) if posts else "?"
            post_b = _nearest_post_tag(posts, (beam.p1[0], beam.p1[1])) if posts else "?"
            errors.append(
                f"beam_soffit_at_post_top: beam {beam.tag} ({post_a}→{post_b}) "
                f"soffit Z={soffit_z:.4f} ft, Z_POST_TOP={scene.Z_POST_TOP:.4f} ft, "
                f"gap={delta * 12:.3f}\""
            )
    return errors


# ---------------------------------------------------------------------------
# Check 2 — Rafter tip on hub face
# ---------------------------------------------------------------------------

def _check_rafter_tip_on_hub_face(scene: "Scene") -> list[str]:
    """
    Each hip rafter p1 (apex end) must lie on a hub vertical face plane within 1/8".
    Distinct from Invariant 2 (which checks apex Z only): this checks XY contact
    with the specific hub face plane, catching lateral drift that Z checks miss.
    Skipped if no hub Solid is present in the scene (e.g., ridge-beam roof type).
    """
    errors: list[str] = []

    hub = next((s for s in scene.solids if s.role == "hub"), None)
    if hub is None:
        return errors  # no hub — skip

    hub_side_faces = [f for f in hub.faces if abs(f.normal[2]) < 0.1]
    if not hub_side_faces:
        return errors  # hub has no vertical faces — skip

    rafters = [s for s in scene.solids if s.role == "rafter" and not (s.tag.startswith("Jack") or s.tag.startswith("J"))]
    for rafter in rafters:
        pt = rafter.p1
        min_dist = min(
            _dist_point_to_plane(pt, face.verts[0], face.normal)
            for face in hub_side_faces
        )
        if min_dist > _CONTACT_TOL:
            errors.append(
                f"rafter_tip_on_hub_face: rafter {rafter.tag}→{hub.tag} p1="
                f"({pt[0]:.4f}, {pt[1]:.4f}, {pt[2]:.4f}) is "
                f"{min_dist * 12:.3f}\" from nearest hub face plane"
            )
    return errors


# ---------------------------------------------------------------------------
# Check 3 — Brace foot on post face
# ---------------------------------------------------------------------------

def _check_brace_foot_on_post_face(scene: "Scene") -> list[str]:
    """
    Each brace's lower endpoint XY must be within the post's circumradius + 1/8".
    The circumradius is computed from the post's actual face vertices.
    Distinct from Invariant 10 (1 ft loose bound): this uses the tight geometric
    post cross-section, catching braces that are placed away from the post body.
    Skipped if no braces are present in the scene.
    """
    errors: list[str] = []

    braces = [s for s in scene.solids if s.role == "brace"]
    posts = [s for s in scene.solids if s.role == "post"]
    if not braces or not posts:
        return errors  # no braces or posts — skip

    # Pre-compute (post center XY, circumradius) for each post
    post_data = [
        ((p.p0[0], p.p0[1]), _post_circumradius(p), p.tag)
        for p in posts
    ]

    for brace in braces:
        lower_pt = brace.p0 if brace.p0[2] <= brace.p1[2] else brace.p1

        nearest_dist, nearest_tag = min(
            (
                math.sqrt((lower_pt[0] - cx) ** 2 + (lower_pt[1] - cy) ** 2),
                tag,
            )
            for (cx, cy), _, tag in post_data
        )

        # Find circumradius for the nearest post
        nearest_circumradius = next(
            cr for _, cr, tag in post_data
            if tag == nearest_tag
        )

        threshold = nearest_circumradius + _CONTACT_TOL
        if nearest_dist > threshold:
            errors.append(
                f"brace_foot_on_post_face: brace {brace.tag}→{nearest_tag} lower foot XY "
                f"({lower_pt[0]:.4f}, {lower_pt[1]:.4f}) is "
                f"{nearest_dist:.4f} ft from {nearest_tag} "
                f"(circumradius={nearest_circumradius:.4f} ft, threshold={threshold:.4f} ft)"
            )
    return errors


def _check_jack_to_hip_contact(scene: "Scene") -> list[str]:
    """
    Each jack rafter's upper endpoint (p1) must lie on the side-face plane
    of its target hip rafter within 1/8".
    Distinct from rafter-to-hub checks: this checks contact with a 3D side plane.
    Fails on gap > 1/8" or penetration > 1/8".
    """
    errors: list[str] = []
    # ID scheme: J{bay}{a|b}
    jacks = [s for s in scene.solids if s.role == "rafter" and s.tag.startswith("J")]
    hips = [s for s in scene.solids if s.role == "rafter" and s.tag.startswith("R")]
    
    if not jacks or not hips:
        return errors

    # Map hip tags to solids for fast lookup
    hip_map = {h.tag: h for h in hips}
    
    # Rafter dimensions (nominal HW)
    # We use the hip rafter's actual face vertices to derive side planes.
    
    for jack in jacks:
        pt = jack.p1
        # ID scheme: J{bay}{a|b}. J1a -> R1, J1b -> R2
        num_str = "".join([c for c in jack.tag if c.isdigit()])
        if not num_str: continue
        bay = int(num_str)
        suffix = jack.tag[-1]
        
        target_hip_tag = f"R{bay}" if suffix == 'a' else f"R{(bay % scene.qty) + 1}"
        target_hip = hip_map.get(target_hip_tag)
        if not target_hip:
            errors.append(f"jack_to_hip_contact: jack {jack.tag} target hip {target_hip_tag} missing")
            continue
            
        # Hip side faces are those with normals perpendicular to hip axis and Z-up
        hip_axis = vnorm(vsub(target_hip.p1, target_hip.p0))
        side_faces = [
            f for f in target_hip.faces 
            if abs(vdot(f.normal, hip_axis)) < 0.05 and abs(f.normal[2]) < 0.1
        ]
        
        if not side_faces:
            errors.append(f"jack_to_hip_contact: hip {target_hip_tag} has no valid side faces")
            continue
            
        # Signed distance to nearest side face plane
        # plane equation: dot(P - P0, N) = d
        # We need the correct side normal.
        # Find the face that has a normal pointing TOWARD the jack.
        # Vector from hip axis to jack endpoint.
        v_offset = vsub(pt, target_hip.p0)
        v_perp = vsub(v_offset, vscl(hip_axis, vdot(v_offset, hip_axis)))
        if vlen(v_perp) < 1e-9:
             errors.append(f"jack_to_hip_contact: jack {jack.tag} is on hip {target_hip_tag} axis")
             continue
        u_perp = vnorm(v_perp)
        
        # Best face is one whose normal is most opposite to u_perp (pointing toward jack)
        # Actually, the face normal points OUT of the solid. 
        # So we want the face whose normal matches u_perp.
        face = max(side_faces, key=lambda f: vdot(f.normal, u_perp))
        
        # Signed distance: dot(pt - face_vert, face_normal)
        # Positive = gap (pt is outside solid)
        # Negative = penetration (pt is inside solid)
        dist = vdot(vsub(pt, face.verts[0]), face.normal)
        
        if dist > _CONTACT_TOL:
            errors.append(
                f"jack_to_hip_contact: GAP detected at jack {jack.tag} endpoint ({dist * 12:.3f}\")"
            )
        elif dist < -_CONTACT_TOL:
            errors.append(
                f"jack_to_hip_contact: PENETRATION detected at jack {jack.tag} endpoint ({abs(dist) * 12:.3f}\")"
            )
            
    return errors


def _check_rafter_seating_on_beam(scene: "Scene") -> list[str]:
    """
    Each rafter's level seat face (birdsmouth) must lie on the Z_BEAM_TOP plane within 1/8".
    The normal pointing OUT of the rafter bottom is (0,0,-1).
    """
    errors: list[str] = []
    rafters = [s for s in scene.solids if s.role == "rafter"]
    for r in rafters:
        # Outward normal for bottom seat face is DOWN (0,0,-1)
        seat_faces = [
            f for f in r.faces 
            if f.normal[2] < -0.95 and abs(vcent(f.verts)[2] - scene.Z_BEAM_TOP) < 0.2
        ]
        if not seat_faces:
            # If no level seat face found, the rafter is likely 'floating' or has no notch
            errors.append(f"rafter_seating_on_beam: rafter {r.tag} has no level seat face near Z_BEAM_TOP (floating)")
            continue
            
        for face in seat_faces:
            fz = vcent(face.verts)[2]
            delta = abs(fz - scene.Z_BEAM_TOP)
            if delta > _CONTACT_TOL:
                errors.append(
                    f"rafter_seating_on_beam: rafter {r.tag} seat face Z={fz:.4f} ft, "
                    f"Z_BEAM_TOP={scene.Z_BEAM_TOP:.4f} ft, gap={delta * 12:.3f}\""
                )
    return errors


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_connections(scene: "Scene") -> list[str]:
    """
    Run all physical contact checks against a Scene.
    Returns a list of error strings — empty list means all checks passed.
    """
    errors: list[str] = []
    errors.extend(_check_beam_soffit_at_post_top(scene))
    errors.extend(_check_rafter_tip_on_hub_face(scene))
    errors.extend(_check_brace_foot_on_post_face(scene))
    errors.extend(_check_jack_to_hip_contact(scene))
    errors.extend(_check_rafter_seating_on_beam(scene))
    return errors


def assert_connections_physical(scene: "Scene") -> None:
    """
    Run validate_connections; raise ConnectionError with details if any check fails.
    Call this after build_structure_scene() and validate_scene_geometry(), before rendering.
    """
    errors = validate_connections(scene)
    if errors:
        lines = "\n".join(f"  {e}" for e in errors)
        raise ContactError(
            f"Physical contact validation FAILED ({len(errors)} error(s)) — "
            f"scene geometry has disconnected members:\n{lines}"
        )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate physical surface contact in a built CAD scene."
    )
    parser.add_argument(
        "structure", nargs="?",
        help="Path to a sealed structure.json (scene will be built and validated)"
    )
    args = parser.parse_args()

    if not args.structure:
        parser.print_help()
        sys.exit(1)

    try:
        from cad_scene import build_structure_scene
    except ImportError:
        print("ERROR: cad_scene module not found — run from scripts/ directory", file=sys.stderr)
        sys.exit(2)

    with open(args.structure, encoding="utf-8") as f:
        structure = json.load(f)

    # Legacy model/calcs split — pass structure as model, geometry-calculations separately if available
    calcs_path = Path(args.structure).parent / "geometry-calculations.json"
    calcs: dict | None = None
    if calcs_path.exists():
        with open(calcs_path, encoding="utf-8") as f:
            calcs = json.load(f)

    scene = build_structure_scene(structure, calcs)
    errors = validate_connections(scene)

    if errors:
        print(f"PHYSICAL CONTACT VALIDATION FAILED — {len(errors)} error(s):")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("PHYSICAL CONTACT VALIDATION PASSED — all members have surface contact")
        sys.exit(0)


if __name__ == "__main__":
    main()
