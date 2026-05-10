#!/usr/bin/env python3
"""
path_utils.py
=====================================
Purpose:
    Core logic for path_utils.py functionality within garden-structure-designer pipeline.
Layer: Execution
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
    return find_repo_root(start) / "plugins" / "garden-structure-designer"

def staging_dir(start: str | Path | None = None) -> Path:
    return plugin_root(start) / "context" / "staging"

def outputs_dir(start: str | Path | None = None) -> Path:
    return find_repo_root(start) / "outputs"

def schemas_dir(start: str | Path | None = None) -> Path:
    return plugin_root(start) / "schemas"

def scripts_dir(start: str | Path | None = None) -> Path:
    return plugin_root(start) / "scripts"

def agent_workspace_dir(start: str | Path | None = None) -> Path:
    return find_repo_root(start) / "agent-workspace" / "garden-structure-designer"

def ensure_dirs() -> None:
    for d in [staging_dir(), outputs_dir(), schemas_dir(), scripts_dir(), 
              agent_workspace_dir(), agent_workspace_dir() / "learned-patterns", 
              agent_workspace_dir() / "generated-tests", agent_workspace_dir() / ".backups"]:
        d.mkdir(parents=True, exist_ok=True)
