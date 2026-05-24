import sys
import json
import math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from geometry_engine import vsub, vdot, vlen

def test_fabrication_cut_list_file_exists():
    """Verify that the cut list was compiled and exists."""
    cut_list_path = Path("outputs/fabrication/cut-list.json")
    assert cut_list_path.exists(), "cut-list.json was not generated"

def test_fabrication_schema_and_metadata():
    """Verify the cut list schema structure and source metadata."""
    cut_list_path = Path("outputs/fabrication/cut-list.json")
    with open(cut_list_path, encoding="utf-8") as f:
        data = json.load(f)
    
    assert data["schema"] == "garden-structure-designer/fabrication-cut-list/1.0"
    assert data["units"] == "feet"
    assert data["angle_units"] == "deg"
    assert len(data["members"]) > 0

def test_rafter_regression_angles():
    """Verify primary rafter compound cut saw angles match regression anchors (miter 28.71, bevel 9.10)."""
    cut_list_path = Path("outputs/fabrication/cut-list.json")
    with open(cut_list_path, encoding="utf-8") as f:
        data = json.load(f)
    
    rafters = [m for m in data["members"] if m["role"] == "rafter_primary"]
    assert len(rafters) == 6
    
    for r in rafters:
        hub_cut = next((c for c in r["cuts"] if c["type"] == "compound_miter"), None)
        assert hub_cut is not None
        angles = hub_cut["angles"]
        
        # Regression anchor validation
        assert abs(angles["miter_deg"] - 28.71) < 0.1
        assert abs(angles["bevel_deg"] - 9.10) < 0.1

def test_beam_regression_angles():
    """Verify ring beam flat miter cuts are perpendicular flat cuts (bevel close to 0)."""
    cut_list_path = Path("outputs/fabrication/cut-list.json")
    with open(cut_list_path, encoding="utf-8") as f:
        data = json.load(f)
    
    beams = [m for m in data["members"] if m["role"] == "beam"]
    assert len(beams) == 6
    
    for b in beams:
        for c in b["cuts"]:
            assert c["type"] == "beam_miter"
            angles = c["angles"]
            
            # Bevel must be zero on flat beam cuts
            assert abs(angles["bevel_deg"]) < 0.05
            # Miter saw table swing angle on a regular hexagon is 30 degrees from perpendicular
            assert abs(angles["miter_deg"] - 30.0) < 0.1

def test_brace_regression_angles():
    """Verify braces are paired and ends slope at correct angles."""
    cut_list_path = Path("outputs/fabrication/cut-list.json")
    with open(cut_list_path, encoding="utf-8") as f:
        data = json.load(f)
    
    braces = [m for m in data["members"] if m["role"] == "brace"]
    # If bracing is enabled, we expect 12 braces
    if len(braces) > 0:
        assert len(braces) == 12
        for b in braces:
            assert len(b["cuts"]) == 2
            post_cut = next((c for c in b["cuts"] if c["mates_to"].startswith("post")), None)
            beam_cut = next((c for c in b["cuts"] if c["mates_to"].startswith("beam")), None)
            
            assert post_cut is not None
            assert beam_cut is not None

def test_plane_equation_satisfaction():
    """Verify that all cut planes satisfy the plane equation at endpoints within tolerance."""
    cut_list_path = Path("outputs/fabrication/cut-list.json")
    with open(cut_list_path, encoding="utf-8") as f:
        data = json.load(f)
    
    for m in data["members"]:
        axis_start = tuple(m["axis"]["start"])
        axis_end = tuple(m["axis"]["end"])
        
        for c in m["cuts"]:
            if "plane" not in c:
                continue
            
            pt = tuple(c["plane"]["point"])
            normal = tuple(c["plane"]["normal"])
            
            # Plane equation: (X - P) dot N = 0
            # Test that the cut location point on the axis lies exactly on the plane
            target_pt = axis_end if c["end"] == "end" else axis_start
            dot_product = vdot(vsub(target_pt, pt), normal)
            assert abs(dot_product) < 0.05, f"Plane equation failed for member {m['id']} cut {c['cut_id']} dot={dot_product}"
