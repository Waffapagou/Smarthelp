"""
Contains all the middlewares for llm CRUD.
"""

from App.Database.mongoDB.llm import get_prompt, modify_prompt, create_prompt, modify_llm_configuration, modify_splitter_configuration
from App.Configs.configuration import load_json

configuration = load_json ("App/Configs/configuration.json")

def middle_get_prompt (filters:dict) -> dict :
    """
    Get prompt from database.

    Args:
        filters (dict): Filters to retrieve prompt.

    Returns:
        dict : Status code.
    """

    return get_prompt(filters)

def middle_modify_prompt (filters:dict, new_values:dict) -> dict :
    """
    Modify prompt in database.

    Args:
        filters (dict): Filters to retrieve prompt.
        new_values (dict): New values to update.

    Returns:
        dict : Status code.
    """

    return modify_prompt(filters, new_values)

def middle_modify_llm_configurations (filters, new_values) -> dict :
    """
    Modify llm configurations in database.

    Args:
        filters (dict): Filters to retrieve prompt.
        new_values (dict): New values to update.

    Returns:
        dict : Status code.
    """

    return modify_llm_configuration(filters, new_values)

def middle_modify_splitter_configurations (filters:dict, new_values:dict) -> dict :
    """
    Modify splitter configurations in database.

    Args:
        filters (dict): Filters to retrieve prompt.
        new_values (dict): New values to update.

    Returns:
        dict : Status code.
    """

    return modify_splitter_configuration(filters, new_values)

def middle_create_prompt (data:dict) -> dict :
    """
    Create prompt in database.

    Args:
        data (dict): Data to create prompt.

    Returns:
        dict : Status code.
    """

    # check if user already has a prompt in the database
    if get_prompt({"user_token": data["user_token"]})["status"] == 200:
        return {"status": 409, "message": "Prompt already exists"}

    return create_prompt(data)