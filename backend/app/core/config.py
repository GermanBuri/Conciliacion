from pathlib import Path
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = Field(default="ConciliarBT API", validation_alias="APP_NAME")
    app_env: str = Field(default="development", validation_alias="APP_ENV")
    debug: bool = Field(default=True, validation_alias="DEBUG")
    api_v1_prefix: str = Field(default="/api/v1", validation_alias="API_V1_PREFIX")
    secret_key: str = Field(validation_alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=60, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    postgres_server: str = Field(default="localhost", validation_alias="POSTGRES_SERVER")
    postgres_port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    postgres_db: str = Field(default="conciliarbt", validation_alias="POSTGRES_DB")
    postgres_user: str = Field(default="conciliarbt", validation_alias="POSTGRES_USER")
    postgres_password: str = Field(default="conciliarbt", validation_alias="POSTGRES_PASSWORD")
    database_url: str = Field(validation_alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias="REDIS_URL")
    cors_origins: list[str] = Field(default_factory=list, validation_alias="CORS_ORIGINS")
    first_superuser_email: str = Field(default="admin@conciliarbt.com", validation_alias="FIRST_SUPERUSER_EMAIL")
    first_superuser_password: str = Field(default="ChangeMe123!", validation_alias="FIRST_SUPERUSER_PASSWORD")
    first_superuser_full_name: str = Field(default="Administrador Inicial", validation_alias="FIRST_SUPERUSER_FULL_NAME")
    upload_dir: str = Field(default="storage/uploads", validation_alias="UPLOAD_DIR")
    max_upload_size_mb: int = Field(default=25, validation_alias="MAX_UPLOAD_SIZE_MB")

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value: bool | str) -> bool:
        if isinstance(value, bool):
            return value
        normalized = str(value).strip().lower()
        if normalized in {"true", "1", "yes", "on", "debug", "development"}:
            return True
        if normalized in {"false", "0", "no", "off", "release", "production"}:
            return False
        return bool(value)

    @field_validator("database_url", mode="before")
    @classmethod
    def parse_database_url(cls, value: str) -> str:
        return value.strip()

    @property
    def upload_path(self) -> Path:
        configured = Path(self.upload_dir)
        if configured.is_absolute():
            return configured
        return BACKEND_ROOT / configured


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
