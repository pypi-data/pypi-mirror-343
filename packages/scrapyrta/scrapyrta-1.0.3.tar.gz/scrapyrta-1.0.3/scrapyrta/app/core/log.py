import logging
import sys
from functools import lru_cache

from scrapyrta.app.core.config import app_settings


@lru_cache
def get_logger(name: str = "scrapyrta") -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(app_settings.LOG_LEVEL)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(app_settings.LOG_LEVEL)

        formatter = logging.Formatter(
            "[%(levelname)s] [%(asctime)s] "
            "[%(filename)s:%(funcName)s:%(lineno)d]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = get_logger()
