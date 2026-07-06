"""
Logging configuration for ThinkFlow Studio.
Uses Loguru for structured logging, handling environment-based formatting.
"""

import sys
import logging
from loguru import logger
from app.config.settings import get_settings


class InterceptHandler(logging.Handler):
    """
    Intercepts standard logging messages and routes them to Loguru.
    """

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging() -> None:
    """
    Configures Loguru based on the current environment settings.
    In production, logs are serialized as JSON.
    In development, logs are colored and rich.
    """
    settings = get_settings()

    # Remove default handler
    logger.remove()

    if settings.app_env.lower() == "production":
        logger.add(
            sys.stdout,
            level=settings.log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
            serialize=True,
            enqueue=True,
            backtrace=True,
            diagnose=False,
        )
    else:
        logger.add(
            sys.stdout,
            level=settings.log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )

    # Intercept standard library logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    # Optional: Suppress noisy loggers here
    for _log in ["uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"]:
        _logger = logging.getLogger(_log)
        _logger.handlers = [InterceptHandler()]
        _logger.propagate = False
