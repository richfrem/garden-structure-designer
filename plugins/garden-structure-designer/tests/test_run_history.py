from pathlib import Path
import sys
import tempfile
import json
import pytest

sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from run_history import record_run, get_history, recent_failures, should_halt, repeated_identical_artifact

def test_run_history_lifecycle(monkeypatch, tmp_path):
    hist_file = tmp_path / "test-history.jsonl"
    monkeypatch.setattr("run_history.get_history_file", lambda: hist_file)
    
    # Empty history
    assert get_history() == []
    assert not should_halt("render_drawings.py", "svg_error")
    
    # Record 3 failures
    record_run("render_drawings.py", ["--model", "test"], 1, "svg_error")
    record_run("render_drawings.py", ["--model", "test"], 1, "svg_error")
    assert not should_halt("render_drawings.py", "svg_error", max_repeats=3)
    
    record_run("render_drawings.py", ["--model", "test"], 1, "svg_error")
    assert should_halt("render_drawings.py", "svg_error", max_repeats=3)
    
    # Check recent failures
    fails = recent_failures("render_drawings.py", "svg_error")
    assert len(fails) == 3
