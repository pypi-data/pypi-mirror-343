"""
.. module:: now
    :platform: Unix, Windows
    :synopsis: Module for providing current date/time
"""

# Python Standard Libraries
import datetime
import logging

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


def utc_now() -> datetime.datetime:
    """Current date & time in UTC time with timezone

    Returns:
        datetime.datetime representing current timestamp
    """
    return datetime.datetime.now(datetime.timezone.utc)
