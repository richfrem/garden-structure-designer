# Revision Mode — Deterministic Output Gate (orchestrator reference)

Used by the `design-orchestrator` agent and the `document-compiler` skill when the user asks to revise, improve, update or restyle existing `outputs/`.

When the user asks to **revise, improve, update, or restyle** existing `outputs/`, this is a **deterministic package revision**, not a presentation-only update.

A revision is NOT complete unless the agent either regenerates or explicitly revalidates this artifact set:

```
outputs/drawing-plan-view.svg          outputs/blueprint-plan.svg
outputs/drawing-elevation-view.svg     outputs/blueprint-elevation.svg
outputs/drawing-isometric-view.svg     outputs/blueprint-isometric.svg
outputs/drawing-perspective-view.svg   outputs/blueprint-component-isolation.svg
outputs/fabrication/cut-list.json      outputs/cad/SB01-structure.dxf  outputs/cad/SB02-plan.dxf
outputs/package-manifest.json
outputs/quality-dashboard.md           outputs/run-insights.json
context/staging/design-run-summary.md
context/staging/schema-validation-report.json
context/staging/physics-validation-report.json
context/staging/drawing-red-team-report.json
context/staging/visual-smoke-report.json
outputs/drawing-red-team-report.md
outputs/visual-smoke-report.md
```

A geometry or intent change is a **new revision**: apply it through the transaction authority (`structure_io.begin_transaction` / `commit_transaction`, or `reset_derived.py`). The commit purges every derived artifact listed above and invalidates earlier approvals; regenerate the full chain and obtain a new red-team approval (approvals are never copied forward).

Markdown files, render prompts, and PNG concept images are **secondary presentation artifacts**. They are never sufficient proof that the package has been revised.

- **Aesthetic-only change:** preserve locked structure.json; re-run/revalidate drawings against existing geometry section.
- **Geometry change** (post count, span, pitch, height, members, bracing, cut lengths): route through the structural pipeline; regenerate `structure.json` geometry section via `geometry_engine.py`. **Never hand-edit deterministic geometry artifacts.**

Before reporting success, always run:

```bash
# 1. Structural & Geometric Compilation
python3 plugins/garden-structure-designer/scripts/schema_validator.py \
  context/staging plugins/garden-structure-designer/schemas \
  --strict --json-output context/staging/schema-validation-report.json

python3 plugins/garden-structure-designer/scripts/structural_physics_validator.py \
  context/staging/structure.json

# 2. Rendering Drawings & Fabrication Cuts
python3 plugins/garden-structure-designer/scripts/render_drawings.py \
  context/staging/structure.json

python3 plugins/garden-structure-designer/scripts/export_cad.py \
  --structure context/staging/structure.json --output-dir outputs/cad

python3 plugins/garden-structure-designer/scripts/fabrication_builder.py \
  context/staging/structure.json

python3 plugins/garden-structure-designer/scripts/builder_docs_compiler.py

# 3. Visual Smoke & Adversarial Red-Team Gates (the red team runs last: it approves the DXFs and cut list too)
python3 plugins/garden-structure-designer/scripts/visual_svg_smoke_test.py \
  --structure context/staging/structure.json \
  --svg-dir outputs \
  --out-dir outputs/visual-smoke \
  --report-json context/staging/visual-smoke-report.json \
  --report-md outputs/visual-smoke-report.md

python3 plugins/garden-structure-designer/scripts/run_drawing_red_team.py \
  --svg-dir outputs \
  --model context/staging/structure.json \
  --report-dir context/staging \
  --md-dir outputs

# 4. Builder Docs & PDF Master Plan Compilation
# (Embeds all SVGs and PNGs in outputs/pergola_plan_embedded.md and compiles outputs/pergola_plan.pdf)
python3 plugins/garden-structure-designer/scripts/package_consistency_validator.py

python3 plugins/garden-structure-designer/scripts/embed_svgs.py \
  outputs/pergola_plan.md \
  outputs/pergola_plan_embedded.md

npx -y md-to-pdf outputs/pergola_plan_embedded.md && cp outputs/pergola_plan_embedded.pdf outputs/pergola_plan.pdf

# 5. Quality Dashboard
python3 plugins/garden-structure-designer/scripts/generate_quality_dashboard.py
```

The final response MUST include: files changed · structural parameters preserved vs changed · commands run · validator results · visual smoke test results · drawing red-team result (`may_claim_success`) · remaining warnings · status: **PASS / PARTIAL / BLOCKED / DRAFT ONLY**.

**Status taxonomy:**
- `PASS` — all deterministic artifacts regenerated/revalidated, validators passed, dashboard updated.
- `PARTIAL` — presentation files updated but deterministic SVG/JSON artifacts not fully regenerated or validated.
- `BLOCKED` — a validator failed, required artifact is missing, or repair loop halted.
- `DRAFT ONLY` — user explicitly requested output despite incomplete validation; stamp every output as not for construction.

Do not claim the package is complete unless the deterministic validation artifacts exist and are current.
