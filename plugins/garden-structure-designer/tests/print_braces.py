import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from cad_scene import build_structure_scene

from test_geometry_engine import STRUCTURE_SEED
from geometry_engine import compute_from_structure
import copy
import json

s_copy = copy.deepcopy(STRUCTURE_SEED)
compute_from_structure(s_copy)

scene = build_structure_scene(s_copy)
braces = [s for s in scene.solids if s.role == "brace"]
for b in braces:
    print(f"{b.tag}: p0={b.p0}, p1={b.p1}")
