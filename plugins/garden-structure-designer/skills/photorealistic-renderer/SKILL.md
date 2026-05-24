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

Write `outputs/render-prompt.txt` as two blocks: a **positive prompt** (dense flowing prose) followed by a **`Negative prompt:`** line. No headers, no bullet lists, no section labels inside the file — those parse poorly in image models.

### Why prose, not headers

Structured headers (`CRITICAL GEOMETRY LOCK`, `STRUCTURAL FRAME`, etc.) are read sequentially by language models that generate images. Dense prose with geometry constraints embedded naturally performs significantly better because the model parses the description holistically rather than as a checklist it can partially ignore.

### Positive prompt — how to write it

Write 6–8 dense sentences. Each sentence covers one system and embeds its exact count directly in natural language. Do not separate counts into a separate lock block — weave them into the description.

**Sentence 1 — Opening + identity + material + location:**
Open with `Ultra-realistic architectural visualization of a handcrafted [shape] [species] timber-frame [structure type]` then add the site context (location, setting). Everything flows from the model data — no defaults.

**Sentence 2 — Posts + footings:**
Describe the posts with the exact count embedded naturally: `exactly [N] evenly spaced [size] [species] posts on visible [footing type] with [hardware]`, then close with the anti-confabulation constraint in the same sentence: `one post at each vertex only, no extra supports, no doubled posts`. Include post height in feet.

**Sentence 3 — Beam ring:**
`Heavy [size] [species] beam ring with exactly [N] beam segments forming a closed [shape], [joinery description], [finish], [material character]`.

**Sentence 4 — Roof structure** (include all roof members that exist in the model):
`Open timber-frame roof with exactly [N] primary hip rafters converging into [hub description]` — if jack rafters exist: `each roof bay containing exactly [count_per_bay] shorter jack rafters terminating into adjacent hip rafters, creating layered timber framing detail`. Include joinery: `traditional birdsmouth cuts`, `chamfered knee braces`. If purlins are absent, say so explicitly (`no purlins`).

**Sentence 5 — Dimensions + what's absent:**
`Roof pitch [pitch] with [overhang_in]-inch rafter tail overhangs, open sky between rafters` — then explicitly name what is NOT there: `no roofing material, no shingles, no ridge beam` and any other members absent from this design.

**Sentence 6 — Camera:**
`Camera angle: slightly elevated 3/4 corner perspective from one vertex of the [shape], [lens]mm lens, deep focus, all [N] posts fully visible and individually countable.`

**Sentence 7 — Environment:**
Derive from `site.*` in structure.json. Include: setting type, hardscape, planting palette, lighting character. Keep it one sentence.

**Sentence 8 — Style:**
Close with style descriptors: `Photorealistic, luxury residential landscape design aesthetic, professional architectural rendering, natural proportions, realistic timber joinery, ultra-detailed wood texture, balanced composition, soft background depth of field.`

### Negative prompt — how to write it

One line, starting with `Negative prompt:`, comma-separated. Always include:

- The specific **wrong shape by name** (e.g. `octagon, 8 posts` if hex; `hexagon, 6 posts` if square)
- All **wrong post counts** by number (e.g. `7 posts, 8 posts, 5 posts`)
- **Confabulation patterns**: `extra columns, doubled posts, asymmetrical spacing, missing jack rafters`
- **Members absent from this design**: `roofing panels, shingles, walls, lattice, railings, enclosed gazebo, ridge beam, purlins` (tailor to the model)
- **Hardware**: `metal brackets, joist hangers, hurricane ties, modern steel hardware`
- **Style**: `cartoon, illustration, CGI artifacts, distorted geometry, fisheye lens, blurry rafters, people, furniture, string lights`

---

> **Example — hexagonal cedar pergola (Vancouver Island):**
> See `references/example-hex-gazebo-prompt.md` for a fully worked example.
> That file is the reference for output quality and prose density — not a template to copy verbatim.

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
