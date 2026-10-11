---
name: joinery-designer
description: Determines joinery type per connection based on structural model bounds and user preferences. Explains load transfer behavior and outputs joinery maps.
allowed-tools: Read, Write
---

# Joinery Designer

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Chooses joinery per connection using the **stable member ids** and the connection graph in `geometry.joints.topology` (post tops to beam soffits, rafter seats, hub faces, braces).
- Joinery never moves or adds members; it only annotates connections. Ids must match across structure.json, SVG `data-tag`, DXF XDATA and QA reports.

## Quick start
```bash
(no script: reads `geometry.joints.topology.connections` and writes the `joinery` section through the transaction authority)
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Input**: validated Stage 2 topology.
2. **Execution**: assign a joint type and load-transfer note to each connection id.
3. **Gate**: every connection id in the joinery map exists in the topology; no member is added or removed.

## Verification
- Compare connection ids against `geometry.joints.topology.connections`.

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
