"""Auth router. Phase 1 exposes user creation and lookup only — no login."""

from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.schemas import UserCreate, UserRead
from app.modules.auth.service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    service = UserService(db)
    user = service.create_user(payload)
    return UserRead.model_validate(user)


@router.get(
    "/users/{user_id}",
    response_model=UserRead,
    summary="Get a user by id",
)
def get_user(user_id: str, db: Session = Depends(get_db)) -> UserRead:
    service = UserService(db)
    user = service.get_user(user_id)
    return UserRead.model_validate(user)
