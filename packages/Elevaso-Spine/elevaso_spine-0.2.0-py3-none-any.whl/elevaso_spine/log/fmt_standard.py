"""
.. module:: fmt_standard
    :platform: Unix, Windows
    :synopsis: Format log messages in standard format
        Best practices retrieved from
        https://docs.python.org/3/howto/logging-cookbook.html
"""

# Python Standard Libraries
import logging

# 3rd Party Libraries


# Project Specific Libraries
from elevaso_spine.fmt.sub import sub_value
from elevaso_spine.log.fmt import DEFAULT_PATTERN, BaseFormatter


LOGGER = logging.getLogger(__name__)


class StandardFormatter(BaseFormatter):
    """Custom class for logging in a standard format"""

    def format_func(self, val: dict, **kwargs) -> str:
        """Final output formatting function

        Args:
            val (dict): Dictionary of values to output

        Kwargs:
            extra_keys (list): List of keys that were included in the extra

        Returns:
            str: String to print
        """
        if self.fmt:
            output = sub_value(self.fmt, val, pattern=DEFAULT_PATTERN)
        else:
            output = val.get("msg", None)

        if self.kwargs.get("include_extra", False):
            output += " || Extra || " + "..".join(
                [
                    f"[{x} || {val[x]}]"
                    for x in kwargs.get("extra_keys", None)
                    if x in val.keys()
                ]
            )

        return output

    output_func = format_func
