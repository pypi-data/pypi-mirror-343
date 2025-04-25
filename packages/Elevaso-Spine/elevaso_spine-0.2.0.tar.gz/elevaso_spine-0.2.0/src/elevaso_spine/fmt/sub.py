"""
.. module:: sub
    :platform: Unix, Windows
    :synopsis: Substitute values from dictionary
"""

# Python Standard Libraries
from collections import OrderedDict
import logging
import re
from typing import Match

# 3rd Party Libraries


# Project Specific Libraries
from elevaso_spine.itr import itr

LOGGER = logging.getLogger(__name__)

DEFAULT_SUB_VALUE_REGEX = re.compile(r"\$\{(?P<var>[_\w\d]+)\}")


def sub_value(value: object, sub_values: dict, **kwargs) -> object:
    """Substitute values based on a RegEx pattern and return updated object

    Args:
        value (object): Python object to look for the pattern

        sub_values (dict): Dictionary of possible values to substitute

    Kwargs:
        pattern (re.Pattern, Optional): RegEx Pattern to search for, defaults
        to DEFAULT_SUB_VALUE_REGEX

        default_val (object, Optional): Default value for placeholder if not
        found in sub_values, default to None (returns original value/item)

        error_not_exist (bool, Optional): Raise error if the placeholder key
        does not exist in sub_values, default is False

        copy_val (bool, Optional): True/False contents of dict/list should be
        copied prior to modifying, defaults to True

    Raises:
        TypeError: If sub_values type is not dict or OrderedDict

    Returns:
        object: Updated object with values substituted
    """

    def __return_match_val(match: Match) -> str:
        """Return the match value

        Args:
            match (re.Match): RegEx Match

        Returns:
            str: String output
        """
        last_val = list(filter(None, match.groups()))[-1]

        output = __get_sub_value(
            last_val, sub_values, error_not_exist, default_val
        )

        if output and not isinstance(output, str):
            return str(output)

        return output

    def __sub_str(str_obj: str) -> str:
        """Substitute pattern with value for a given str

        Args:
            str_obj (str): String object to sub

        Returns:
            str: String output
        """
        return pattern.sub(__return_match_val, str_obj)

    if (
        not isinstance(sub_values, (dict, OrderedDict, list))
        and sub_values is not None
    ):
        raise TypeError(f"Invalid type of {type(sub_values)} for sub_values")

    pattern = kwargs.pop("pattern", DEFAULT_SUB_VALUE_REGEX)
    default_val = kwargs.pop("default_val", None)
    error_not_exist = kwargs.pop("error_not_exist", False)

    if sub_values and len(sub_values) > 0:
        return itr.iterate(
            value,
            copy_val=kwargs.pop("copy_val", True),
            custom_type_map={str: __sub_str},
        )

    return value


def __get_sub_value(
    key: str,
    sub_values: dict,
    error_not_exist: bool = False,
    default_val: object = None,
) -> object:
    """Get the value to be substituted

    Args:
        key (str): Key to search within the dict of values

        sub_values (dict): Dictionary of substitution values

        error_not_exist (bool, Optional): Raise error if the placeholder key
        does not exist in sub_values, default is False

        default_val (object, Optional): Default value for placeholder if not
        found in sub_values, default to None (returns original value/item)

    Raises:
        KeyError: If error_not_exist is True and placeholder value does not
        exist in sub_values

    Returns:
        object from the sub_values
    """
    try:
        return sub_values[key]
    except KeyError:
        if error_not_exist:
            raise KeyError(f"Value {key} not found")

        LOGGER.debug("Value %s not found, returning %s", key, default_val)
        return default_val
