import sys
import os
import json
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from compile_package import compile_package

@pytest.fixture
def mock_package_env(tmp_path):
    staging = tmp_path / "context" / "staging"
    staging.mkdir(parents=True)
    outputs = tmp_path / "outputs"
    outputs.mkdir(parents=True)
    img_dir = outputs / "high-resolution-image"
    img_dir.mkdir(parents=True)
    
    # Gate report
    report = {"may_claim_success": True, "summary": "Approved"}
    with open(staging / "drawing-red-team-report.json", "w") as f:
        json.dump(report, f)
        
    # Photorealistic render
    (img_dir / "pergola_render_1.png").write_bytes(b"PNG fake data")
    
    # Sample SVG sheet
    (outputs / "S01-plan-view.svg").write_text('<svg width="100" height="100"><circle cx="50" cy="50" r="40"/></svg>')
    
    # Sample markdown document
    md_content = "# Test Plan\n![Plan View](S01-plan-view.svg)\n![Render](high-resolution-image/pergola_render_1.png)"
    (outputs / "pergola_plan.md").write_text(md_content)
    
    return tmp_path

def test_compile_package_blocked_if_red_team_missing(tmp_path):
    staging = tmp_path / "context" / "staging"
    staging.mkdir(parents=True)
    outputs = tmp_path / "outputs"
    outputs.mkdir(parents=True)
    
    res = compile_package(staging_dir=staging, outputs_dir=outputs, md_filename="pergola_plan.md")
    assert res["status"] == "BLOCKED"
    assert "drawing-red-team-report.json not found" in res["reason"]
    assert (outputs / "COMPILATION_BLOCKED.md").exists()

def test_compile_package_success_and_fallback(mock_package_env):
    staging = mock_package_env / "context" / "staging"
    outputs = mock_package_env / "outputs"
    
    res = compile_package(staging_dir=staging, outputs_dir=outputs, md_filename="pergola_plan.md")
    # Will result in COMPLETE or FALLBACK depending on node / md-to-pdf availability
    assert res["status"] in ("COMPLETE", "FALLBACK")
    assert (outputs / "pergola_plan_embedded.md").exists()
    embedded_text = (outputs / "pergola_plan_embedded.md").read_text()
    assert '<svg' in embedded_text
    assert 'data:image/png;base64,' in embedded_text
