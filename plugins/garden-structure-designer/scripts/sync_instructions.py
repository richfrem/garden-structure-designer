#!/usr/bin/env python3
"""
sync_instructions.py
====================

Purpose:
    Mirrors the body of the repo-root CLAUDE.md into GEMINI.md and
    .github/copilot-instructions.md. WARNING (stale): CLAUDE.md is now only a pointer to
    AGENTS.md ("Read AGENTS.md"), so running this overwrites both mirrors with that one-line body.
    It no longer executes at import time; run it only after re-pointing it at AGENTS.md.
    Review finding: propose removal (not part of the CADCraft pipeline).

Layer: Maintenance / Repo Tooling

Key Input Dependencies:
    - ./CLAUDE.md, ./GEMINI.md (run from the repo root); writes ./GEMINI.md and ./.github/copilot-instructions.md

Key Functions:
    main() -> None

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/sync_instructions.py   # from the repo root (see warning)
"""
from __future__ import annotations


def main() -> None:
    """Rewrite GEMINI.md and the Copilot instructions from CLAUDE.md (see module warning)."""
    with open("CLAUDE.md") as f:
        claude = f.read()

    # Extract body from CLAUDE.md (strip first line)
    claude_lines = claude.split("\n")
    claude_body = "\n".join(claude_lines[1:])

    # Gemini.md
    with open("GEMINI.md") as f:
        gemini = f.read()
    gemini_footer_idx = gemini.find("## Gemini CLI Tool Mapping")
    gemini_footer = gemini[gemini_footer_idx:] if gemini_footer_idx != -1 else ""

    new_gemini = "# GEMINI.md\n" + claude_body
    if gemini_footer:
        new_gemini += "\n" + gemini_footer

    with open("GEMINI.md", "w") as f:
        f.write(new_gemini)

    # Copilot
    new_copilot = """# Copilot Instructions for garden-structure-designer

> Authoritative rules for all AI agents (Claude Code, Copilot, Gemini) working in this repo.
> Mirrors CLAUDE.md — keep in sync.
""" + "\n".join(claude_lines[2:])

    with open(".github/copilot-instructions.md", "w") as f:
        f.write(new_copilot)

    print("Synchronized.")


if __name__ == "__main__":
    main()
