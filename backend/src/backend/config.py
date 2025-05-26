from pathlib import Path
from typing import Any, Literal
from pydantic_settings import BaseSettings
from pydantic import AnyUrl, PostgresDsn, MySQLDsn, MariaDBDsn, Field

def get_default_origin():
    from backend.core.mdns import get_local_ip
    ips = ["http://localhost:3000", "http://localhost", "http://127.0.0.1", "http://127.0.0.1:3000"]
    local_ip = 'http://' + get_local_ip()
    ips.append(local_ip)
    ips.append(local_ip + ':3000')
    ips.append(local_ip + ':*')
    return ips


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
    LOGIN_URL: str = Field(default_factory=lambda conf: f"{conf["ROUTER_GLOBAL_PREFIX"]}/v1/auth/login")


    DEFAULT_DOCTOR_ROLE_ID: int = 1

    BASE_DIR: Path = Path(__file__).parent
    MEDIA_DIR: Path = BASE_DIR.parent / "media"

    ALEMBIC_CFG: Path = BASE_DIR.parent / "alembic.ini"
    MIGRATIONS_DIR: Path = BASE_DIR.parent / "migrations"

    OLLAMA_MODEL: str = "llama3.2"
    ORIGINS: list[str] = get_default_origin()
    

config = BackendConfig(_env_file="config.env")



            