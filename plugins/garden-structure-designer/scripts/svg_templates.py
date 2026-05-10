#!/usr/bin/env python3
"""
svg_templates.py (CLI)
=====================================

Purpose:
    svg_templates.py Shared SVG template functions for drawing generation.

Layer: Execution

Usage Examples:
    python svg_templates.py [args]

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
def title_block(dwg_no: str, title: str, project: str, date: str, extra_lines: list[str]) -> str:
    lines = "".join(f'<text x="20" y="{40 + i*20}">{line}</text>' for i, line in enumerate(extra_lines))
    return f'''
    <g id="title-block" font-family="sans-serif" font-size="14">
        <rect x="10" y="10" width="300" height="{100 + len(extra_lines)*20}" fill="none" stroke="black"/>
        <text x="20" y="30" font-weight="bold">{title}</text>
        <text x="20" y="50">Project: {project}</text>
        <text x="20" y="70">Date: {date}</text>
        <text x="20" y="90">DWG: {dwg_no}</text>
        {lines}
    </g>
    '''

def grid_pattern(spacing: int) -> str:
    return f'''
    <defs>
        <pattern id="grid" width="{spacing}" height="{spacing}" patternUnits="userSpaceOnUse">
            <path d="M {spacing} 0 L 0 0 0 {spacing}" fill="none" stroke="gray" stroke-width="0.5"/>
        </pattern>
    </defs>
    '''

def arrow_markers() -> str:
    return '''
    <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" />
        </marker>
    </defs>
    '''

def dimension_line(x1: float, y1: float, x2: float, y2: float, label: str, offset: int) -> str:
    # Very simplified dimension line
    return f'''
    <g class="dimension" stroke="black">
        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
        <text x="{(x1+x2)/2}" y="{(y1+y2)/2 - 5}" text-anchor="middle" font-size="12">{label}</text>
    </g>
    '''

def border_frame(width: int, height: int) -> str:
    return f'<rect x="0" y="0" width="{width}" height="{height}" fill="none" stroke="black" stroke-width="2"/>'
