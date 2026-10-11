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
- Strictly follow deterministic execution contracts for photorealistic-renderer.
- Input parameters must resolve from staging structure.json.

## Quick start


## Workflow
1. **Input Phase**: Load parameters for photorealistic-renderer.
2. **Execution Phase**: Process and emit deterministic output.
3. **Gate Phase**: Validate schema and physics integrity.

## Verification


## References
- [Acceptance Criteria](references/acceptance-criteria.md)
