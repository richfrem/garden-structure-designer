# Example: Hexagonal Cedar Pergola (Vancouver Island)

Fully worked example of `outputs/render-prompt.txt` produced by the `photorealistic-renderer`
skill for a hexagonal western red cedar pergola, Saanich BC.

**This shows the output quality and prose density expected — not a template to copy.**
Every structure produces different sentences derived from its own model data.

---

## Why prose beats headers

| Attempt | Format | Result |
|---------|--------|--------|
| 1 | Simple count statement mid-paragraph | 7–8 posts |
| 2 | `CRITICAL GEOMETRY LOCK` header block + bullet lists | 7–8 posts |
| 3 | Dense flowing prose with counts embedded naturally + negative prompt | **6 posts ✓** |

The header-block format is read as a checklist that image models can partially ignore.
Dense prose forces the model to parse the geometry description holistically.
Wrong shapes belong in the negative prompt, not cluttering the positive description.

---

## Working prompt (produced correct 6-post image)

```
Ultra-realistic architectural visualization of a handcrafted hexagonal western red cedar timber-frame pergola in a lush Pacific Northwest residential garden, regular true hexagon geometry with exactly 6 evenly spaced 6x6 cedar posts on visible white concrete pier footings with black metal standoffs, one post at each vertex only, no extra supports, no doubled posts.
Heavy 6x12 cedar beam ring with exactly 6 beam segments forming a closed hexagon, exposed timber joinery, warm amber oil finish, visible cedar grain and knots, precision mortise-and-tenon craftsmanship.
Open timber-frame roof with exactly 6 primary hip rafters converging into a prominent central cedar hub block, each roof bay containing exactly 2 shorter jack rafters terminating into adjacent hip rafters, creating layered timber framing detail. Traditional birdsmouth cuts, chamfered knee braces, no metal brackets visible.
Roof pitch 4:12 with 9-inch rafter tail overhangs, open sky between rafters, no roofing material, no shingles, no purlins, no ridge beam.
Camera angle: slightly elevated 3/4 corner perspective from one vertex of the hexagon, 35mm lens, deep focus, all 6 posts fully visible and individually countable.
Environment: high-end Vancouver Island garden in late spring, flagstone patio beneath structure, ferns, hostas, rhododendrons, mossy stone borders, cedar privacy fence, mature evergreens, soft overcast daylight with warm cedar tones.
Photorealistic, luxury residential landscape design aesthetic, professional architectural rendering, natural proportions, realistic timber joinery, ultra-detailed wood texture, balanced composition, soft background depth of field.

Negative prompt: octagon, 8 posts, 7 posts, square pergola, extra columns, doubled posts, metal brackets, roofing panels, shingles, walls, lattice, railings, enclosed gazebo, modern steel hardware, distorted geometry, fisheye lens, cartoon, illustration, CGI artifacts, blurry rafters, missing jack rafters, asymmetrical spacing, people, furniture, string lights.
```

---

## Sentence-by-sentence breakdown

| Sentence | Covers | Key technique |
|----------|--------|---------------|
| 1 | Opening + identity + geometry + site | Embeds "exactly 6" and "one post at each vertex only, no doubled posts" in natural prose |
| 2 | Beam ring | Count embedded: "exactly 6 beam segments forming a closed hexagon" |
| 3 | Roof — hip rafters + jack rafters + braces | Counts embedded: "exactly 6 primary", "exactly 2 shorter jack rafters per bay" |
| 4 | Pitch + overhang + absent members | Explicitly names what is NOT there |
| 5 | Camera | Corner perspective at 6–7 ft, "all 6 posts fully visible and individually countable" |
| 6 | Environment | Derived from site.location and site.surroundings |
| 7 | Style | Closes with rendering quality descriptors |
| Negative | Wrong shapes + wrong counts + absent members + style | All negatives in one place — not in the positive description |
