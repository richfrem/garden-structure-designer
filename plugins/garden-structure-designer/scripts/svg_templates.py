#!/usr/bin/env python3
"""
svg_templates.py
================

Purpose:
    Small SVG fragment helpers: title block, grid pattern, arrow markers, dimension line and border
    frame. REVIEW FINDING: nothing imports this module (render_drawings.py draws its own title block),
    and these fragments carry no data-role/data-tag attributes and hardcoded stroke widths, so
    they violate the semantic-SVG invariant (AGENTS.md) and the drafting constants. Removal is proposed;
    do not use these helpers for pipeline drawings.

Layer: Execution / Legacy SVG Helpers

Key Input Dependencies:
    Standard library only.

Key Functions:
    title_block(dwg_no, title, project, date, extra_lines) -> str
    grid_pattern(spacing) -> str
    arrow_markers() -> str
    dimension_line(x1, y1, x2, y2, label, offset) -> str
    border_frame(width, height) -> str
"""
def title_block(dwg_no: str, title: str, project: str, date: str, extra_lines: list[str]) -> str:
    """SVG group with the drawing title, project, date, drawing number and extra lines."""
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
    """SVG <defs> pattern for a square background grid of the given spacing."""
    return f'''
    <defs>
        <pattern id="grid" width="{spacing}" height="{spacing}" patternUnits="userSpaceOnUse">
            <path d="M {spacing} 0 L 0 0 0 {spacing}" fill="none" stroke="gray" stroke-width="0.5"/>
        </pattern>
    </defs>
    '''

def arrow_markers() -> str:
    """SVG <defs> arrowhead marker used by dimension lines."""
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
    """Simplified dimension line with arrow ends and a centred label (the offset argument is currently unused)."""
    return f'''
    <g class="dimension" stroke="black">
        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
        <text x="{(x1+x2)/2}" y="{(y1+y2)/2 - 5}" text-anchor="middle" font-size="12">{label}</text>
    </g>
    '''

def border_frame(width: int, height: int) -> str:
    """Outer border rectangle for a sheet of the given size."""
    return f'<rect x="0" y="0" width="{width}" height="{height}" fill="none" stroke="black" stroke-width="2"/>'
