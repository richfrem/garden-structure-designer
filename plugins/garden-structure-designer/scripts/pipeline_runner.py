#!/usr/bin/env python3
"""
pipeline_runner.py
=====================================

Purpose:
    Programmatic pipeline runner seam (``run_pipeline``) used for deterministic
    testing, stage injection, and isolated candidate execution. Also hosts the
    registry of topology error codes (``TopologyErrorCode``).

Layer: Core

Stage Contract:
    Each stage is ``Callable[[dict, Path, Path], dict]`` taking
    ``(structure, reports_dir, outputs_dir)``. A returned dict becomes the new
    structure. A returned dict containing an ``error_code`` key is a failure
    (optional ``error_message``). A raised exception is also a failure; its
    ``error_code`` attribute, if present, is reported. Execution halts at the
    first failure and downstream stages are never invoked.

Key Functions:
    run_pipeline(structure_path, *, stages, reports_dir, outputs_dir, stop_after_stage) -> PipelineResult

Script Dependencies:
    Standard library only (json, dataclasses, enum, pathlib).
"""

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Mapping, Optional

STAGE_ORDER = ("0", "0.5", "1", "2", "3", "4", "5.5", "5.6", "6", "5", "7")

StageFn = Callable[[dict, Path, Path], dict]


class TopologyErrorCode(str, Enum):
    TOPOLOGY_CARDINALITY_MISMATCH = "TOPOLOGY_CARDINALITY_MISMATCH"
    DUPLICATE_MEMBER_ID = "DUPLICATE_MEMBER_ID"
    DANGLING_CONNECTION_ENDPOINT = "DANGLING_CONNECTION_ENDPOINT"
    ATTACHMENT_GEOMETRY_MISMATCH = "ATTACHMENT_GEOMETRY_MISMATCH"
    UNKNOWN_TOPOLOGY_FAMILY = "UNKNOWN_TOPOLOGY_FAMILY"
    TOPOLOGY_NOT_IMPLEMENTED = "TOPOLOGY_NOT_IMPLEMENTED"
    FEATURE_NOT_IMPLEMENTED = "FEATURE_NOT_IMPLEMENTED"
    GEOMETRY_INVALID = "GEOMETRY_INVALID"
    HUB_TYPE_MISMATCH = "HUB_TYPE_MISMATCH"
    STALE_REVISION = "STALE_REVISION"
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"


@dataclass
class PipelineResult:
    success: bool
    structure: dict
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    failed_stage: Optional[str] = None
    completed_stages: list[str] = field(default_factory=list)


def _stub_stage(structure: dict, reports_dir: Path, outputs_dir: Path) -> dict:
    return structure


def _error_code_value(code) -> Optional[str]:
    if code is None:
        return None
    return code.value if isinstance(code, Enum) else str(code)


def run_pipeline(
    structure_path: Path | str,
    *,
    stages: Optional[Mapping[str, StageFn]] = None,
    reports_dir: Optional[Path | str] = None,
    outputs_dir: Optional[Path | str] = None,
    stop_after_stage: Optional[str] = None,
) -> PipelineResult:
    structure_path = Path(structure_path)
    overrides = dict(stages or {})

    unknown = [name for name in overrides if name not in STAGE_ORDER]
    if unknown:
        raise ValueError(f"Unknown stage(s): {unknown}. Valid stages: {list(STAGE_ORDER)}")
    if stop_after_stage is not None and stop_after_stage not in STAGE_ORDER:
        raise ValueError(f"Unknown stop_after_stage: {stop_after_stage!r}")

    reports_path = Path(reports_dir) if reports_dir is not None else structure_path.parent / "reports"
    outputs_path = Path(outputs_dir) if outputs_dir is not None else structure_path.parent / "outputs"

    structure = json.loads(structure_path.read_text(encoding="utf-8"))
    completed: list[str] = []

    for stage_name in STAGE_ORDER:
        stage_fn = overrides.get(stage_name, _stub_stage)

        try:
            result = stage_fn(structure, reports_path, outputs_path)
        except Exception as exc:
            return PipelineResult(
                success=False,
                structure=structure,
                error_code=_error_code_value(getattr(exc, "error_code", None)),
                error_message=str(exc),
                failed_stage=stage_name,
                completed_stages=completed,
            )

        if isinstance(result, dict) and "error_code" in result:
            return PipelineResult(
                success=False,
                structure=structure,
                error_code=_error_code_value(result["error_code"]),
                error_message=result.get("error_message"),
                failed_stage=stage_name,
                completed_stages=completed,
            )

        if isinstance(result, dict):
            structure = result
        completed.append(stage_name)

        if stage_name == stop_after_stage:
            break

    return PipelineResult(success=True, structure=structure, completed_stages=completed)
