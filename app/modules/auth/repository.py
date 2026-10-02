"""User repository."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.common.base import BaseRepository
from app.modules.auth.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session) -> None:
        super().__init__(User, db)

    def get_by_username(self, username: str) -> User | None:
        return self.get_by(username=username)

    def get_by_email(self, email: str) -> User | None:
        return self.get_by(email=email)


__all__ = ["UserRepository"]
