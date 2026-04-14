---
name: drawing-generator
description: Produces orthographic projections (Plan view, Elevation view) based on the structural model coordinates. Output uses consistent scaling and styling.
allowed-tools: Read, Write
---

## Expected Inputs
`context/staging/structural-model.json` 
`context/staging/joinery-model.json`

## Behavior
Parses the 3D grid relationships and structural sizes. Generates localized representations (.svg or .png parameters) for high-quality injection into the final PDF.
