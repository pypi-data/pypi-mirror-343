from functools import lru_cache
import os

from pydantic_settings import SettingsConfigDict, BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    API_VERSION: str
    APP_NAME: str
    DATABASE_DIALECT: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_SSL_MODE: bool
    DEBUG_MODE: bool

    LOG_CLI: bool
    LOG_CLI_LEVEL: str
    LOG_CLI_FORMAT: str
    LOG_CLI_DATE_FORMAT: str

    LOG_FILE: str
    LOG_FILE_MODE: str
    LOG_FILE_LEVEL: str
    LOG_FILE_FORMAT: str
    LOG_FILE_DATE_FORMAT: str
    LOG_FILE_MAX_BYTES: int
    LOG_FILE_BACKUP_COUNT: int

    LOG_FILE_DEBUG: str
    LOG_FILE_WARNING: str

    JWT_TOKEN_SECRET: str
    JWT_ACCESS_TOKEN_DURATION_IN_SEC: str
    JWT_ACCESS_TOKEN_REMEMBER_DURATION_IN_SEC: str
    JWT_REFRESH_TOKEN_DURATION_IN_SEC: str

    UVICORN_LOG_FILE: str

    model_config = SettingsConfigDict(env_file=get_env_filename(), env_file_encoding="utf-8")


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()
