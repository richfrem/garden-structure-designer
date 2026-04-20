## claude

*The following improvements are grounded in firsthand failures observed while building the Saanich 10-ft hexagonal pavilion construction set — specifically the compound-cut angle error (wrong Miter/Bevel values shipped in SB01 and design-spec.json, caught by Gemini's review), the SVG XML validity failure (double-hyphen in comments broke D02), and the fragile manual redraw required when pitch changed from 6:12 to 4:12.*

### C1. Embed Verified Compound Cut Formulas in `structural-engine` and `shop-blueprint-generator`

The current `structural-engine` SKILL.md says "calculate minimum safe timber dimensions" but gives no formula for compound miter/bevel angles at polygon hubs. This forces agents to derive the math from scratch each session — and the formula is non-obvious enough that I got it wrong: I used the raw pitch angle (18.43°) as the miter setting instead of the true compound formula.

**Proposed Fix:** Add a `## Compound Cut Reference` section to `structural-engine/SKILL.md` with the canonical formula:
```
Miter = arctan(cos(pitch_deg) × tan(plan_half_angle_deg))
Bevel = arcsin(sin(pitch_deg) × sin(plan_half_angle_deg))
```
Include a worked example for hexagonal (plan_half_angle=30°) at 4:12 pitch (18.43°) giving Miter=28.7°, Bevel=9.1°. The `shop-blueprint-generator` should be instructed to copy these values from `structural-model.json`, never derive them independently.

This pairs with Gemini's `geometry_engine.py` proposal — the script can produce the JSON, and both skills read it. Neither should do mental math.

---

### C2. XML Validity Rules Must Be a Hard Gate in `drawing-generator` and `shop-blueprint-generator`

During this session, D02-elevation-face.svg silently failed to render in all viewers because an XML comment contained `----` (four hyphens, illegal in XML). The skill instructions mention XML escaping for text nodes (`&amp;`, `&quot;`, etc.) but say nothing about comment syntax.

**Proposed Fix:** Add an explicit pre-flight checklist to both `drawing-generator/SKILL.md` and `shop-blueprint-generator/SKILL.md`:
```
## SVG XML Hard Rules
- Comments: <!-- --> only. Never use -- inside a comment body.
- Attribute values: always double-quoted.
- All text nodes: escape & " ' < > per XML spec.
- Validate with: python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.svg')"
```
Make this a mandatory step before writing any SVG. A broken SVG is worse than no SVG.

---

### C3. Coordinate-Derived SVG Geometry from `structural-model.json`

When pitch changed from 6:12 to 4:12, I had to manually recalculate pixel positions (hub apex Y, post top Y, beam soffit Y, etc.) and rewrite D02, D03, and D05 by hand. This is fragile, slow, and error-prone.

**Proposed Fix:** `drawing-generator` should derive all pixel coordinates from a parametric formula block keyed to values in `structural-model.json` (scale, post height, pitch, overhang). Document a standard coordinate mapping table at the top of each generated SVG as an XML comment block — then geometry updates require only one JSON edit, not a full SVG rewrite.

This is a process improvement, not a code change. Add a `## Coordinate Derivation Protocol` section to `drawing-generator/SKILL.md` with the mapping formula and require agents to show their derivation before emitting SVG paths.

---

### C4. Add a Builder Documents Stage to the Orchestrator

The current `design-orchestrator` pipeline ends at document-compiler (PDF). The parallel Gemini run on this same project produced `budget-estimate.md`, `assembly-guide.md`, and `lumber-purchase-list.md` — documents that Richard found immediately useful and that the Claude pipeline entirely missed.

**Proposed Fix:** Add a Step 9 to `design-orchestrator.md`:
> Invoke `builder-docs-generator` (new skill) to produce: `outputs/budget-estimate.md`, `outputs/lumber-purchase-list.md`, `outputs/assembly-guide.md`. Source material costs from `builder-contacts/` profiles and lumber board-foot totals from `structural-model.json`.

This makes the plugin output immediately usable for a builder quote, not just a PDF for an engineer.

---

### C5. Incremental Re-render — Only Redraw Affected Sheets

Currently, any change to a single dimension triggers a full redraw of all sheets. The `document-compiler` skill has a `manifest.json` but no concept of dirty/clean state per drawing.

**Proposed Fix:** Add a `checksum` field to `manifest.json` keyed to the source `structural-model.json` hash that each drawing was generated from. The `drawing-generator` should skip (and log "unchanged") any sheet whose checksum still matches. This pairs with Gemini's staging-lock proposal — once locked, sheets derived from that lock should not be re-rendered unless the lock is broken.

---

### C6. Validation-Agent Fallback When `gemini-cli` Is Unavailable

Step 5 and Step 7 of the design-orchestrator both require a `gemini-cli` sub-agent for validation. If `gemini-cli` returns 429 (capacity exhausted) or is not installed, the pipeline silently hangs or fails with an unhelpful error. This happened in this session.

**Proposed Fix:** Document a Claude-native fallback validation path in `validation-agent.md`:
> If `gemini-cli` is unavailable or returns non-zero exit code, Claude performs a self-review pass: re-read `structural-model.json` and each SVG, verify all labeled dimensions against JSON values, report any mismatches in `context/staging/validation-report.json`. Flag the report as `"reviewer": "claude-self"` so the human knows it was not cross-model verified.

This keeps the pipeline moving while making the reduced confidence level transparent.

## gemini

### 1. Geometric Hardening (Zero-Hallucination Drafting)
Claude is exceptional at drafting professional-grade SVGs but, as discovered in the recent 4:12 Hexagon session, can hallucinate compound miter/bevel angles.
*   **Proposed Fix:** Implement a unified `scripts/geometry_engine.py`. This script will be the **Sole Source of Truth** for all mathematical calculations (pitch angles, rise, compound cuts).
*   **Enforcement:** Modify `shop-blueprint-generator` instructions to **forbid** mental calculation. The agent MUST run the script and pipe the JSON output directly into SVG `<text>` nodes.

### 2. Dual-Channel Multimodal QA
Current validation relies heavily on text-based XML parsing. We should move to a dual-channel gate:
*   **Static XML Check:** Parsing the SVG XML to verify that dimension labels match the `structural-model.json` precisely.
*   **Multimodal Vision Check:** Render SVGs to PNG and use **Gemini 1.5 Pro** to perform an "Isolated Vision Proxy" audit. This ensures the visual topology (e.g., exactly 6 posts) matches the mathematical topology.

### 3. Handoff Protocol & Drift Correction
To prevent "drift" between the structural engine and the final drawing set:
*   **Staging Locks:** Implement a `LOCKED` status in `context/staging/structural-model.json`. 
*   **Automated Feedback Loop:** If the `validation-agent` detects a dimensional mismatch, it should generate a `drift_report.json` and automatically re-trigger the rendering skill with the corrective delta, creating a self-healing loop before human review.

### 4. Integration with Gemini CLI
Standardize all high-reasoning validation gates to run via `gemini-cli --model gemini-1.5-pro`. This ensures that even if the primary orchestrator is running on a faster/cheaper model (like Flash), the final engineering audit is always performed by a model with maximum reasoning and multimodal capability.

### 5. Architectural L4 Alignment (Folder-per-Agent)
Currently, agents are stored as flat files in `agents/`. To align with the modular L4 plugin architecture (as noted in `CLAUDE.md`), we should move to a folder-per-agent structure (e.g., `agents/design-orchestrator/AGENT.md`). This allows each agent to carry its own local references and evaluation suites.

### 6. Session Context Flushing
Large gazebo/pergola design sessions can lead to significant token bloat. I propose a **"Checkpointing & Flush"** protocol: once a phase (e.g., Structural Engineering) is validated and `LOCKED`, the orchestrator should summarize the state and flush the raw thought-process from the current context to maintain high performance in the subsequent Drafting phase.
