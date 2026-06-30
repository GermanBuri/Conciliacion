from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.exc import UnknownHashError
from passlib.context import CryptContext

from app.core.config import settings

ALGORITHM = "HS256"
password_context = CryptContext(schemes=["argon2"], deprecated="auto")


def create_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    if not password_hash or not str(password_hash).strip():
        return False
    try:
        return password_context.verify(plain_password, password_hash)
    except (ValueError, TypeError, UnknownHashError):
        return False


def create_access_token(subject: str) -> str:
    expire_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": subject, "exp": expire_at}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
