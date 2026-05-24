
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from render_drawings import generate_svg

def test_svg_generation(tmp_path):
    model = {"members": {"posts": {"quantity": 6, "spanDistance_ft": 5.0}}}
    calcs = {"svg_coordinates": {"width_px": 800, "height_px": 600}}
    out = tmp_path / "plan.svg"
    generate_svg("drawing-plan-view.svg", model, calcs, str(out))
    content = out.read_text()
    assert content.count('data-role="post"') == 6
    assert content.count('data-role="beam"') == 6
    assert content.count('data-role="rafter"') == 18
    assert 'SAW_SETTINGS' in content
    assert 'COORDINATE MAP' in content
