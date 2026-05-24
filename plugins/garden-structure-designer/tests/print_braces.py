import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from cad_scene import build_structure_scene

MODEL = {
    "members": {"posts": {"quantity": 6}},
    "dimensions": {"max_diagonal_ft": 10.0},
}
CALCS = {
    "total_height": {"post_ft": 8.33, "beam_depth_ft": 1.0},
    "roof_rise":    {"rise_ft": 1.6},
}

scene = build_structure_scene(MODEL, CALCS)
braces = [s for s in scene.solids if s.role == "brace"]
for b in braces:
    print(f"{b.tag}: p0={b.p0}, p1={b.p1}")
