"""Seed the first admin user.

Reads ADMIN_USERNAME / ADMIN_EMAIL / ADMIN_PASSWORD from the environment.
Idempotent — re-running is safe.
"""

from __future__ import annotations

import logging
import os
import sys

from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.logging import configure_logging
from app.core.security import hash_password
from app.modules.auth.models import User, UserRole

logger = logging.getLogger("scripts.seed")


def seed_admin() -> None:
    username = os.environ.get("ADMIN_USERNAME", "admin")
    email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    password = os.environ.get("ADMIN_PASSWORD")

    if not password:
        logger.error("ADMIN_PASSWORD env var is required")
        sys.exit(1)

    db = SessionLocal()
    try:
        existing = db.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()
        if existing is not None:
            logger.info("admin already exists, skipping", extra={"username": username})
            return
        db.add(
            User(
                username=username,
                email=email,
                hashed_password=hash_password(password),
                role=UserRole.ADMIN,
                is_active=True,
            )
        )
        db.commit()
        logger.info("admin created", extra={"username": username})
    finally:
        db.close()


def seed_programs() -> None:
    # TODO: Phase 2 — once a Program model exists, insert: CS, ME, MC, CE, AD, CY
    logger.info("programs seed: no Program model yet, skipping")


def main() -> None:
    configure_logging()
    seed_admin()
    seed_programs()


if __name__ == "__main__":
    main()
