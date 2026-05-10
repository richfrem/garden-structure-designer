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
    
    overall_status = "COMPLETED"
    if repair.get("status") in ["FAIL", "BLOCKED"] or drift.get("failed_axes"):
        overall_status = "BLOCKED / FAILED"
        
    repair_str = "None"
    if repair.get("attempts"):
        repair_str = "\n".join([f"- Attempt {a['attempt']}: {a['repair_stage']} for {a['failure_axis']} -> {a['validation_status']}" for a in repair["attempts"]])
        
    ev_str = "None"
    if evidence.get("evidence"):
        ev_str = "\n".join([f"- {e['evidence_id']}: {e['claim']} -> {e['artifact']}" for e in evidence["evidence"]])
        
    physics_checks = "\n".join([f"- {c['name']}: {c['status']} (Val: {c['value']}, Lim: {c['limit']})" for c in physics.get("checks", [])])
    if not physics_checks: physics_checks = "- No checks executed."

    content = f"""# Garden Structure Designer Quality Dashboard

## Run Status
- Overall status: {overall_status}
- Physics status: {physics.get("status", "UNKNOWN")}
- Last updated: Auto-generated

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
