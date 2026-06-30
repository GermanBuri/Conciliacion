import logging

from app.core.config import settings
from app.core.database import SessionLocal, wait_for_database
from app.services.bootstrap import seed_initial_superuser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    wait_for_database()
    db = SessionLocal()
    try:
        seed_initial_superuser(db)
        logger.info("Initial data completed successfully for %s.", settings.first_superuser_email)
    finally:
        db.close()


if __name__ == "__main__":
    main()
