# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import ast
import os
import re
from functools import reduce
from inspect import getdoc, signature
from typing import Any, Callable, List, TypeVar

import pandas as pd
from pydantic import BaseModel, TypeAdapter


def convert_df_to_list(df: pd.DataFrame, features: list):
    """
        Method to convert pandas df to 2d array
    """
    if len(features) > 0:
        return df[features].values.tolist()
    else:
        return df.values.tolist()


def convert_to_list_of_lists(value):
    """Method to convert a dataframe column to list of lists

    Args:
        value (_type_): DataFrame column

    Returns:
        _type_: _description_
    """
    if isinstance(value, list):
        # Check if it's already a list of lists
        if all(isinstance(i, list) for i in value):
            return value
        # If it's a list of strings, wrap it to make it a list of lists
        elif all(isinstance(i, str) for i in value):
            return [value]
    # Return empty list if value is None or 'NULL' string
    return []


def get(dictionary, keys: str, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)


def find_instance(dict_: dict, class_type: Any) -> Any:
    """
    Find the first instance of a class in a dictionary.

    Args:
        dict_ (dict): The dictionary to search.
        class_type (Any): The class type to find.

    Returns:
        Any: The first instance of the class found in the dictionary, or None if no instance is found.
    """
    values = [value for value in dict_.values(
    ) if isinstance(value, class_type)]
    return values[0] if len(values) > 0 else None


def get_argument_value(func: Callable, args: tuple, kwargs: dict, param_name: str) -> Any:
    """
    Gets an argument value from the arguments or keyword arguments of a function.

    Args:
        func (Callable): The function to get the argument value from.
        args (tuple): The arguments of the function.
        kwargs (dict): The keyword arguments of the function.
        param_name (str): The parameter name to get the value for.

    Raises:
        ValueError: If the parameter name is not found in the function signature.
        Exception: If any TypeError is found while getting the argument

    Returns:
        Any: The argument value
    """
    try:
        sig = signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # 0. Check if one of the arguments is an instance of EvaluationState
        from ..entities.state import EvaluationState
        state_var = find_instance(dict_=bound_args.arguments,
                                  class_type=EvaluationState)
        if state_var is not None:
            if not hasattr(state_var, param_name):
                raise ValueError(
                    f"'{param_name}' attribute missing from the state.")
            return getattr(state_var, param_name)

        # 1. Check if one of the arguments is named "state"
        if "state" in bound_args.arguments:
            state_var = bound_args.arguments.get("state")

        #   1.1 If yes, check if the argument type is a BaseModel or Dict
        #   1.1.1.1 If BaseModel, get the argument value from state's attribute. If not present, throw error.
            if isinstance(state_var, BaseModel):
                if not hasattr(state_var, param_name):
                    raise ValueError(
                        f"'{param_name}' attribute missing from the state.")
                return getattr(state_var, param_name)
        #   1.1.1.2 If Dict, get the argument value from state's key. If not present, throw error.
            if isinstance(state_var, dict):
                if param_name not in state_var:
                    raise ValueError(
                        f"'{param_name}' key missing from the state.")
                return state_var[param_name]
        #   1.1.1 If not, no-op. Continue below

        # 2. Check if the argument is passed as a keyword argument. If not present, throw error.
        if param_name not in bound_args.arguments:
            raise ValueError(
                f"{param_name} argument missing from the function.")

        return bound_args.arguments.get(param_name)
    except TypeError as te:
        raise Exception(
            f"Got an error while getting {param_name} argument.") from te


T = TypeVar("T")


def add_if_unique(obj: T, obj_list: List[T], keys: List[str]) -> None:
    """
    Add an object to a list only if there is no existing object that matches all the specified keys.

    Args:
        obj: The object to potentially add to the list
        obj_list: The list to which the object may be added
        keys: A list of attribute names to check for uniqueness

    """
    # Check if any existing object matches all keys
    for existing_obj in obj_list:
        matches_all_keys = True
        for key in keys:
            if not hasattr(obj, key) or not hasattr(existing_obj, key):
                matches_all_keys = False
                break
            if getattr(obj, key) != getattr(existing_obj, key):
                matches_all_keys = False
                break

        if matches_all_keys:
            # Found a match, don't add the object
            return

    # No match found, add the object to the list
    obj_list.append(obj)


def transform_str_to_list(input_str: str) -> list[str]:
    """
    Parse the context columns correctly and make sure it is a list and not a string. This is intended
    to be used with pd.DataFrame.apply() method. Specifically, in some cased where values are read from
    csv files and cells are intended to contain a list, pandas will parse them as strings, this helper
    would parse them as expected

    Args:
        input_str (str): the cell content

    Returns:
        list of strings

    """
    contexts_list = []
    # The input is a list already, no need to update it
    if isinstance(input_str, list):
        return input_str

    # The input is parsed as a string, check if it is lateral array and parse it, other wise add it to a list and return it
    if isinstance(input_str, str):
        try:
            contexts_list = ast.literal_eval(input_str)
        except Exception:
            # The user only gave one context column
            contexts_list = [input_str]
    return contexts_list


def parse_functions_to_schema(func: Callable) -> dict:
    """
    Converts a callable function into a structured schema for LLM tool calling.

    Extracts function metadata including name, description, parameters, parameter types,
    and required parameters.

    Args:
        func (Callable): Callable function to parse

    Returns:
        dict: Schema details of the provided function
        Example schema format:

        {
        "name": "function_name",
        "description": "Function description.",
        "parameters": {
            "parameter1": {
                "description": "The parameter description.",
                "type": "datatype"
            },
            "parameter2": {
                "description": "The parameter description.",
                "type": "datatype"
            }
            "required": ["parameter1"]
        }
    }
    """
    try:

        # Get the function parameter schema
        # using pydantic TypeAdapter
        schema = TypeAdapter(func).json_schema()
        parameters = schema.get("properties")

        # Get the doc string of the func
        doc = getdoc(func) or ""

        parameter_schema = {}
        # Loop over each parameter
        for param_name, param_properties in parameters.items():
            param_desc = ""
            if doc:
                match = re.search(rf"{param_name}\s*:\s*(.+?)(?:\n|$)", doc)
                if match:
                    param_desc = match.group(1).strip()

            parameter_schema[param_name] = {
                "type": param_properties.get("type", "string"),
                "description": param_desc
            }

        parameter_schema["required"] = schema.get("required")
        return {
            "name": func.__name__,
            "description": doc.split("\n\n")[0] if doc else "",
            "parameters": parameter_schema
        }

    except Exception as ex:
        raise Exception(
            f"Got an error while parsing the {func} argument. Error: {ex}")


def get_environment_variable_value(possible_env_variables: list) -> str | None:
    """
    Helper to get environment variable based on list of option. This will return the first
    found value, otherwise None

    Args:
        possible_env_variables (list[str]): list of environment variable to find
    Returns:
        str | None: the first found value, otherwise None
    """
    for env_key in possible_env_variables:
        env_value = os.getenv(env_key)

        if env_value:
            return env_value
    return None
