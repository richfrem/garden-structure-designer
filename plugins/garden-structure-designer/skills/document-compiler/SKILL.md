---
name: document-compiler
description: Assembles all outputs into a structured document and formats for PDF export. Ensures sections are complete, ordered matching the Option A Architectural Layout constraint.
allowed-tools: Read, Write, Bash
---

# Check the gate report exists and is approved, and verify photorealistic renders

## Contents
- [Critical Constraints](#critical-constraints)
- [Quick start](#quick-start)
- [Workflow](#workflow)
- [Verification](#verification)
- [References](#references)

## Critical Constraints
- Strictly follow deterministic execution contracts for document-compiler.
- Input parameters must resolve from staging structure.json.
- Verifies drawing-red-team-report.json before allowing PDF generation (`may_claim_success: true`).
- Emits CAD deliverables via ExchangeWriter port: `outputs/cad/SB01-structure.dxf` and `outputs/cad/SB02-plan.dxf`.
- Generates cryptographic `outputs/package-manifest.json` recording SHA-256 digests and byte sizes of all package artifacts.

## Quick start
```bash
python3 plugins/garden-structure-designer/scripts/compile_package.py [staging_dir] [outputs_dir] [md_filename]
```

## Workflow
1. **Preflight Gate**: Assert `drawing-red-team-report.json` exists with `may_claim_success: true` and photorealistic renders exist.
2. **CAD Deliverables Export**: Invoke `export_cad.py` via `ExchangeWriter` (`CadcraftAdapter` / `EzdxfAdapter`) to write SB01 (3D framing) and SB02 (2D plan).
3. **Asset Embedding**: Embed all SVG and PNG assets inline into `<stem>_embedded.md`.
4. **PDF Compilation**: Render final standalone PDF package via `npx md-to-pdf` (with graceful markdown fallback).
5. **Package Manifest**: Generate `outputs/package-manifest.json` hashing all produced deliverables.

## Verification
- Verify `outputs/package-manifest.json` exists and matches SHA-256 digests.
- Verify `outputs/cad/SB01-structure.dxf` and `outputs/cad/SB02-plan.dxf` exist and pass parsed audit.
- Run `pytest plugins/garden-structure-designer/tests/test_compile_package.py`.

## References
- [Acceptance Criteria](references/acceptance-criteria.md)
