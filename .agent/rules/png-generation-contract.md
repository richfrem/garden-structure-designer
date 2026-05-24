# PNG Generation Contract

## Architecture

```
render_drawings.py
  → writes SVG  outputs/<sheet>.svg
  → writes PNG  outputs/visual-smoke/<sheet>.png   (immediately, same call)

visual_svg_smoke_test.py / joint_visual_audit.py
  → consumes existing PNGs
  → runs OpenCV, crops, and vision review on existing evidence
  → does NOT re-render unless PNG is missing or explicitly requested
```

**PNG creation belongs in the render stage, not the review stage.**

The review stage spends its effort on every rafter, every jack rafter, every
purlin, every brace, every beam, every post, every hub face, every visible
connection — not on relaunching Chromium to recreate images that already exist.

---

## Rendering Contract — render_drawings.py

For every generated SVG, `render_drawings.py` MUST:

1. Write the SVG to `outputs/<sheet>.svg`
2. Immediately generate the matching PNG: `outputs/visual-smoke/<sheet>.png`
3. Verify the PNG exists and is non-empty
4. Correct the PNG to the exact SVG viewport dimensions (qlmanage on macOS
   Sequoia produces square thumbnails regardless of SVG aspect ratio; resize
   after generation using Pillow)
5. Log the result per sheet

Required log format:

```
✓ drawing-isometric-view.svg  [PNG ok]
✓ blueprint-plan.svg          [PNG ok]
...
✗ drawing-elevation-view.svg  [PNG MISSING]
```

---

## PNG Generation Strategy (in priority order)

1. **qlmanage** (macOS) — fast, zero browser overhead, no network, no process
   spawn per SVG.  Primary path.  Correct aspect ratio with Pillow after.
2. **Playwright chromium** — fallback only when qlmanage is unavailable or
   produces a zero-byte file.  Never the primary path on normal pipeline runs.

---

## Visual Audit Contract — visual_svg_smoke_test.py

MUST:

1. Look for existing PNG evidence first (`outputs/visual-smoke/<sheet>.png`)
2. Use existing PNGs for OpenCV analysis, hub crops, and vision review
3. Emit `BROWSER_RENDER_BLOCKED` (fail) if a PNG is absent and all fallbacks fail
4. Only invoke qlmanage fallback if PNG is missing
5. Only invoke Playwright if qlmanage fallback also fails AND Playwright is installed

Default behaviour MUST be equivalent to `--use-existing-png`.

---

## Playwright's Role

Playwright exists only for:

- Debugging browser-specific SVG rendering bugs
- Re-rendering missing PNG evidence if explicitly requested via
  `--rerender-missing` or `--force-browser-render`
- Headed manual visual inspection (`--headed`)
- Cross-browser regression testing

**Not for every normal pipeline run.**

---

## PNG Staleness Rule

A PNG is valid evidence only when ALL of the following hold:

- Matching SVG exists at `outputs/<sheet>.svg`
- PNG mtime ≥ SVG mtime (PNG is not older than the SVG)
- PNG file size > 0
- (Optional) source hash in `visual-smoke-report.json` matches
  `structure.meta.source_hash`

If the PNG is absent or stale:

```
PNG_STALE_OR_MISSING → re-render via qlmanage → re-run validation
```

---

## What NOT to do

- Do not launch Playwright merely to recreate PNGs that already exist.
- Do not call `visual_svg_smoke_test.py` before `render_drawings.py` has run.
- Do not treat a passing XML/content validation as sufficient without PNG
  evidence of visual correctness.
- Do not suppress secondary framing (jack rafters, purlins) by disabling them
  in `structure.json` — suppress them in the 3D renderer only.  The plan view
  must continue to show all members.
