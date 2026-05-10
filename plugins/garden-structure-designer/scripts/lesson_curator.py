#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir

def load_registry():
    reg = staging_dir() / "learning-registry.json"
    if reg.exists():
        with open(reg) as f: return json.load(f)
    return {"schema": "garden-structure-designer/learning-registry/1.1", "active_lessons": []}

def save_registry(data):
    with open(staging_dir() / "learning-registry.json", "w") as f:
        json.dump(data, f, indent=2)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 lesson_curator.py <status|pin|archive|restore|backup> [lesson-id]")
        sys.exit(1)
        
    cmd = sys.argv[1]
    reg = load_registry()
    
    if cmd == "status":
        print(f"Total Lessons: {len(reg['active_lessons'])}")
        for l in reg['active_lessons']:
            print(f"- {l.get('id', 'unknown')} [{l.get('state', 'active')}] pinned: {l.get('pinned', False)}")
            
    elif cmd in ["pin", "archive", "restore"]:
        if len(sys.argv) < 3:
            print("Missing lesson-id")
            sys.exit(1)
        lid = sys.argv[2]
        for l in reg['active_lessons']:
            if l.get('id') == lid:
                if cmd == "pin": l['pinned'] = True
                elif cmd == "archive": l['state'] = "archived"
                elif cmd == "restore": l['state'] = "active"
                save_registry(reg)
                print(f"Lesson {lid} updated to {cmd}")
                return
        print(f"Lesson {lid} not found.")
        
    elif cmd == "backup":
        import subprocess
        subprocess.run([sys.executable, str(Path(__file__).parent / "learning_backup.py")])

if __name__ == "__main__":
    main()
