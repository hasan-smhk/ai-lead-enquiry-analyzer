"""
core/logging_config.py
Sets up application-wide structured logging.
"""

import logging
from backend.app.core.config import settings


def configure_logging():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    return logging.getLogger("ai_lead_analyzer")


logger = configure_logging()
