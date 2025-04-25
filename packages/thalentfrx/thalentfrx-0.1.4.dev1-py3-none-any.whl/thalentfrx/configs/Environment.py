from functools import lru_cache
import os

from pydantic_settings import SettingsConfigDict, BaseSettings

from thalentfrx import __version__


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    ENV: str = ''
    APP_NAME: str = ''
    APP_VERSION: str = __version__
    DATABASE_DIALECT: str = ''
    DATABASE_HOSTNAME: str = ''
    DATABASE_PORT: int = 0
    DATABASE_NAME: str = ''
    DATABASE_USERNAME: str = ''
    DATABASE_PASSWORD: str = ''
    DATABASE_SSL_MODE: bool = False
    DEBUG_MODE: bool = True

    LOG_CLI: bool = False
    LOG_CLI_LEVEL: str = ''
    LOG_CLI_FORMAT: str = ''
    LOG_CLI_DATE_FORMAT: str = ''

    LOG_FILE: str = ''
    LOG_FILE_MODE: str = ''
    LOG_FILE_LEVEL: str = ''
    LOG_FILE_FORMAT: str = ''
    LOG_FILE_DATE_FORMAT: str = ''
    LOG_FILE_MAX_BYTES: int = 0
    LOG_FILE_BACKUP_COUNT: int = 0

    LOG_FILE_DEBUG_PATH: str = ''
    LOG_FILE_WARNING_PATH: str = ''

    JWT_TOKEN_SECRET: str = ''
    JWT_ACCESS_TOKEN_DURATION_IN_SEC: int = 0
    JWT_ACCESS_TOKEN_REMEMBER_DURATION_IN_SEC: int = 0
    JWT_REFRESH_TOKEN_DURATION_IN_SEC: int = 0

    UVICORN_LOG_FILE_PATH: str = ''

    env_file: str = get_env_filename()
    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding="utf-8")


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()
