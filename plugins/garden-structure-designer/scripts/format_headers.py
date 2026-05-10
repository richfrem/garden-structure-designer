import os
import glob
import ast

def extract_docstring(content):
    try:
        module = ast.parse(content)
        doc = ast.get_docstring(module)
        return doc if doc else ""
    except Exception:
        return ""

def format_header(filename, original_doc):
    lines = original_doc.split("\n")
    purpose = lines[0] if lines else "Script functionality."
    if len(lines) > 1 and lines[1]:
        purpose += " " + lines[1]
        
    return f'''#!/usr/bin/env python3
"""
{filename} (CLI)
=====================================

Purpose:
    {purpose.strip()}

Layer: Execution

Usage Examples:
    python {filename} [args]

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
'''

files = glob.glob("*.py")
for f in files:
    if f in ['format_headers.py', 'generate_schemas.py']:
        continue
    with open(f, "r") as file:
        content = file.read()
        
    # Remove existing shebang and module docstring
    lines = content.split('\n')
    start_idx = 0
    if lines and lines[0].startswith("#!"):
        start_idx = 1
        
    in_docstring = False
    doc_char = ""
    for i in range(start_idx, len(lines)):
        line = lines[i].strip()
        if not in_docstring:
            if line.startswith('"""') or line.startswith("'''"):
                in_docstring = True
                doc_char = line[:3]
                if line.endswith(doc_char) and len(line) > 3:
                    in_docstring = False
                    start_idx = i + 1
                    break
        else:
            if line.endswith(doc_char):
                start_idx = i + 1
                break
            elif '"""' in line or "'''" in line:
                start_idx = i + 1
                break
                
    if start_idx == 0 and '"""' not in content[:100]:
        pass # No docstring found at the start
        
    rest_of_code = "\n".join(lines[start_idx:]).lstrip()
    
    docstring = extract_docstring(content)
    header = format_header(f, docstring)
    
    with open(f, "w") as file:
        file.write(header + rest_of_code)

print("Headers formatted.")
