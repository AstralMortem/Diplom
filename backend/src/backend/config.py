from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class BackendConfig(BaseSettings):
    DEBUG: bool = True
    DATABASE_URL: PostgresDsn = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"  # type: ignore
    )

    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_TIME: int = 60 * 60 * 12  # 24 hours
    JWT_AUTH_AUDIENCE: list[str] = ["med-voice:auth"]
    AUTH_COOKIE_NAME: str = "med_voice_auth_token"

    ROUTER_GLOBAL_PREFIX: str = "/api"


    DEFAULT_DOCTOR_ROLE_ID: int = 1

    BASE_DIR: Path = Path(__file__).parent
    MEDIA_DIR: Path = BASE_DIR.parent / "media"


config = BackendConfig()
