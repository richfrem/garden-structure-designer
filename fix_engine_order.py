with open("plugins/garden-structure-designer/scripts/geometry_engine.py", "r") as f:
    lines = f.readlines()
    
# Find where structure["geometry"] is assigned
idx = -1
for i, line in enumerate(lines):
    if "structure[\"geometry\"] = {" in line:
        idx = i
        break
        
if idx != -1:
    # 1. Change _sealed to False in the assignment
    for j in range(idx, idx + 10):
        if "\"_sealed\":" in lines[j]:
            lines[j] = lines[j].replace("True", "False")
            break
            
    # 2. Move joints = compute_joints(structure) BEFORE the final assignment or fix it
    # Wait, the current order in file is:
    # 720: joints = compute_joints(structure)
    # 723: structure["geometry"] = { ... }
    
    # Let's change it to:
    # 723: structure["geometry"] = { ... } (unsealed)
    # joints = compute_joints(structure)
    # structure["geometry"]["joints"] = joints
    # structure["geometry"]["_sealed"] = True
    
    # Actually, I'll just change compute_joints to take the individual components.
    pass

# Alternative: update compute_joints to use the variables directly instead of structure["geometry"]
