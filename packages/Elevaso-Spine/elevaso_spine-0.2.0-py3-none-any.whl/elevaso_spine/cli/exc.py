"""
.. module:: exc
    :platform: Unix, Windows
    :synopsis: Command Line Interface (CLI) execution functions
"""

# Python Standard Libraries
import logging

# 3rd Party Libraries


# Project Specific Libraries
from elevaso_spine.cli.args import args_to_dict
from elevaso_spine.cli.setup import build
from elevaso_spine.cli.ver import add_version
from elevaso_spine.environ.load import load_env
from elevaso_spine.log.config import setup

LOGGER = logging.getLogger(__name__)


def __get_log_level(args: dict, quiet_flag: str, debug_flag: str) -> str:
    """Determine the log level based on args

    Args:
        args (dict): Dictionary of arguments

        quiet_flag (str): Argument name to determine if log level is quiet

        debug_flag (str): Argument name to determine if log level is debug

    Returns:
        str Log level in string format
    """
    if args.get(quiet_flag, False):
        log_level = "WARN"
    elif args.get(debug_flag, False):
        log_level = "DEBUG"
    else:
        log_level = "INFO"

    return log_level


def exec_func(func_map: object, function_flag: str, args: dict):
    """Execute command line interface function/command

    Args:
        func_map (object): Object containing the functions
        to execute for CLI commands

        function_flag (str): Argument name to determine the function/command
        to execute

        args (dict): Dictionary of arguments from command line interface

    Raises:
        AttributeError if function/command does not exist
    """
    exec_func_flag = args.get(function_flag, None)

    if exec_func_flag is None:
        return

    if isinstance(func_map, dict):
        func = func_map.get(exec_func_flag, None)
    else:
        func = getattr(func_map, exec_func_flag)

    if func:
        func(**args)
    else:
        raise AttributeError(f"Command/Function {exec_func_flag} not found")


def main(config_path: str, func_map: dict, func_args: dict = None, **kwargs):
    """Main command line interface function

    Args:
        config_path (str): Path to configuration file

        func_map (dict): Dictionary of functions to execute based on CLI func
        argument

        func_args (dict, Optional): Dictionary of arguments to pass to CLI
        func, defaults to None

    Kwargs:
        cli_version (str): Current version of the CLI program,
        defaults to None

        quiet_flag (str): Name of the CLI argument for quiet logging,
        defaults to quiet

        debug_flag (str): Name of the CLI argument for verbose logging,
        defaults to verbose

        log_format (str): Type of log format (see
        spine.log.config.DEFAULT_LOG_CONFIG for possible values), defaults
        to standard

        function_flag (str): Name of the CLI argument for the function name
        (exists as key in func_map), defaults to func
    """
    parser = build(path=config_path)
    func_args = func_args or {}

    add_version(parser, kwargs.pop("cli_version", None))

    args = args_to_dict(parser.parse_args())

    setup(
        log_level=__get_log_level(
            args,
            kwargs.pop("quiet_flag", "quiet"),
            kwargs.pop("debug_flag", "verbose"),
        ),
        log_format=kwargs.pop("log_format", "standard"),
    )

    load_env()

    exec_func(
        func_map,
        kwargs.pop("function_flag", "func"),
        args={**func_args, **args},
    )
