import logging
from logging import Logger
from typing import Any, TypeVar, Generic, List

from fastapi import FastAPI, APIRouter
from pydantic_settings import BaseSettings

from thalentfrx.helpers import StartUpInfo
from thalentfrx.configs.Logger import get_logger
from thalentfrx.helpers.fastapi.ExceptionHandlers import add_custom_exception_handler

T = TypeVar('T', bound=BaseSettings)


class ThalentFrx(FastAPI, Generic[T]):

    def __init__(self, *args, **kwargs):
        # Instantiate FastAPI
        super().__init__(*args, **kwargs)
        self.uvicorn_logger: Logger | None = None
        self.logger: Logger | None = None
        self.env: T | None = None

    def environment_init(self, env: T = None):
        self.env = env
        self.version = env.APP_VERSION
        self.title = env.APP_NAME

    def logger_init(self, env: T = None):
        self.logger: logging.Logger = get_logger(env=env, name=__name__)
        self.uvicorn_logger: logging.Logger = logging.getLogger(
            "uvicorn.error"
        )
        add_custom_exception_handler(app=self)
        StartUpInfo.show_startup_info(app=self)

    def router_init(self, routers: List[APIRouter]) -> None:
        for router in routers:
            self.include_router(router)
