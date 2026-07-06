"""
Application lifecycle management.
Provides context managers to handle startup and shutdown gracefully.
"""

import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from loguru import logger

from app.config.logging_config import setup_logging


@asynccontextmanager
async def app_lifecycle() -> AsyncGenerator[None, None]:
    """
    Asynchronous context manager for the application lifecycle.
    Handles bootstrapping and graceful shutdown of core services.
    
    Usage (FastAPI example):
        app = FastAPI(lifespan=app_lifecycle)
        
    Usage (Manual):
        async with app_lifecycle():
            # Run application
    """
    try:
        # Startup Phase
        setup_logging()
        logger.info("Starting ThinkFlow Studio infrastructure...")
        
        # Here we would initialize database connections, caches, etc.
        logger.info("Application startup complete.")
        
        yield
        
    except Exception as e:
        logger.exception("Fatal error during application lifecycle")
        sys.exit(1)
        
    finally:
        # Shutdown Phase
        logger.info("Shutting down ThinkFlow Studio gracefully...")
        # Close database connections, flush logs, etc.
        logger.info("Application shutdown complete.")
