"""
.. module:: var
    :platform: Unix, Windows
    :synopsis: Work with environment variables
"""

# Python Standard Libraries
import logging
import os

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


def get_var(name: str, default_val: object = None) -> object:
    """Retrieve environment variable value if exists

    Args:
        name (str): Name of the environment variable

        default_val (object, Optional): Default value to return,
        defaults to None

    Returns:
        object: Python object value, or None if not exists
    """
    return os.environ.get(name, default_val)


def set_var(
    name: str, val: str, overwrite: bool = False, set_val: bool = True
) -> bool:
    """Set or update an environment variable

    Args:
        name (str): Environment variable name

        val (str): Value for the environment variable

        overwrite (bool, Optional): Determines if value should be overwritten
        if Variable already exists, defaults to False

        set_val (bool, Optional): Determines if the value should be
        set or just "mocked", defaults to True

    Returns:
        bool: True/False if successfully updated
    """
    if set_val and name in os.environ.keys() and not overwrite:
        LOGGER.debug(
            "Overwrite is False, skipping environment variable %(name)s",
            {"name": name},
        )

        return False

    if set_val:
        LOGGER.debug("Setting environment variable %(name)s", {"name": name})

        os.environ[name] = val

    return True
