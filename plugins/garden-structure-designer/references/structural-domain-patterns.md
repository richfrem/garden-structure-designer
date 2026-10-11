# Structural Domain Patterns

Domain-specific structural engineering knowledge for hexagonal and polygonal timber frame garden structures.  
These patterns are the curated ground truth the structural-engine skill uses to avoid hallucination.

---

## Pattern 1: Hexagonal Post Spacing from Long Diagonal

A regular hexagon has the property that **side length = radius = half the long diagonal**.

Given `max_diagonal_ft` (longest vertex-to-vertex span):

```
radius_ft        = max_diagonal_ft / 2
side_length_ft   = radius_ft          # for a regular hexagon
center-to-center span (face-adjacent posts) = side_length_ft
```

**Example:** 10ft max diagonal → radius = 5ft, post-to-post side span = 5ft.

---

## Pattern 2: Post Cut Length from Target Total Height

Total height = post cut length + beam depth + roof rise.

```
roof_rise_ft  = (pitch_rise / pitch_run) × radius_ft
beam_depth_ft = beam_nominal_depth_in / 12
post_cut_ft   = total_height_ft - beam_depth_ft - roof_rise_ft
```

**Example (4:12 pitch, 5ft radius, 7.25" beam, 10.5ft target):**
- roof_rise = (4/12) × 5.0 = 1.667ft
- beam_depth = 7.25/12 = 0.604ft
- post_cut = 10.5 − 0.604 − 1.667 = **8.229ft (≈ 8'-2¾")**

---

## Pattern 3: Minimum Timber Dimensions by Span

Based on BC Building Code for single-storey open agricultural/garden structures.  
Species assumption: Douglas Fir-Larch No.1 or better.

| Member       | Span     | Minimum Section | Notes                                     |
|:-------------|:---------|:----------------|:------------------------------------------|
| Post         | ≤ 10ft   | 6×6             | Slenderness ratio L/d < 50 (6" face)      |
| Beam         | ≤ 5ft    | 4×8             | 7.25" actual depth for L/360 deflection   |
| Beam         | 5–8ft    | 6×8 or 4×10     | Increase depth to control deflection      |
| Hip Rafter   | ≤ 6.5ft  | 4×6             | Includes 12" overhang typical             |
| Knee Brace   | N/A      | 4×4             | 36" length, 45°, both ends pegged M&T     |

---

## Pattern 4: Saanich BC Load Table (Coastal Vancouver Island)

Source: BC Building Code, Table C-2 / Saanich Municipal Engineering Standards

| Load Type    | Value     | Notes                                                       |
|:-------------|:----------|:------------------------------------------------------------|
| Snow (Ss)    | 1.9 kPa (≈ 40 psf)  | Coastal variant; open structures reduce by 0.6 factor |
| Wind (q)     | 0.48 kPa (≈ 10 psf) | Hourly wind, 1:50 return period, Saanich exposure B    |
| Seismic      | Category C | Standard ductile connections required                  |
| Frost depth  | 18"        | Below grade for footings/caissons                      |

Note: Open pergola structures (no solid roof) qualify for a 40% snow load reduction under NBC 2020 Part 9.

---

## Pattern 5: Compound Cut Formula (Polygonal Hip Rafters)

For a regular polygon with `N` sides and roof pitch `rise:run`:

```python
pitch_angle_deg     = degrees(atan(rise / run))
plan_half_angle_deg = 180 / N

miter_deg = degrees(atan(cos(radians(pitch_angle_deg)) * tan(radians(plan_half_angle_deg))))
bevel_deg = degrees(asin(sin(radians(pitch_angle_deg)) * sin(radians(plan_half_angle_deg))))
```

**Verified values — Hexagon (N=6), 4:12 pitch:**

| Parameter         | Value    |
|:------------------|:---------|
| Pitch angle       | 18.43°   |
| Plan half-angle   | 30.0°    |
| **Miter**         | **28.71°** |
| **Bevel**         | **9.10°**  |

> **Critical pitfall:** Using pitch_angle (18.43°) directly as the miter setting is the most common error. At a hexagonal hub the miter is 28.71° — always use the compound formula or geometry_engine.py.

---

## Pattern 6: Post Slenderness Ratio Check

Sawn lumber post slenderness limit: `L/d < 50`

```
L = unsupported post length in inches (post cut length × 12)
d = minimum face dimension in inches

For 6×6 post (d = 5.5"):  max safe length = 50 × 5.5 / 12 = 22.9ft
```

A 6×6 at 8.23ft (≈ 99") has L/d = 99/5.5 = **18** → well within limit.

---

## Pattern 7: Caisson Sizing for Coastal BC

Default for pergola point loads (Saanich):
- **Diameter:** 12" (minimum) for 6×6 post on residential use
- **Depth:** 24" below grade (exceeds 18" frost depth with margin)
- **Concrete:** 3000 psi minimum
- **J-bolt:** ½" × 8" J-bolt, 4" embedment, set wet to ABA66Z base plate bolt pattern

Bearing capacity check: Assume 2000 psf soil bearing (conservative residential soil).  
Post tributary area = (5ft side × 5ft side) / 2 × 6 posts at perimeter = ~12.5 sq ft per post.  
At 40 psf snow + 10 psf dead: 50 psf × 12.5 sq ft = **625 lbs per post** → well within 12" caisson capacity.
