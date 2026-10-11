#!/usr/bin/env python3
"""
hardcode_guard.py
=================

Purpose:
    Static (AST) gate for the data-driven rule: reports silent numeric/string fallbacks in
    .get(key, default), silent numeric defaults written as x.get(...) or <number> and
    hardcoded scale = <number> assignments. Exit 1 lists every violation (file:line, rule, code).
    Default targets are the drawing/geometry scripts plus the scripts hardened to fail closed in the
    v1.5 alignment review (see _DEFAULT_TARGET_NAMES).

Layer: Execution / QA Static Scan Gate

Key Input Dependencies:
    - Python source files given on the command line (default: _DEFAULT_TARGET_NAMES next to this file)

Key Functions / Classes:
    HardcodeVisitor(filepath, content)   visit_Call / visit_BoolOp / visit_Assign / add_violation
    scan_file(filepath) -> list[dict]
    main() -> None

Usage Examples:
    python3 hardcode_guard.py [file_paths...]
"""
import sys
import ast
from pathlib import Path
import typing

# Files to strictly scan by default: the original drawing/geometry scripts plus the scripts hardened to fail closed
# during the v1.5 alignment review. (The original four still carry known violations; see the review tracker.)
_DEFAULT_TARGET_NAMES: tuple[str, ...] = (
    "render_drawings.py",
    "cad_scene.py",
    "geometry_engine.py",
    "cad_language_translator.py",
    "fabrication_builder.py",
    "builder_docs_compiler.py",
    "cad_backend_build123d.py",
    "structural_physics_validator.py",
    "strict_access.py",
    "compile_package.py",
    "package_consistency_validator.py",
)
DEFAULT_TARGETS: list[Path] = [Path(__file__).parent / name for name in _DEFAULT_TARGET_NAMES]

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

    # External Comment: Inspect `x.get(...) or <number>` silent numeric defaults.
    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        """
        Flags ``<dict>.get(...) or <numeric literal>``: a silent structural default that hides a missing key.

        Args:
            node: The boolean-operation AST node being visited.
        """
        if isinstance(node.op, ast.Or):
            has_get = any(
                isinstance(v, ast.Call) and isinstance(v.func, ast.Attribute) and v.func.attr == "get"
                for v in node.values[:-1]
            )
            last = node.values[-1]
            is_number = (
                isinstance(last, ast.Constant)
                and isinstance(last.value, (int, float))
                and not isinstance(last.value, bool)
            )
            if has_get and is_number:
                self.add_violation(
                    node,
                    f"FORBIDDEN_OR_NUMBER_DEFAULT: Silent numeric default {last.value!r} after .get(). "
                    "A missing structural value must fail closed (strict_access.require), not be invented."
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
