"""
.. module:: eval
    :platform: Unix, Windows
    :synopsis: Functions to evaluate a rule
"""

# Python Standard Libraries
import logging

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


def format_value(key: str, record: dict, output: list, **kwargs):
    """Format a value for evaluation

    Args:
        key (str): Key within the record

        record (dict): Single record being evaluated

        output (list): List of output

    Kwargs:
        cls (object): Rule engine class

        operator_func (object): Function to execuate for operator

        value (object): Value to be compared to

    Raises:
        KeyError if key not found in record and val_if_no_key_found = False
    """
    cls = kwargs["cls"]
    operator_func = kwargs["operator_func"]
    value = kwargs["value"]

    if key not in record.keys() and not cls.eval_if_no_key_found:
        cls.__raise_exception__(KeyError(f"{key} not found in record"))
    else:
        output.append(
            operator_func(
                record.get(key, cls.default_value_no_key_found),
                value,
            )
        )


def format_case_sensitive(value: object, case_sensitive: bool) -> object:
    """Check and format case sensitive value

    Args:
        value (object): Value to format

        case_sensitive (bool): True/False if value is case sensitive

    Returns:
        object representing formatted value
    """
    if isinstance(value, str):
        if case_sensitive:
            return value

        return value.lower()

    return value


def format_trim(value: object, trim_strings: bool) -> object:
    """Check and formats strings for empty spaces

    Args:
        value (object): Value to format

        trim_strings (bool): True/False if string should be trimmed of empty
        spaces

    Returns:
        object representing formatted value
    """
    if isinstance(value, str):
        if not trim_strings:
            return value

        return value.strip()

    return value


def format_none(value: object, empty_equals_none: bool) -> object:
    """Check and formats empty strings to None

    Args:
        value (object): Value to format

        empty_equals_none (bool): True/False if string should be converted to
        None if empty

    Returns:
        object representing formatted value
    """
    if isinstance(value, str):
        if empty_equals_none and value == "":
            return None

        return value

    return value
