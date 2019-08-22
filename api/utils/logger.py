import logging
import os
import sys
from typing import Any

DEFAULT_LOG_LEVEL = getattr(logging, os.environ.get("LOG_LEVEL", "DEBUG").upper())

def get_logger(logger_name) -> logging.Logger:
    logger: Any = logging.getLogger(logger_name)
    logger.setLevel(DEFAULT_LOG_LEVEL)
    ch: Any = logging.StreamHandler(sys.stdout)
    ch.setLevel(DEFAULT_LOG_LEVEL)
    logger.addHandler(ch)

    return logger
