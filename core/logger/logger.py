import os
import errno
import logging
import logging.handlers

from core.patterns.singleton import Singleton

from .formatter import LogFormatter


class Logger(metaclass=Singleton):
    LOGGER_MAP: dict = {}

    def load_config(self, config: dict, task_id: int = 0):
        logger_conf = config["logger"]
        if isinstance(logger_conf, dict):
            self._init_loggers(logger_conf, task_id)
        else:
            raise ValueError

    def _init_loggers(self, logger_conf: dict, task_id: int):
        for key in logger_conf.keys():
            conf_dict: dict = logger_conf[key]
            if isinstance(conf_dict, dict):
                self.LOGGER_MAP[key] = logging.getLogger(key)
                canonical_file_path = self._build_canonical_file_path(
                    base_path=conf_dict["path"], filename=conf_dict["filename"]
                )

                options = {
                    "logging": "info",
                    "log_file_prefix": None,
                    "log_file_max_size": 1024 * 1024,
                    "log_file_num_backups": 10,
                    "log_to_stderr": None,
                }
                options["level"] = conf_dict["level"]
                options["log_file_prefix"] = canonical_file_path
                self._enable_pretty_logging(
                    logger=self.LOGGER_MAP[key],
                    options=options,
                    task_id=task_id,
                )
            else:
                raise ValueError

    def _build_canonical_file_path(self, base_path: str, filename: str) -> str:
        try:
            if not os.path.isdir(base_path):
                os.makedirs(base_path, 0o755)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(base_path):
                pass
            else:
                raise

        canonical_file_path = base_path
        if not canonical_file_path.endswith("/"):
            canonical_file_path += "/"
        canonical_file_path += filename
        return canonical_file_path

    def _enable_pretty_logging(
        self, logger: logging.Logger, options: dict, task_id: int = 0
    ):
        logger.setLevel(getattr(logging, options["logging"].upper()))
        logger.propagate = False

        if options["log_file_prefix"]:
            channel = logging.handlers.RotatingFileHandler(
                filename=options["log_file_prefix"],
                maxBytes=options["log_file_max_size"],
                backupCount=options["log_file_num_backups"],
            )
            channel.setFormatter(LogFormatter(task_id=task_id, color=False))
            if logger.hasHandlers():
                logger.handlers.clear()
            logger.addHandler(channel)

        if options["log_to_stderr"] or (
            not options["log_to_stderr"] and not logger.handlers
        ):
            channel = logging.StreamHandler()
            channel.setFormatter(LogFormatter(task_id=task_id, color=False))
            if logger.hasHandlers():
                logger.handlers.clear()
            logger.addHandler(channel)

    def get_logger(self, logger: str) -> logging.Logger:
        return self.LOGGER_MAP[logger]
