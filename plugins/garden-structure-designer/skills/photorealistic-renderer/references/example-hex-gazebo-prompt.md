# Example: Hexagonal Cedar Pergola (Vancouver Island)

Fully worked example of `outputs/render-prompt.txt` for a hexagonal western red cedar pergola,
Saanich BC. Includes jack rafters (2 per bay), no purlins.

**This shows the expected section structure and level of detail — not a template to copy verbatim.**
Every structure produces different content derived from its own model data.

---

## Working prompt

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
Size: 9'9" flat-to-flat span (approx 11'3" point-to-point diameter)
Posts positioned on a perfect circumscribed circle
Post spacing: exactly 60° increments


STRUCTURAL FRAME

Posts
- 6x6 warm cedar timber
- Quantity: EXACTLY 6
- Height: 8'5" to beam soffit
- Mounted on visible white concrete pier footings with black metal standoffs
- Perfect vertical alignment

Heavy Primary Beam Ring
- 6 segments (one between each pair of posts)
- Material: heavy 6x12 cedar timber
- Each segment connects post-to-post only
- Forms a closed 6-sided ring — no extra segments

Roof Structure (OPEN FRAME — NO ROOFING)
- 6 exposed hip rafters (4x6 cedar)
- One rafter per post
- Decorative rafter tails extending 9 inches past the beam ring
- Rafters converge into a central polygonal cedar hub block at the apex
- Pitch: 4:12
- Each roof bay contains exactly 2 jack rafters (4x4 cedar)
- Jack rafters terminate into adjacent hip rafters — do not reach the hub
- Creates layered timber framing detail in each bay

Knee Bracing
- 12 total diagonal knee braces
- 2 per post
- Material: 4x4 cedar
- Curved or chamfered profile, ~45° angle
- Symmetrical and evenly distributed

Joinery
- Traditional mortise-and-tenon
- Visible joinery / connector detailing at post-to-beam and brace intersections
- No modern metal hardware visible anywhere


MATERIAL + FINISH

Wood: warm cedar timber appearance
Finish: transparent amber oil
Visible grain, tonal variation, subtle tool marks
Realistic, professional-grade timber frame presentation


SCENE + ENVIRONMENT

Photorealistic setting in a Vancouver Island residential garden (Saanich, BC):
- Irregular flagstone patio beneath the structure
- Ferns, hostas, rhododendrons, ornamental grasses, mossy stone borders
- Cedar privacy fence, mature Douglas fir backdrop
- Soft overcast Pacific Northwest daylight with warm cedar tones


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
- There are exactly 6 posts on white concrete pier footings
- There are exactly 6 exposed hip rafters with 9-inch decorative tails
- There are exactly 12 jack rafters (2 per bay, visible between hip rafters)
- There are exactly 12 diagonal knee braces
- The structure is symmetrical and physically believable

If any of these conditions fail, the image is incorrect.


Exclude: metal brackets, joist hangers, hurricane ties, screws, bolts, plywood,
pressure treated lumber, green lumber, modern furniture, string lights, anime style,
cartoon, illustration, watercolor, blueprint overlay, distorted perspective, fisheye,
people, animals, cars, shadows too dark, overexposed sky, clipping, grain noise,
JPEG artifacts, octagonal geometry, 7 posts, 8 posts, extra post, 5 posts,
doubled posts, closely spaced posts, decorative posts, asymmetric posts,
uneven post spacing, extra vertical members, railings, partial walls,
roofing panels, shingles, solid roof, walls, purlin ring, ridge beam,
missing jack rafters
```

---

## What changed from the old example

The old example in this repo had several values that did not match the current model:

| Field | Old (wrong) | Current (correct) |
|-------|-------------|-------------------|
| Beam size | 4x8 | 6x12 |
| Jack rafters | "No intermediate rafters" | 2 per bay (12 total) |
| Purlins | Purlin Ring section included | Omitted (show_purlins=false) |
| Hub | "6x6 king post" | "polygonal cedar hub block" |
| Post height | 8'6" | 8'5" (8.42 ft) |
| Footing | "concrete footing pads" | "white concrete pier footings with black metal standoffs" |

Always read the current `structure.json` — never copy values from this example.
