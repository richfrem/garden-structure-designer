#!/usr/bin/env python3
"""
run_obstacle_triage.py (CLI)
=====================================

Purpose:
    run_obstacle_triage.py =====================================

Layer: Execution

Usage Examples:
    python run_obstacle_triage.py [args]

Supported Object Types:
    JSON, SVG, Markdown

CLI Arguments:
    Varies per script, typically input file paths.

Input Files:
    context/staging/ *.json outputs/ *.svg

Output:
    Validation codes (0 or 1), generated JSON or SVG files.

Key Functions:
    Refer to module docstring or inner functions.

Script Dependencies:
    Standard library json, os, sys, math, hashlib, etc.

Consumed by:
    design-orchestrator, various skills in the pipeline.
"""
import json
import os
import sys
from pathlib import Path

def main():
    sys.path.append(str(Path(__file__).parent.resolve()))
    from path_utils import staging_dir, outputs_dir
    
    _STAGING = staging_dir()
    _OUTPUTS = outputs_dir()
    
    # Check for path splits
    plugin_staging = Path("plugins/garden-structure-designer/context/staging")
    root_staging = Path("context/staging")
    
    classifications = []
    evidence = []
    
    has_path_split = False
    if plugin_staging.exists() and root_staging.exists() and plugin_staging.resolve() != root_staging.resolve():
        if (plugin_staging / "structure.json").exists() and (root_staging / "structure.json").exists():
            classifications.append("PATH_SPLIT")
            evidence.append("structure.json found in both context/staging and plugin staging")
            has_path_split = True
            
    # Check for missing staging artifacts
    missing_artifacts = []
    for artifact in ["structure.json"]:
        if not (_STAGING / artifact).exists():
            missing_artifacts.append(artifact)
            
    if missing_artifacts:
        classifications.append("MISSING_STAGING_ARTIFACT")
        evidence.append(f"Missing staging artifacts in {_STAGING}: {', '.join(missing_artifacts)}")
        
    # Check for stale dashboard or conflicting red-team report
    red_team_path = _STAGING / "drawing-red-team-report.json"
    dashboard_path = _OUTPUTS / "quality-dashboard.md"
    
    red_team_may_claim = False
    if red_team_path.exists():
        try:
            with open(red_team_path) as f:
                r = json.load(f)
                red_team_may_claim = bool(r.get("may_claim_success"))
        except Exception:
            pass
            
    if dashboard_path.exists() and not red_team_may_claim:
        content = dashboard_path.read_text()
        if "Overall status: COMPLETED" in content:
            classifications.append("DASHBOARD_STALE_OR_WRONG_PATH")
            evidence.append("quality-dashboard.md says COMPLETED while red-team report does not approve (or is missing)")
            
    # Check for toy renderer placeholder output
    # If SVGs exist and are very small (< 10KB) or have no title block
    svgs = list(_OUTPUTS.glob("*.svg"))
    if svgs and not missing_artifacts and red_team_path.exists() and not red_team_may_claim:
        # Check if they are just placeholders
        placeholder = False
        for svg in svgs:
            if svg.stat().st_size < 3000:
                placeholder = True
                break
        if placeholder:
            classifications.append("RENDERER_PLACEHOLDER_OUTPUT")
            evidence.append("Generated SVGs are extremely small (likely placeholder stubs)")
            
    if not classifications:
        classifications.append("UNKNOWN_OBSTACLE")
        evidence.append("No specific obstacle pattern matched")
        
    # Recommend next action
    if "PATH_SPLIT" in classifications:
        next_action = "FIX_PATHS_FIRST"
    elif "MISSING_STAGING_ARTIFACT" in classifications:
        next_action = "RERUN_REPORTS_FIRST"
    elif "DASHBOARD_STALE_OR_WRONG_PATH" in classifications:
        next_action = "RERUN_REPORTS_FIRST"
    elif "RENDERER_PLACEHOLDER_OUTPUT" in classifications:
        next_action = "FIX_RENDERER_FIRST"
    else:
        next_action = "BLOCK_AND_REPORT"
        
    report = {
        "schema": "garden-structure-designer/obstacle-triage-report/1.0",
        "status": "ACTION_REQUIRED",
        "failure_classification": classifications,
        "active_staging_path": str(_STAGING),
        "conflicting_staging_paths": [str(plugin_staging)] if has_path_split else [],
        "evidence": evidence,
        "recommended_next_action": next_action,
        "do_not_do": [
            "Do not weaken validators",
            "Do not claim PASS",
            "Do not compile PDF"
        ]
    }
    
    os.makedirs(str(_STAGING), exist_ok=True)
    with open(_STAGING / "obstacle-triage-report.json", "w") as f:
        json.dump(report, f, indent=2)
        
    md_content = f"""# Obstacle Triage Report

**Status:** {report['status']}
**Recommended Next Action:** `{report['recommended_next_action']}`

## Failure Classifications
"""
    for cls in classifications:
        md_content += f"- **{cls}**\n"
        
    md_content += "\n## Evidence\n"
    for e in evidence:
        md_content += f"- {e}\n"
        
    md_content += "\n## Constraints\n"
    for d in report['do_not_do']:
        md_content += f"- 🛑 {d}\n"
        
    os.makedirs(str(_OUTPUTS), exist_ok=True)
    with open(_OUTPUTS / "obstacle-triage-report.md", "w") as f:
        f.write(md_content)
        
    print(f"Obstacle triage complete. Action required: {next_action}")
    for c in classifications:
        print(f" - {c}")
        
if __name__ == "__main__":
    main()
