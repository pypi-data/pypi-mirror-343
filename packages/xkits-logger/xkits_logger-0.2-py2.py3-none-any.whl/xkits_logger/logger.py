# coding:utf-8

from enum import Enum
import logging
import os
import sys
from time import time
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from typing import TextIO

from colorlog import ColoredFormatter
from colorlog.formatter import LogColors

from xkits_logger.attribute import __project__
from xkits_logger.colorful import Color


class OnceFilter(logging.Filter):
    def __init__(self, name: str = "logging_once_filter",
                 max_interval_seconds: int = 60):
        self.__max_interval: int = max(3, max_interval_seconds)
        self.__timestamp: float = time()
        self.__message = None
        super().__init__(name)

    def filter(self, record: logging.LogRecord) -> bool:
        current_message = (record.msg, record.args)
        if current_message != self.__message or self.timeout:
            self.__message = current_message
            self.__timestamp = time()
            return True
        return False

    @property
    def max_interval_seconds(self) -> int:
        return self.__max_interval

    @property
    def interval_seconds(self) -> float:
        return time() - self.__timestamp

    @property
    def timeout(self) -> bool:
        return self.interval_seconds > self.max_interval_seconds


class Logger:
    class LOG_LEVELS(Enum):
        CRITICAL = "fatal"
        ERROR = "error"
        WARNING = "warn"
        INFO = "info"
        DEBUG = "debug"
    ALLOWED_LOG_LEVELS: List[str] = [
        LOG_LEVELS.CRITICAL.value,
        LOG_LEVELS.ERROR.value,
        LOG_LEVELS.WARNING.value,
        LOG_LEVELS.INFO.value,
        LOG_LEVELS.DEBUG.value,
    ]
    DEFAULT_LOG_FORMAT: str = "%(log_color)s%(message)s"
    DEFAULT_LOG_COLORS: LogColors = {
        LOG_LEVELS.CRITICAL.name: "light_red",
        LOG_LEVELS.ERROR.name: "red",
        LOG_LEVELS.WARNING.name: "yellow",
        LOG_LEVELS.INFO.name: "green",
        LOG_LEVELS.DEBUG.name: "white",
    }

    def __init__(self):
        self.__initiated_names: Set[str] = set()

    def logger_initiated(self, name: str) -> bool:
        return name in self.__initiated_names

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        return logging.getLogger(name or __project__)

    def initiate_logger(self, logger: logging.Logger,
                        level: Optional[str] = None,
                        handlers: Optional[Iterable[logging.Handler]] = None,
                        filters: Optional[Iterable[logging.Filter]] = None):
        if self.logger_initiated(logger.name):
            logger.warning(F"logger {logger.name} is already initiated")

        if isinstance(level, str):
            name = level.upper()
            logger.setLevel(
                logging._nameToLevel[name]  # pylint: disable=protected-access
            )

        if filters is None:
            filters = [OnceFilter()]

        for _filter in filters:
            logger.addFilter(_filter)

        if handlers is None:
            handlers = [self.new_stream_handler(stream=sys.stdout)]

        for handler in handlers:
            logger.addHandler(handler)

        self.__initiated_names.add(logger.name)

    @classmethod
    def new_stream_handler(cls, stream: Optional[TextIO] = None,
                           fmt: Optional[str] = None,
                           log_colors: Optional[LogColors] = None
                           ) -> logging.StreamHandler:
        if fmt is None:
            fmt = cls.DEFAULT_LOG_FORMAT
        if log_colors is None:
            log_colors = cls.DEFAULT_LOG_COLORS
        formatter: logging.Formatter = ColoredFormatter(
            fmt=fmt, datefmt=None, log_colors=log_colors)
        handler: logging.StreamHandler = logging.StreamHandler(stream=stream)
        handler.setFormatter(formatter)
        return handler

    @classmethod
    def new_file_handler(cls, filename: str,
                         fmt: Optional[str] = None) -> logging.FileHandler:
        assert isinstance(filename, str), f"Unexpected type: {type(filename)}"
        dirname: str = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        assert os.path.isdir(dirname), f"{dirname} not an existing directory"
        formatter: logging.Formatter = ColoredFormatter(
            fmt=fmt, datefmt=None, no_color=True)
        handler: logging.FileHandler = logging.FileHandler(filename=filename)
        handler.setFormatter(formatter)
        return handler

    @classmethod
    def stdout(cls, context: Any):
        '''Output string to sys.stdout.'''
        sys.stdout.write(f"{context}\n")
        sys.stdout.flush()

    @classmethod
    def stdout_yellow(cls, context: Any):
        '''Output string to sys.stdout with yellow color.'''
        cls.stdout(Color.yellow(context))

    @classmethod
    def stdout_green(cls, context: Any):
        '''Output string to sys.stdout with green color.'''
        cls.stdout(Color.green(context))

    @classmethod
    def stdout_red(cls, context: Any):
        '''Output string to sys.stdout with red color.'''
        cls.stdout(Color.red(context))

    @classmethod
    def stderr(cls, context: Any):
        '''Output string to sys.stderr.'''
        sys.stderr.write(f"{context}\n")
        sys.stderr.flush()

    @classmethod
    def stderr_yellow(cls, context: Any):
        '''Output string to sys.stderr with yellow color.'''
        cls.stderr(Color.yellow(context))

    @classmethod
    def stderr_green(cls, context: Any):
        '''Output string to sys.stderr with green color.'''
        cls.stderr(Color.green(context))

    @classmethod
    def stderr_red(cls, context: Any):
        '''Output string to sys.stderr with red color.'''
        cls.stderr(Color.red(context))
