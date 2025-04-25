"""
.. module:: args
    :platform: Unix, Windows
    :synopsis: Command Line Interface (CLI) argument functions
"""

# Python Standard Libraries
import argparse
import logging


# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


def args_to_dict(args: argparse.Namespace) -> dict:
    """Function to parse args to dict format

    Args:
        args (argparse.Namespace): CLI Arguments

    Returns:
        dict: Dictionary of key/value pair
    """
    return {arg: getattr(args, arg) for arg in vars(args)}
