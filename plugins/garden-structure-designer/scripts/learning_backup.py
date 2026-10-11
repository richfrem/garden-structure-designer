#!/usr/bin/env python3
"""
learning_backup.py
==================

Purpose:
    Timestamped backup of the learning artifacts (learned patterns, generated tests, the learning
    registry, repair-map.json and every skill's SKILL.md) under agent-workspace/.../.backups/<ts>.

Layer: Execution / Learning Loop

Key Input Dependencies:
    - agent workspace learned-patterns/ and generated-tests/, context/staging/learning-registry.json,
      plugin repair-map.json, skills/*/SKILL.md, path_utils.py

Key Functions:
    main() -> None

Usage Examples:
    python3 learning_backup.py
"""
import json
import sys
import shutil
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir, agent_workspace_dir, plugin_root

def main():
    """Copies the learning artifacts and each SKILL.md into a new timestamped backup directory."""
    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    backup_dir = agent_workspace_dir() / ".backups" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    targets = [
        agent_workspace_dir() / "learned-patterns",
        agent_workspace_dir() / "generated-tests",
        staging_dir() / "learning-registry.json",
        plugin_root() / "repair-map.json"
    ]
    
    for t in targets:
        if not t.exists():
            continue
        dest = backup_dir / t.name
        if t.is_dir():
            shutil.copytree(t, dest)
        else:
            shutil.copy2(t, dest)
            
    # Backup skills SKILL.md
    skills_dir = plugin_root() / "skills"
    if skills_dir.exists():
        dest_skills = backup_dir / "skills"
        dest_skills.mkdir(parents=True, exist_ok=True)
        for skill in skills_dir.iterdir():
            if skill.is_dir():
                skill_md = skill / "SKILL.md"
                if skill_md.exists():
                    (dest_skills / skill.name).mkdir(parents=True, exist_ok=True)
                    shutil.copy2(skill_md, dest_skills / skill.name / "SKILL.md")
                    
    print(f"Backed up learning artifacts to {backup_dir}")

if __name__ == "__main__":
    main()
