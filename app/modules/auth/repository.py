"""Data-access layer for users and refresh tokens. No business rules here."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.modules.auth.models import RefreshToken, User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).where(
            User.id == user_id,
            User.deleted_at.is_(None),
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(
            User.username == username,
            User.deleted_at.is_(None),
        )
        return self.db.execute(stmt).scalar_one_or_none()


class RefreshTokenRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, token: RefreshToken) -> RefreshToken:
        self.db.add(token)
        self.db.flush()  # populate token.id for replaced_by_id
        return token

    def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.deleted_at.is_(None),
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def revoke(
        self, token: RefreshToken, *, replaced_by_id: uuid.UUID | None = None
    ) -> None:
        if token.revoked_at is not None:
            return
        token.revoked_at = datetime.now(timezone.utc)
        token.replaced_by_id = replaced_by_id
        self.db.flush()

    def revoke_all_for_user(self, user_id: uuid.UUID) -> None:
        """Revoke every non-revoked refresh token owned by the user."""
        now = datetime.now(timezone.utc)
        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )
        self.db.execute(stmt)
        self.db.flush()


__all__ = ["UserRepository", "RefreshTokenRepository"]