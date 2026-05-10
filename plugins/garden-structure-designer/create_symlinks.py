import os
import glob
import subprocess

symlink_mgr = "/Users/richardfremmerlid/Projects/garden-structure-designer/.agents/skills/symlink-manager/scripts/symlink_manager.py"
plugin_dir = "/Users/richardfremmerlid/Projects/garden-structure-designer/plugins/garden-structure-designer"
scripts = glob.glob(os.path.join(plugin_dir, "scripts", "*.py"))
skills_dir = os.path.join(plugin_dir, "skills")
skills = [os.path.join(skills_dir, d) for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]

for skill in skills:
    skill_scripts_dir = os.path.join(skill, "scripts")
    os.makedirs(skill_scripts_dir, exist_ok=True)
    for script in scripts:
        script_name = os.path.basename(script)
        dst = os.path.join(skill_scripts_dir, script_name)
        # We need the relative path from dst to src.
        # dst is plugins/garden-structure-designer/skills/XYZ/scripts/foo.py
        # src is plugins/garden-structure-designer/scripts/foo.py
        # Relative is ../../../scripts/foo.py
        src_rel = f"../../../scripts/{script_name}"
        
        # dst relative to plugin root for the symlink manager
        dst_rel = os.path.relpath(dst, plugin_dir)
        
        print(f"Creating symlink {dst_rel} -> {src_rel}")
        subprocess.run(["python3", symlink_mgr, "create", "--src", src_rel, "--dst", dst_rel], cwd=plugin_dir)

print("Symlinks created.")
