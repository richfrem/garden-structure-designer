#!/usr/bin/env python3
"""
embed_svgs.py — Inline SVG and PNG assets into a Markdown file for PDF compilation.

Usage:
    python3 scripts/embed_svgs.py <input.md> <output.md>

Transforms:
    ![alt](path/to/file.svg)  → inline <svg>...</svg> block
    ![alt](path/to/file.png)  → <img src="data:image/png;base64,...">

The output Markdown/HTML is suitable for npx md-to-pdf which renders inline HTML.
All paths are resolved relative to the input Markdown file's directory.
"""
import sys
import os
import re
import base64


def embed_svg(svg_path: str) -> str:
    """Read SVG file and return it as an inline HTML block."""
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    # Remove XML declaration if present — browsers and md-to-pdf don't need it
    content = re.sub(r"<\?xml[^>]*\?>", "", content).strip()
    # Wrap in a div so md-to-pdf treats it as a block element
    return f'<div class="svg-embed" style="page-break-inside:avoid;margin:16px 0;">\n{content}\n</div>'


def embed_png(png_path: str, alt: str) -> str:
    """Read PNG file and return it as a base64 data-URI img tag."""
    with open(png_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return (
        f'<div class="img-embed" style="page-break-inside:avoid;margin:16px 0;">'
        f'<img src="data:image/png;base64,{data}" alt="{alt}" '
        f'style="max-width:100%;height:auto;" />'
        f"</div>"
    )


def process(input_path: str, output_path: str) -> None:
    base_dir = os.path.dirname(os.path.abspath(input_path))

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match Markdown image syntax: ![alt text](relative/path.svg) or .png
    img_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    def replace_image(m: re.Match) -> str:
        alt = m.group(1)
        raw_path = m.group(2)

        # Resolve path relative to the markdown file
        resolved = os.path.normpath(os.path.join(base_dir, raw_path))

        if not os.path.isfile(resolved):
            print(f"  WARNING: asset not found, leaving as-is: {resolved}", file=sys.stderr)
            return m.group(0)  # leave unchanged

        ext = os.path.splitext(resolved)[1].lower()
        if ext == ".svg":
            print(f"  Embedding SVG: {resolved}")
            return embed_svg(resolved)
        elif ext in (".png", ".jpg", ".jpeg", ".webp"):
            print(f"  Embedding image: {resolved}")
            return embed_png(resolved, alt)
        else:
            # Unknown type — leave as-is
            return m.group(0)

    result = img_pattern.sub(replace_image, content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Written: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.md> <output.md>")
        sys.exit(1)
    process(sys.argv[1], sys.argv[2])
