"""
Logging utilities for Books2Skill
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

from books2skill.config import settings


def setup_logging(
    level: Optional[str] = None,
    log_file: Optional[Path] = None,
    enable_rich: bool = True,
) -> logging.Logger:
    """
    Setup logging configuration

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        enable_rich: Enable rich console output

    Returns:
        Configured logger instance
    """
    # Install rich traceback for better error messages
    install_rich_traceback(show_locals=settings.DEBUG)

    # Determine log level
    if level is None:
        level = settings.LOG_LEVEL if not settings.DEBUG else "DEBUG"

    log_level = getattr(logging, level.upper())

    # Create logger
    logger = logging.getLogger("books2skill")
    logger.setLevel(log_level)

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler
    if enable_rich:
        console_handler = RichHandler(
            rich_tracebacks=True,
            tracebacks_show_locals=settings.DEBUG,
            show_time=settings.DEBUG,
            show_path=settings.DEBUG,
            console=Console(stderr=True),
        )
    else:
        console_handler = logging.StreamHandler(sys.stderr)

    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file is None:
        log_file = settings.LOG_FILE

    if log_file:
        # Ensure log directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)

        if settings.LOG_FORMAT == "json":
            from pythonjsonlogger import jsonlogger

            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            formatter = jsonlogger.JsonFormatter(
                "%(asctime)s %(name)s %(levelname)s %(message)s"
            )
            file_handler.setFormatter(formatter)
        else:
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_formatter = logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_formatter)

        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)

    # Add log rotation if specified
    if settings.LOG_ROTATION:
        try:
            from logging.handlers import RotatingFileHandler

            if log_file:
                # Remove existing file handler
                for handler in logger.handlers[:]:
                    if isinstance(handler, logging.FileHandler):
                        logger.removeHandler(handler)

                # Add rotating file handler
                max_bytes = parse_size(settings.LOG_ROTATION)
                backup_count = 5  # Keep 5 backup files

                rotating_handler = RotatingFileHandler(
                    log_file,
                    maxBytes=max_bytes,
                    backupCount=backup_count,
                    encoding="utf-8",
                )

                if settings.LOG_FORMAT == "json":
                    from pythonjsonlogger import jsonlogger
                    formatter = jsonlogger.JsonFormatter(
                        "%(asctime)s %(name)s %(levelname)s %(message)s"
                    )
                else:
                    formatter = logging.Formatter(
                        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                    )

                rotating_handler.setFormatter(formatter)
                rotating_handler.setLevel(log_level)
                logger.addHandler(rotating_handler)

        except ImportError:
            logger.warning("RotatingFileHandler not available, using regular file handler")

    # Log startup message
    logger.info(f"Books2Skill logging initialized (level: {level})")
    if log_file:
        logger.info(f"Log file: {log_file.absolute()}")

    if settings.DEBUG:
        logger.debug("Debug mode enabled")

    return logger


def parse_size(size_str: str) -> int:
    """
    Parse size string (e.g., "10 MB", "1 GB") to bytes

    Args:
        size_str: Size string with unit

    Returns:
        Size in bytes
    """
    size_str = size_str.upper().strip()

    # Define units
    units = {
        "B": 1,
        "KB": 1024,
        "MB": 1024 ** 2,
        "GB": 1024 ** 3,
        "TB": 1024 ** 4,
    }

    # Find unit
    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            number = float(size_str[:-len(unit)].strip())
            return int(number * multiplier)

    # If no unit found, assume bytes
    try:
        return int(float(size_str))
    except ValueError:
        raise ValueError(f"Invalid size format: {size_str}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(f"books2skill.{name}")


class LoggingContext:
    """Context manager for temporary logging configuration"""

    def __init__(
        self,
        level: Optional[str] = None,
        log_file: Optional[Path] = None,
        enable_rich: bool = True,
    ):
        self.level = level
        self.log_file = log_file
        self.enable_rich = enable_rich
        self.original_handlers = None
        self.original_level = None

    def __enter__(self):
        logger = logging.getLogger("books2skill")

        # Save original state
        self.original_handlers = logger.handlers[:]
        self.original_level = logger.level

        # Clear existing handlers
        logger.handlers.clear()

        # Setup new logging
        setup_logging(
            level=self.level,
            log_file=self.log_file,
            enable_rich=self.enable_rich,
        )

        return logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger = logging.getLogger("books2skill")

        # Restore original state
        logger.handlers.clear()
        for handler in self.original_handlers:
            logger.addHandler(handler)
        logger.setLevel(self.original_level)


# Default logger
logger = setup_logging()
