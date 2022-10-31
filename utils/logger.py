import logging

import constants
from utils.custom_formatter import CustomFormatter


class Logger:
    def __init__(self, log_level: int = None):
        if log_level is None:
            log_level = logging.ERROR

        logging.basicConfig(level=log_level, format=constants.LOGGING_FORMAT)
        logger = logging.getLogger(constants.APP_NAME)
        logger.setLevel(log_level)
        logger.log(logging.WARNING, f"Set log level to {log_level}")
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(log_level)

        ch.setFormatter(CustomFormatter())

        logger.addHandler(ch)
        self.logger = logger

    def log(self, message: str, level: int = None) -> None:
        if level is None:
            level = logging.INFO
        self.logger.setLevel(level)
        self.logger.log(level, f" {message}")
