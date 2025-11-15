"""
Structured logger utility with structlog package (Phase 2B).

Generated - do not edit directly.
"""

import structlog
import logging
import sys
from typing import Optional
from ..config import SdkConfig

_logger: Optional[structlog.BoundLogger] = None


def get_logger(config: Optional[SdkConfig] = None) -> structlog.BoundLogger:
    """Get or create a structured logger instance.

    Args:
        config: SDK configuration (optional)

    Returns:
        Structured logger instance
    """
    global _logger

    if _logger is not None:
        return _logger

    log_level = (config.log_level if config else None) or "error"

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            (
                structlog.processors.JSONRenderer()
                if (config.structured_logging if config else False)
                else structlog.dev.ConsoleRenderer()
            ),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Set standard library logging level
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.ERROR),
    )

    _logger = structlog.get_logger("finatic_sdk")

    return _logger
