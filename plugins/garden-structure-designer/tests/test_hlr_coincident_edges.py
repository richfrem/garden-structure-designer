"""Tests for HLR coincident edge deduplication and provenance preservation."""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import cad_projection_hlr as hlr  # type: ignore[import]  # noqa: E402


def test_coincident_edges_deduplication():
    """Verify that two touching members sharing a joint seam emit only ONE visible seam."""
    edge1 = hlr.ProjectedEdge(
        member_id="B1",
        role="beam",
        visibility="visible",
        edge_kind="sharp",
        start_pt=(0.0, 0.0),
        end_pt=(100.0, 0.0),
    )
    # Touching beam B2 shares the identical seam in reverse direction
    edge2 = hlr.ProjectedEdge(
        member_id="B2",
        role="beam",
        visibility="visible",
        edge_kind="sharp",
        start_pt=(100.0, 0.0),
        end_pt=(0.0, 0.0),
    )

    deduped = hlr.deduplicate_coincident_edges([edge1, edge2], tol_mm=0.01)

    assert len(deduped) == 1
    seam = deduped[0]
    # Primary tag is alphabetically earliest ("B1")
    assert seam.member_id == "B1"
    # Contributing members set includes both B1 and B2
    assert getattr(seam, "contributing_members", ("B1",)) == ("B1", "B2")


def test_visible_over_hidden_coincidence():
    """Verify that a visible edge takes precedence over an exactly coincident hidden edge."""
    edge_vis = hlr.ProjectedEdge(
        member_id="P1",
        role="post",
        visibility="visible",
        edge_kind="sharp",
        start_pt=(0.0, 0.0),
        end_pt=(0.0, 2000.0),
    )
    edge_hid = hlr.ProjectedEdge(
        member_id="FT1",
        role="footing",
        visibility="hidden",
        edge_kind="sharp",
        start_pt=(0.0, 0.0),
        end_pt=(0.0, 2000.0),
    )

    deduped = hlr.deduplicate_coincident_edges([edge_vis, edge_hid], tol_mm=0.01)

    assert len(deduped) == 1
    assert deduped[0].visibility == "visible"
