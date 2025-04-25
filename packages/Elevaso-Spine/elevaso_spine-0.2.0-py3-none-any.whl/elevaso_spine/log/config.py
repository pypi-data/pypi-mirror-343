"""
.. module:: config
    :platform: Unix, Windows
    :synopsis: Functions to support log sub-modules or project setup
"""

# Python Standard Libraries
import json
import logging
import logging.config
import os

# 3rd Party Libraries


# Project Specific Libraries
from elevaso_spine.app.caller import get_caller
from elevaso_spine.fmt.sub import sub_value


LOGGER = logging.getLogger(__name__)

COMMON_LOG_APPEND = {}

DEFAULT_LOG_CONFIG = {
    "standard": os.path.join(
        os.path.dirname(__file__), "data", "default_logging_standard.json"
    ),
    "json": os.path.join(
        os.path.dirname(__file__), "data", "default_logging_json.json"
    ),
}


def setup(
    path: str = None,
    log_format: str = None,
    log_config: dict = None,
    **kwargs,
):
    """Function to setup initial logging configuration

    Args:
        path (str, Optional): Path to the directory of the logging config,
        defaults to calling object path & data directory

        .. note::
            If log_config is None and path is None, then the path to the
            calling object will be used as the root directory. This function
            will look for a file named log_config (either .json, .yml, .yaml)
            in /data/directory

        log_format (str, Optional): Format of the logging (standard or json),
        defaults to None

        .. note::
            If log_format is None, it will attempt to load from the environment
            variable LOG_FORMAT. If that does not exist, standard will be
            used as the default value

        log_config (dict, Optional): Logging configuration (to override
        defaults and not retrieve from a file), defaults to None

    Kwargs:
        log_level (str, Optional): Log level to set the global LOGGER to,
        defaults to None

        .. note::
            If log_level is None, it will attempt to load from the environment
            variable LOG_LEVEL. If that does not exist, INFO will be
            used as the default value
    """
    log_format = __get_log_format(log_format)

    log_level = (
        kwargs.pop("log_level", os.environ.get("LOG_LEVEL", None)) or None
    )

    log_config = __get_log_config(log_format, log_config, path)

    log_config = sub_value(log_config, dict(os.environ), copy_val=False)

    if log_level is not None and log_config.get("root", None):
        log_config.update(
            {
                "root": {
                    **log_config.get("root"),
                    "level": logging.getLevelName(log_level),
                }
            }
        )

    log_config = __append_extra(log_config, __get_common(**kwargs))

    logging.config.dictConfig(log_config)


def __get_log_config(
    log_format: str, log_config: dict = None, path: str = None
) -> dict:
    """Checks or retrieves logging configuration

    Args:
        log_format (str): Logging format

        log_config (dict, Optional): Logging configuration (to override
        defaults and not retrieve from a file), defaults to None

        path (str, Optional): Path to the directory of the logging config,
        defaults to calling object path & data directory

        .. note::
            If log_config is None and path is None, then the path to the
            calling object will be used as the root directory. This function
            will look for a file named log_config (either .json, .yml, .yaml)
            in /data/directory

    Returns:
        dict: Dictionary of logging configuration

    Raises:
        ValueError if no configuration is found
    """
    if log_config is None:
        if path is None:
            _, path = get_caller()

        log_config = __load_log_config(
            os.path.join(path, "log_config.json"), log_format
        )

    if log_config is not None:
        return log_config

    raise ValueError("log_config cannot be None")  # pragma: no cover


def __get_log_format(log_format: str = None) -> str:
    """Get log format from value, environment, or default

    Args:
        log_format (str, Optional): Value provided by user during setup

    Returns:
        str of the log format

    Raises:
        ValueError: if log_format is invalid
    """
    log_format = (
        log_format or os.environ.get("LOG_FORMAT") or "standard"
    ).lower()

    if log_format not in DEFAULT_LOG_CONFIG.keys():
        raise ValueError(f"Invalid log_format specified: {log_format}")

    return log_format


def __get_common(**kwargs) -> dict:
    """Append common environment variables to log output

    Kwargs:
        aws_context (object, Optional): Amazon Web Services Lambda Context
        Object
    """
    append_dict = {
        v: os.environ[k]
        for k, v in COMMON_LOG_APPEND.items()
        if k in os.environ.keys()
    }

    return append_dict


def __append_extra(log_config: dict, extra_vals: dict) -> dict:
    """Append extra values to the Json Formatter

    Args:
        extra_vals (dict): Dictionary of extra values
    """
    for _, value in log_config.get("formatters", {}).items():
        if value.get("()", None) == "spine.log.fmt_json.JsonFormatter":
            value["extra"] = {**value.get("extra", {}), **extra_vals}

    return log_config


def __load_file(path: str, name: str) -> dict:
    """Load a logging config file

    Args:
        path (str): Path to the file

        name (str): File name

    Returns:
        dict: Dictionary of logging configuration
    """
    if os.path.exists(os.path.join(path, name)) and os.path.isfile(
        os.path.join(path, name)
    ):
        with open(os.path.join(path, name), "r") as file:
            return json.load(file)
    else:
        return None


def __load_log_config(path: str, log_format: str) -> dict:
    """Load log config based on root path or default

    Args:
        path (str): Path to check first

        log_format (str): Log Format

    Returns:
        dict: Dictionary of logging configuration
    """
    log_config = __load_file(*(os.path.split(path)))

    if not log_config:
        LOGGER.debug(
            "File not found at %(path)s, using library default", {"path": path}
        )
        log_config = __load_file(
            *(os.path.split(DEFAULT_LOG_CONFIG.get(log_format)))
        )

    return log_config
