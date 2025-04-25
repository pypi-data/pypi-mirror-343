"""
.. module:: caller
    :platform: Unix, Windows
    :synopsis: Get information about the application calling this module
"""

# Python Standard Libraries
import inspect
import logging
import os
from typing import Tuple

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


def get_caller() -> Tuple[str, str]:
    """Get calling file/path

    Returns:
        str: File path to root calling file

        str: Directory path of root caller
    """
    root_caller = inspect.stack()[-1][0].f_code.co_filename

    LOGGER.debug("Retrieved root calling file", extra={"path": root_caller})

    return root_caller, os.path.dirname(root_caller)
