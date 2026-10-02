"""User service. Phase 1: create + duplicate check only."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import DuplicateError, NotFoundError
from app.core.security import hash_password
from app.modules.auth.models import User
from app.modules.auth.repository import UserRepository
from app.modules.auth.schemas import UserCreate


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = UserRepository(db)

    def create_user(self, payload: UserCreate) -> User:
        if self.repo.get_by_username(payload.username):
            raise DuplicateError(f"Username '{payload.username}' is taken.")
        if self.repo.get_by_email(payload.email):
            raise DuplicateError(f"Email '{payload.email}' is already registered.")
        return self.repo.create(
            username=payload.username,
            email=payload.email,
            hashed_password=hash_password(payload.password),
            role=payload.role,
            is_active=payload.is_active,
        )

    def get_user(self, user_id) -> User:
        user = self.repo.get(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} not found.")
        return user


__all__ = ["UserService"]
