#!/usr/bin/env python3
"""
format_headers.py
=================

Purpose:
    Adds the standard script header (Purpose, Layer, Key Input Dependencies, Key Functions,
    Usage) to Python files in the current directory that have NO module docstring. It is safe by
    default: nothing is written without ``--apply``, and a file that already has any module
    docstring is never touched. (An earlier version rewrote every header with a generic template
    on import; the boilerplate it produced has since been replaced with real headers.) Review
    finding: the generated template carries no information, so removal is proposed.

Layer: Maintenance / Repo Tooling

Key Input Dependencies:
    - *.py files in the current working directory

Key Functions:
    extract_docstring(content) -> str
    format_header(filename, original_doc) -> str
    main(argv=None) -> int

Usage Examples:
    python3 format_headers.py            # dry run: lists files that would receive a header
    python3 format_headers.py --apply    # writes the template into docstring-less files
"""
from __future__ import annotations

import argparse
import ast
import glob
import sys

SKIPPED = ("format_headers.py", "generate_schemas.py")


def extract_docstring(content: str) -> str:
    """Returns the module docstring of ``content`` ('' when absent or unparsable)."""
    try:
        return ast.get_docstring(ast.parse(content)) or ""
    except SyntaxError:
        return ""


def format_header(filename: str, original_doc: str) -> str:
    """Builds the standard header text for ``filename`` (``original_doc`` seeds the Purpose line)."""
    lines = original_doc.split("\n")
    purpose = lines[0] if lines and lines[0] else "Describe what this script does."
    return f'''#!/usr/bin/env python3
"""
{filename}
{"=" * len(filename)}

Purpose:
    {purpose.strip()}

Layer: Execution

Key Input Dependencies:
    - list required files, environment variables or libraries here

Key Functions:
    - list every function with its signature here

Usage Examples:
    python3 {filename} [args]
"""
'''


def _strip_shebang(content: str) -> str:
    """Removes a leading shebang line so the new header can supply its own."""
    return content.split("\n", 1)[1] if content.startswith("#!") and "\n" in content else content


def main(argv: list[str] | None = None) -> int:
    """Lists (default) or fixes (--apply) Python files lacking a module docstring; never touches documented files."""
    parser = argparse.ArgumentParser(description="Add the standard header to docstring-less scripts.")
    parser.add_argument("--apply", action="store_true", help="write headers (default: dry run)")
    args = parser.parse_args(argv)

    changed = 0
    for path in sorted(glob.glob("*.py")):
        if path in SKIPPED:
            continue
        with open(path, encoding="utf-8") as file:
            content = file.read()
        if extract_docstring(content):
            continue
        changed += 1
        print(f"{'Adding header to' if args.apply else 'Would add header to'} {path}")
        if args.apply:
            with open(path, "w", encoding="utf-8") as file:
                file.write(format_header(path, "") + _strip_shebang(content).lstrip())
    print("Headers formatted." if args.apply else f"Dry run: {changed} file(s) lack a module docstring.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
