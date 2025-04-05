import logging
import os


class MyLogger:
    def __init__(self, name="default", log_file=None, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False  # da ne duplira poruke

        formatter = logging.Formatter(
            fmt="[{asctime}] [{levelname}] {name}: {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{",
        )

        # Ako već postoji handler, ne dodaji nove
        if not self.logger.handlers:
            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

            # File handler (ako treba)
            if log_file:
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                fh = logging.FileHandler(log_file, encoding="utf-8")
                fh.setLevel(level)
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
