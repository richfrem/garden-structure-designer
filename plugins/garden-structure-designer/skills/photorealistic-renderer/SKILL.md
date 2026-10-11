---
name: photorealistic-renderer
description: Generates a detailed photorealistic image-generation prompt driven entirely by the locked structural model. Works for any garden structure (gazebo, pergola, arbour, shed, fence, trellis, etc.). Produces a single paste-ready file with geometry locks, structural description, camera direction, and exclusions tailored to whatever was designed. Trigger with "render the structure", "create a photorealistic image", "generate a render prompt", "visualize the design", or "show me what this will look like".
allowed-tools: Read, Write, Bash
---

# Photorealistic Renderer

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Builds the render prompt **from the locked structure.json only**: member counts, sides, hub, roof pitch and materials are read, not assumed.
- The package compiler requires at least one render in `outputs/high-resolution-image/` (Stage 7 preflight).
- A render is derived from one revision: after a new committed revision it is purged and must be regenerated.

## Quick start
```bash
(no script: writes the prompt file; the image lands in outputs/high-resolution-image/)
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: sealed structure.json and the approved drawings.
2. **Execution**: write the geometry-locked prompt (structure type, N sides, hub, roof, materials, camera, exclusions).
3. **Gate**: `compile_package.py` blocks when no render exists.

## Verification
- `ls outputs/high-resolution-image/*_render_*.png`

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
