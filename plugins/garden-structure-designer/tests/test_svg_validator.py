from pathlib import Path
import sys
import pytest

sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from svg_validator import validate

def test_svg_validator_xml_error(tmp_path):
    bad_svg = tmp_path / "bad.svg"
    bad_svg.write_text("<svg><unclosed></svg>")
    model_path = tmp_path / "model.json"
    model_path.write_text('{"roof": {"pitch": "4:12"}, "layout": {"post_count": 6}}')
    
    errors = validate(str(bad_svg), str(model_path))
    assert any("XML_INVALID" in e for e in errors)

def test_svg_validator_pitch_error(tmp_path):
    svg = tmp_path / "test.svg"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg"><g data-role="post"/><g data-role="post"/><g data-role="post"/><g data-role="post"/><g data-role="post"/><g data-role="post"/><text>5:12 pitch</text></svg>')
    model_path = tmp_path / "model.json"
    model_path.write_text('{"roof": {"pitch": "4:12"}, "layout": {"post_count": 6}}')
    
    errors = validate(str(svg), str(model_path))
    assert any("MISSING_PITCH_LABEL" in e for e in errors)
