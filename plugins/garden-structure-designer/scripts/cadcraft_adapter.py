#!/usr/bin/env python3
"""
cadcraft_adapter.py
===================

Purpose:
    ``ExchangeWriter`` adapter that drives ``vendor/cadcraft/target/release/cadcraft-cli``
    to author the DXF sheet (layers, 3D polylines, text). cadcraft has no XDATA
    command, so the saved file is reopened with ``ezdxf`` to register the ``GSD`` APPID
    and stamp member XDATA onto the entities cadcraft reported by handle.

Layer: Adapter

Key Input Dependencies:
    Built cadcraft-cli binary (see scripts/build_cadcraft.py); ``ezdxf``;
    exchange_writer.py contract.

Key Functions / Classes:
    default_binary_path()               - repo-relative cadcraft-cli location
    CadcraftError                       - CLI missing or failed
    CadcraftAdapter.export_sheet(...)   - write one sheet, return metadata dict

Usage:
    CadcraftAdapter().export_sheet("SB02", structure, Path("SB02-plan.dxf"),
                                   revision_id=rid, revision_hash=rh)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import ezdxf

sys.path.append(str(Path(__file__).parent))
from exchange_writer import (  # noqa: E402
    APPID,
    INSUNITS_MM,
    LAYER_COLORS,
    DrawEntity,
    build_draw_entities,
    build_metadata,
    xdata_strings,
)
from ezdxf_adapter import stamp_xdata  # noqa: E402

CLI_TIMEOUT_S = 120


class CadcraftError(RuntimeError):
    """Raised when cadcraft-cli is unavailable or fails."""


def default_binary_path() -> Path:
    """Return the repo-relative path of the release cadcraft-cli binary."""
    name = "cadcraft-cli.exe" if sys.platform == "win32" else "cadcraft-cli"
    return Path(__file__).resolve().parents[3] / "vendor" / "cadcraft" / "target" / "release" / name


def _command(cmd_id: str, params: dict) -> str:
    """Format one ``--cmd`` argument."""
    return f"{cmd_id} {json.dumps(params)}"


def _build_commands(entities: list[DrawEntity]) -> list[str]:
    """Return the cadcraft command list; each entity yields exactly one handle, in order."""
    commands = [
        _command("new", {"metric": True}),
        _command("setvar", {"name": "INSUNITS", "value": INSUNITS_MM}),
    ]
    for layer, color in LAYER_COLORS.items():
        commands.append(_command("layer.new", {"name": layer, "color": color}))
    current_layer = None
    for entity in entities:
        if entity.layer != current_layer:
            commands.append(_command("layer.current", {"name": entity.layer}))
            current_layer = entity.layer
        if entity.text is not None:
            params = {"at": list(entity.points[0][:2]), "text": entity.text, "height": entity.text_height}
            commands.append(_command("text", params))
        else:
            commands.append(_command("3dpoly", {"points": [list(p) for p in entity.points]}))
    return commands


def _entity_handles(stdout: str) -> list[str]:
    """Extract the entity handles cadcraft printed, one JSON line per drawn entity."""
    handles = []
    for line in stdout.splitlines():
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and set(payload) == {"handle"}:
            handles.append(payload["handle"])
    return handles


class CadcraftAdapter:
    """Writes sheets through cadcraft-cli, then stamps XDATA via ezdxf."""

    name = "cadcraft"

    def __init__(self, binary: Path | None = None) -> None:
        self.binary = Path(binary) if binary else default_binary_path()

    def is_available(self) -> bool:
        """True when the cadcraft-cli binary exists."""
        return self.binary.is_file()

    def _run_cli(self, commands: list[str], output_path: Path) -> str:
        """Run cadcraft-cli with ``commands``, saving to ``output_path``; return stdout."""
        if not self.is_available():
            raise CadcraftError(f"cadcraft-cli not found at {self.binary}")
        argv = [str(self.binary), "run"]
        for command in commands:
            argv += ["--cmd", command]
        argv += ["--save", str(output_path)]
        result = subprocess.run(argv, capture_output=True, text=True, timeout=CLI_TIMEOUT_S)
        if result.returncode != 0 or not output_path.is_file():
            raise CadcraftError(f"cadcraft-cli failed (rc={result.returncode}): {result.stderr.strip()}")
        return result.stdout

    def export_sheet(
        self,
        sheet_id: str,
        structure: dict,
        output_path: Path,
        *,
        revision_id: str,
        revision_hash: str,
    ) -> dict:
        """Write ``sheet_id`` of ``structure`` to ``output_path`` and return metadata."""
        entities = build_draw_entities(structure, sheet_id)
        commands = _build_commands(entities)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        handles = _entity_handles(self._run_cli(commands, output_path))
        if len(handles) != len(entities):
            raise CadcraftError(f"cadcraft reported {len(handles)} handles for {len(entities)} entities")

        doc = ezdxf.readfile(output_path)
        doc.appids.add(APPID)
        for entity, handle in zip(entities, handles):
            if entity.member_id is not None:
                stamp_xdata(doc.entitydb[handle], xdata_strings(entity, sheet_id, revision_id, revision_hash))
        doc.saveas(output_path)
        return build_metadata(sheet_id, output_path, self.name, len(entities))
