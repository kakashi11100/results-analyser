import pytest

from app.core.exceptions import DuplicateError
from app.modules.auth.schemas import UserCreate
from app.modules.auth.service import UserService


def test_duplicate_username_raises(db):
    service = UserService(db)
    service.create_user(
        UserCreate(username="alice", email="alice@example.com", password="password123")
    )
    with pytest.raises(DuplicateError):
        service.create_user(
            UserCreate(username="alice", email="alice2@example.com", password="password123")
        )


def test_duplicate_email_raises(db):
    service = UserService(db)
    service.create_user(
        UserCreate(username="bob", email="bob@example.com", password="password123")
    )
    with pytest.raises(DuplicateError):
        service.create_user(
            UserCreate(username="bob2", email="bob@example.com", password="password123")
        )
