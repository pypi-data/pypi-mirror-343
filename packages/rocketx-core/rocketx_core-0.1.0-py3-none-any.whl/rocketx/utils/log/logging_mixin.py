# encoding: utf8
import abc
import enum
import logging
import re
import sys
from io import TextIOBase, UnsupportedOperation
from logging import Handler, StreamHandler, Logger
from typing import IO, TYPE_CHECKING, Any, Optional, TypeVar, cast


# 7-bit C1 ANSI escape sequences
ANSI_ESCAPE = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
_T = TypeVar("_T")

class SetContextPropagate(enum.Enum):
    """
    Sentinel objects for log propagation contexts.

    :meta private:
    """
    # If a `set_context` function wants to _keep_ propagation set on its logger it needs to return this
    # special value.
    MAINTAIN_PROPAGATE = object()
    # Don't use this one anymore!
    DISABLE_PROPAGATE = object()


class LoggingMixin:
    """Super-class to have a logger configured with the class name."""
    log: logging.Logger | None = None
    _log_config_logger_name: Optional[str] = None 
    _logger_name: Optional[str] = None

    def __init__(self, context=None):
        self._set_context(context)
        super().__init__()

    @staticmethod
    def _create_logger_name(
        logged_class: type[_T],
        log_config_logger_name: Optional[str] = None,
        class_logger_name: Optional[str] = None,
    ) -> str:
        """
        Generate a logger name for the given `logged_class`.

        By default, this function returns the `class_logger_name` as logger name. If it is not provided,
        the `{class.__module__}.{class.__name__}` is returned instead. When a `parent_logger_name` is provided,
        it will prefix the logger name with a separating dot.
        """
        logger_name: str =  class_logger_name or f"{logged_class.__module__}.{logged_class.__name__}"

        if log_config_logger_name:
            return f"{log_config_logger_name}.{logger_name}" if logger_name else log_config_logger_name

        return logger_name

    @classmethod
    def _get_log(cls, obj: Any, clazz: type[_T]) -> Logger:
        if obj.log is None:
            logger_name: str = cls._create_logger_name(
                logged_class=clazz,
                log_config_logger_name=obj._log_config_logger_name,
                class_logger_name=obj._logger_name,
            )
            obj.log = logging.getLogger(logger_name)

        return obj.log

    @classmethod
    def logger(cls):
        """Return a logger instance."""
        return LoggingMixin._get_log(obj=cls, clazz=cls)


    def _set_context(self, context: Any) -> None:
        if context is not None:
            set_context(self.log, context)


def set_context(logger: Logger, value: Any) -> None:
    """
    Walk the tree of loggers and try to set the context for each handler.

    :param logger: logger
    :param value: value to set
    """
    while logger:
        orig_propagate = logger.propagate

        for handler in logger.handlers:
            # Not all handlers need to have context passed in so we ignore
            # the error when handlers do not have set_context defined.

            # Don't use `getatrr` so we have type checking. And we don't care if handler is actually a
            # FileTaskHandler, it just needs to have a set_context function!
            if hasattr(handler, "set_context"):
                from .file_handler import FileHandler  # noqa: TC001

                flag = cast(FileHandler, handler).set_context(value)
                # By default, we disable propagate once we have configured the logger, unless that handler
                # explicitly asks us to keep it on.
                if flag is not SetContextPropagate.MAINTAIN_PROPAGATE:
                    logger.propagate = False
    
        if orig_propagate is True:
            # If we were set to propagate before we turned if off, then keep passing set_context up
            logger = logger.parent
        else:
            break