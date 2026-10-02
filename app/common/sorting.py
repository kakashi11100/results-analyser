"""Generic sort-param parsing."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class SortParams(BaseModel):
    sort_by: str = "created_at"
    order: Literal["asc", "desc"] = "desc"

    def as_sqlalchemy(self, model: object) -> object:
        column = getattr(model, self.sort_by)
        return column.asc() if self.order == "asc" else column.desc()


__all__ = ["SortParams"]
