import logging
import logging.config
from config.settings import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
