"""
.. module:: fmt_json
    :platform: Unix, Windows
    :synopsis: Format log messages in JSON format
        Best practices retrieved from
        https://docs.python.org/3/howto/logging-cookbook.html
"""

# Python Standard Libraries
import json
import logging

# 3rd Party Libraries


# Project Specific Libraries
from elevaso_spine.log.fmt import BaseFormatter


LOGGER = logging.getLogger(__name__)


class JsonFormatter(BaseFormatter):
    """Custom class for logging in Json format"""

    def format_func(self, val: dict, **kwargs) -> \
            str:  # pylint: disable=unused-argument
        """Final output formatting function

        Args:
            val (dict): Dictionary of values to output in JSON

        Returns:
            str: JSON string
        """
        return json.dumps(val, default=str)

    output_func = format_func
