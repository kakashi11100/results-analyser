# uploads/models
"""UploadLog: one row per ingestion attempt of a source file.

`error_summary` is JSONB so a failed parse can carry structured per-row errors
without forcing a schema change. `uploaded_by` uses RESTRICT (matching the
project default) — users are soft-deleted, so hard-deleting the user row would
never legitimately happen, and if it ever did we want it to fail loudly.
"""

from __future__ import annotations

import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum as SAEnum, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.base import TimestampMixin
from app.core.database import Base

from app.modules.auth.models import User 


class UploadFileType(str, enum.Enum):
    STUDENT_LIST = "student_list"
    COURSE_BOOK = "course_book"
    GRADE_CARD = "grade_card"
    RESULT = "result"
    REVALUATION = "revaluation"


class UploadStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


class UploadLog(TimestampMixin, Base):
    __tablename__ = "upload_logs"

    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[UploadFileType] = mapped_column(
        SAEnum(
            UploadFileType,
            name="upload_file_type",
            native_enum=True,
            values_callable=lambda c: [m.value for m in c],
        ),
        nullable=False,
    )
    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=True,  # null = system/automated upload (e.g. scheduled job)
    )

    rows_parsed: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    rows_failed: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    status: Mapped[UploadStatus] = mapped_column(
        SAEnum(
            UploadStatus,
            name="upload_status",
            native_enum=True,
            values_callable=lambda c: [m.value for m in c],
        ),
        nullable=False,
        default=UploadStatus.PENDING,
        server_default=UploadStatus.PENDING.value,
    )
    error_summary: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        CheckConstraint("rows_parsed >= 0", name="rows_parsed_non_negative"),
        CheckConstraint("rows_failed >= 0", name="rows_failed_non_negative"),
        CheckConstraint("rows_failed <= rows_parsed", name="rows_failed_le_parsed"),
        # Dashboard: "recent uploads by type". Ordering is done at query time.
        Index("ix_upload_logs_type_status_created", "file_type", "status", "created_at"),
    )

    uploader: Mapped["User | None"] = relationship(backref="upload_logs")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<UploadLog {self.file_name} type={self.file_type.value} status={self.status.value}>"


__all__ = ["UploadLog", "UploadFileType", "UploadStatus"]