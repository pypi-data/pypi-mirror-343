"""
.. module:: append
    :platform: Unix, Windows
    :synopsis: Module for assisting with appending log values to
    all messages
"""

# Python Standard Libraries
import logging
from typing import Tuple

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


class LogAppend(logging.LoggerAdapter):
    """Custom class for managing appended data to all log messages"""

    def __init__(self, logger: logging.Logger, extra: dict, **kwargs):
        """Initialize an instance of the LogAppend class

        Args:
            logger (logging.Logger): Logger to associate with this class

            extra (dict): dictionary of values to append to each log record

        Kwargs:
            adapter_priority: If key exists in log message and adapter, does
            the adapter have priority, defaults to False
        """
        self.logger = logger
        self.extra = extra or {}
        self.__adapter_priority = kwargs.pop("adapter_priority", False)

        super().__init__(logger=logger, extra=extra)

    def process(self, msg: str, kwargs: dict) -> Tuple[str, dict]:
        """Process the CustomAdapter log message and append extra values if
        provided

        .. note::

            This actually processes the logging message, the custom handler is
            needed because if you pass in extra into the LoggerAdapter and
            extra into the individual logging, the standard Python
            LoggerAdapter will ignore/overwrite the logging extra.

        Args:
            msg (str): Message for the log

            kwargs (dict): Dictionary of keyword arguments

            .. note::
                Normally we would use :code:`**kwargs`, however, the logging
                process function passes in as a positional argument

        Returns:
            msg (str): Message for the log

            kwargs (dict): Updated keyword arguments
        """
        if self.__adapter_priority:
            extra = {**kwargs.get("extra", {}), **self.extra}
        else:
            extra = {**self.extra, **kwargs.get("extra", {})}

        kwargs["extra"] = extra

        return msg, kwargs
