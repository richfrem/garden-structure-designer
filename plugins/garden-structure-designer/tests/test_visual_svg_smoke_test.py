from pathlib import Path
import sys
import pytest

sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from visual_svg_smoke_test import sheet_kind, hub_sheet_key, project_iso, detect_brace_float, detect_beam_gap

def test_sheet_kind():
    assert sheet_kind("outputs/blueprint-plan.svg") == "blueprint"
    assert sheet_kind("outputs/drawing-plan-view.svg") == "drawing"

def test_hub_sheet_key():
    assert hub_sheet_key("drawing-isometric-view.svg") == "drawing-isometric"
    assert hub_sheet_key("blueprint-isometric.svg") == "blueprint-isometric"
    assert hub_sheet_key("drawing-perspective-view.svg") == "drawing-perspective"

def test_project_iso():
    x, y = project_iso(0.0, 0.0, 10.0, scale=10.0, cx=500.0, cy=500.0)
    assert x == 500.0
    assert y == 400.0

def test_detect_brace_float():
    struct_valid = {
        "bracing": {"enabled": True},
        "geometry": {
            "joints": {
                "braces": {
                    "endpoints": [{"id": "K1A", "start": [0.0, 0.0, 5.0], "end": [2.0, 0.0, 7.0]}]
                }
            }
        }
    }
    assert detect_brace_float(struct_valid) is None

    struct_float = {
        "bracing": {"enabled": True},
        "geometry": {
            "joints": {
                "braces": {
                    "endpoints": [{"id": "K1A", "start": [0.0, 0.0, 5.0], "end": [0.0, 0.0, 5.0]}]
                }
            }
        }
    }
    res = detect_brace_float(struct_float)
    assert res is not None
    assert res["code"] == "BRACE_FLOAT"

def test_detect_beam_gap():
    struct = {
        "layout": {"inscribed_radius_ft": 5.0, "post_count": 6},
        "geometry": {"spans": {"beam_span_ft": 5.0}}
    }
    assert detect_beam_gap(struct) is None
