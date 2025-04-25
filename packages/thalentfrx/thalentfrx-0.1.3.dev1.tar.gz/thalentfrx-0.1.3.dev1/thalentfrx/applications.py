import logging

from fastapi import FastAPI
from thalentfrx.configs.Environment import EnvironmentSettings
from thalentfrx import __version__
from thalentfrx.configs.Logger import get_logger

class ThalentFrx(FastAPI):

    # Logger
    logger: logging.Logger = get_logger(__name__)
    uvicorn_logger: logging.Logger = logging.getLogger(
        "uvicorn.error"
    )

    def __init__(self, env: EnvironmentSettings = None, *args, **kwargs):
        # Application Environment Configuration
        self.env: EnvironmentSettings = env

        if self.env.API_VERSION is not None:
            version = self.env.API_VERSION
        else:
            version = __version__

        # Instantiate FastAPI
        super().__init__(*args,
                         title = self.env.APP_NAME,
                         version = version,
                          **kwargs)


