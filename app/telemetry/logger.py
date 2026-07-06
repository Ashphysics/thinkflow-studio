"""
Secure logger that sanitizes secrets.
"""
import re
from loguru import logger as base_logger

class SecureLogger:
    SECRET_PATTERN = r"(?i)(api[_-]?key|secret|token|password)[\s:=]+['\"]?([a-zA-Z0-9\-_]+)['\"]?"

    @classmethod
    def sanitize(cls, message: str) -> str:
        return re.sub(cls.SECRET_PATTERN, r"\1=***REDACTED***", str(message))

    @classmethod
    def info(cls, message: str):
        base_logger.info(cls.sanitize(message))

    @classmethod
    def error(cls, message: str):
        base_logger.error(cls.sanitize(message))

    @classmethod
    def warning(cls, message: str):
        base_logger.warning(cls.sanitize(message))
        
logger = SecureLogger()
