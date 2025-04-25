import logging

from fastapi import FastAPI
from thalentfrx.configs.Environment import EnvironmentSettings
from thalentfrx import __version__
from thalentfrx.configs.Logger import get_logger

class ThalentFrx(FastAPI):

    def __init__(self, *args, **kwargs):
        # Instantiate FastAPI
        super().__init__(*args, **kwargs)
        self.uvicorn_logger = None
        self.logger = None
        self.env = None

    def environment_init(self, env: EnvironmentSettings = None):
        self.env = env
        self.version = env.APP_VERSION
        self.title = env.APP_NAME

    def logger_init(self, env: EnvironmentSettings = None):
        self.logger: logging.Logger = get_logger(env=env, name=__name__)
        self.uvicorn_logger: logging.Logger = logging.getLogger(
            "uvicorn.error"
        )