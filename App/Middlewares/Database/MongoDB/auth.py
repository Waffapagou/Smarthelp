"""
Contains all the middlewares for authentication.

This module provides functions for handling user authentication and user information retrieval from the database.
"""
from App.Database.mongoDB.auth import activate_account, modify_credentials ,register_user, get_user_info_token, modify_user_password, get_user_info
from App.Utilities.Functions.tokens import generate_jwt, verify_password
from App.Configs.configuration import load_json
from App.Middlewares.Database.ChromaDB.chromaDB import middleware_init_chromaDB

from App.Utilities.FileSystem.UserDirectory  import create_user_directory

import bcrypt

from uuid import uuid4

from datetime import datetime

configuration = load_json ("App/Configs/configuration.json")

def middle_update_credentials (user_token:str, new_pseudo:str, new_email:str) :
    """
    Modify user pseudo and email.

    Args:
        user_token (str): User token.
        new_pseudo (str): New username (pseudo).
        new_email (str): New user email.

    Returns:
        dict : Status code.
    """
    # Check if user exist with the given user_token
    result = get_user_info_token(user_token)

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

    return modify_credentials(user_token, new_pseudo, new_email)

def middle_get_user (user_token) :
    """
    Retrieve user information from the database.

    Args:
        user_token (str): Token to identify user.

    Returns:
        tuple: Status code and user information.
    """

    return get_user_info_token(user_token)

def middle_modify_password (user_token,new_pwd) :
    """
    Change specific user password and secure it by hashing it.

    Args:
        user_token (str): The user token.
        new_pwd (str): The new password to be stored and hashed.
    """

    hasded_pwd = bcrypt.hashpw(new_pwd.encode('utf8'),bcrypt.gensalt())
    token_pwd = str(uuid4())

    return modify_user_password (user_token, hasded_pwd,token_pwd)

def middle_register_user(user_credentials):
    """
    Crypt the incoming data and store them to the database.
    Create user directory in the file system.

    Args:
        user_credentials (dict): A dictionary containing user credentials.

    Returns:
        str: The user token generated after registration.
    """

    # Verify if the email is already in the database
    already_user_database_dict = get_user_info({"email" : user_credentials["email"].lower()})
    if already_user_database_dict ["status"] == 200:
        return {
            "result" : "Email already exists",
            "status" : 409
        }

    credentials = {}

    # Hash password
    hasded = bcrypt.hashpw(user_credentials["pwd"].encode('utf8'), bcrypt.gensalt())
    # Change pwd with hashed one
    credentials["pwd"] = hasded

    # Generating user token
    credentials["user_token"] = str(uuid4())
    # Generating user verification
    credentials["status"] = {
        "type" : "unverified",
        "reason" : "email_verification"
    }

    # Time of creation
    credentials["createdAt"] = datetime.now().strftime("%Y-%m-%d")

    credentials["status"] = "pending"
    credentials["role"] = user_credentials["type"]
    
    credentials["name"]     =   user_credentials["name"]
    credentials["email"]    =   user_credentials["email"].lower()
    credentials["jwt"]      =   generate_jwt(
            payload={
                "user_token"    : credentials["user_token"],
                "email"         : credentials["email"]
            },
        secret_key=configuration["app"]["security"]["jwt"]["secret_key"]
    )

    results = register_user(credentials)

    chromaDB_result = middleware_init_chromaDB(
        client_path = configuration["database"]["chromaDB"]["directory_path"],
        collection_name = credentials["user_token"]
    )

    if chromaDB_result["status"] != 200:
        return {
            "status" : 500,
            "message" : "Error while creating chromaDB collection"
        }

    # Create user directories
    status_user_repo = create_user_directory(credentials["user_token"])

    if status_user_repo :
        return {
            "token" : credentials["user_token"],
            "status" : 200
        }

def middle_check_user_credentials (user_credentials):
    """
    Check if user exists.

    Args:
        user_credentials (dict): User credentials.

    Returns:
        bool: True if user exists, False otherwise.
    """

    # Lowering email
    user_credentials["email"] = user_credentials["email"].lower()

    # Retrieve user credentials from database
    user_result = get_user_info({"email" : user_credentials["email"]})

    if user_result["status"] == 500:
        return {
            "status": 500,
            "message": "Error during user information retrieval"
        }
    
    if user_result["status"] == 404:
        return {
            "status": 404,
            "message": "No user found"
        }
    
    # Check if the password is correct
    verify_password_result = verify_password(user_credentials["pwd"], user_result["data"]["pwd"])

    if verify_password_result == False:
        return {
            "status": 401,
            "message": "Wrong password"
        }
    
    if user_result["data"]["status"] == "pending":
        return {
            "status": 403,
            "message": "Account not activated"
        }

    return {
        "status": 200,
        "user_token": user_result["data"]["user_token"],
        "role": user_result["data"]["role"],
        "email": user_result["data"]["email"]
    }

def middle_activate_account (user_token) :
    """
    Activate the user account in the database.

    Args:
        user_token (str): The user token.

    Returns:
        dict: The result of the activation.
            - If the account is successfully activated, returns {"status": 200, "message": "Account activated"}.
            - If the user is not found, returns {"status": 404, "message": "No user found"}.
            - If there is an error during the activation, returns {"status": 500, "message": "Error during account activation"}.
    """

    return activate_account(user_token)