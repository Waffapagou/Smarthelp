"""
Contains all the middlewares for file CRUD.

This module provides functions for handling file CRUD in the database.
"""

from App.Database.mongoDB.file import add_file, get_files, get_file_info, delete_file
from App.Configs.configuration import load_json
from App.Utilities.FileSystem.UserDirectory import get_user_dir
from App.Database.mongoDB.auth import get_user_info

from uuid import uuid4

configuration = load_json ("App/Configs/configuration.json")

def middle_add_file (user_token:str, file_name:str, file_extension:str, file_size:int) -> dict :
    """
    Add file to database.

    Args:
        user_token (str): User token.
        file_name (str): File name.
        file_extension (str): File extension.
        file_size (int): File size.

    Returns:
        dict : Status code.
    """

    # Check if user exist in the database
    result = get_user_info({"user_token": user_token})

    if result["status"] == 404:
        return {
            "status": 404,
            "message": "No user found"
        }
    
    if result["status"] == 500:
        return {
            "status": 500,
            "message": "Error during user information retrieval"
        }

    # Check if file exist with the given file_name
    result = get_file_info({"file_name": file_name})

    if result["status"] == 200:
        return {
            "status": 500,
            "message": "File already exist"
        }
    
    if result["status"] == 500:
        return {
            "status": 500,
            "message": "Error during file information retrieval"
        }

    return add_file({
        "_id" : str(uuid4()),
        "user_token": user_token,
        "file_name": file_name,
        "file_extension": file_extension,
        "file_size": file_size
    })

def middle_get_files (user_token:str) -> dict :
    """
    Get all files from the database.

    Args:
        user_token (str): User token.

    Returns:
        dict : Status code.
    """

    # Check if user exist in the database
    result = get_user_info({"user_token": user_token})

    if result["status"] == 404:
        return {
            "status": 404,
            "message": "No user found"
        }
    
    if result["status"] == 500:
        return {
            "status": 500,
            "message": "Error during user information retrieval"
        }

    return get_files({"user_token": user_token})

# Delete file
def middle_delete_file (user_token:str, file_name:str) -> dict :
    """
    Delete file from database.

    Args:
        user_token (str): User token.
        file_name (str): File name.

    Returns:
        dict : Status code.
    """

    # Check if user exist in the database
    result = get_user_info({"user_token": user_token})

    if result["status"] == 404:
        return {
            "status": 404,
            "message": "No user found"
        }
    
    if result["status"] == 500:
        return {
            "status": 500,
            "message": "Error during user information retrieval"
        }

    # Check if file exist with the given file_name
    result = get_file_info({"user_token" : user_token, "file_name": file_name})

    if result["status"] == 404:
        return {
            "status": 404,
            "message": "No file found"
        }
    
    if result["status"] == 500:
        return {
            "status": 500,
            "message": "Error during file information retrieval"
        }

    return delete_file({"user_token": user_token, "file_name": file_name})