---
name: document-compiler
description: Assembles all outputs into a structured document and formats for PDF export. Ensures sections are complete, ordered matching the Option A Architectural Layout constraint.
allowed-tools: Read, Write, Bash
---

## Expected Inputs
All models inside `context/staging/`.
Visuals from `drawing-generator` (Plan, Elevation, Perspective, Isometric).
Technical cut-sheets from `shop-blueprint-generator` (Dimensioned orthographics and isolated joinery components).

## Core Responsibilities
1. Construct the document adhering to the PDF Layout requirements (architectural diagrams and 3D visual layouts first, then the detailed technical shop blueprints, followed by timber cut-list tables and fastener tables).
2. Generate intermediate format (e.g. Markdown or LaTeX) and execute external tool if necessary to produce the final .pdf binary in `outputs/`.
