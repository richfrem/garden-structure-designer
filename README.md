# 🏡 Garden Structure Designer (Agent Plugin)

> **Translate your backyard vision into build-ready architectural reality without needing an engineering degree.**

The **Garden Structure Designer** is a modular, AI-native plugin built for advanced agentic environments (like Claude Cowork, Antigravity, and Gemini CLI). It acts as your personal master builder and timber framer—taking hazy, non-technical descriptions of pergolas, gazebos, or pavilions and translating them into structurally sound, permit-ready construction PDF plans.

---

## 🎯 Target Audience
- **Homeowners & Novice DIYers:** You know what you want it to look like, but you don't know the span mathematics to guarantee it won't collapse under winter snow.
- **Professional Carpenters & Builders:** You want a rapid way to generate professional intake documents, accurate visual references, and precise cut-lists for your clients while offloading the repetitive drafting work.

---

## 🚀 The Guided Discovery Process

Generalized AI struggles to design structures reliably because the required architectural pipeline is too complex for a single prompt. This plugin solves that by encapsulating an entire **Multi-Agent Design Firm**:

1. **Vision Alignment (`Interactive-Designer`)**: The agent interviews you. You don't need CAD software. Just upload inspiration images and answer simple questions about the size and style.
2. **Structural Translation (`Structural-Engine & Code-Validator`)**: You provide your jurisdiction (e.g., British Columbia). The engine natively runs your design against local building code constraints, mapping required wind and snow load capacities to safe post/beam thicknesses. *(Safety and physics override aesthetics 100% of the time).*
3. **Joinery & Bracing**: Choose between traditional mortise-and-tenon timber framing or modern mechanical fasteners (like Simpson Strong-Ties). The system automatically computes the anti-racking brace geometry.
4. **Professional Handoff**: The orchestration layer compiles your inputs and logic into a final blueprint.

---

## 📑 What You Get (The Outputs)

The ultimate deliverable is a comprehensive **Architectural & Structural Construction Packet (PDF)** matching professional timber-framing standards.

**Output features include:**
- **Orthographic Projections:** Clear top-down plan views and side elevation views.
- **Detailed Assembly:** Linear, easy-to-follow step-by-step assembly workflows.
- **Cut-Lists:** Precise timber schedules, exact board dimensions, and required hardware/fastener inventories.
- **Joinery Diagrams:** Exploded or detailed maps for connections, post plans, and knee-bracing logic.

*(Example outputs match the structural depth and clarity of professional 30x24 Timber Frame Cabin blueprints, ensuring a builder can start cutting wood immediately).*

---

## 🏗️ Under the Hood (Architecture)

Built using strict separation-of-concerns, this plugin is completely loosely coupled and self-contained.

### Sub-Agents
- `interactive-designer`: Conducts the user interview and captures the vision.
- `design-orchestrator`: Pipeline controller ensuring sequential execution of design components.
- `validation-agent`: A Red-Team reviewer that critiques physics calculations before document compilation.

### Specialized Skills
- `intake-normalizer`: Converts conversational text into strict JSON parameters.
- `building-code-validator`: Maps regions to building code physics constraints.
- `structural-engine`: Computes timber span mathematics.
- `joinery-designer` & `bracing-system-designer`: Assigns appropriate structural connections.
- `drawing-generator` & `document-compiler`: Emits visual SVG/PNG representations inside a formatted Markdown/PDF document.

---

### Installation

This plugin adheres to strict Agentic OS boundaries and requires zero external framework dependencies natively.

```bash
uvx --from git+https://github.com/richfrem/agent-plugins-skills plugin-add richfrem/garden-structure-designer
```

### Claude Code Installation

If you are using Claude Code directly, you can install via the plugin marketplace:

```bash
# Add this repository to your known marketplaces
/plugin marketplace add richfrem/garden-structure-designer

# Open the interactive TUI to browse, discover, and install plugins
/plugin

# Or install the specific plugin directly
/plugin install garden-structure-designer
```
