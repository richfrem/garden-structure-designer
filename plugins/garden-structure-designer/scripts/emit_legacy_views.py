#!/usr/bin/env python3
"""
emit_legacy_views.py — M1 compatibility shim.
Reads structure.json and writes legacy staging files as derived read-only views.
REMOVE IN MILESTONE 2 once all agents/skills are updated.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from structure_io import load_structure  # type: ignore[import]


def emit(structure_path: str) -> None:
    structure = load_structure(structure_path)
    staging = Path(structure_path).parent
    geom = structure.get("geometry", {})
    src_hash = structure["meta"]["source_hash"]

    # design-spec.json
    design_spec = {
        "schema": "garden-structure-designer/design-spec/1.0",
        "source_hash": src_hash,
        "structureType": structure["structure"]["type"],
        "planShape": structure["structure"]["shape"],
        "jurisdiction": structure["intent"]["jurisdiction"],
        "pitch": structure["roof"]["pitch"],
        "pitchDefaulted": structure["roof"].get("pitch_defaulted", False),
        "project": {
            "structure_type": structure["structure"]["type"].capitalize(),
            "shape": structure["structure"]["shape"].capitalize(),
            "primary_material": structure["intent"].get("material_preference", "Cedar"),
        },
        "dimensions": {
            "height_total_ft": structure["members"]["posts"]["cut_length_ft"],
            "max_diagonal_ft": structure["layout"]["inscribed_radius_ft"] * 2,
            "post_spacing_diagonal_ft": structure["layout"]["inscribed_radius_ft"] * 2,
        },
        "materials": {
            "post_size": structure["members"]["posts"]["nominal_size"],
            "timber_species": structure["intent"].get("material_preference", "Western Red Cedar"),
        },
        "site": {
            "location": structure["intent"]["jurisdiction"],
            "canonical_location_id": structure["intent"]["jurisdiction"],
        },
        "style": {
            "joinery_preference": structure["intent"].get("joinery_style", "Traditional timber framing"),
            "knee_braces": "Decorative 4x4 cedar braces" if structure.get("bracing", {}).get("enabled") else "None",
            "rafter_tails": structure.get("joinery", {}).get("rafter_tail", "decorative_scallop"),
            "roof_pitch": structure["roof"]["pitch"],
        },
    }

    # structural-model.json
    br = structure.get("bracing", {})
    brace = br.get("brace", {})
    structural_model = {
        "schema": "garden-structure-designer/structural-model/1.0",
        "source_hash": src_hash,
        "_locked": True,
        "structureType": structure["structure"]["type"],
        "planShape": structure["structure"]["shape"],
        "members": {
            "posts": {
                "quantity":         structure["layout"]["post_count"],
                "dimensions":       structure["members"]["posts"]["nominal_size"],
                "cutLength_ft":     structure["members"]["posts"]["cut_length_ft"],
                "spanDistance_ft":  structure["layout"]["inscribed_radius_ft"],
                "nominalSize":      structure["members"]["posts"]["nominal_size"],
                "width_in":         structure["members"]["posts"]["actual_width_in"],
                "depth_in":         structure["members"]["posts"]["actual_depth_in"],
            },
            "beams": {
                "quantity":    structure["layout"]["post_count"],
                "dimensions":  structure["members"]["beams"]["nominal_size"],
                "depth_in":    structure["members"]["beams"]["actual_depth_in"],
                "width_in":    structure["members"]["beams"]["actual_width_in"],
                "nominalSize": structure["members"]["beams"]["nominal_size"],
                "cutLength_ft": structure["members"]["beams"]["cut_length_ft"],
            },
            "kneebraces": {
                "quantity":      structure["layout"]["post_count"] * brace.get("count_per_post", 2),
                "dimensions":    brace.get("nominal_size", "4x4"),
                "cutLength_in":  round(brace.get("length_ft", 2.5) * 12),
                "angle_deg":     brace.get("angle_deg", 45),
                "width_in":      brace.get("actual_width_in", 3.5),
                "depth_in":      brace.get("actual_depth_in", 3.5),
            },
            "rafters": {
                "quantity":       structure["roof"]["primary_rafters"]["count"],
                "dimensions":     structure["roof"]["primary_rafters"]["nominal_size"],
                "miterAngle_deg": geom.get("compound_cut", {}).get("miter_deg", 28.71),
                "cutLength_ft":   geom.get("rafter", {}).get("total_with_overhang_ft", 6.2),
                "nominalSize":    structure["roof"]["primary_rafters"]["nominal_size"],
                "width_in":       structure["roof"]["primary_rafters"]["actual_width_in"],
                "depth_in":       structure["roof"]["primary_rafters"]["actual_depth_in"],
            },
        },
        "roofStructure": {
            "pitch": structure["roof"]["pitch"],
            "pitchDefaulted": structure["roof"].get("pitch_defaulted", False),
            "style": structure.get("presentation", {}).get("roof_style", "Open Rafter"),
        },
        "overhang_in": round(structure["roof"]["primary_rafters"]["overhang_ft"] * 12),
        "bracing_added": br.get("enabled", True),
        "materials": {"primary": structure["intent"].get("material_preference", "Cedar").split()[0]},
        "joinery": {"type": "traditional"},
        "foundation": {"caisson_diameter_in": structure["footings"]["diameter_in"]},
    }

    # geometry-calculations.json
    geometry_calculations = {
        "schema": "geometry-calculations/1.0",
        "source": "context/staging/structure.json",
        "source_hash": src_hash,
        "pitch":        structure["roof"]["pitch"],
        "sides":        structure["structure"]["sides"],
        "compound_cut": geom.get("compound_cut", {}),
        "beam_ring":    geom.get("beam_ring", {}),
        "rafter":       geom.get("rafter", {}),
        "roof_rise":    geom.get("roof_rise", {}),
        "total_height": geom.get("total_height", {}),
        "svg_coordinates": geom.get("svg_coordinates", {}),
        "warnings":     geom.get("warnings", []),
    }

    (staging / "design-spec.json").write_text(json.dumps(design_spec, indent=2))
    (staging / "structural-model.json").write_text(json.dumps(structural_model, indent=2))
    (staging / "geometry-calculations.json").write_text(json.dumps(geometry_calculations, indent=2))
    print(f"Legacy views emitted to {staging}/")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 emit_legacy_views.py context/staging/structure.json")
        sys.exit(1)
    emit(sys.argv[1])


if __name__ == "__main__":
    main()
