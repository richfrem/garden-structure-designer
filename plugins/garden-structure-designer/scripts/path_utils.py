"""
path_utils.py
=============

Purpose:
    Single resolver for the repository layout used by every script: the repo root, the plugin
    root, the staging bus directory (context/staging, home of structure.json), the outputs
    directory, schemas, scripts and the agent workspace. Resolution walks up from the start path
    (or cwd) to a repo marker, so scripts are cwd-agnostic.

Layer: Core / Shared Utility

Key Input Dependencies:
    - a repo marker above the start path: .git, pyproject.toml or plugins/garden-structure-designer

Key Functions:
    find_repo_root(start=None) -> Path
    plugin_root(start=None) -> Path          schemas_dir(start=None) -> Path        scripts_dir(start=None) -> Path
    staging_dir(start=None) -> Path          outputs_dir(start=None) -> Path        agent_workspace_dir(start=None) -> Path
    ensure_dirs() -> None

Usage Examples:
    python3 path_utils.py          # creates the standard directories and prints them
"""
from pathlib import Path
import os

def find_repo_root(start: str | Path | None = None) -> Path:
    """Walk upward from start/cwd until a repo marker is found."""
    current = Path(start).resolve() if start else Path.cwd().resolve()
    for parent in [current] + list(current.parents):
        if (parent / ".git").exists() or (parent / "pyproject.toml").exists() or (parent / "plugins" / "garden-structure-designer").exists():
            return parent
    return Path.cwd().resolve()

def plugin_root(start: str | Path | None = None) -> Path:
    """Plugin root: <repo>/plugins/garden-structure-designer."""
    return find_repo_root(start) / "plugins" / "garden-structure-designer"

def staging_dir(start: str | Path | None = None) -> Path:
    """Staging bus directory: <repo>/context/staging (holds structure.json)."""
    return find_repo_root(start) / "context" / "staging"

def get_project_name(structure_dict: dict | None = None, start: str | Path | None = None) -> str:
    """Infers the project subfolder name from structure data, environment, or staging structure.json."""
    env_sub = os.environ.get("GSD_OUTPUT_SUBDIR")
    if env_sub:
        return env_sub.strip()
    
    data = structure_dict
    if data is None:
        try:
            stg = staging_dir(start) / "structure.json"
            if stg.exists():
                import json
                with open(stg, encoding="utf-8") as f:
                    data = json.load(f)
        except Exception:
            data = None

    if isinstance(data, dict):
        # 1. Explicit project_name in meta
        meta = data.get("meta", {})
        if meta.get("project_name"):
            return str(meta["project_name"]).strip()
        # 2. Derive from source_hash (e.g. intent_10ft_hex_pergola_yellow_cedar_20261011 -> 10ft-hex-pergola)
        src_hash = meta.get("source_hash", "")
        if "10ft_hex" in src_hash:
            return "10ft-hex-pergola"
        # 3. Derive from structure layout & type
        struct_info = data.get("structure", {})
        layout_info = data.get("layout", {})
        stype = struct_info.get("type", "pergola")
        sshape = struct_info.get("shape", layout_info.get("shape", "structure"))
        radius = layout_info.get("inscribed_radius_ft")
        if radius:
            size_str = f"{int(round(radius * 2))}ft"
            return f"{size_str}-{sshape[:3]}-{stype}".lower()
        if sshape:
            return f"{sshape}-{stype}".lower()

    return "10ft-hex-pergola"


def outputs_dir(start: str | Path | None = None, subdir: str | Path | None = None) -> Path:
    """Outputs directory: strictly returns <repo>/outputs/<project-subdir> to prevent writing at root."""
    base = find_repo_root(start) / "outputs"
    sub = subdir or get_project_name(start=start)
    return base / str(sub).strip()


def schemas_dir(start: str | Path | None = None) -> Path:
    """Schemas directory inside the plugin (assets/schemas)."""
    return plugin_root(start) / "assets" / "schemas"

def scripts_dir(start: str | Path | None = None) -> Path:
    """Canonical scripts directory inside the plugin."""
    return plugin_root(start) / "scripts"

def agent_workspace_dir(start: str | Path | None = None) -> Path:
    """Agent workspace: <repo>/temp/agent-workspace/garden-structure-designer."""
    return find_repo_root(start) / "temp" / "agent-workspace" / "garden-structure-designer"

def ensure_dirs() -> None:
    """Creates the standard working directories (staging, outputs, schemas, scripts, agent workspace)."""
    for d in [staging_dir(), outputs_dir(), schemas_dir(), scripts_dir(), 
              agent_workspace_dir(), agent_workspace_dir() / "learned-patterns", 
              agent_workspace_dir() / "generated-tests", agent_workspace_dir() / ".backups"]:
        d.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_dirs()
    print(f"Repo Root:       {find_repo_root()}")
    print(f"Plugin Root:     {plugin_root()}")
    print(f"Staging Dir:     {staging_dir()}")
    print(f"Outputs Dir:     {outputs_dir()}")
    print(f"Schemas Dir:     {schemas_dir()}")
    print(f"Scripts Dir:     {scripts_dir()}")
    print(f"Agent Workspace: {agent_workspace_dir()}")
