#!/usr/bin/env python3
"""
ezdxf_adapter.py
================

Purpose:
    ``ExchangeWriter`` adapter that writes DXF sheets with the pure-Python ``ezdxf``
    library. Zero external binaries; this is the fallback writer.

Layer: Adapter

Key Input Dependencies:
    ``ezdxf`` (pinned in requirements-core.txt); exchange_writer.py contract.

Key Functions / Classes:
    stamp_xdata(entity, strings)        - attach GSD XDATA to an ezdxf entity
    EzdxfAdapter.export_sheet(...)      - write one sheet, return metadata dict

Usage:
    EzdxfAdapter().export_sheet("SB01", structure, Path("SB01-structure.dxf"),
                                revision_id=rid, revision_hash=rh)
"""
from __future__ import annotations

import sys
from pathlib import Path

import ezdxf
from ezdxf.entities import DXFEntity

sys.path.append(str(Path(__file__).parent))
from exchange_writer import (  # noqa: E402
    APPID,
    INSUNITS_MM,
    LAYER_COLORS,
    build_draw_entities,
    build_metadata,
    xdata_strings,
)


def stamp_xdata(entity: DXFEntity, strings: list[str]) -> None:
    """Attach the GSD application XDATA (group 1000 strings) to ``entity``."""
    entity.set_xdata(APPID, [(1000, s) for s in strings])


class EzdxfAdapter:
    """Writes sheets as DXF R2018 using ezdxf."""

    name = "ezdxf"

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
        doc = ezdxf.new("R2018")
        doc.header["$INSUNITS"] = INSUNITS_MM
        doc.header["$MEASUREMENT"] = 1
        doc.appids.add(APPID)
        for layer, color in LAYER_COLORS.items():
            doc.layers.add(layer, color=color)
        msp = doc.modelspace()
        for entity in entities:
            attribs = {"layer": entity.layer}
            if entity.text is not None:
                dxf_entity = msp.add_text(entity.text, height=entity.text_height, dxfattribs=attribs)
                dxf_entity.set_placement(entity.points[0])
            else:
                dxf_entity = msp.add_polyline3d(entity.points, dxfattribs=attribs)
            if entity.member_id is not None:
                stamp_xdata(dxf_entity, xdata_strings(entity, sheet_id, revision_id, revision_hash))
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.saveas(output_path)
        return build_metadata(sheet_id, output_path, self.name, len(entities))
