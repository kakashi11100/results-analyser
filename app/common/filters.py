"""Generic filter parsing helper."""

from __future__ import annotations

from typing import Any


def pick_filters(raw: dict[str, Any], allowed: set[str]) -> dict[str, Any]:
    return {k: v for k, v in raw.items() if k in allowed and v is not None}


__all__ = ["pick_filters"]
