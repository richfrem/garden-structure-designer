import json

def update_json(path, updater):
    with open(path, 'r') as f:
        data = json.load(f)
    updater(data)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def upd_geo(d):
    d["required"] = ["schema", "compound_cut", "beam_ring", "svg_coordinates", "warnings", "source_hash"]
    d["properties"] = {
        "schema": {"type": "string"},
        "source_hash": {"type": "string"},
        "compound_cut": {"type": "object"},
        "beam_ring": {"type": "object"},
        "svg_coordinates": {"type": "object"},
        "warnings": {"type": "array"}
    }
update_json("plugins/garden-structure-designer/schemas/geometry-calculations.schema.json", upd_geo)

def upd_design(d):
    d["required"] = ["schema", "structureType", "planShape", "jurisdiction", "pitch"]
    d["properties"] = {
        "schema": {"type": "string"},
        "source_hash": {"type": "string"},
        "structureType": {"type": "string"},
        "planShape": {"type": "string"},
        "pitch": {"type": "string"},
        "jurisdiction": {"type": "string"}
    }
update_json("plugins/garden-structure-designer/schemas/design-spec.schema.json", upd_design)

def upd_struct(d):
    d["properties"]["roofStructure"]["properties"]["pitch"] = {"type": "string", "pattern": "^\\d+:\\d+$"}
    if "spanDistance_ft" not in d["properties"]["members"]["properties"]["posts"]["required"]:
        d["properties"]["members"]["properties"]["posts"]["required"].append("spanDistance_ft")
    d["properties"]["members"]["properties"]["posts"]["properties"]["spanDistance_ft"] = {"type": "number"}
update_json("plugins/garden-structure-designer/schemas/structural-model.schema.json", upd_struct)

with open("plugins/garden-structure-designer/context/staging/learning-registry.json", "w") as f:
    json.dump({"schema": "garden-structure-designer/learning-registry/1.0", "active_lessons": []}, f, indent=2)
