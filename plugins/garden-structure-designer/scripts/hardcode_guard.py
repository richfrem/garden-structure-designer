#!/usr/bin/env python3
"""
hardcode_guard.py (CLI)
=====================================

Purpose:
    Performs abstract syntax tree (AST) static analysis on CAD rendering scripts
    to detect and prevent forbidden hardcoded layout scale constants and silent
    fallback defaults (e.g. dictionary .get() default values).

Layer: Execution / QA Validation

Usage Examples:
    python hardcode_guard.py [file_paths...]
    python hardcode_guard.py plugins/garden-structure-designer/scripts/render_drawings.py

Supported Object Types:
    Python files (*.py)

CLI Arguments:
    file_paths: Optional list of specific python files to scan. If omitted,
                defaults to render_drawings.py.

Input Files:
    plugins/garden-structure-designer/scripts/render_drawings.py

Output:
    Exit code 0 on PASS, 1 on FAIL with detailed violation reporting to stderr.

Key Classes/Functions:
    HardcodeVisitor: AST visitor for scanning dictionary gets and assignment statements.
    scan_file: Parses file content to AST and runs the visitor.
    main: Orchestrates the scan of targets and controls exit status.

Script Dependencies:
    sys, ast, pathlib

Consumed by:
    design-orchestrator (Stage 5.6 Static Scan Gate)
"""

import sys
import ast
from pathlib import Path
import typing

# Files to strictly scan by default
DEFAULT_TARGETS: list[Path] = [
    Path(__file__).parent / "render_drawings.py",
    Path(__file__).parent / "cad_scene.py",
    Path(__file__).parent / "geometry_engine.py",
    Path(__file__).parent / "cad_language_translator.py",
    Path(__file__).parent / "fabrication_builder.py",
]

# External Comment: AST NodeVisitor that inspects dictionary lookups and assignments.
class HardcodeVisitor(ast.NodeVisitor):
    """
    AST node visitor class designed to inspect Call and Assign nodes.
    It identifies forbidden dictionary get call fallbacks and direct scale hardcodes.
    """

    # External Comment: Initialize the visitor with filepath and file contents.
    def __init__(self, filepath: Path, content: str) -> None:
        """
        Initializes visitor with the file path and splits file contents into lines.
        
        Args:
            filepath: Path to the scanned file.
            content: Raw string content of the file.
        """
        self.filepath: Path = filepath
        self.lines: list[str] = content.splitlines()
        self.violations: list[dict[str, typing.Any]] = []

    # External Comment: Inspect call nodes for forbidden silent fallbacks in .get() methods.
    def visit_Call(self, node: ast.Call) -> None:
        """
        Visits call nodes to check for dictionary .get() methods with hardcoded fallbacks.
        
        Args:
            node: The call AST node being visited.
        """
        if isinstance(node.func, ast.Attribute) and node.func.attr == "get":
            # Check arguments
            if len(node.args) >= 2:
                default_arg = node.args[1]
                # Check for literal number default (e.g. .get("scale_px_per_ft", 55.0))
                if isinstance(default_arg, ast.Constant):
                    val = default_arg.value
                    if isinstance(val, (int, float)):
                        self.add_violation(
                            node,
                            f"FORBIDDEN_GET_NUMBER: Use of silent number fallback default {val!r} in .get(). "
                            "Must be driven dynamically from structure.json geometry."
                        )
                    elif isinstance(val, str) and val in ("cedar_warm", "blueprint", "Cedar"):
                        self.add_violation(
                            node,
                            f"FORBIDDEN_GET_FALLBACK: Use of fallback default string {val!r} in .get(). "
                            "Config must be parsed directly from structure.json and validated."
                        )
        self.generic_visit(node)

    # External Comment: Inspect assignment nodes for hardcoded scale factor variables.
    def visit_Assign(self, node: ast.Assign) -> None:
        """
        Visits assignment AST nodes to check for direct literal numbers assigned to scale.
        
        Args:
            node: The assignment AST node being visited.
        """
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id.lower() == "scale":
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)):
                    self.add_violation(
                        node,
                        f"FORBIDDEN_SCALE_LITERAL: Scale literal assignment {node.value.value!r} found. "
                        "Scale factors must be driven by coordinates or calculated dynamically based on viewport/bounding box."
                    )
        self.generic_visit(node)

    # External Comment: Formulate violation report and append it to self.violations list.
    def add_violation(self, node: ast.AST, message: str) -> None:
        """
        Builds a structured violation dictionary and tracks it in the findings list.
        
        Args:
            node: The violating AST node.
            message: Explanation of the violation.
        """
        line_num: int = node.lineno
        col_offset: int = node.col_offset
        snippet: str = self.lines[line_num - 1].strip() if 0 < line_num <= len(self.lines) else ""
        self.violations.append({
            "file": str(self.filepath.name),
            "line": line_num,
            "col": col_offset,
            "message": message,
            "snippet": snippet
        })

# External Comment: Parse Python file content to AST and run the visitor class.
def scan_file(filepath: Path) -> list[dict[str, typing.Any]]:
    """
    Parses file contents into an AST and traverses it with the HardcodeVisitor class.
    
    Args:
        filepath: Path to the target file.
        
    Returns:
        List of violation dictionaries discovered in the file.
    """
    if not filepath.exists():
        print(f"[GUARD] File not found: {filepath}", file=sys.stderr)
        return []
    
    with open(filepath, "r", encoding="utf-8") as f:
        content: str = f.read()

    try:
        tree: ast.Module = ast.parse(content, filename=str(filepath))
    except SyntaxError as e:
        print(f"[GUARD] Syntax error parsing {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

    visitor: HardcodeVisitor = HardcodeVisitor(filepath, content)
    visitor.visit(tree)
    return visitor.violations

# External Comment: Parse arguments, trigger checks on targets, and exit with status code.
def main() -> None:
    """
    Main orchestrator for scanning CLI targets for scale and default get violations.
    """
    targets: list[Path] = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else DEFAULT_TARGETS
    all_violations: list[dict[str, typing.Any]] = []

    print("[GUARD] Starting static analysis for silent fallback defaults and hardcodes...")
    for target in targets:
        print(f"[GUARD] Scanning {target.resolve()}...")
        violations: list[dict[str, typing.Any]] = scan_file(target)
        all_violations.extend(violations)

    if all_violations:
        print("\n❌ [GUARD] FAILED: Hardcoded geometry values or silent fallbacks detected!", file=sys.stderr)
        for v in all_violations:
            print(f"  File: {v['file']}:{v['line']}:{v['col']}", file=sys.stderr)
            print(f"  Violation: {v['message']}", file=sys.stderr)
            print(f"  Code: `{v['snippet']}`\n", file=sys.stderr)
        sys.exit(1)

    print("\n✅ [GUARD] PASS: No forbidden silent defaults or scale literals found in target files.")
    sys.exit(0)

if __name__ == "__main__":
    main()
