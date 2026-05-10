import json
import os

schemas_dir = "plugins/garden-structure-designer/schemas"

structural_model = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "structural-model",
    "type": "object",
    "required": ["schema", "source_hash", "_locked", "roofStructure", "members"],
    "properties": {
        "schema": {"type": "string"},
        "source_hash": {"type": "string"},
        "_locked": {"type": "boolean"},
        "roofStructure": {
            "type": "object",
            "required": ["pitch", "style"],
            "properties": {
                "pitch": {"type": "number"},
                "style": {"type": "string"}
            }
        },
        "members": {
            "type": "object",
            "required": ["posts", "beams", "rafters"],
            "properties": {
                "posts": {
                    "type": "object",
                    "required": ["quantity", "cutLength_ft", "nominalSize"],
                    "properties": {
                        "quantity": {"type": "integer"},
                        "cutLength_ft": {"type": "number"},
                        "nominalSize": {"type": "string"}
                    }
                },
                "beams": {
                    "type": "object",
                    "required": ["quantity", "cutLength_ft", "nominalSize"],
                    "properties": {
                        "quantity": {"type": "integer"},
                        "cutLength_ft": {"type": "number"},
                        "nominalSize": {"type": "string"}
                    }
                },
                "rafters": {
                    "type": "object",
                    "required": ["quantity", "cutLength_ft", "nominalSize", "miterAngle_deg"],
                    "properties": {
                        "quantity": {"type": "integer"},
                        "cutLength_ft": {"type": "number"},
                        "nominalSize": {"type": "string"},
                        "miterAngle_deg": {"type": "number"}
                    }
                }
            }
        }
    }
}

design_spec = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "design-spec",
    "type": "object",
    "required": ["schema", "style", "footprint_ft", "jurisdiction"],
    "properties": {
        "schema": {"type": "string"},
        "source_hash": {"type": "string"},
        "style": {"type": "string"},
        "footprint_ft": {
            "type": "object",
            "required": ["width", "length"],
            "properties": {
                "width": {"type": "number"},
                "length": {"type": "number"}
            }
        },
        "jurisdiction": {"type": "string"}
    }
}

building_code = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "building-code",
    "type": "object",
    "required": ["schema", "jurisdiction", "snowLoad_psf", "windLoad_mph", "frostDepth_in"],
    "properties": {
        "schema": {"type": "string"},
        "source_hash": {"type": "string"},
        "jurisdiction": {"type": "string"},
        "snowLoad_psf": {"type": "number"},
        "windLoad_mph": {"type": "number"},
        "frostDepth_in": {"type": "number"}
    }
}

bracing_model = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "bracing-model",
    "type": "object",
    "required": ["schema", "braces"],
    "properties": {
        "schema": {"type": "string"},
        "source_hash": {"type": "string"},
        "braces": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["type", "quantity", "length_in"],
                "properties": {
                    "type": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "length_in": {"type": "number"}
                }
            }
        }
    }
}

cut_list = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "cut-list",
    "type": "object",
    "required": ["schema", "items", "total_board_feet", "waste_factor"],
    "properties": {
        "schema": {"type": "string"},
        "source_hash": {"type": "string"},
        "total_board_feet": {"type": "number"},
        "waste_factor": {"type": "number"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["partId", "quantity", "length_ft", "nominal"],
                "properties": {
                    "partId": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "length_ft": {"type": "number"},
                    "nominal": {"type": "string"}
                }
            }
        }
    }
}

joinery_model = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "joinery-model",
    "type": "object",
    "required": ["schema", "connections"],
    "properties": {
        "schema": {"type": "string"},
        "source_hash": {"type": "string"},
        "connections": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["node", "type", "fasteners"],
                "properties": {
                    "node": {"type": "string"},
                    "type": {"type": "string"},
                    "fasteners": {"type": "string"}
                }
            }
        }
    }
}

geometry_calculations = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "geometry-calculations",
    "type": "object",
    "required": ["schema", "nodes", "angles"],
    "properties": {
        "schema": {"type": "string"},
        "source_hash": {"type": "string"},
        "nodes": {
            "type": "object"
        },
        "angles": {
            "type": "object"
        }
    }
}

manifest_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "manifest",
    "type": "object",
    "required": ["version", "components"],
    "properties": {
        "version": {"type": "string"},
        "source_hash": {"type": "string"},
        "components": {"type": "array"}
    }
}

schemas = {
    "structural-model.schema.json": structural_model,
    "design-spec.schema.json": design_spec,
    "building-code.schema.json": building_code,
    "bracing-model.schema.json": bracing_model,
    "cut-list.schema.json": cut_list,
    "joinery-model.schema.json": joinery_model,
    "geometry-calculations.schema.json": geometry_calculations,
    "manifest.schema.json": manifest_schema
}

for filename, data in schemas.items():
    with open(os.path.join(schemas_dir, filename), "w") as f:
        json.dump(data, f, indent=2)

print("Real schemas generated.")
