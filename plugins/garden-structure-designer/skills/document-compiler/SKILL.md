---
name: document-compiler
description: Assembles all outputs into a structured document and formats for PDF export. Ensures sections are complete, ordered matching the Option A Architectural Layout constraint.
allowed-tools: Read, Write, Bash
---

## Expected Inputs
All models inside `context/staging/`.
Visuals from `drawing-generator`.

## Core Responsibilities
1. Construct the document adhering to the PDF Layout requirements (elevations & diagrams first, timber tables, fastener tables).
2. Generate intermediate format (e.g. Markdown or LaTeX) and execute external tool if necessary to produce the final .pdf binary in `outputs/`.
