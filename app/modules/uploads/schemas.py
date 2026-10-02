# uploads/schemas
"""Pydantic v2 schemas for upload logs."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.modules.uploads.models import UploadFileType, UploadStatus


class UploadLogBase(BaseModel):
    file_name: str = Field(min_length=1, max_length=255)
    file_type: UploadFileType
    uploaded_by: uuid.UUID | None = None
    rows_parsed: int = Field(default=0, ge=0)
    rows_failed: int = Field(default=0, ge=0)
    status: UploadStatus = UploadStatus.PENDING
    error_summary: dict | None = None


class UploadLogCreate(UploadLogBase):
    pass


class UploadLogUpdate(BaseModel):
    rows_parsed: int | None = Field(default=None, ge=0)
    rows_failed: int | None = Field(default=None, ge=0)
    status: UploadStatus | None = None
    error_summary: dict | None = None


class UploadLogRead(UploadLogBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


__all__ = [
    "UploadLogBase", "UploadLogCreate", "UploadLogUpdate", "UploadLogRead",
]