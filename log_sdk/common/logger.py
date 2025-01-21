from datetime import datetime, timezone
import os
import logging
from logging.handlers import RotatingFileHandler


class LoggerConfig:

    
    @staticmethod
    def init_log_file(directory):


        if not os.path.exists(directory):
            os.makedirs(directory)

        log_file = os.path.join(directory, f"apm_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.log")
        handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=3)
        formatter = logging.Formatter('%(asctime)s - %(message)s')

        handler.setFormatter(formatter)
        logger = logging.getLogger("apm_logger")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        return logger
    