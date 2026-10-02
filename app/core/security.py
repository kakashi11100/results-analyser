# core/security
# app/core/security.py
"""Password hashing helpers. JWT/auth flow is Phase 3."""

from passlib.context import CryptContext

# bcrypt has a 72-byte input limit; passlib truncates silently.
# bcrypt<4.1 avoids the passlib 1.7.4 `__about__` warning — pin in pyproject.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


__all__ = ["hash_password", "verify_password", "pwd_context"]