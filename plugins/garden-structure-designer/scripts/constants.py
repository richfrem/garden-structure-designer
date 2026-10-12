#!/usr/bin/env python3
"""
constants.py
============

Purpose:
    Single source of truth for drafting, layer, unit and tolerance constants shared
    by the DXF exchange writers, the SVG blueprint renderer and the cross-artifact
    validator. Never redefine these values locally; import them from here.

Layer: Core (constants)

Consumers:
    exchange_writer.py, cadcraft_adapter.py, export_cad.py, cross_artifact_validator.py,
    compile_package.py, structure_io.py, pipeline_runner.py, cad_backend_build123d.py,
    render_drawings.py, tests.

Key Constants (index):
    Units: MM_PER_INCH, INCHES_PER_FOOT, MM_PER_FOOT, MM_PER_UNIT, INSUNITS_MM
    CAD limits: CAD_EXPORT_TIMEOUT_S (C3 15s export deadline)
    DXF sheets/layers: APPID, SHEET_ID_STRUCTURE, SHEET_ID_PLAN, SHEET_IDS, SHEET_FILENAMES, CAD_SUBDIR,
        DIMENSION_LAYER, LAYER_COLORS, ROLE_LAYERS
    Dimension standards: DIM_OFFSET_MM, DIM_TEXT_HEIGHT_MM, DIM_TICK_OFFSET_MM
    SVG lineweights: LW_*
    Tolerances: DXF_BOUNDS_TOL_MM (C4 0.01 mm), DXF_PLANAR_TOL_MM, DIM_CROSSCHECK_TOL_MM
    C5: ERROR_STALE_REVISION, ERROR_RECOVERY_REQUIRED, C5_PURGE_GLOBS, C5_PURGE_ROOTS

Script Dependencies:
    Standard library only.
"""
from __future__ import annotations

# --- Units ---
MM_PER_INCH = 25.4
INCHES_PER_FOOT = 12
MM_PER_FOOT = 304.8  # = MM_PER_INCH * INCHES_PER_FOOT
MM_PER_UNIT: dict[str, float] = {"feet": MM_PER_FOOT, "ft": MM_PER_FOOT, "mm": 1.0}
INSUNITS_MM = 4  # DXF $INSUNITS code for millimetres

# --- DXF sheets, application id and layers (C4 contract) ---
APPID = "GSD"
SHEET_ID_STRUCTURE = "SB01"  # full-scale 3D WCS wireframe
SHEET_ID_PLAN = "SB02"  # XY plan projection (Z = 0)
SHEET_IDS = (SHEET_ID_STRUCTURE, SHEET_ID_PLAN)
SHEET_FILENAMES: dict[str, str] = {
    SHEET_ID_STRUCTURE: "SB01-structure.dxf",
    SHEET_ID_PLAN: "SB02-plan.dxf",
}
CAD_SUBDIR = "cad"
DIMENSION_LAYER = "DIMENSIONS_ARCH"
# layer name -> AutoCAD color index
LAYER_COLORS: dict[str, int] = {
    "FRAMING_POSTS": 1,
    "FRAMING_BEAMS": 3,
    "FRAMING_RAFTERS": 4,
    "FRAMING_HUBS": 6,
    "FRAMING_BRACES": 5,
    "FOOTINGS_PIERS": 8,
    DIMENSION_LAYER: 2,
}
ROLE_LAYERS: dict[str, str] = {
    "post": "FRAMING_POSTS",
    "beam": "FRAMING_BEAMS",
    "rafter": "FRAMING_RAFTERS",
    "hub": "FRAMING_HUBS",
    "brace": "FRAMING_BRACES",
    "footing": "FOOTINGS_PIERS",
}

# --- CAD subprocess limits (C3) ---
CAD_EXPORT_TIMEOUT_S = 15  # export deadline for one cadcraft-cli invocation

# --- SVG drawing sheets (Stage 4 produces all eight) ---
SVG_SHEET_FILENAMES: tuple[str, ...] = (
    "drawing-plan-view.svg",
    "drawing-elevation-view.svg",
    "drawing-isometric-view.svg",
    "drawing-perspective-view.svg",
    "blueprint-plan.svg",
    "blueprint-elevation.svg",
    "blueprint-isometric.svg",
    "blueprint-component-isolation.svg",
)
FABRICATION_SUBDIR = "fabrication"
CUT_LIST_FILENAME = "cut-list.json"

# --- DXF dimension standards (millimetres) ---
DIM_OFFSET_MM = 600.0  # dimension line offset from the post extents
DIM_TEXT_HEIGHT_MM = 150.0
DIM_TICK_OFFSET_MM = 100.0  # architectural tick overshoot past the extension line

# --- SVG lineweights (px) ---
LW_TITLE_BORDER = 1.8
LW_TITLE_RULE = 1.0
LW_LEADER = 0.8
LW_DIMENSION = 1.2
LW_GROUND_LINE = 2.0
LW_MEMBER_DRAWING = 1.2
LW_MEMBER_BLUEPRINT = 3.0

# --- Camera & Viewport Standards (C1/C4/Option C) ---
VIEWPORT_MARGIN_PX = 40.0
ISOMETRIC_OUTWARD_VECTOR = (1.0, -1.0, 1.0)  # Unnormalized direction
PERSPECTIVE_DEFAULT_FOV_DEG = 60.0


# --- Validation tolerances ---
DXF_BOUNDS_TOL_MM = 0.01  # C4: max absolute exchange error vs sealed solved geometry (WCS mm)
DXF_PLANAR_TOL_MM = 1e-6  # SB02 must be planar (|Z| <= tol)
DIM_CROSSCHECK_TOL_MM = MM_PER_INCH  # SVG label vs DXF geometry parity (1 in)

# --- Topology family registry (C1): radial family and orthogonal grid family ---
IMPLEMENTED_FAMILIES: tuple[str, ...] = ("RadialHubTopology", "OrthogonalGridTopology")
RESERVED_FAMILIES: tuple[str, ...] = ("HipRidgeTopology",)

# --- Footings ---
FOOTING_STUB_ABOVE_GRADE_FT = 0.33  # declared nowhere in structure.json; planning assumption for the pier stub above grade

# --- Physical contact tolerances (feet) used by validate_connections ---
CONTACT_BEAM_SOFFIT_TOL_FT = 0.0104  # ~1/8 inch
CONTACT_RAFTER_TIP_TOL_FT = 0.2
CONTACT_BRACE_FOOT_MAX_FT = 1.0
CONTACT_SEAT_WARN_RANGE_FT = (0.1, 0.2)  # (lower, upper) deviation that raises a seating warning
CONTACT_BRACE_RADIUS_WARN_FT = 0.5

# --- Stage 2 radial polygon regularity (post_xy is rounded to 4 decimal feet by the geometry solver) ---
POLYGON_RADIUS_TOL_FT = 1e-3
POLYGON_ANGLE_TOL_RAD = 1e-3

# --- C5 transaction purge inventory (globs relative to the project root) ---
ERROR_STALE_REVISION = "STALE_REVISION"
ERROR_RECOVERY_REQUIRED = "RECOVERY_REQUIRED"
C5_PURGE_GLOBS: tuple[str, ...] = (
    # Solved staging mirrors
    "context/staging/structural-model.json",
    "context/staging/geometry-calculations.json",
    "context/staging/design-spec.json",  # legacy shim artifact
    # Drawings / CAD
    "outputs/*.svg",
    "outputs/cad/*.dxf",
    # Fabrication
    "outputs/fabrication/cut-list.json",
    "outputs/fabrication/*-cut-list.json",
    # Packages / docs
    "outputs/pergola_plan.md",
    "outputs/pergola_plan.pdf",
    # Builder docs / package outputs
    "outputs/assembly-guide.md",
    "outputs/budget-estimate.md",
    "outputs/lumber-purchase-list.md",
    "outputs/pergola_plan_embedded.md",
    "outputs/pergola_plan_embedded.pdf",
    "outputs/package-manifest.json",
    "outputs/COMPILATION_BLOCKED.md",
    "outputs/PDF_GENERATION_FAILED.md",
    # Legacy cut list (deprecated cut_list_engine) and preview rasters
    "outputs/shop-blueprint/*",
    "outputs/visual-smoke/*",
    "outputs/high-resolution-image/*",
    # QA / approval (archived run history such as script-run-history.jsonl is intentionally excluded)
    "context/staging/*-report.json",
    "outputs/*-report.md",
    "outputs/quality-dashboard*",
    "outputs/run-insights.json",
)
C5_PURGE_ROOTS: tuple[str, ...] = ("context/staging", "outputs")
