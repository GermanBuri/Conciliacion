from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.user import User
from app.repositories.user import UserRepository


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)

    def authenticate_user(self, *, email: str, password: str) -> User | None:
        user = self.user_repository.get_by_email(email)
        if user is None:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
