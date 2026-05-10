#!/usr/bin/env python3
"""
generate_quality_dashboard.py
=====================================
Purpose:
    Core logic for generate_quality_dashboard.py functionality within garden-structure-designer pipeline.
Layer: Execution
"""
import json
import os
from pathlib import Path

def safe_load(path, default=None):
    if default is None: default = {}
    p = Path(path)
    if p.exists():
        try:
            with open(p) as f: return json.load(f)
        except Exception:
            return default
    return default

def main():
    import sys
    sys.path.append(str(Path(__file__).parent.resolve()))
    from path_utils import staging_dir, outputs_dir
    
    stage_dir = staging_dir()
    out_dir = outputs_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    
    repair = safe_load(stage_dir / "repair-report.json", {"status": "NONE", "attempts": []})
    physics = safe_load(stage_dir / "physics-validation-report.json", {"status": "UNKNOWN", "checks": []})
    learning = safe_load(stage_dir / "learning-registry.json", {"active_lessons": []})
    model = safe_load(stage_dir / "structural-model.json", {})
    evidence = safe_load(stage_dir / "evidence-registry.json", {"evidence": []})
    drift = safe_load(stage_dir / "drift_report.json", {"failed_axes": []})
    red_team = safe_load(stage_dir / "drawing-red-team-report.json", {})
    content_report = safe_load(stage_dir / "drawing-content-report.json", {})
    
    overall_status = "COMPLETED"
    if repair.get("status") in ["FAIL", "BLOCKED"] or drift.get("failed_axes"):
        overall_status = "BLOCKED / FAILED"

    # Content validation failure always overrides to BLOCKED — checked first
    content_status = content_report.get("status", "MISSING")
    if content_status == "FAIL":
        overall_status = "BLOCKED / FAILED"
    elif content_status == "MISSING" and overall_status == "COMPLETED":
        overall_status = "PARTIAL — drawing content report missing"

    # Red-team state checked after content (content failure is more severe)
    red_team_status = red_team.get("status", "MISSING")
    red_team_may_claim = red_team.get("may_claim_success", False)
    if red_team_status == "MISSING" or not red_team_may_claim:
        if overall_status == "COMPLETED":
            overall_status = "PARTIAL — drawing red-team not approved"
        
    repair_str = "None"
    if repair.get("attempts"):
        repair_str = "\n".join([f"- Attempt {a['attempt']}: {a['repair_stage']} for {a['failure_axis']} -> {a['validation_status']}" for a in repair["attempts"]])
        
    ev_str = "None"
    if evidence.get("evidence"):
        ev_str = "\n".join([f"- {e['evidence_id']}: {e['claim']} -> {e['artifact']}" for e in evidence["evidence"]])
        
    physics_checks = "\n".join([f"- {c['name']}: {c['status']} (Val: {c['value']}, Lim: {c['limit']})" for c in physics.get("checks", [])])
    if not physics_checks: physics_checks = "- No checks executed."

    # Per-sheet content validation summary
    content_files = content_report.get("files", [])
    if content_files:
        content_rows = []
        for cf in content_files:
            icon = "✅" if cf.get("status") == "PASS" else "❌"
            codes = ", ".join(cf.get("failure_codes", [])) or "none"
            content_rows.append(f"- {icon} `{cf['file']}`: {cf.get('status','?')} — codes: {codes}")
        content_sheet_str = "\n".join(content_rows)
    else:
        content_sheet_str = "- No content-validation report found. Run run_drawing_red_team.py."

    content = f"""# Garden Structure Designer Quality Dashboard

## Run Status
- Overall status: {overall_status}
- Physics status: {physics.get("status", "UNKNOWN")}
- Drawing content validation: {content_status}
- Drawing red-team review: {red_team_status}
- May claim success: {str(red_team_may_claim).lower()}
- Last updated: Auto-generated

## Drawing Red-Team Status
- Reviewer: {red_team.get("reviewer", "N/A")}
- Status: {red_team_status}
- May claim success: {str(red_team_may_claim).lower()}
- Summary: {red_team.get("summary", "No red-team report found. Run run_drawing_red_team.py before claiming PASS.")}

## Drawing Content Validation (Stage 5.75)
{content_sheet_str}

## Physics Validations
{physics_checks}

## Repair Attempts
{repair_str}

## Learning / Self-Healing
- Lessons available: {len(learning.get("active_lessons", []))}
- Active failures: {len(drift.get("failed_axes", []))}

## Evidence IDs
{ev_str}
"""
    with open(out_dir / "quality-dashboard.md", "w") as f:
        f.write(content)
        
    with open(out_dir / "run-insights.json", "w") as f:
        json.dump({"status": overall_status, "physics": physics.get("status")}, f, indent=2)
        
    print("Dynamic quality dashboard generated.")

if __name__ == "__main__":
    main()
