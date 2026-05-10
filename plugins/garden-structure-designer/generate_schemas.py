import os
import json

schemas_dir = "/Users/richardfremmerlid/Projects/garden-structure-designer/plugins/garden-structure-designer/schemas"
os.makedirs(schemas_dir, exist_ok=True)

names = [
    "design-spec", "structural-model", "geometry-calculations", 
    "bracing-model", "joinery-model", "building-code", 
    "cut-list", "manifest"
]

for name in names:
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": name,
        "type": "object",
        "properties": {
            "schema": {"type": "string"},
            "source_hash": {"type": "string"}
        },
        "additionalProperties": True
    }
    with open(os.path.join(schemas_dir, f"{name}.schema.json"), "w") as f:
        json.dump(schema, f, indent=2)

print("Schemas generated.")
