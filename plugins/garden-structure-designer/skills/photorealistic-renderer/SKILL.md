---
name: photorealistic-renderer
description: Generates a detailed photorealistic image-generation prompt driven entirely by the locked structural model. Works for any garden structure (gazebo, pergola, arbour, shed, fence, trellis, etc.). Produces a single paste-ready file with geometry locks, structural description, camera direction, and exclusions tailored to whatever was designed. Trigger with "render the structure", "create a photorealistic image", "generate a render prompt", "visualize the design", or "show me what this will look like".
allowed-tools: Read, Write, Bash
---

## Expected Inputs
- `context/staging/structural-model.json` (must be locked: `_locked: true`)
- `context/staging/geometry-calculations.json`
- `context/staging/design-spec.json` (optional — enriches prompt with site context)

## Outputs
- `outputs/render-prompt.txt` — single self-contained file: all geometry locks, structural description, camera direction, and exclusions. Paste the whole thing verbatim into ChatGPT or any image model.
- `outputs/photorealistic-render.png` — generated image (if the user pastes and generates)
- `outputs/RENDER_FAILED.md` — written if the skill cannot complete; prompt file still saved

---

## Phase 1 — Read Locked Model

Read `context/staging/structural-model.json`. If `_locked` is not `true`, halt with:
```
ERROR: structural-model.json is not locked. Run structural-engine first.
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

Also read `context/staging/geometry-calculations.json`:
- `total_height_ft`, `post_cut_ft`, `span_ft`, `diameter_ft` — whatever dimensions are present

Also read `context/staging/design-spec.json` (if present):
- `site.location`, `site.setting`, `site.surroundings` → used to set the scene realistically

---

## Phase 2 — Compose and Write Prompt

Write `outputs/render-prompt.txt` by assembling the prompt from the model data. There is no fixed template — the content is derived from what was actually designed. The structure below defines the **sections to include and how to populate each one**.

### Prompt structure (always in this order)

**1. Geometry Lock block** *(always first — see Gotchas for why)*

Open with a `CRITICAL GEOMETRY LOCK — NON-NEGOTIABLE:` block using the CAD-SPEC approach (validated as the only technique that reliably enforced 6 posts):

- **Absolute geometry definition:** State sides, vertices, and structural corner posts as three separate lines. Use "ONLY N POSTS TOTAL" with explicit wrong counts.
- **Perimeter rule:** "The viewer must be able to visually trace the perimeter and make exactly N directional turns ([angle]° each). Interior angle at every corner = [angle]°."
- **Name the failure shape explicitly:** "This is NOT an octagon — never 8 sides, never 8 posts" (or whatever the likely confabulation shape is).
- **Post count hard lock:** "TOTAL POSTS = N" as a standalone line. Add "No doubled posts, no closely spaced posts, no decorative posts."
- **System parity constraint:** "N posts = N beam segments = N roof edges = N hip rafters. All systems must match this count exactly."
- **Plan geometry construction logic:** State that posts are positioned on a circumscribed circle at equal angular increments (e.g. 60° for hex).
- **Visibility + countability:** "Viewer must be able to count: 1, 2, 3…N — clearly and unambiguously."
- **Failure condition:** "If more or fewer than N [members] appear, the image is incorrect."
- Only include constraints meaningful for this structure — a lean-to shed does not need a rafter parity lock.

**2. Scene & Setting**

Derive from `design-spec.json` if present. Otherwise use reasonable defaults for the project context. Include: location/climate, garden character, time of day, lighting conditions.

**3. Structure (Must Be Geometrically Correct & Buildable)**

One section per structural system, populated from model data. Include only the systems that exist in the model. Example sections: Plan shape / Posts / Primary beam / Roof structure / Bracing / Joinery / Special members. For each repeated member, state the exact quantity with `EXACTLY N` where count accuracy matters visually.

**4. Material & Finish**

Derive species, grade, and finish from the model. Include grain character, finish tone, and craftsmanship quality.

**5. Camera & Composition**

Choose the camera angle that best reveals the structure's defining geometry. For symmetrical structures, a **slightly elevated 3/4 corner view (camera height 6–7 ft)** works best — the extra elevation helps the viewer count perimeter members without foreshortening. For linear structures (pergola, fence run), a 3/4 angled view along the length. For simple sheds, a straight-on 3/4 elevation. Always include: angle, height, lens, aperture, focus point, depth of field intent.

Add: "All [primary structural members] must be clearly visible — no post fully hidden behind another. No overlap that could obscure counting."

**6. Final Validation Requirement**

List 3–5 things the viewer must be able to count or confirm in the image. Derived from the most visually critical members.

**7. Exclude block** *(always last)*

- Standard hardware/style exclusions (see base list below)
- Add the **specific wrong shape by name** (e.g. `octagonal geometry, 8 posts, 8 sides` if the structure is hexagonal)
- Add all wrong counts explicitly (e.g. `7 posts, 8 posts, 5 posts`)
- Add confabulation patterns: `doubled posts, closely spaced posts, decorative posts, uneven spacing, extra vertical elements, distorted polygon`
- Add structural exclusions specific to what was NOT designed (no roofing if open-rafter, no walls if open-sided)

Standard base exclusions:
```
metal brackets, joist hangers, hurricane ties, screws, bolts, plywood,
pressure treated lumber, green lumber, modern furniture, string lights,
anime style, cartoon, illustration, watercolor, blueprint overlay,
distorted perspective, fisheye, people, animals, cars, shadows too dark,
overexposed sky, clipping, grain noise, JPEG artifacts
```

---

> **Example only — hexagonal cedar gazebo (Vancouver Island):**
> See `references/example-hex-gazebo-prompt.md` for a fully worked example showing
> what the output looks like for this specific project. That file shows the level of
> detail expected, not a template to copy.

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
- **Do not hardcode angles.** Read `miter_deg`, `bevel_deg`, `pitch` from geometry-calculations.json every time.
- **Model must be locked.** Never generate a render prompt from an unlocked structural model.
- **Image output path is `outputs/photorealistic-render.png`** — not `output/`.
- **Copilot CLI cannot generate images.** Every model in the CLI (GPT-5.4, GPT-5.5, Claude, etc.) is a language model only. Direct the user to ChatGPT, Midjourney, Firefly, or the OpenAI images API. Do not call `copilot image` — that command does not exist.
- **The CAD-SPEC approach is the only validated technique for exact post counts.** Simple count statements and stop-sign analogies alone still produced 7–8 posts across multiple generations. What finally worked: (1) perimeter rule with explicit turn count and interior angle, (2) naming the specific failure shape ("NOT an octagon"), (3) system parity constraint cross-locking all member counts, (4) plan geometry construction logic (circumscribed circle, equal angular increments), (5) camera raised to 6–7 ft, (6) dedicated Anti-Failure Constraints section. All of these together produced a correct 6-post image on the first run.
- **Even with the CAD-SPEC approach, verify the count.** It maximises probability but is not a guarantee. Instruct the user to regenerate if wrong.

---

## Smoke Test

1. **Locked model → single prompt file written:** Given `_locked: true`: `outputs/render-prompt.txt` is created with real values substituted, geometry lock block at top, `Exclude:` block at bottom. ✓
2. **Unlocked model → halt:** Given `_locked: false`: skill halts with clear error message; no prompt files written. ✓
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
