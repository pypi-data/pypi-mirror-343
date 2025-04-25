"""
.. module:: explain
    :platform: Unix, Windows
    :synopsis: Functions to explain a rule in friendly format
"""

# Python Standard Libraries
import logging

# 3rd Party Libraries


# Project Specific Libraries
from elevaso_spine.rule.operators import CONDITIONS, OPERATORS

LOGGER = logging.getLogger(__name__)


def explain_rule(rule: object) -> str:
    """Explain a single rule in simple terms

    Args:
        rule (dict): Rule in dictionary format

    Returns:
        str representing the explained rule
    """
    output = ""

    for key, value in rule.items():
        if key in CONDITIONS.keys():
            output = __explain_rule_condition(key, value)
        elif key in OPERATORS.keys():
            output = __explain_rule_operator(key, value)

    return output


def __explain_rule_condition(condition: str, rule: dict) -> str:
    """Build the explain statement starting with a condition

    Args:
        condition (str): Condition value

        rule (dict): Remaining portion of rule

    Returns:
        str representing the condition(s)
    """
    output = []

    for key, value in rule.items():
        if key in CONDITIONS.keys():
            output.append(__explain_rule_condition(key, value))
        elif key in OPERATORS.keys():
            output.append(__explain_rule_operator(key, value, condition))

    if len(output) > 1:
        return "(" + (" " + condition + " ").join(output) + ")"

    return "".join(output)


def __explain_rule_operator(
    operator: str, rule: dict, condition: str = ""
) -> str:
    """Build the explain statement starting with an operator

    Args:
        operator (str): Operator separating the two values

        rule (dict): Remaining portion of rule

        condition (Optional, str): Condition value if multiple operators
        provided, defaults to empty string

    Returns:
        str representing the operator(s)
    """
    output = []

    if isinstance(rule, dict):
        for key, value in rule.items():
            output.append(f'record["{key}"] {operator} "{value}"')
    elif isinstance(rule, list):
        for item in rule:
            output.extend(
                [f'record["{k}"] {operator} "{v}"' for k, v in item.items()]
            )

    if len(output) > 1:
        return "(" + (" " + condition + " ").join(output) + ")"

    return "".join(output)
