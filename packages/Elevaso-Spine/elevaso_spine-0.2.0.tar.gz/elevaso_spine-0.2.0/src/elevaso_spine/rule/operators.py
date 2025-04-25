"""
.. module:: operators
    :platform: Unix, Windows
    :synopsis: Additional operator functions
"""

# Python Standard Libraries
import logging
import operator

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


def not_contains(value: str, values: list) -> bool:
    """Check if a value is not in a list

    Args:
        values (list): List of values to check

        value (str): Value to check in the list

    Returns:
        bool if value is not in list
    """
    return value not in values


def contains(value: str, values: list) -> bool:
    """Check if a value is in a list

    Args:
        values (list): List of values to check

        value (str): Value to check in the list

    Returns:
        bool if value is in list
    """
    return value in values


# NOTE: These must remain at the bottom
OPERATORS = {
    "==": operator.eq,
    "!=": operator.ne,
    "<=": operator.le,
    ">=": operator.ge,
    "<": operator.lt,
    ">": operator.gt,
    "in": contains,
    "!in": not_contains,
}

CONDITIONS = {
    "or": operator.or_,
    "OR": operator.or_,
    "and": operator.and_,
    "AND": operator.and_,
}
