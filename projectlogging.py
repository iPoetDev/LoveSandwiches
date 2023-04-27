#!/user/bin/env python3
"""Module Run GSheet."""

# 0.1 Core Imports
import logging
import sys
import warnings

from loguru import logger as LOGR

from settings import HOST, HTTPS, LOGS

# Logging
SINK_ERROR: str = "error.log"
SINK_PROJECT: str = "lovesand.log"
ENABLED: bool = True
DISABLED: bool = False
FORMAT: str = "{time} | {level} || {message}"
LEVEL: str = "DEBUG"
METRE: str = "KB"
ROTATEON: str = f"500 {METRE}"

CONFIG = {
        "handlers": [
                {  # Standard Error Handler
                        "sink": sys.stderr,
                        "colorize": ENABLED,
                        "format": FORMAT,
                        "level": LEVEL,
                        "enqueue": DISABLED,
                        "backtrace": ENABLED,
                        "diagnose": ENABLED,
                        },
                {  # Error Handler
                        "sink": SINK_ERROR,
                        "level": LEVEL,
                        "enqueue": ENABLED,
                        "format": FORMAT,
                        "backtrace": ENABLED,
                        "diagnose": ENABLED,
                        },
                {  # Project Handler
                        "sink": SINK_PROJECT,
                        "level": LEVEL,
                        "enqueue": DISABLED,
                        "format": FORMAT,
                        "backtrace": ENABLED,
                        "diagnose": ENABLED,
                        },
                ],
        }


def configure_logging(logname: str, DOESWARN: bool = True):
    logging.basicConfig(filename=logname, level=logging.DEBUG)
    logging.captureWarnings(DOESWARN)
    logging.info('Running on %s on port %d', HOST, HTTPS)
    warnings.filterwarnings("ignore", category=DeprecationWarning)


def configure_loguru():
    """
    Configure loguru logger.
    1: System Error
    2: Error Logging
    3: Project Logging
    """
    LOGR.configure(**CONFIG)
    return LOGR


configure_logging(LOGS)
