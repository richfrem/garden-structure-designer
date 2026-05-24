---
name: document-compiler
description: Assembles all outputs into a structured document and formats for PDF export. Ensures sections are complete, ordered matching the Option A Architectural Layout constraint.
allowed-tools: Read, Write, Bash
---

## 🚨 Pre-Flight: Drawing Red-Team & Photorealistic Render Gate Check (MANDATORY)

Before compilation begins, this skill MUST verify:

```bash
# Check the gate report exists and is approved, and verify photorealistic renders
python3 - <<'PY'
import json, sys
from pathlib import Path
sys.path.append("plugins/garden-structure-designer/scripts")
from path_utils import staging_dir, outputs_dir

report_path = staging_dir() / "drawing-red-team-report.json"

try:
    r = json.load(open(report_path))
except FileNotFoundError:
    print(f"BLOCKED: {report_path} not found. Run Stage 5.75 first.")
    sys.exit(1)

if not r.get("may_claim_success"):
    print("BLOCKED: drawing-red-team-report.json has may_claim_success: false")
    print("Summary:", r.get("summary", ""))
    sys.exit(1)

# Verify photorealistic renders exist
image_dir = outputs_dir() / "high-resolution-image"
renders = list(image_dir.glob("*_render_*.png"))
if not renders:
    print(f"BLOCKED: No photorealistic renders found in {image_dir}")
    sys.exit(1)

print(f"Gate approved — proceeding with compilation. Found {len(renders)} photorealistic renders.")
PY
```

If this check fails, **do not compile**. Write a blocking message to `outputs/COMPILATION_BLOCKED.md` explaining that the drawing red-team gate and photorealistic render verification must pass first. Do not proceed to `embed_svgs.py` or PDF conversion.


## Expected Inputs
All models inside `context/staging/`.
Visuals from `drawing-generator` (Plan, Elevation, Perspective, Isometric).
Technical cut-sheets from `shop-blueprint-generator` (Dimensioned orthographics and isolated joinery components).

## Core Responsibilities
1. Construct the document adhering to the PDF Layout requirements. Place the primary photorealistic render (`outputs/high-resolution-image/*_render_1.png`) at the top of the compiled document, directly underneath the main title. Follow this with architectural diagrams and 3D visual layouts, then the detailed technical shop blueprints, and lastly the timber cut-list tables and fastener tables.
2. Write the intermediate Markdown to `outputs/design-package.md` (or `outputs/pergola_plan.md` depending on the active naming convention) using standard `![alt](path)` image references pointing to the actual SVG/PNG files in `outputs/`.
3. **Embed all assets before PDF conversion** — run `embed_svgs.py` to inline every SVG and PNG as raw HTML so the PDF contains the visuals, not broken links:
   ```bash
   python3 plugins/garden-structure-designer/scripts/embed_svgs.py \
       outputs/design-package.md \
       outputs/design-package-embedded.md
   ```
4. Convert the embedded Markdown to PDF:
   ```bash
   npx -y md-to-pdf outputs/design-package-embedded.md
   # produces outputs/design-package-embedded.pdf
   ```
5. Rename to final output:
   ```bash
   mv outputs/design-package-embedded.pdf outputs/design-package.pdf
   ```

## Gotchas

- **Always embed before converting.** Passing the raw Markdown with `![](path.svg)` references to `npx md-to-pdf` produces a PDF with broken image placeholders — the PDF renderer cannot read local SVG files by path. `embed_svgs.py` must run first to inline all assets.
- **`embed_svgs.py` warns on missing assets** — any `WARNING: asset not found` line in its stderr means a drawing is absent. Treat this as a blocking failure; do not proceed to `npx md-to-pdf`.
- **`npx -y md-to-pdf` may fail on headless environments** (no display, missing Chrome). If the command exits non-zero, write `outputs/PDF_GENERATION_FAILED.md` with the error message. The `outputs/design-package-embedded.md` file is always written regardless, so the user has a fallback they can open in a browser and print to PDF.
- **Layout order is a hard requirement:** architectural diagrams first, shop blueprints second, cut-list/fastener tables last. Any reordering makes the package non-compliant with the Option A Architectural Layout constraint.
- **Verify the manifest before compiling.** Read `outputs/document-compiler/manifest.json` and confirm all listed sheets are present and their checksums match the current files. A stale manifest means some drawings may be outdated — halt and report which sheets need regenerating.
- **All builder documents must be present.** budget-estimate.md, lumber-purchase-list.md, and assembly-guide.md must exist and be non-empty before compilation begins. A missing builder document is a blocking failure.
- **PDF binary must be confirmed to exist.** After running the PDF tool, verify the output file exists with `os.path.exists()` before signaling stage completion. Tool exit-0 alone is not sufficient.

## Smoke Test

1. **Full happy path:** Given all staging files and drawings present: `embed_svgs.py` runs clean (no warnings), PDF written to `outputs/design-package.pdf`, compilation manifest updated, stage signals complete. ✓
2. **Embedded SVGs in PDF:** Open `outputs/design-package-embedded.md` in a browser — all 8 drawings (4 architectural + 4 shop blueprint) render as visible diagrams, not broken image icons. ✓
3. **PDF tool failure graceful degradation:** Force `npx md-to-pdf` to fail: `outputs/PDF_GENERATION_FAILED.md` is created, `outputs/design-package-embedded.md` fallback is written with all SVGs inlined, skill does not crash. ✓
4. **Stale manifest detection:** Remove one SVG after compiler reads manifest: compiler halts and reports the missing sheet by name. ✓
5. **Missing asset detection:** Point embed_svgs.py at a Markdown referencing a non-existent SVG: WARNING is printed to stderr, compiler halts before invoking npx. ✓
