#!/usr/bin/env python3
"""
learning_backup.py (CLI)
=====================================

Purpose:
    learning_backup.py =====================================

Layer: Execution

Usage Examples:
    python learning_backup.py [args]

Supported Object Types:
    JSON, SVG, Markdown

CLI Arguments:
    Varies per script, typically input file paths.

Input Files:
    context/staging/ *.json outputs/ *.svg

Output:
    Validation codes (0 or 1), generated JSON or SVG files.

Key Functions:
    Refer to module docstring or inner functions.

Script Dependencies:
    Standard library json, os, sys, math, hashlib, etc.

Consumed by:
    design-orchestrator, various skills in the pipeline.
"""
import json
import sys
import shutil
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir, agent_workspace_dir, plugin_root

def main():
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
