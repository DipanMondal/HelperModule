import logging
import os
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(
        self,
        name: str,
        log_dir: str = "logs",
        max_log_size: int = 5 * 1024 * 1024,  # 5MB
        backup_count: int = 3,
        file_handle: bool = True,
        console_handle: bool = True,
    ):
        """
        Independent logger instance.

        :param name: Unique logger name
        :param log_dir: Directory to store logs
        :param max_log_size: Max size per log file
        :param backup_count: Number of backup files
        """

        self.name = name
        self.log_dir = log_dir
        self.max_log_size = max_log_size
        self.backup_count = backup_count

        # Create log directory if not exists
        os.makedirs(self.log_dir, exist_ok=True)

        # Create logger with unique name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False  # Prevent duplicate logs

        # Avoid adding handlers multiple times
        if not self.logger.handlers:
            formatter = logging.Formatter(
                "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s"
            )

            if file_handle:
                log_file_path = os.path.join(self.log_dir, f"{self.name}.log")
                file_handler = RotatingFileHandler(
                    log_file_path,
                    maxBytes=self.max_log_size,
                    backupCount=self.backup_count,
                )
                file_handler.setFormatter(formatter)
                file_handler.setLevel(logging.DEBUG)
                self.logger.addHandler(file_handler)

            if console_handle:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                console_handler.setLevel(logging.INFO)
                self.logger.addHandler(console_handler)

    # Wrapper methods
    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

    def exception(self, message: str):
        self.logger.exception(message)