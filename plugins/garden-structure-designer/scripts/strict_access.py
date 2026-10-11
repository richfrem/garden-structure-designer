#!/usr/bin/env python3
"""
strict_access.py
================

Purpose:
    Fail-closed accessors for structural inputs. Replaces silent ``.get(key) or default``
    patterns: a missing dimension, angle, count or jurisdiction raises ``MissingInputError``
    (``MISSING_INPUT: <label>.<key>``) instead of being invented (AGENTS data-driven rule,
    spec C1 "never supply silent structural defaults").

Layer: Core / Shared Utility

Key Input Dependencies:
    Standard library only.

Key Functions / Classes:
    MissingInputError(ValueError)
    require(mapping, key, label) -> Any
    require_path(mapping, *keys) -> Any

Usage Examples:
    from strict_access import require, require_path
    cut = require_path(structure, "members", "posts", "cut_length_ft")
"""
from __future__ import annotations

from typing import Any


class MissingInputError(ValueError):
    """A required structural input is absent; callers report it and halt rather than guess."""


def require(mapping: Any, key: str, label: str) -> Any:
    """Returns ``mapping[key]``; None, empty string and non-mappings raise ``MISSING_INPUT: label.key``."""
    if not isinstance(mapping, dict) or mapping.get(key) in (None, ""):
        raise MissingInputError(f"MISSING_INPUT: {label}.{key}")
    return mapping[key]


def require_path(mapping: Any, *keys: str) -> Any:
    """Walks nested mappings with ``require``, naming the first missing level in the error."""
    node: Any = mapping
    for depth, key in enumerate(keys):
        node = require(node, key, ".".join(keys[:depth]) or "structure")
    return node
