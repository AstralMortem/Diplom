from pathlib import Path
from typing import Any, Literal
from pydantic_settings import BaseSettings
from pydantic import AnyUrl, PostgresDsn, MySQLDsn, MariaDBDsn, Field


def get_database_url(config: dict[str, Any]) -> AnyUrl:
    driver = "asyncpg"
    db_config = {
        "scheme": f"{config["DATABASE_TYPE"]}+{driver}",
        "host": config["DATABASE_HOST"],
        "port": config["DATABASE_PORT"],
        "username": config["DATABASE_USERNAME"],
        "password": config["DATABASE_PASSWORD"],
        "path": config["DATABASE_NAME"],
    }

    if config["DATABASE_TYPE"] == "postgresql":
        driver = "asyncpg"
        return str(PostgresDsn.build(**db_config))
    
    if config["DATABASE_TYPE"] == "mysql":
        driver = "aiomysql"
        return str(MySQLDsn.build(**db_config))
    
    if config["DATABASE_TYPE"] == "mariadb":
        driver = "aiomysql"
        return str(MariaDBDsn.build(**db_config))
    
    raise ValueError(f"Invalid database type: {config['DATABASE_TYPE']}")
    

class BackendConfig(BaseSettings):
    DEBUG: bool = True

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_USERNAME: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_NAME: str = "postgres"
    DATABASE_TYPE: Literal["postgresql", "mysql", "sqlite"] = "postgresql"
    DATABASE_URL: AnyUrl = Field(default_factory=get_database_url)


    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_TIME: int = 60 * 60 * 12  # 24 hours
    JWT_AUTH_AUDIENCE: list[str] = ["med-voice:auth"]
    AUTH_COOKIE_NAME: str = "med_voice_auth_token"

    ROUTER_GLOBAL_PREFIX: str = "/api"


    DEFAULT_DOCTOR_ROLE_ID: int = 1

    BASE_DIR: Path = Path(__file__).parent
    MEDIA_DIR: Path = BASE_DIR.parent / "media"

    ALEMBIC_CFG: Path = BASE_DIR.parent / "alembic.ini"
    MIGRATIONS_DIR: Path = BASE_DIR.parent / "migrations"


config = BackendConfig()
