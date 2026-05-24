import sys

def fix_legacy_path():
    with open("plugins/garden-structure-designer/scripts/cad_scene.py", "r") as f:
        lines = f.readlines()
        
    for i in range(len(lines)):
        if 'term_pts = geom.get("joints", {}).get("rafters"' in lines[i]:
            # Check if we are in _build_scene_legacy or _build_scene_from_structure
            # If we are in legacy, we should probably check if calcs has joints
            # But the variable is 'calcs' in legacy, 'geom' in from_structure
            
            # Find the function context
            j = i
            while j > 0 and "def " not in lines[j]:
                j -= 1
            
            if "_build_scene_legacy" in lines[j]:
                lines[i] = '            term_pts = calcs.get("joints", {}).get("rafters", {}).get("hub_termination_points", {}).get("points", [])\n'
            
        elif 'beam_id = f"B{i+1}"' in lines[i] and 'end_planes = geom.get("joints"' in lines[i+1]:
             j = i
             while j > 0 and "def " not in lines[j]:
                 j -= 1
             if "_build_scene_legacy" in lines[j]:
                 lines[i+1] = '        end_planes = calcs.get("joints", {}).get("beam_ring", {}).get("beam_end_planes", [])\n'
                 
        elif 'endpoints = geom.get("joints", {}).get("braces"' in lines[i]:
             j = i
             while j > 0 and "def " not in lines[j]:
                 j -= 1
             if "_build_scene_legacy" in lines[j]:
                 lines[i] = '        endpoints = calcs.get("joints", {}).get("braces", {}).get("endpoints", {}).get("pairs", [])\n'

    with open("plugins/garden-structure-designer/scripts/cad_scene.py", "w") as f:
        f.writelines(lines)

fix_legacy_path()
