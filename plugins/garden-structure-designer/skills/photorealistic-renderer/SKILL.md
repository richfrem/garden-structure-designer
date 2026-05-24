---
name: photorealistic-renderer
description: Generates a detailed photorealistic image-generation prompt driven entirely by the locked structural model. Works for any garden structure (gazebo, pergola, arbour, shed, fence, trellis, etc.). Produces a single paste-ready file with geometry locks, structural description, camera direction, and exclusions tailored to whatever was designed. Trigger with "render the structure", "create a photorealistic image", "generate a render prompt", "visualize the design", or "show me what this will look like".
allowed-tools: Read, Write, Bash
---

## Photorealistic Render Boundary

Photorealistic PNG/JPG renders are **presentation artifacts only**.

This skill may generate or update:
```
outputs/render-prompt.txt
outputs/*visualization*.png
outputs/*render*.png
```

This skill must **NOT** claim the design package is complete, and must **NOT** claim that a PNG validates post count, beam count, rafter count, brace count, span, height, pitch, miter angles, cut lengths, or structural safety.

Every render output must be accompanied by:
```
Visual concept only — construction geometry is governed by validated JSON/SVG artifacts.
```

If a render appears to conflict with deterministic geometry, the render is subordinate to:
```
context/staging/structure.json
outputs/*.svg
```

After generating a render, hand control back to `design-orchestrator` to confirm deterministic artifacts and quality dashboard status.


- `context/staging/structure.json` (must be locked: `_locked: true`; includes members, geometry, and intent/meta sections)

## Outputs
- `outputs/render-prompt.txt` — single self-contained file: all geometry locks, structural description, camera direction, and exclusions. Paste the whole thing verbatim into ChatGPT or any image model.
- `outputs/photorealistic-render.png` — generated image (if the user pastes and generates)
- `outputs/RENDER_FAILED.md` — written if the skill cannot complete; prompt file still saved

---

## Phase 1 — Read Locked Model

Read `context/staging/structure.json`. If `_locked` is not `true`, halt with:
```
ERROR: structure.json is not locked. Run structural-engine first.
```

Extract the fields that describe **this specific structure** — the exact fields vary by structure type:
- `structureType` → what kind of structure (gazebo, pergola, arbour, shed, screen, trellis…)
- `planShape` → geometry (hexagonal, rectangular, square, L-shaped, octagonal…)
- `members.posts.dimensions`, `members.posts.quantity`
- `members.beams.dimensions` (if present)
- `members.rafters.dimensions`, `members.rafters.quantity` (if present)
- `members.bracing.*` (if present — type, angle, quantity)
- `members.roofType` → open rafter, solid, pergola-style, lean-to, flat, no roof…
- `roofStructure.pitch` (if present)
- `materials.primary` → species and finish
- `joinery.type` → mortise-and-tenon, screwed, bolted, notched…
- Any unique members (king post hub, ridge beam, purlins, lattice panels, gates…)

Also read `context/staging/structure.json` (geometry section):
- `total_height_ft`, `post_cut_ft`, `span_ft`, `diameter_ft` — whatever dimensions are present

Also read `context/staging/structure.json` (intent/meta section, if present):
- `site.location`, `site.setting`, `site.surroundings` → used to set the scene realistically

---

## Phase 2 — Compose and Write Prompt

Write `outputs/render-prompt.txt` using the **CAD-SPEC format** — structured sections with a title, explicit geometry locks, per-member subsections, and a final `Exclude:` block. All values are derived from `structure.json`; nothing is hardcoded.

### Format overview

```
[SHAPE] TIMBER FRAME — CAD-SPEC PROMPT (MAX ENFORCEMENT)

ABSOLUTE GEOMETRY DEFINITION (TOP PRIORITY — DO NOT VIOLATE):
[geometry constraints]

PLAN GEOMETRY (EXPLICIT CONSTRUCTION LOGIC)
[dimensions and spacing]

STRUCTURAL FRAME
[one subsection per member type that exists in the model]

MATERIAL + FINISH
[species, finish, character]

SCENE + ENVIRONMENT
[site, planting, lighting]

CAMERA + VISUAL VERIFICATION (CRITICAL)
[angle, lens, counting test]

ANTI-FAILURE CONSTRAINTS
[explicitly forbid wrong shapes and wrong counts]

FINAL VALIDATION CHECK (MANDATORY)
[list of things that must be true for the image to be correct]

Exclude: [comma-separated list]
```

---

### Section 1 — Title

`[SHAPE] TIMBER FRAME — CAD-SPEC PROMPT (MAX ENFORCEMENT)`

Derive shape from `structure.shape` (e.g. HEXAGONAL, SQUARE, OCTAGONAL).

---

### Section 2 — ABSOLUTE GEOMETRY DEFINITION

Always first. Derive every value from the model — no guessing.

- **Shape definition**: N sides, N vertices, N structural corner posts ONLY
- **Perimeter rule**: "The outer boundary consists of exactly N straight edges. The viewer must be able to visually trace the perimeter and make exactly N directional turns ([interior_angle]° each). Interior angle at every corner = [interior_angle] degrees."
- **Name the failure shape explicitly**: "This is NOT an [confabulation_shape] — never [wrong_N] sides, never [wrong_N] posts." For hexagon the failure shape is octagon. For square it is hexagon. Name whatever the model is most likely to confuse.
- **Post count hard lock**: "TOTAL POSTS = N. One post per vertex. No additional vertical supports anywhere on the perimeter or inside. No doubled posts, no closely spaced posts, no decorative posts. Posts must be evenly spaced at [360/N]° around the center."
- **System parity constraint**: "N posts = N beam segments = N roof edges = N hip rafters. All systems must match this count exactly." Only include systems that actually exist in the model.

Interior angles by shape: triangle=60°, square=90°, pentagon=108°, hexagon=120°, octagon=135°.

---

### Section 3 — PLAN GEOMETRY

Derive from `layout.*` and `structure.*`:
- Shape name
- Span or diameter (from `inscribed_radius_ft` × 2, or `circumscribed_radius_ft` × 2)
- Post positioning logic ("Posts positioned on a perfect circumscribed circle")
- Post spacing in degrees (360 / post_count)

---

### Section 4 — STRUCTURAL FRAME

One subsection per member type that **exists in the model**. Do not include sections for members that are absent. Use nominal lumber sizes (6x6, 4x8) — not actual dimensions (5.5×5.5). Do not include cut angles or miter values — those are carpenter specs, not visual descriptions.

**Posts subsection** (always present):
```
Posts
- [species] timber, nominal [size]
- Quantity: EXACTLY [post_count]
- Height: [cut_length_ft rounded to nearest half-foot]' to beam soffit
- Mounted on visible [footing description]
- Perfect vertical alignment
```

**Beam Ring subsection** (if beams exist):
```
[descriptor] Primary Beam Ring
- [beam_count] segments (one between each pair of posts)
- Material: [nominal_size] [species] timber
- Each segment connects post-to-post only
- Forms a closed [N]-sided ring — no extra segments
```

**Roof Structure subsection** (if roof exists):
```
Roof Structure (OPEN FRAME — NO ROOFING)
- [primary_rafter_count] exposed hip rafters ([nominal_size] [species])
- One rafter per post
- Decorative rafter tails extending past the beam ring
- Rafters converge into a central [hub description]
- Pitch: [pitch]
```

If **jack rafters** exist (`secondary_rafters.enabled = true`):
```
- Each roof bay contains exactly [count_per_side] jack rafters (shorter, [nominal_size])
- Jack rafters terminate into adjacent hip rafters — do not reach the hub
- Creates layered timber framing detail in each bay
```

If **purlins** are enabled (`purlins.enabled = true` AND `show_purlins = true` in visibility_rules):
```
Purlin Ring
- Continuous horizontal ring inside roof
- Follows [shape] symmetry — no added segmentation
```
If purlins are disabled or suppressed: **omit this subsection entirely**.

**Knee Bracing subsection** (if bracing enabled):
```
Knee Bracing
- [total_brace_count] total diagonal knee braces
- [count_per_post] per post
- Material: [nominal_size] [species]
- Curved or chamfered profile, ~[angle_deg]° angle
- Symmetrical and evenly distributed
```

**Joinery subsection** (always):
```
Joinery
- Traditional mortise-and-tenon
- Visible joinery / connector detailing at post-to-beam and brace intersections
- No modern metal hardware visible anywhere
```

---

### Section 5 — MATERIAL + FINISH

Derive from `materials.primary`, `intent.finish` (if present), or project context:
```
Wood: warm [species] timber appearance
Finish: [finish description]
Visible grain, tonal variation, subtle tool marks
Realistic, professional-grade timber frame presentation
```

---

### Section 6 — SCENE + ENVIRONMENT

Derive from `intent.site`, `intent.jurisdiction`, and project context:
```
Photorealistic setting in a [location] garden/patio:
- [hardscape description]
- [planting palette]
- [lighting conditions]
- [atmosphere]
```

---

### Section 7 — CAMERA + VISUAL VERIFICATION

For symmetrical structures use a **slightly elevated 3/4 corner view at 6–7 ft** — this camera height is critical for making all posts countable without foreshortening. For linear structures use a 3/4 angled view along the length.

```
CAMERA + VISUAL VERIFICATION (CRITICAL)
- Perspective: slightly elevated 3/4 view (camera height ~6–7 ft)
- Lens: 35mm equivalent
- Aperture: f/8
- All [N] posts must be clearly visible — no post fully hidden behind another
- No overlap that could obscure counting
- Counting test: viewer must be able to count 1, 2, 3…[N] posts clearly
```

---

### Section 8 — ANTI-FAILURE CONSTRAINTS

```
ANTI-FAILURE CONSTRAINTS

Explicitly forbid:
- [failure shape] geometry (e.g. Octagonal geometry)
- [wrong_count+1] or [wrong_count+2] posts
- Any extra vertical elements
- Uneven spacing
- Distorted or non-regular polygon shapes

This is a simple [N]-node structural system.
The perimeter contains ONLY [N] structural verticals.
No visual clutter that could resemble additional posts.
```

---

### Section 9 — FINAL VALIDATION CHECK

List exactly what must be true. Derive counts from the model — never hardcode.

```
FINAL VALIDATION CHECK (MANDATORY)

The generated image is ONLY correct if:
- The perimeter is a true [shape] ([N] edges)
- There are exactly [N] posts on [footing type]
- There are exactly [N] exposed [primary member] with [tail description]
[- There are exactly [jack_count] jack rafters (if they exist)]
- There are exactly [brace_count] diagonal knee braces (if bracing enabled)
- The structure is symmetrical and physically believable

If any of these conditions fail, the image is incorrect.
```

---

### Section 10 — Exclude block

Always last. One paragraph starting with `Exclude:`. Include:
- Standard hardware: `metal brackets, joist hangers, hurricane ties, screws, bolts, plywood, pressure treated lumber, green lumber`
- Wrong geometry by name: `octagonal geometry` (if hex), `7 posts, 8 posts, extra post, 5 posts`
- Confabulation patterns: `doubled posts, closely spaced posts, decorative posts, asymmetric posts, uneven post spacing, extra vertical members`
- Absent members: `roofing material, shingles` (if open-rafter); `walls, railings, partial walls` (if open-sided); `purlins` (if purlins disabled)
- Style exclusions: `modern furniture, string lights, anime style, cartoon, illustration, watercolor, blueprint overlay, distorted perspective, fisheye, people, animals, cars, shadows too dark, overexposed sky, clipping, grain noise, JPEG artifacts`

---

> **Example — hexagonal cedar pergola (Vancouver Island):**
> See `references/example-hex-gazebo-prompt.md` for a fully worked example showing
> what the output looks like for this specific project. That file shows the level of
> detail and section structure expected — not a template to copy verbatim.

---

## Phase 3 — Tell the User to Paste

**The Copilot CLI is text-only — it cannot generate images.** After writing `outputs/render-prompt.txt`, output this message:

```
Render prompt ready: outputs/render-prompt.txt

Paste the ENTIRE file verbatim into:
  • ChatGPT (chatgpt.com) — uses gpt-image-1 / DALL-E 4 internally
  • Midjourney (midjourney.com) — use /imagine
  • Adobe Firefly (firefly.adobe.com)
  • OpenAI API: openai api images.generate --model dall-e-3

Known issue: even with geometry locks, some image model runs still produce
7 or 8 posts. Verify the count before accepting the result. Regenerate if
needed — the geometry lock improves odds but is not a guarantee.
```

---

## Gotchas

- **Prompt file is always written first.** A user should always get a usable prompt even if image generation is not available in the environment.
- **Do not hardcode angles.** Read `miter_deg`, `bevel_deg`, `pitch` from `structure.json` (geometry section) every time.
- **Model must be locked.** Never generate a render prompt from an unlocked `structure.json`.
- **Image output path is `outputs/photorealistic-render.png`** — not `output/`.
- **Copilot CLI cannot generate images.** Every model in the CLI (GPT-5.4, GPT-5.5, Claude, etc.) is a language model only. Direct the user to ChatGPT, Midjourney, Firefly, or the OpenAI images API. Do not call `copilot image` — that command does not exist.
- **The CAD-SPEC approach is the only validated technique for exact post counts.** Simple count statements and stop-sign analogies alone still produced 7–8 posts across multiple generations. What finally worked: (1) perimeter rule with explicit turn count and interior angle, (2) naming the specific failure shape ("NOT an octagon"), (3) system parity constraint cross-locking all member counts, (4) plan geometry construction logic (circumscribed circle, equal angular increments), (5) camera raised to 6–7 ft, (6) dedicated Anti-Failure Constraints section. All of these together produced a correct 6-post image on the first run.
- **Even with the CAD-SPEC approach, verify the count.** It maximises probability but is not a guarantee. Instruct the user to regenerate if wrong.

---

## Smoke Test

1. **Locked model → single prompt file written:** Given `structure.json` with `_locked: true`: `outputs/render-prompt.txt` is created with real values substituted, geometry lock block at top, `Exclude:` block at bottom. ✓
2. **Unlocked model → halt:** Given `structure.json` with `_locked: false`: skill halts with clear error message; no prompt files written. ✓
3. **CLI unavailable → graceful fallback:** Given `copilot` CLI not in PATH: `outputs/RENDER_FAILED.md` is written and `outputs/render-prompt.txt` is still present for manual use. ✓
4. **Value substitution check:** `[POST_CUT_FT]` and `[TOTAL_HEIGHT_FT]` must not appear literally in the output prompt — they must be replaced with model values. ✓

## Completion: HANDOFF_BLOCK

```json
{
  "stage": "photorealistic-renderer",
  "status": "COMPLETE",
  "outputs": [
    "outputs/render-prompt.txt",
    "outputs/photorealistic-render.png"
  ],
  "prompt_ready_for_paste": true,
  "image_generated": true
}
```

If image generation failed, set `"image_generated": false` and add `"outputs/RENDER_FAILED.md"` to the outputs array.
