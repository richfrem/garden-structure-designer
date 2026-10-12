"""
test_render_toolchain.py
========================

Phase 0 Task 0.4 Toolchain Verification:
Verifies that all required 3D CAD modeling, OpenCASCADE, and browser rendering
dependencies are installed and importable in the Python environment:
- OCP (OpenCASCADE Python C++ bindings)
- build123d (Parametric CAD modeling kernel)
- playwright (Headless Chromium browser automation)
"""
import pytest


def test_cad_and_browser_toolchain_imports():
    """Verify that OCP, build123d, and playwright are importable with functional modules."""
    import OCP
    from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
    from OCP.HLRAlgo import HLRAlgo_Projector

    assert HLRBRep_Algo is not None
    assert HLRBRep_HLRToShape is not None
    assert HLRAlgo_Projector is not None

    import build123d
    from build123d import BuildPart, Box, Compound

    assert BuildPart is not None
    assert Box is not None
    assert Compound is not None

    import playwright
    from playwright.sync_api import sync_playwright

    assert sync_playwright is not None
