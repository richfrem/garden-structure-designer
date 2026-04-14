# Discovery Plan — 2026-04-14
**Session type:** Greenfield

## Problem Statement
Non-expert users (like DIYers or homeowners) want to build garden structures, but they lack the technical vocabulary and expert timber-framing, structural, and joinery knowledge needed to design them safely. Generalized AI chat interfaces struggle to convert a user's vision into an accurate, buildable plan natively because the required architectural pipeline is too complex for standard conversational prompting.

## Intervention Type
- Primary: Software — new plugin for agentic environments (e.g., Claude Cowork, Antigravity, Copilot CLI, Gemini CLI)
- Software needed: yes

## Stakeholders
- Users: Homeowners trying to design a garden structure (like a pergola), or novice to professional carpenters/builders using the system to accelerate their design process.
- Decision maker: The user running the plugin
- Affected parties: The builder executing the generated plans

## Success Criteria
The plugin must produce a high-quality PDF design package that:
1. Achieves conceptual alignment with the user's vision via accurate top and side views.
2. Contains architecturally and engineering-sound dimensions and load-bearing logic, prioritizing physics over aesthetics.
3. Provides detailed assembly instructions and a cut list (pieces of wood, materials, joinery) that a competent builder can execute flawlessly.

## Must-Have Requirements
1. **Interactive Vision Extraction:** A dedicated sub-agent must ask structured, non-technical questions and accept inspiration images to capture user intent.
2. **Structural Translation:** The system must process this intent using a multi-step pipeline (structural engine, joinery designer) to ensure real-world buildability.
3. **Professional Output Generator:** Output a cohesive PDF with build-ready plans, structural notes, materials, and step-by-step instructions.
4. **Platform Agnostic Plugin Structure:** Must be installable and usable via universal agentic environments.

## Constraints and Rules
1. **Local Building Code Aware:** The interactive designer sub-agent must explicitly ask the user about their local building jurisdiction constraints (e.g., BC Building Code) to apply proper wind/snow loads.
2. **Safety First:** Aesthetic choices must never override load-bearing or structural necessities.
3. **Strict Modularity:** Must be built using the `create-skill`, `create-sub-agent`, and `create-plugin` meta-skills to ensure repeatable outputs.

## Open Questions
- What specific joinery types (e.g., mortise and tenon vs. mechanical fastners) should be supported out-of-the-box in version 1?
- How will the precise orthographic drawings (plan and elevation views) be rendered into the PDF?
