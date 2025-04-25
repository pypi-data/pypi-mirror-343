"""
.. module:: engine
    :platform: Unix, Windows
    :synopsis: Main rule engine class
"""

# Python Standard Libraries
import copy
import logging
from typing import Tuple

# 3rd Party Libraries


# Project Specific Libraries
from elevaso_spine.rule.base import RuleEngineBase
from elevaso_spine.rule.explain import explain_rule
from elevaso_spine.rule.eval import (
    format_case_sensitive,
    format_none,
    format_trim,
    format_value,
)
from elevaso_spine.rule.operators import CONDITIONS, OPERATORS
from elevaso_spine.rule.validate import validate_rule

LOGGER = logging.getLogger(__name__)


class RuleEngine(RuleEngineBase):
    """
    A class to evaluate a set of records against a complex set of rules to
    identify matches
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__rule_set__ = []
        self.__record_set__ = []
        self.__output = []

    def add_rule(self, rule: dict, rule_num: str = None):
        """Add a single rule

        Args:
            rule (dict): Single rule in dictionary format

            rule_num (str, Optional): Rule number, defaults to the order
            number when added
        """
        if rule_num is None:
            rule_num = self.rule_len + 1

        # TODO Check if the rule_num already exists and throw error

        self.add_rule_set([{"rule_num": rule_num, "rule": rule}])

    def add_rule_set(self, rule_set: list):
        """Add a list of rules pre-formatted

        Args:
            rule_set (list): List of dictionary containing rule_num, and rule

        Raises:
            TypeError if rule_set is not in list format
        """
        if not isinstance(rule_set, list):
            self.__raise_exception__(
                TypeError("rule_set must be in list format")
            )

        for item in rule_set:
            try:
                validate_rule(item)
            except Exception as exc:
                self.__raise_exception__(exc)

        rule_set = copy.deepcopy(rule_set)

        self.__rule_set__.extend(rule_set)

    def add_record(self, record: dict):
        """Add a single record

        Args:
            record (dict): Single record in dictionary format
        """
        if not isinstance(record, dict):
            self.__raise_exception__(
                TypeError("record must be in dictionary format")
            )

        self.add_record_set([record])

    def add_record_set(self, record_set: list):
        """Add list of records to the rule engine

        Args:
            record_set (list): List of records in dictionary format
        """
        if not isinstance(record_set, list):
            self.__raise_exception__(
                TypeError("record_set must be in list format")
            )

        if not isinstance(record_set[0], dict):
            self.__raise_exception__(
                TypeError("record_set items must be in dictionary format")
            )

        record_set = copy.deepcopy(record_set)

        self.__record_set__.extend(record_set)

    def __check_values__(self) -> Tuple[list, list]:
        """Check to make sure rule(s) and record(s) exist

        Returns:
            list representing the formatted rule_set

            list representing the formatted record_set
        """

        if len(self.__rule_set__) == 0:
            self.__raise_exception__(ValueError("Rules must be provided"))

        if len(self.__record_set__) == 0:
            self.__raise_exception__(ValueError("Records must be provided"))

        rule_set = [self.__apply_settings__(item)
                    for item in self.__rule_set__]
        record_set = [
            self.__apply_settings__(item) for item in self.__record_set__
        ]

        return rule_set, record_set

    def eval(self):
        """Perform evaluation of rule_set against record_set"""

        rule_set, record_set = self.__check_values__()

        self.__output = []

        for record in record_set:
            matching_rules = []

            for rule in rule_set:
                if self.__eval_rule__(record, rule["rule"]):
                    matching_rules.append(rule["rule_num"])

            self.__output.append((record, matching_rules))

    def __eval_rule__(self, record: dict, rule: dict) -> bool:
        """Evaluate a single rule against a record

        Args:
            record (dict): Dictionary representing the record

            rule (dict): Rule to evaluate

        Returns:
            bool if the record matches the rule
        """
        output = False

        for key, value in rule.items():
            if key in CONDITIONS.keys():
                output = self.__eval_condition__(key, record, value)
            elif key in OPERATORS.keys():
                output = self.__eval_operator__(key, record, value)

        return output

    def __eval_condition__(
        self, condition: str, record: str, rule: dict
    ) -> bool:
        """Evaluate a condition statement

        Args:
            condition (str): Condition key

            record (dict): Dictionary representing the record

            rule (dict): Remainder of the rule

        Returns:
            bool if the record matches the rule
        """
        output = []

        for key, value in rule.items():
            if key in CONDITIONS.keys():
                output.append(self.__eval_condition__(key, record, value))
            elif key in OPERATORS.keys():
                output.append(
                    self.__eval_operator__(key, record, value, condition)
                )

        if len(output) > 1:
            condition_func = CONDITIONS.get(condition, "AND")

            return condition_func(*output)

        return output[0]

    def __eval_operator__(
        self, operator: str, record: str, rule: dict, condition: str = None
    ) -> bool:
        """Evaluate a condition statement

        Args:
            operator (str): Operator key

            record (dict): Dictionary representing the record

            rule (dict): Remainder of the rule

            condition (str, Optional): Condition key, defaults to None
        Returns:
            bool if the record matches the rule
        """
        output = []
        operator_func = OPERATORS[operator]

        if isinstance(rule, dict):
            rule = [rule]

        for item in rule:
            for key, value in item.items():
                format_value(
                    key,
                    record,
                    output,
                    cls=self,
                    operator_func=operator_func,
                    value=value,
                )

        if len(output) > 1:
            condition_func = CONDITIONS.get(condition, "AND")

            return condition_func(*output)

        return output[0]

    def explain_rule(self, rule_num: object) -> str:
        """Explain a single rule in simple terms

        Args:
            rule_num (object): Rule number to explain

        Returns:
            str representing the explained rule
        """
        rule = list(
            filter(lambda x: x["rule_num"] == rule_num, self.__rule_set__)
        )

        if len(rule) == 1:
            return explain_rule(rule[0]["rule"])

        if len(rule) == 0:
            self.__raise_exception__(
                ValueError(f"{rule_num} not found in rule_set")
            )

        return ""

    def __apply_settings__(self, item: dict) -> dict:
        """Apply settings to a single item (rule or record)

        Args:
            item (dict): Dictionary of the item

        Returns:
            dict representing the formmatted item
        """
        output = {}

        for key, value in item.items():
            formatted_key = self.__apply_settings_to_value__(key)

            if isinstance(value, dict):
                formatted_value = self.__apply_settings__(value)
            elif isinstance(value, list):
                if len(value) == 0:
                    self.__raise_exception__(
                        ValueError("value cannot be empty list")
                    )
                elif isinstance(value[0], (dict, list)):
                    formatted_value = [
                        self.__apply_settings__(item) for item in value
                    ]
                else:
                    formatted_value = [
                        self.__apply_settings_to_value__(item)
                        for item in value
                    ]
            else:
                formatted_value = self.__apply_settings_to_value__(value)

            output[formatted_key] = formatted_value

        return output

    def __apply_settings_to_value__(self, value: object) -> object:
        """Apply rule engine settings to a single value

        Args:
            value (object): Object to apply settings to

        Returns:
            object representing the formatted value
        """
        output = value

        output = format_case_sensitive(output, self.case_sensitive)
        output = format_trim(output, self.trim_strings)
        output = format_none(output, self.empty_equals_none)

        return output

    @property
    def rule_len(self) -> int:
        """Number of rules in the engine

        Returns:
            int representing the number of rules
        """
        return len(self.__rule_set__)

    @property
    def record_len(self) -> int:
        """Number of records in the engine

        Returns:
            int representing the number of records
        """
        return len(self.__record_set__)

    @property
    def output(self) -> list:
        """Return output from eval function

        Returns:
            list of tuple containing the record and list of rules matched
        """
        return self.__output
