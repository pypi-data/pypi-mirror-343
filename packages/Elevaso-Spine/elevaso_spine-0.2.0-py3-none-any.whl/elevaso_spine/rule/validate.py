"""
.. module:: validate
    :platform: Unix, Windows
    :synopsis: Validate the structure of the rule engine values
"""

# Python Standard Libraries
import logging

# 3rd Party Libraries


# Project Specific Libraries
from elevaso_spine.rule.operators import CONDITIONS, OPERATORS

LOGGER = logging.getLogger(__name__)


def validate_rule(rule: dict):
    """Validate the format of a rule

    Args:
        rule (dict): Dictionary representing the rule, contains: rule_num,
        rule keys

    Raises:
        AttributeError if rule_num or rule are missing

        TypeError if rule is not in dict format
    """
    if "rule_num" not in rule.keys():
        raise AttributeError("rule_num is missing from one or more rules")

    if "rule" not in rule.keys():
        raise AttributeError("rule is missing from one or more rules")

    __check_type__(rule["rule"], (dict), "rule must be in dictionary format")

    # TODO If len(rule["rule"]) > 1 then error
    # TODO Check if value == dict with multiple keys and condition not present
    validate_rule_structure(rule["rule"])


def __check_type__(
    value: object,
    value_types: tuple,
    message: str = None,
    exc_type: Exception = TypeError,
):
    """Check the type of the value and raise an error if not valid

    Args:
        value (object): Value to check the type

        value_types (tuple): Valid types of data

        message (Optional, str): Message to display, defaults to None

        exc_type (Optional, Exception): Exception type, defaults to TypeError
    """
    if not isinstance(value, value_types):
        raise exc_type(message)


def validate_rule_structure(rule: dict):
    """Validate the structure of a rule

    Args:
        rule (dict): Single rule to validate

    Raises:
        NotImplementedError if condition or operator is not supported

        TypeError if structure is invalid
    """
    for key, value in rule.items():
        if key in CONDITIONS.keys():
            __check_type__(value, (dict), "Must be in dictionary format")

            validate_rule_structure(value)
        elif key in OPERATORS.keys():
            __check_type__(
                value, (dict, list), "Must be in dictionary or list format"
            )

            if isinstance(value, list) and not all(
                [isinstance(item, dict) for item in value]
            ):
                raise TypeError("List of items must be in dictionary format")
        else:
            raise NotImplementedError(f"{key} is not supported")
