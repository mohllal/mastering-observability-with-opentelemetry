import logging
import sys

from opentelemetry._logs import get_logger_provider
from opentelemetry.sdk._logs import LoggingHandler


def init_logger(name: str = "logger") -> logging.Logger:
    """Set up a logger with both console and OpenTelemetry handlers."""

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # OpenTelemetry handler
    otel_handler = LoggingHandler(
        level=logging.INFO,
        logger_provider=get_logger_provider()
    )
    otel_handler.setFormatter(formatter)
    logger.addHandler(otel_handler)

    return logger
