---
name: drawing-generator
description: Produces orthographic projections (Plan view, Elevation view), along with 3D visualizations (Perspective View, Isometric/Axonometric View) based on the structural model coordinates. Output uses consistent scaling and styling.
allowed-tools: Read, Write
---

## Expected Inputs
`context/staging/structural-model.json` 
`context/staging/joinery-model.json`

## Behavior
Parses the 3D grid relationships and structural sizes. Generates four distinct representations (.svg or .png parameters) for high-quality injection into the final PDF:
1. Plan View (Top-down orthographic layout)
2. Elevation View (Front/Side orthographic projection)
3. Perspective View (Simulates human vision with vanishing points for a realistic sense of depth, scale, and spatial relationships)
4. Isometric or Axonometric View (3D representation where parallel lines remain parallel, maintaining accurate geometric proportions)
