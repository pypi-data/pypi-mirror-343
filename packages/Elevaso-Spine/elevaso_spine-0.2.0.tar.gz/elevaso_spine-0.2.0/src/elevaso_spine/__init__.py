"""
.. module:: __init__
    :platform: Unix, Windows
    :synopsis: Main module entry point
"""
# Python Standard Libraries
import logging

# 3rd Party Libraries


# Code Repository Sub-Packages


__version__ = "0.2.0"

# Defining a logger for this library to separate out log messages from
# applications leveraging the library
LOGGER = logging.getLogger("elevaso-spine")

# Set up logging to /dev/null like a library is supposed to
# https://docs.python.org/3.10/howto/logging.html#configuring-logging-for-a-library
LOGGER.addHandler(logging.NullHandler())
