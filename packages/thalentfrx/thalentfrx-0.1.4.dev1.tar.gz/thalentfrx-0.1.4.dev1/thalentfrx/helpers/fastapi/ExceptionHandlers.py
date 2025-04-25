import logging
import shortuuid
from functools import wraps
from typing import Dict, Optional, Mapping

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from thalentfrx.helpers.fastapi.AppExceptions import (
    AppException,
    CredentialException,
    InvalidTokenException,
    app_http_exception,
    http_exception, UnexpectedException,
)
from thalentfrx.configs.Logger import get_logger

# Logger
logger: logging.Logger = get_logger(__name__)
uvicorn_logger: logging.Logger = logging.getLogger(
    "uvicorn.error"
)

def __message_response(status_code: int, detail: str, headers: Optional[Mapping[str,str]] = None) -> (JSONResponse, PlainTextResponse):
    response_json = JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({"detail": detail}),
        headers=headers,
    )
    # response_txt = PlainTextResponse(status_code=status_code, content=detail, headers=headers)
    response_txt = f'{detail}'
    return response_json, response_txt

def http_exception_handler():  # all, only_admin
    """Http exception handler decorator as alternative exception handler for fastapi built-in exception handler mechanism.

    Example:

    @UserRouterExt.post("/token/refresh", status_code=status.HTTP_200_OK, response_model=TokenResultSchema)
    @http_exception_handler()
    def token_refresh(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Session = Depends(get_db_session),
    ) -> Any:

        ...

    Args:
        None
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except InvalidTokenException as ex:
                logger.warning(msg=ex.__str__(), exc_info=True)
                raise app_http_exception(
                    ex,
                    headers={"WWW-Authenticate": "Bearer"},
                )
            except CredentialException as ex:
                logger.warning(msg=ex.__str__(), exc_info=True)
                raise app_http_exception(
                    ex,
                    headers={"WWW-Authenticate": "Bearer"},
                )
            except AppException as ex:
                logger.warning(msg=ex.__str__(), exc_info=True)
                raise app_http_exception(ex)

            except RequestValidationError as ex:
                ex = UnexpectedException(status_code=400, detail=ex.__str__())
                logger.warning(msg=ex.__str__(), exc_info=True)
                raise http_exception(
                    status_code=400, detail=ex.__str__()
                )
            except StarletteHTTPException as ex:
                ex = UnexpectedException(status_code=ex.status_code, detail=ex.__str__())
                logger.warning(msg=ex.__str__(), exc_info=True)
                raise http_exception(
                    status_code=ex.status_code, detail=ex.__str__()
                )
            except Exception as ex:
                ex = UnexpectedException(status_code=500, detail=ex.__str__())
                logger.error(msg=ex.__str__(), exc_info=True)
                raise http_exception(
                    status_code=500, detail=ex.__str__()
                )

        return decorator

    return wrapper

def add_unicorn_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(
            request: Request, exc: AppException
    ):
        response_json, response_txt = __message_response(status_code=exc.status_code, detail=exc.__str__())
        logger.warning(msg=response_txt, exc_info=True)
        return response_json

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_exception_handler(
            request: Request, exc: InvalidTokenException
    ):
        headers: Dict[str, str] = {
            "WWW-Authenticate": "Bearer"
        }
        response_json, response_txt = __message_response(status_code=exc.status_code, detail=exc.__str__(), headers=headers)
        logger.warning(msg=response_txt, exc_info=True)
        return response_json

    @app.exception_handler(CredentialException)
    async def credential_exception_handler(
            request: Request, exc: CredentialException
    ):
        headers: Dict[str, str] = {
            "WWW-Authenticate": "Bearer"
        }
        response_json, response_txt = __message_response(status_code=exc.status_code, detail=exc.__str__(),
                                                         headers=headers)
        logger.warning(msg=response_txt, exc_info=True)
        return response_json

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
        ex = UnexpectedException(exc.status_code, exc.detail)
        response_json, response_txt = __message_response(status_code=ex.status_code, detail=ex.__str__())
        logger.warning(msg=response_txt, exc_info=True)
        return response_json

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        ex = UnexpectedException(422, detail=exc.__str__())
        response_json, response_txt = __message_response(status_code=ex.status_code, detail=ex.__str__())
        logger.warning(msg=response_txt, exc_info=True)
        return response_json

    @app.exception_handler(Exception)
    async def generic_exception_handler(
            request: Request, exc: Exception
    ):
        headers: Dict[str, str] = {}

        if (
                request.url.path == "/v1/users/login"
                or request.url.path == "/v1/users/token/refresh"
        ):
            headers = {"WWW-Authenticate": "Bearer"}

        ex = UnexpectedException(500, detail=exc.__str__())
        response_json, response_txt = __message_response(status_code=ex.status_code, detail=ex.__str__(), headers=headers)
        logger.error(msg=response_txt, exc_info=True)
        return response_json