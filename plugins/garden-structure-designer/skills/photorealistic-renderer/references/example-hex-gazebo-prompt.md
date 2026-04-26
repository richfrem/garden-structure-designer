# Example: Hexagonal Cedar Gazebo (Vancouver Island)

This is a fully worked example of the `render-prompt.txt` output produced by the
`photorealistic-renderer` skill for the hexagonal western red cedar gazebo project.

**This is an example of the level of detail expected — not a template to copy.**
Every garden structure is different. A pergola, shed, arbour, or fence would produce
completely different sections derived from its own structural model.

---

## Why this prompt is structured this way

Image models don't count — they pattern-match. Iterations with progressively stronger
prompts produced these results:

| Attempt | Prompt approach | Result |
|---------|----------------|--------|
| 1 | Simple count statement ("exactly 6 posts") mid-paragraph | 7 posts |
| 2 | Front-loaded GEOMETRY LOCK + stop-sign analogy + rafter pairing | 8 posts |
| 3 | CAD-SPEC approach (perimeter rule + system parity + anti-failure section + raised camera) | **6 posts ✓** |

**What the CAD-SPEC approach adds that earlier attempts lacked:**
- Perimeter rule: explicit turn count (6 turns at 120°) and interior angle — gives the model a geometric definition it can parse
- System parity: "6 posts = 6 beam segments = 6 roof edges = 6 hip rafters" — cross-locks all member counts
- Names the failure shape explicitly: "NOT an octagon — never 8 sides, never 8 posts"
- Plan geometry construction logic: posts on a circumscribed circle at 60° increments
- Camera raised to 6–7 ft (helps viewer count perimeter members without foreshortening)
- Dedicated Anti-Failure Constraints section that explicitly forbids octagonal geometry

---

## Working prompt (produced correct 6-post image)

```
HEXAGONAL TIMBER FRAME — CAD-SPEC PROMPT (MAX ENFORCEMENT)

ABSOLUTE GEOMETRY DEFINITION (TOP PRIORITY — DO NOT VIOLATE):

The structure is a regular hexagon defined explicitly as:
- 6 sides
- 6 vertices
- 6 structural corner posts ONLY

Perimeter rule:
- The outer boundary consists of exactly 6 straight edges
- The viewer must be able to visually trace the perimeter and make exactly 6
  directional turns (120° each)
- Interior angle at every corner = 120 degrees
- This is NOT an octagon — never 8 sides, never 8 posts

Post count constraint (hard lock):
- TOTAL POSTS = 6
- One post per vertex
- No additional vertical supports anywhere on the perimeter or inside
- No doubled posts, no closely spaced posts, no decorative posts
- Posts must be evenly spaced at 60° around the center

System parity constraint:
- 6 posts = 6 beam segments = 6 roof edges = 6 hip rafters
- All systems must match this count exactly


PLAN GEOMETRY (EXPLICIT CONSTRUCTION LOGIC)

Shape: regular hexagon
Size: 10 feet point-to-point diameter
Posts positioned on a perfect circumscribed circle
Post spacing: exactly 60° increments


STRUCTURAL FRAME

Posts
- 6x6 western red cedar
- Quantity: EXACTLY 6
- Height: 8.33 ft to beam soffit
- Mounted on concrete pier blocks with standoff bases
- Perfect vertical alignment

Primary Beam Ring
- 6 segments (one between each pair of posts)
- Material: 4x8 cedar
- Each segment connects post-to-post only
- Joints: precise compound miter (~28.71°)
- Forms a closed 6-sided ring — no extra segments

Roof Structure (OPEN FRAME — NO ROOFING)
- 6 hip rafters (4x6 cedar)
- One rafter per post
- Rafters converge into a central 6x6 king post hub
- Pitch: 4:12
- Rafters define 6 roof planes ONLY
- No intermediate rafters, no secondary rafters

Purlin Ring
- Continuous horizontal ring inside roof
- Follows hexagonal symmetry — no added segmentation beyond 6-sided logic

Knee Bracing
- 12 total braces
- 2 per post
- Material: 4x4 cedar
- Curved profile, ~45° angle
- Symmetrical and evenly distributed

Joinery
- Traditional mortise-and-tenon
- No metal hardware visible anywhere


MATERIAL + FINISH

Wood: western red cedar
Finish: transparent amber oil
Visible grain, tonal variation, subtle tool marks
Realistic, professional-grade timber frame appearance


SCENE + ENVIRONMENT

Photorealistic setting in a Pacific Northwest coastal garden (Vancouver Island, BC):
- Ferns, moss, rhododendrons
- Mature coastal Douglas fir trees
- Soft overcast daylight
- Slight atmospheric moisture
- Natural diffuse shadows


CAMERA + VISUAL VERIFICATION (CRITICAL)

- Perspective: slightly elevated 3/4 view (camera height ~6–7 ft)
- Lens: 35mm equivalent
- Aperture: f/8
- All 6 posts must be clearly visible — no post fully hidden behind another
- No overlap that could obscure counting
- Counting test: viewer must be able to count 1, 2, 3, 4, 5, 6 posts clearly


ANTI-FAILURE CONSTRAINTS

Explicitly forbid:
- Octagonal geometry
- 7 or 8 posts
- Any extra vertical elements
- Uneven spacing
- Distorted or non-regular polygon shapes

This is a simple 6-node structural system.
The perimeter contains ONLY 6 structural verticals.
No visual clutter that could resemble additional posts.


FINAL VALIDATION CHECK (MANDATORY)

The generated image is ONLY correct if:
- The perimeter is a true hexagon (6 edges)
- There are exactly 6 posts
- There are exactly 6 rafters meeting at center
- There are exactly 12 knee braces
- The structure is symmetrical and physically believable

If any of these conditions fail, the image is incorrect.


Exclude: metal brackets, joist hangers, hurricane ties, screws, bolts, plywood,
pressure treated lumber, green lumber, modern furniture, string lights, anime style,
cartoon, illustration, watercolor, blueprint overlay, distorted perspective, fisheye,
people, animals, cars, shadows too dark, overexposed sky, clipping, grain noise,
JPEG artifacts, octagonal geometry, 7 posts, 8 posts, extra post, 5 posts,
doubled posts, closely spaced posts, decorative posts, asymmetric posts,
uneven post spacing, extra vertical members, railings, partial walls
```

