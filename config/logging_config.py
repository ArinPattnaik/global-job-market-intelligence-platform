"""
Centralized Logging Configuration
====================================
Structured logging with file rotation and consistent formatting.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config.settings import (
    LOG_BACKUP_COUNT,
    LOG_DATE_FORMAT,
    LOG_DIR,
    LOG_FORMAT,
    LOG_LEVEL,
    LOG_MAX_BYTES,
)

_configured = False


def setup_logging(name: str = "gjmip") -> logging.Logger:
    """
    Configure and return a logger with console + rotating file handlers.

    Calling this multiple times with the same name returns the same
    logger without adding duplicate handlers.
    """
    global _configured

    logger = logging.getLogger(name)

    if _configured and logger.handlers:
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    logger.propagate = False

    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Rotating file handler
    log_file = LOG_DIR / f"{name}.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    _configured = True
    return logger


def get_logger(module_name: str) -> logging.Logger:
    """Get a child logger under the main application logger."""
    parent = setup_logging()
    return parent.getChild(module_name)
