"""
.. module:: itr
    :platform: Unix, Windows
    :synopsis: Iterate collections
"""

# Python Standard Libraries
from collections import OrderedDict
import copy
import logging

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


def iterate(
    val: object,
    copy_val: bool = True,
    custom_type_map: dict = None,
) -> object:
    """Iterate a nested list, dict, tuple object to execute function on
    string values

    Args:
        val (object): Object to iterate

        copy_val (bool, Optional): True/False contents of dict/list should be
        copied prior to modifying, defaults to True

        custom_type_map (dict, Optional): Optional mapping of type and
        functions, defaults to None

    Raises:
        NotImplementedError: If value object type is not supported

        Warning: If type of object does not support string substitution

    Returns:
        object: Modified object after function calls
    """
    func = __get_iterate_func(type(val), custom_type_map)
    custom_type_map = custom_type_map or {}

    if func:
        return __call_iterate_func(val, custom_type_map, copy_val, func)

    LOGGER.warning(
        "Value object type %s does not support iteration,"
        " returning original value",
        type(val).__name__,
    )

    return val


def __call_iterate_func(
    val: object, custom_type_map: dict, copy_val: bool, func: object
):
    """Call the iterate function and return the output

    Args:
        val (object): Object to iterate

        custom_type_map (dict): Extra type and function maps

        copy_val (bool, Optional): True/False contents of dict/list should be
        copied prior to modifying, defaults to True

        func (object): Function returned based on the type

    Returns:
        object: Modified object after function calls
    """
    # pylint: disable=unidiomatic-typecheck
    if (
        type(val) in custom_type_map.keys()
    ):
        return func(val)

    if copy_val:
        return func(copy.deepcopy(val), custom_type_map)

    return func(val, custom_type_map)


def __iterate_list(val: list, custom_type_map: dict) -> list:
    """Iterate a list to execute function on string

    Args:
        val (list): List to iterate

        custom_type_map (dict): Extra type and function maps

    Returns:
        object: Modified object after function calls
    """
    for enum, item in enumerate(val):
        func = __get_iterate_func(type(item), custom_type_map)

        # pylint: disable=unidiomatic-typecheck
        if (
            type(item) in custom_type_map.keys()
        ):
            val[enum] = func(item)
        elif func is not None:
            val[enum] = func(item, custom_type_map)

    return val


def __iterate_dict(val: dict, custom_type_map: dict) -> dict:
    """Iterate a dict to execute function on string

    Args:
        val (dict): Dictionary to iterate

        custom_type_map (dict): Extra type and function maps

    Returns:
        object: Modified object after function calls
    """
    output = {}

    for key, value in val.items():
        func = __get_iterate_func(type(value), custom_type_map)

        # pylint: disable=unidiomatic-typecheck
        if (
            type(value) in custom_type_map.keys()
        ):
            output[key] = func(value)
        elif func is not None:
            output[key] = func(value, custom_type_map)
        else:
            output[key] = value

    return output


def __get_iterate_func(obj_type: object, custom_func_map: dict) -> object:
    """Get iterate function to execute based on object type

    Args:
        obj_type (object): Type of the object

        custom_func_map (dict): Mapping of functions

    Returns:
        object representing function
    """
    __func_mapping = {
        dict: __iterate_dict,
        OrderedDict: __iterate_dict,
        list: __iterate_list,
        set: __iterate_list,
        tuple: __iterate_list,
        **custom_func_map,  # Always keep this last
    }

    return __func_mapping.get(obj_type, None)
