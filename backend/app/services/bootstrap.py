import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_password_hash
from app.repositories.user import UserRepository

logger = logging.getLogger(__name__)
LEGACY_SUPERUSER_EMAIL = "admin@conciliarbt.local"


def seed_initial_superuser(db: Session) -> None:
    repository = UserRepository(db)
    existing_user = repository.get_by_email(settings.first_superuser_email)
    if existing_user:
        logger.info("Initial superuser already exists: %s", settings.first_superuser_email)
        return

    legacy_user = repository.get_by_email(LEGACY_SUPERUSER_EMAIL)
    if legacy_user:
        legacy_user.email = settings.first_superuser_email
        db.add(legacy_user)
        db.commit()
        db.refresh(legacy_user)
        logger.info(
            "Initial superuser email updated from %s to %s",
            LEGACY_SUPERUSER_EMAIL,
            settings.first_superuser_email,
        )
        return

    repository.create(
        email=settings.first_superuser_email,
        full_name=settings.first_superuser_full_name,
        password_hash=create_password_hash(settings.first_superuser_password),
        is_superuser=True,
    )
    logger.info("Initial superuser created: %s", settings.first_superuser_email)
