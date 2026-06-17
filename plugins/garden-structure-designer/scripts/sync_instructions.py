import os

with open("CLAUDE.md") as f:
    claude = f.read()

# Extract body from CLAUDE.md (strip first line)
claude_lines = claude.split("\n")
claude_body = "\n".join(claude_lines[1:])

# Gemini.md
with open("GEMINI.md") as f:
    gemini = f.read()
gemini_lines = gemini.split("\n")
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
