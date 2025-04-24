import logging

from fastapi import FastAPI


def show_startup_info(
    app: FastAPI, logger: logging.Logger
) -> None:
    logger.info("API is starting up.")
    logger.info(f"APP NAME: {app.title}")
    logger.info(f"VERSION: {app.version}")

    logger.info(f"BASE_DIR: {app.basedir}")
    logger.info(f"ENV: {app.environment}")

    logger.info(
        f"DATABASE_DIALECT: {app.env.DATABASE_DIALECT}"
    )
    logger.info(
        f"DATABASE_HOSTNAME: {app.env.DATABASE_HOSTNAME}"
    )
    logger.info(f"DATABASE_PORT: {app.env.DATABASE_PORT}")
    logger.info(f"DATABASE_SSL_MODE: {app.env.DATABASE_SSL_MODE}")
    logger.info(f"DATABASE_NAME: {app.env.DATABASE_NAME}")

    logger.debug(
        f"DATABASE_USERNAME: {app.env.DATABASE_USERNAME}"
    )
    logger.info(f"DEBUG_MODE: {app.env.DEBUG_MODE}")

    logger.info(f"LOG_CLI: {app.env.LOG_CLI}")
    logger.info(f"LOG_CLI_LEVEL: {app.env.LOG_CLI_LEVEL}")
    logger.info(f"LOG_FILE: {app.env.LOG_FILE}")
    logger.info(f"LOG_FILE_LEVEL: {app.env.LOG_FILE_LEVEL}")

    logger.info(
        f"JWT_ACCESS_TOKEN_DURATION_IN_SEC: {app.env.JWT_ACCESS_TOKEN_DURATION_IN_SEC}"
    )
    logger.info(
        f"JWT_ACCESS_TOKEN_REMEMBER_DURATION_IN_SEC: {app.env.JWT_ACCESS_TOKEN_REMEMBER_DURATION_IN_SEC}"
    )
    logger.info(
        f"JWT_REFRESH_TOKEN_DURATION_IN_SEC: {app.env.JWT_REFRESH_TOKEN_DURATION_IN_SEC}"
    )

    if app.environment != "prod":
        pass
        # logger.debug("TEST DEBUG")
        # logger.info("TEST INFO")
        # logger.warning("TEST WARNING")
        # logger.error("TEST ERROR")
        # logger.critical("TEST CRITICAL")
