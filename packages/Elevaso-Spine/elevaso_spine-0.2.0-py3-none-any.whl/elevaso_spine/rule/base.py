"""
.. module:: base
    :platform: Unix, Windows
    :synopsis: Main rule engine base class
"""

# Python Standard Libraries
import logging

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


class RuleEngineBase:
    """
    A class to evaluate a set of records against a complex set of rules to
    identify matches
    """

    def __init__(self, **kwargs):
        """Initialize an instance of the class

        Kwargs:
            case_sensitive (bool, Optional): True/False if values should be
            case sensitive, defaults to True

            trim_strings (bool, Optional): True/False if strings should be
            trimmed (remove head/trail spaces) before comparing rules,
            defaults to True

            empty_equals_none (bool, Optional): True/False if an empty string
            (even after trimming [if set]) == None or Null, defaults to True

            eval_if_no_key_found (bool, Optional): True/False if the rule
            should be evaluated even if the key does not exist in the record,
            defaults to True

            default_value_no_key_found (object, Optional): Default value to
            use if the key does not exist in the record (only applies if
            eval_if_no_key_found == True), defaults to None

            exit_on_error (bool, Optional): True/False if RuleEngine class
            should raise exception and exit on error, defaults to True
        """
        self.case_sensitive = kwargs.get("case_sensitive", True)
        self.trim_strings = kwargs.get("trim_strings", True)
        self.empty_equals_none = kwargs.get("empty_equals_none", True)
        self.eval_if_no_key_found = kwargs.get("eval_if_no_key_found", True)
        self.default_value_no_key_found = kwargs.get(
            "default_value_no_key_found", None
        )
        self.exit_on_error = kwargs.get("exit_on_error", True)

    def __raise_exception__(self, exc: Exception):
        """Log and raise the exception

        Args:
            exc (Exception): The exception to raise
        """
        LOGGER.error(str(exc))

        if self.exit_on_error:
            raise exc

    @property
    def case_sensitive(self) -> bool:
        """Determines if the values during comparison are case sensitive

        .. note::

            When set to True, then Y==y
            When set to False, then Y!=y

        Returns:
            bool indicating if it's sensitive
        """
        return self.__case_sensitive

    @case_sensitive.setter
    def case_sensitive(self, value: bool):
        """Set the case_sensitive property

        .. note::

            When set to True, then Y==y
            When set to False, then Y!=y

        Args:
            value (bool): True if case sensitive
        """
        if not isinstance(value, bool):
            self.__raise_exception__(TypeError("value must be boolean"))

        self.__case_sensitive = value

    @property
    def trim_strings(self) -> bool:
        """Determines if string values should be trimmed (eliminate spaces at
        the end/beginning of string) before comparison

        .. note::

            When set to True, then " Y"=="Y"
            When set to False, then " Y"!="Y"

        Returns:
            bool indicating if values should be trimmed
        """
        return self.__trim_strings

    @trim_strings.setter
    def trim_strings(self, value: bool):
        """Set the trim_strings property

        .. note::

            When set to True, then " Y"=="Y"
            When set to False, then " Y"!="Y"

        Args:
            value (bool): True if values should be trimmed
        """
        if not isinstance(value, bool):
            self.__raise_exception__(TypeError("value must be boolean"))

        self.__trim_strings = value

    @property
    def empty_equals_none(self) -> bool:
        """Determines if if an empty string (even after trimming [if set]) ==
        None or Null

        .. note::

            When set to True, then "" is None
            When set to False, then "" is not None

        Returns:
            bool indicating if values an empty string is equal to None
        """
        return self.__empty_equals_none

    @empty_equals_none.setter
    def empty_equals_none(self, value: bool):
        """Set the empty_equals_none property

        .. note::

            When set to True, then "" is None
            When set to False, then "" is not None

        Args:
            value (bool): True if values an empty string is equal to None
        """
        if not isinstance(value, bool):
            self.__raise_exception__(TypeError("value must be boolean"))

        self.__empty_equals_none = value

    @property
    def eval_if_no_key_found(self) -> bool:
        """Determines if the rule should be evaluated even if the key does not
        exist in the record

        .. note::

            Uses the default_value_no_key_found property value during
            comparison if key is not found and eval_if_no_key_found = True

        Returns:
            bool indicating if evaluation should occur when key is not
            found in the record
        """
        return self.__eval_if_no_key_found

    @eval_if_no_key_found.setter
    def eval_if_no_key_found(self, value: bool):
        """Set the eval_if_no_key_found property

        .. note::

            Uses the default_value_no_key_found property value during
            comparison if key is not found and eval_if_no_key_found = True

        Args:
            value (bool): True if evaluation should occur when key is not
            found in the record
        """
        if not isinstance(value, bool):
            self.__raise_exception__(TypeError("value must be boolean"))

        self.__eval_if_no_key_found = value

    @property
    def default_value_no_key_found(self) -> bool:
        """Default value to use if the key does not exist in the record

        .. note::

            Only applies if eval_if_no_key_found == True

        Returns:
            value to use if key is not found in the record
        """
        return self.__default_value_no_key_found

    @default_value_no_key_found.setter
    def default_value_no_key_found(self, value: object):
        """Set the default_value_no_key_found property

        Args:
            value (object): Default value if key is not found in the
            record
        """
        self.__default_value_no_key_found = value

    @property
    def exit_on_error(self) -> bool:
        """Determines if RuleEngine class should raise exception and exit on
        error

        Returns:
            bool indicating if errors should be raised as an exception
        """
        return self.__exit_on_error

    @exit_on_error.setter
    def exit_on_error(self, value: bool):
        """Set the exit_on_error property

        Args:
            value (bool): True if errors should be raised as an exception
        """
        if not isinstance(value, bool):
            self.__raise_exception__(TypeError("value must be boolean"))

        self.__exit_on_error = value
