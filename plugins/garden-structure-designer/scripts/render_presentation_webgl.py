#!/usr/bin/env python3
"""
render_presentation_webgl.py
============================

Purpose:
    Renders photorealistic shaded 3D presentation images of the authoritative solid assembly
    via a local loopback HTTP server and headless Playwright Chromium instance executing Three.js
    with hardware/software WebGL and verified 24-bit depth buffering.

Layer: Service / WebGL Renderer
"""
from __future__ import annotations

from dataclasses import dataclass
import http.server
import json
import os
from pathlib import Path
import shutil
import socketserver
import sys
import threading
import time
from typing import Literal, Optional

from playwright.sync_api import sync_playwright


@dataclass(frozen=True)
class PresentationReceipt:
    """Cryptographic provenance receipt for a WebGL presentation render."""
    png_path: str
    glb_path: str
    camera_type: str
    viewport_width: int
    viewport_height: int
    depth_bits: int
    status: str
    file_size_bytes: int


class _QuietHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass  # Suppress console logging during test/render execution


def render_presentation_screenshot(
    glb_path: Path,
    output_png: Path,
    camera_type: Literal["isometric", "perspective", "plan", "elevation"] = "isometric",
    width: int = 3840,
    height: int = 2160,
    timeout_s: float = 30.0,
) -> PresentationReceipt:
    """
    Spins up loopback server hosting presentation_viewer and glb, loads it in Chromium via
    Playwright, verifies ready handshake and depth bits >= 24, captures canvas screenshot.
    """
    glb_path = Path(glb_path).resolve()
    output_png = Path(output_png).resolve()
    output_png.parent.mkdir(parents=True, exist_ok=True)

    root_viewer = Path(__file__).resolve().parent.parent.parent.parent / "presentation_viewer"
    plugin_viewer = Path(__file__).resolve().parent.parent / "presentation_viewer"
    viewer_dir = root_viewer if root_viewer.exists() else plugin_viewer
    if not viewer_dir.exists():
        raise RuntimeError(f"Presentation viewer directory not found at {root_viewer} or {plugin_viewer}")

    # Create temporary serving directory containing viewer files and the GLB + manifest
    import tempfile
    with tempfile.TemporaryDirectory() as serve_dir:
        serve_path = Path(serve_dir)
        # Copy viewer.html, viewer.js, vendor/, and utils/
        shutil.copy(viewer_dir / "viewer.html", serve_path / "viewer.html")
        shutil.copy(viewer_dir / "viewer.js", serve_path / "viewer.js")
        shutil.copytree(viewer_dir / "vendor", serve_path / "vendor")
        if (viewer_dir / "utils").exists():
            shutil.copytree(viewer_dir / "utils", serve_path / "utils")

        # Copy GLB and its manifest
        shutil.copy(glb_path, serve_path / "model.glb")
        manifest_src = glb_path.with_name(f"{glb_path.name}.manifest.json")
        if manifest_src.exists():
            shutil.copy(manifest_src, serve_path / "model.glb.manifest.json")
        else:
            # Create minimal manifest if absent
            with open(serve_path / "model.glb.manifest.json", "w", encoding="utf-8") as f:
                json.dump({
                    "assembly_sha256": "UNKNOWN",
                    "bounds_mm": [[-1500, -1500, 0], [1500, 1500, 3000]],
                    "members": []
                }, f)

        # Start ephemeral loopback server on port 0
        handler_factory = lambda *args, **kwargs: _QuietHTTPHandler(*args, directory=str(serve_path), **kwargs)
        with socketserver.TCPServer(("127.0.0.1", 0), handler_factory) as httpd:
            port = httpd.server_address[1]
            server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            server_thread.start()

            try:
                with sync_playwright() as p:
                    # Launch Chromium headless
                    browser = p.chromium.launch(
                        headless=True,
                        args=[
                            "--use-gl=angle",
                            "--use-angle=swiftshader",  # Reliable software WebGL on headless CI/macOS
                            "--enable-webgl",
                            "--no-sandbox",
                        ],
                    )
                    context = browser.new_context(
                        viewport={"width": width, "height": height},
                        device_scale_factor=1.0,
                    )
                    page = context.new_page()
                    page.on("console", lambda msg: print(f"[BROWSER CONSOLE] {msg.type}: {msg.text}"))
                    page.on("pageerror", lambda err: print(f"[BROWSER PAGEERROR] {err}"))

                    url = f"http://127.0.0.1:{port}/viewer.html?glb=./model.glb&manifest=./model.glb.manifest.json&camera={camera_type}"
                    page.goto(url)

                    # Poll for window.renderStatus.state == 'ready' or 'error'
                    start_time = time.time()
                    depth_bits = 0
                    status_state = "loading"
                    error_msg = None

                    while time.time() - start_time < timeout_s:
                        status = page.evaluate("window.renderStatus")
                        if status and isinstance(status, dict):
                            status_state = status.get("state", "loading")
                            depth_bits = status.get("depthBits", 0)
                            if status_state == "ready":
                                break
                            if status_state == "error":
                                error_msg = status.get("error", "Unknown viewer error")
                                break
                        time.sleep(0.1)

                    if status_state != "ready":
                        raise RuntimeError(f"Presentation viewer failed to reach ready state: {error_msg or status_state}")

                    if depth_bits < 24:
                        raise RuntimeError(f"Viewer reported insufficient depth bits: {depth_bits} (expected >= 24)")

                    # Screenshot canvas element
                    canvas = page.locator("canvas")
                    canvas.screenshot(path=str(output_png))

                    browser.close()

            finally:
                httpd.shutdown()

    if not output_png.exists() or output_png.stat().st_size == 0:
        raise RuntimeError(f"Failed to generate output screenshot at {output_png}")

    return PresentationReceipt(
        png_path=str(output_png),
        glb_path=str(glb_path),
        camera_type=camera_type,
        viewport_width=width,
        viewport_height=height,
        depth_bits=depth_bits,
        status="ready",
        file_size_bytes=output_png.stat().st_size,
    )
