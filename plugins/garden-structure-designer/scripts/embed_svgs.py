#!/usr/bin/env python3
"""
embed_svgs.py
=============

Purpose:
    Inlines the images referenced by a package markdown file: SVG sheets become inline
    responsive ``<div>`` blocks (all ``data-role``/``data-tag`` attributes preserved) and
    PNG/JPG/WebP files become base64 data URIs, so md-to-pdf renders one self-contained
    document. Assets that cannot be found are collected and returned (and the CLI exits 1)
    instead of leaving silent broken references in the final package.

Layer: Execution / Stage 7 Document Assembly

Key Input Dependencies:
    - outputs/pergola_plan.md (or the path argument) and the images it references (relative paths)
    - path_utils.py (default outputs directory)

Key Functions:
    embed_svg(svg_path) -> str
    embed_png(png_path, alt) -> str
    process(input_path, output_path) -> list[str]     # returns missing asset paths
    main(argv=None) -> int

Usage Examples:
    python3 plugins/garden-structure-designer/scripts/embed_svgs.py [in.md] [out.md]
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
    # Make SVG responsive by replacing hardcoded width/height with 100%/auto
    content = re.sub(r'(<svg[^>]*)\bwidth="[^"]+"', r'\g<1>width="100%"', content)
    content = re.sub(r'(<svg[^>]*)\bheight="[^"]+"', r'\g<1>height="auto"', content)
    # Wrap in a div so md-to-pdf treats it as a block element
    return f'<div class="svg-embed" style="page-break-inside:avoid;margin:16px 0;width:100%;max-width:100%;box-sizing:border-box;">\n{content}\n</div>'


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


def process(input_path: str, output_path: str) -> list[str]:
    """Writes the embedded markdown to ``output_path``; returns the resolved paths of assets that were missing."""
    missing: list[str] = []
    base_dir = os.path.dirname(os.path.abspath(input_path))

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match Markdown image syntax: ![alt text](relative/path.svg) or .png
    img_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    def replace_image(m: re.Match) -> str:
        """Replaces one markdown image reference with its inline HTML (or leaves it, recording a missing file)."""
        alt = m.group(1)
        raw_path = m.group(2)

        # Resolve path relative to the markdown file
        resolved = os.path.normpath(os.path.join(base_dir, raw_path))

        if not os.path.isfile(resolved):
            print(f"  WARNING: asset not found, leaving as-is: {resolved}", file=sys.stderr)
            missing.append(resolved)
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
    return missing


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint; exits 1 when any referenced asset was missing."""
    args = sys.argv[1:] if argv is None else argv
    in_path = args[0] if len(args) > 0 else str(outputs_dir() / "pergola_plan.md")
    out_path = args[1] if len(args) > 1 else str(outputs_dir() / "pergola_plan_embedded.md")
    return 1 if process(in_path, out_path) else 0


sys.path.append(str(os.path.dirname(os.path.abspath(__file__))))
from path_utils import outputs_dir

if __name__ == "__main__":
    sys.exit(main())
