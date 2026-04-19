import os

files_to_merge = {
    "SOURCE INTENT (design-spec.json)": "context/staging/design-spec.json",
    "ENGINEERED PHYSICS (structural-model.json)": "context/staging/structural-model.json",
    "GENERATED OUTPUT 1 (blueprint-plan.svg)": "outputs/blueprint-plan.svg",
    "GENERATED OUTPUT 2 (blueprint-isometric.svg)": "outputs/blueprint-isometric.svg"
}

with open("validation_payload.md", "w") as out:
    for title, path in files_to_merge.items():
        out.write(f"--- {title} ---\n")
        try:
            with open(path, "r") as f:
                out.write(f.read() + "\n\n")
        except FileNotFoundError:
            out.write(f"Error: {path} not found.\n\n")

print("Created validation_payload.md")
