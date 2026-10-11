---
name: document-compiler
description: Assembles all outputs into a structured document and formats for PDF export. Ensures sections are complete, ordered matching the Option A Architectural Layout constraint.
allowed-tools: Read, Write, Bash
---

# Document Compiler

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- **Stage 7.** Compiles the final package from artifacts that were already approved; it **never regenerates drawings or DXFs** (changed bytes would need renewed QA).
- Preflight: `drawing-red-team-report.json` has `may_claim_success: true` **and** is bound to the current revision; photorealistic renders exist; structure.json exists.
- The parsed validator (`cross_artifact_validator.validate_dxf_artifacts`) runs on the exact DXF bytes being packaged; any error fails packaging.
- Referenced markdown assets must exist (`embed_svgs.py` reports missing ones and packaging fails).
- `outputs/package-manifest.json` records revision identity and SHA-256 + size for every file. It does not yet carry producer/config fingerprints or dependency digests, and the package does not yet include the structure.json snapshot (F-10).

## Quick start
```bash
python3 scripts/compile_package.py [staging_dir] [outputs_dir] [md_filename]
python3 scripts/package_consistency_validator.py
```
Run commands from the skill root. `scripts/` entries are file-level symlinks to the plugin's canonical `scripts/` (dereferenced on install); never edit them through the symlink.

## Workflow
1. **Preflight**: red-team approval bound to the revision, renders present.
2. **CAD**: validate the existing `outputs/cad/SB01-structure.dxf` and `SB02-plan.dxf` (no regeneration).
3. **Assets + PDF**: embed SVG/PNG assets into `<stem>_embedded.md`; convert with `npx md-to-pdf` (degrades to a documented markdown fallback; unpinned npx is a known risk, F-9).
4. **Manifest**: write `package-manifest.json`.

## Verification
- `pytest tests/test_compile_package.py tests/test_compile_package_stage7.py tests/test_package_consistency_validator.py tests/test_embed_svgs.py` (development checkout, run from the plugin root).

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
