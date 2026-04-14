# Garden Structure Designer Plugin — Improvement Specification

**Version:** 1.0  
**Date:** 2026-04-14  
**Author:** Richard (via Cowork session)  
**Repo:** antigravity agent repo  
**Plugin:** `garden-structure-designer`

---

## Background & Problem Statement

The `garden-structure-designer` plugin was tested end-to-end to design a freestanding hexagonal cedar pergola (10 ft long diagonal, 8.5 ft tall, Victoria BC). The pipeline worked — it produced structural output, joinery maps, bracing analysis, drawings, and a compiled PDF — but three significant problems were identified:

### Problem 1 — No Progressive Elaboration (Fails Fast Expensively)

The current pipeline runs all skills sequentially in one go: intake → building-code → structural-engine → joinery → bracing → drawing-generator → document-compiler. If the user's mental model of the structure doesn't match what the system computed (wrong shape, wrong scale, wrong orientation), the error is only discovered at the end after burning through the full token budget. There is no checkpoint.

**Impact:** Wasted ~20–30 minutes of runtime and a large token spend before the user can course-correct.

### Problem 2 — Excessive Token Consumption (All Skills Run in Main Session)

All pipeline skills are currently invoked via the Agent tool, which loads each skill's full output into the main session's context window. By the time the document-compiler runs, the main context contains the full output of every prior skill. For a complex structure this becomes very expensive.

**Impact:** Token consumption is 5–10× higher than necessary. The main session context window fills up, degrading quality of later outputs.

### Problem 3 — JSON Values Are Not Fact-Checked Against Reference Data

The structural-engine, building-code-validator, and other skills generate plausible-looking JSON values (load tables, member capacities, utilization ratios) that are not cross-checked against actual code tables before being fed into the document-compiler. In testing, the pipeline produced correct-looking but occasionally overconfident outputs (e.g., asserting a P.Eng. stamp was required for a small exempt backyard pergola — incorrect for Victoria BC).

**Impact:** The PDF contains errors that the user must catch manually. For a permit-supporting document this is a credibility problem.

---

## Proposed Improvements

### Improvement 1 — Progressive Elaboration with Diagram Checkpoint

**Goal:** Generate only the plan view (top-down) and elevation view (side) diagrams first. Show them to the user and ask for confirmation before proceeding to the full structural pipeline.

#### Implementation

**New workflow gate in `design-orchestrator`:**

```
Stage 0:  intake-normalizer          → design-spec.json
Stage 1:  drawing-generator (EARLY)  → plan-view.svg + elevation.svg  ← CHECKPOINT
          ↓ Show diagrams to user
          ↓ Ask: "Does this match your intent? Correct anything."
          ↓ If corrections → loop back to intake-normalizer with delta
          ↓ If confirmed → proceed
Stage 2:  building-code-validator    → building-code.json
Stage 3:  structural-engine          → structural-model.json
Stage 4:  joinery-designer           → joinery.json
Stage 5:  bracing-system-designer    → bracing.json
Stage 6:  drawing-generator (FULL)   → full drawing set
Stage 7:  document-compiler          → final PDF
```

**Changes required:**

- `design-orchestrator/SKILL.md`: Add checkpoint logic. After Stage 1 completes, output the two SVG diagrams and prompt the user with a structured confirmation message. Do not proceed to Stage 2 until explicit "confirmed" signal is received.

- `drawing-generator/SKILL.md`: Add an `--early-mode` flag (or equivalent JSON parameter `"mode": "early_preview"`) that generates only the plan view and one elevation view without the full detail sheet set. Should complete in under 60 seconds and under 2000 tokens.

- `intake-normalizer/SKILL.md`: Accept a `delta` input in addition to a fresh transcript. When a delta is provided (user corrections after diagram review), merge it with the existing `design-spec.json` rather than starting from scratch.

**Diagram checkpoint prompt template** (to be emitted by orchestrator after Stage 1):

```
Here are your preliminary diagrams:

[PLAN VIEW — top-down]
[ELEVATION VIEW — front face]

Before I run the full structural analysis, please confirm:
1. Does the shape and orientation look right?
2. Is the scale approximately correct?
3. Anything to adjust (height, size, style)?

Reply "confirmed" to proceed, or describe any corrections.
```

---

### Improvement 2 — Claude CLI Subprocess Pattern for Token Reduction

**Goal:** Each pipeline skill should be invoked as a `claude -p` subprocess call via Bash, not as an Agent tool spawn. The main orchestrator session writes input JSON, shells out, reads back output JSON. Each skill runs in its own isolated context window, then exits. The main session's context stays lean.

#### How the Claude CLI works in this context

The Claude CLI supports non-interactive piped execution:

```bash
claude -p "$(cat prompt.txt)" \
  --output-format text \
  --max-turns 1 \
  > output.txt
```

Or with model selection:

```bash
claude -p "$(cat prompt.txt)" \
  --model claude-haiku-4-5-20251001 \
  --output-format text \
  > output.txt
```

This is the key pattern: **use a cheaper/faster model for mechanical pipeline stages** (structural math, JSON formatting, code lookups) and reserve Sonnet/Opus for the interview stage and final document compilation where quality matters.

#### Recommended model assignment per stage

| Stage | Skill | Recommended Model | Rationale |
|-------|-------|-------------------|-----------|
| 0 | intake-normalizer | claude-sonnet-4-6 | Needs language understanding |
| 1 | drawing-generator (early) | claude-haiku-4-5-20251001 | Pure geometry, fast |
| 2 | building-code-validator | claude-haiku-4-5-20251001 | Lookup + formatting |
| 3 | structural-engine | claude-haiku-4-5-20251001 | Arithmetic + JSON |
| 4 | joinery-designer | claude-haiku-4-5-20251001 | Rule lookup + JSON |
| 5 | bracing-system-designer | claude-haiku-4-5-20251001 | Arithmetic + JSON |
| 6 | drawing-generator (full) | claude-haiku-4-5-20251001 | Geometry |
| 7 | document-compiler | claude-sonnet-4-6 | Prose quality matters |

#### Orchestrator bash pattern

Replace Agent tool spawns with this pattern in `design-orchestrator/SKILL.md`:

```bash
# Write the skill prompt to a temp file
cat > /tmp/skill_prompt.txt << 'PROMPT'
You are the structural-engine skill for the garden-structure-designer plugin.
Read the design spec at: /path/to/context/staging/design-spec.json
Produce structural analysis output to: /path/to/context/staging/structural-model.json
[... skill instructions ...]
PROMPT

# Run the skill as a subprocess
claude -p "$(cat /tmp/skill_prompt.txt)" \
  --model claude-haiku-4-5-20251001 \
  --output-format text \
  > /tmp/skill_result.txt 2>&1

# Check result
if [ $? -ne 0 ]; then
  echo "ERROR: structural-engine failed"
  cat /tmp/skill_result.txt
  exit 1
fi

# Continue to next stage
echo "structural-engine complete"
```

**Changes required:**

- `design-orchestrator/SKILL.md`: Rewrite the pipeline execution section to use Bash subprocess calls instead of Agent spawns. Each stage becomes a Bash block. Add error handling and retry logic for each stage.

- Each skill's `SKILL.md`: Ensure skills are written to be fully self-contained when invoked via CLI — they must read all inputs from files and write all outputs to files, with no dependency on the parent session's context.

- Add a `context/staging/` working directory convention (already partially in place) with a clear file manifest so skills know exactly what to read and where to write.

**Expected token reduction:** ~60–75% reduction in main session token consumption. The orchestrator becomes a lightweight coordinator. Each skill's full reasoning is isolated to its own subprocess context and discarded after the output JSON is written.

---

### Improvement 3 — JSON Fact-Check Pass Before PDF Compilation

**Goal:** Before the document-compiler renders the PDF, run a validation pass that cross-references all generated JSON values against a reference table of known-correct values. Flag and correct any discrepancies.

#### What needs fact-checking

The following values are generated by skills and must be validated before entering the PDF:

**Building code values (Victoria BC / BCBC 2024):**

| Parameter | Known Correct Value | Source |
|-----------|--------------------|---------| 
| Ground snow load (Ss), Victoria | 1.1 kPa | NBCC 2020 Appendix C, Table C-2 |
| Frost line depth, Victoria | 450 mm | City of Victoria standard |
| Exposure category, Victoria | B (suburban) | NBCC |
| Seismic Sa(0.2), Victoria | ~1.2g | NBCC Seismic Hazard |
| Wind reference pressure Vref, Victoria | 70 km/h | NBCC |
| Accessory structure permit exemption | < 10 m² | City of Victoria Bylaw |
| P.Eng. stamp requirement | NOT required for <10m² pergola | City of Victoria Building Division |

**CSA O86-24 Western Red Cedar No.1 (reference values):**

| Member | Property | Reference Value |
|--------|----------|----------------|
| 6×6 (140×140 mm) | Fb (bending) | 11.5 MPa |
| 6×6 | Fc (compression) | 8.0 MPa |
| 4×8 (89×184 mm) | Fb | 11.5 MPa |
| 2×6 (38×140 mm) | Fb | 11.5 MPa |
| All WRC | E (modulus) | 10,000 MPa |

**Geometry checks (for a regular hexagon with 10 ft long diagonal):**

| Property | Correct Value |
|----------|--------------|
| Long diagonal | 10.00 ft = 3048 mm |
| Side length | 5.00 ft = 1524 mm |
| Short diagonal (flat-to-flat) | 8.66 ft = 2639 mm |
| Circumradius | 5.00 ft = 1524 mm |
| Inradius | 4.33 ft = 1320 mm |
| Plan area | 6.80 m² |
| Interior angle | 120° |

#### Implementation

**New skill: `fact-checker`** (or add as a sub-step in document-compiler):

Reads all JSON files in `context/staging/`, checks every numeric value that has a known reference, and produces a `fact-check-report.json` listing:
- `PASS` — value matches reference within tolerance
- `WARN` — value is plausible but differs from reference by >10%
- `FAIL` — value is clearly wrong (e.g., wrong units, impossible geometry)
- `UNVERIFIABLE` — no reference data available

**document-compiler** should:
1. Run fact-checker before rendering
2. Block PDF generation if any `FAIL` items exist
3. Include `WARN` items as footnotes in the PDF (not block generation)
4. Correct known-wrong values (e.g., P.Eng. requirement for small pergola) using the reference table

**Reference data storage:** Add a `reference-data/` directory to the plugin:

```
plugin_017xRak7j84FaS9dJ6nRtYcg/
  reference-data/
    bcbc-2024-victoria.json      ← building code lookups
    csa-o86-24-wrc-properties.json  ← wood species properties
    city-of-victoria-bylaws.json    ← local permit rules
    hexagon-geometry.json           ← geometry formulas
```

These JSON files are ground-truth references that the fact-checker reads directly, rather than relying on what the LLM generates from memory.

---

## Summary of File Changes Required

| File | Change Type | Description |
|------|------------|-------------|
| `design-orchestrator/SKILL.md` | Rewrite | Add Stage 1 checkpoint gate; rewrite pipeline as Bash subprocess calls |
| `drawing-generator/SKILL.md` | Extend | Add `early_preview` mode for fast diagram-only output |
| `intake-normalizer/SKILL.md` | Extend | Accept `delta` corrections to existing design-spec.json |
| `document-compiler/SKILL.md` | Extend | Add fact-checker call before PDF render; block on FAIL |
| `reference-data/bcbc-2024-victoria.json` | New file | Ground-truth BC building code values for Victoria |
| `reference-data/csa-o86-24-wrc-properties.json` | New file | WRC timber properties from CSA O86-24 |
| `reference-data/city-of-victoria-bylaws.json` | New file | Permit exemptions, setback rules, local amendments |
| `reference-data/hexagon-geometry.json` | New file | Hexagon geometry formulas and cross-checks |
| `skills/fact-checker/SKILL.md` | New skill | Validates all staging JSON against reference-data |

---

## Additional Issues Identified During Testing

These are bugs and inaccuracies found during the test session that should be fixed regardless of the above improvements:

### Bug: P.Eng. Stamp Incorrectly Required

The pipeline asserted that a Professional Engineer stamp is required for a small backyard pergola in Victoria BC. This is incorrect.

- **Correct rule:** City of Victoria exempts freestanding accessory structures under 10 m² from building permits entirely. This pergola is 6.8 m² — below the threshold.
- **Fix:** Add City of Victoria permit exemption rules to `city-of-victoria-bylaws.json` and have the building-code-validator read them before making permit assertions.

### Bug: "200-page PDF" Scope Creep

The document-compiler generated an extremely detailed document (14 sections, full code compliance matrix, maintenance schedules, etc.) for what is a simple backyard build. The depth should scale with structure complexity and permit requirements.

- **Fix:** Add a `document_detail_level` parameter to `design-spec.json` with values: `sketch` | `homeowner` | `contractor` | `permit`. Default to `homeowner` for exempt structures. Only `permit` level triggers full code compliance sections.

### Bug: Three Hub Options Left Unresolved

The joinery-designer outputted three alternative hub designs without selecting one. This means the structural model has an unresolved critical detail.

- **Fix:** The joinery-designer should select the recommended option based on user's stated aesthetic (timber frame preference → laminated cedar hub) and output a single resolved design. Alternatives can be listed as an appendix.

### Bug: Rafter Spacing Annotation Inconsistency

`design-spec.json` says `spacing_in: 8` (inches) but the structural-model computed 508 mm spacing (≈ 20 inches). These are inconsistent.

- **Fix:** The fact-checker should catch unit/value mismatches between design-spec and structural-model. The intake-normalizer should clarify whether 8-inch spacing means between rafter centres or between rafter edges.

### Enhancement: Standoff Height Default Too Low for Coastal BC

The pipeline defaulted to 75 mm standoff post base height. For Victoria's coastal climate (high rainfall, marine exposure), 100 mm is the appropriate minimum.

- **Fix:** Add a `coastal_climate` flag to the building-code-validator. If `coastal_climate: true`, override default standoff to 100 mm and add a maintenance note about marine hardware.

---

## Acceptance Criteria

The improved plugin is considered complete when:

1. A new pergola design session produces plan + elevation SVG diagrams within the first 3 skill calls, before any structural math runs
2. The orchestrator pauses and asks for user confirmation before proceeding past the diagram checkpoint
3. Each pipeline skill (stages 2–6) runs as a `claude -p` Bash subprocess rather than an Agent spawn
4. The document-compiler refuses to generate a PDF if any `FAIL` items are found by the fact-checker
5. The P.Eng. requirement is not asserted for structures under 10 m² in Victoria BC
6. The hub design is resolved to a single option (not three options) by the joinery-designer
7. Total main-session token consumption for a simple pergola design is under 15,000 tokens

---

*Spec prepared from live Cowork test session — garden-structure-designer plugin v0.1*