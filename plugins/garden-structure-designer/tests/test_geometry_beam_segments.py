"""C1: the geometry producer emits exactly N beam_segments (id, i0, i1) closing the polygon."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
sys.path.insert(0, str(PLUGIN_ROOT))
from geometry_engine import compute_from_structure  # type: ignore[import]  # noqa: E402
from tests.test_geometry_engine import STRUCTURE_SEED  # type: ignore[import]  # noqa: E402


@pytest.mark.parametrize("sides", [5, 6, 8])
def test_beam_segments_cover_every_polygon_edge(tmp_path, sides):
    seed = copy.deepcopy(STRUCTURE_SEED)
    seed["structure"]["sides"] = sides
    seed["layout"]["post_count"] = sides
    seed["roof"]["primary_rafters"]["count"] = sides
    path = tmp_path / "structure.json"
    path.write_text(json.dumps(seed))
    segments = compute_from_structure(str(path))["geometry"]["joints"]["layout"]["beam_segments"]
    assert segments == [{"id": f"B{i + 1}", "i0": i, "i1": (i + 1) % sides} for i in range(sides)]
