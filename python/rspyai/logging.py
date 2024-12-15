"""Logging utilities for rspyai."""

import logging
from typing import Literal

from rich.console import Console
from rich.logging import RichHandler


def get_logger(name: str) -> logging.Logger:
    """Get a logger nested under rspyai namespace.

    Args:
        name: the name of the logger, which will be prefixed with 'rspyai.'

    Returns:
        a configured logger instance
    """
    return logging.getLogger(f'rspyai.{name}')


def configure_logging(
    level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO',
) -> None:
    """Configure logging for rspyai.

    Args:
        level: the log level to use
    """
    logging.basicConfig(
        level=level,
        format='%(message)s',
        handlers=[RichHandler(console=Console(stderr=True), rich_tracebacks=True)],
    )
