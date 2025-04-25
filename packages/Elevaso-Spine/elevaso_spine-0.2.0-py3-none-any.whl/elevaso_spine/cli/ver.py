"""
.. module:: ver
    :platform: Unix, Windows
    :synopsis: Command Line Interface (CLI) version functions
"""

# Python Standard Libraries
import argparse
import logging

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


def add_version(parser_obj: argparse.ArgumentParser, version: object):
    """Add CLI version argument

    Args:
        parser_obj (argparse.ArgumentParser) : Parser to add version

        version (object): Version to add/display
    """
    if version:
        parser_obj.add_argument(
            "-v",
            "--version",
            help="Command Line Interface Version",
            action="version",
            version=version,
        )
    else:
        LOGGER.debug("No version provided, skipping")
