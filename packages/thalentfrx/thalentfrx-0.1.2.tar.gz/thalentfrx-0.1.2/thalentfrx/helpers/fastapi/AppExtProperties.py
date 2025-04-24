import logging
import os

from fastapi import FastAPI

from thalentfrx.configs import Environment
from thalentfrx.configs.Logger import get_logger

# Application Environment Configuration
env: Environment.EnvironmentSettings = (
    Environment.get_environment_variables()
)
basedir: str = os.path.abspath(os.path.dirname(__file__))
environment: str = os.getenv("ENV")

# Logger
logger: logging.Logger = get_logger(__name__)
uvicorn_logger: logging.Logger = logging.getLogger(
    "uvicorn.error"
)


def add_app_extend_property(app: FastAPI) -> None:
    # Add Env
    app.environment = environment
    app.basedir = basedir

    # Add Config
    app.env = env

    # Add Logger
    app.logger = logger
    app.uvicorn_logger = uvicorn_logger
