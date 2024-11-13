"""
Contains all the scripts to create / connect a user
"""
from App.Database.mongoDB.connexion import get_database, connect_database
from pymongo.errors import DuplicateKeyError

import bcrypt

import logging

# Getting the collections "users" that stores all the users
connect_database()

database = get_database()
users = database["users"]

def get_user_info(filters:dict):
    """
    Get user information using user_token.

    Args:
        filters (dict): The filters used to retrieve information from Database.

    Returns:
        dict: The result of the operation.
            - If the user is found, returns {"status": 200, "data": {"pseudo": str, "email": str, "mdp": str}}.
            - If the user is not found, returns {"status": 404, "message": "No user found"}.
    """
    global users

    try:

        logging.info("Retrieving user information from database using the following filters : {}".format(filters))

        results = users.find_one(filters)

        if results is not None:
            logging.info("User found for filters : {}".format(filters))
            return {
                "status": 200,
                "data": results
            }
        else:
            logging.info("No user found for filters : {}".format(filters))
            return {
                "status": 404,
                "message": "No user found"
            }
        
    except Exception as e:
        logging.error("Error during user information retrieval")
        logging.error(e)

        return {
            "status": 500,
            "message": "Error during user information retrieval"
        }

def get_user_info_token(user_token):
    """
    Get user information using user_token.

    Args:
        user_token (str): The user token.

    Returns:
        dict: The result of the operation.
            - If the user is found, returns {"status": 200, "data": {"pseudo": str, "email": str, "mdp": str}}.
            - If the user is not found, returns {"status": 404, "message": "No user found"}.
    """
    global users

    try:
        logging.info("Retrieving user information from database using the following user_token : {}".format(user_token))
        results = users.find_one({
            "user_token": user_token
        })


        if results is not None :
            logging.info("User found for user_token : {}".format(user_token))
            return {
                "status": 200,
                "data": {
                    "user_token": results["user_token"],
                    "name": results["name"],
                    "email": results["email"],
                    "role" : results["role"],
                    "mdp": "itspasswordtime"
                }
            }
        else:
            logging.info("No user found for user_token : {}".format(user_token))
            return {
                "status": 404,
                "message": "No user found"
            }
    except Exception as e:
        logging.error("Error during user information retrieval")
        logging.error(e)

        return {
            "status": 500,
            "message": "Error during user information retrieval"
        }

def register_user(user_data):
    """
    Register the user into the database.

    Args:
        user_data (dict): The user data to be registered.

    Returns:
        dict: The result of the registration.
            - If the user is successfully registered, returns {"status": 200, "message": "User registered in database"}.
            - If there is a duplicate key error, returns {"status": 409, "message": "Duplicate Key"}.
            - If there is an error during the registration, returns {"status": 500, "message": "Error during user registration"}.
    """
    global users

    try:
        logging.info("Registering user in database with the following data : {}".format(user_data))
        users.insert_one(user_data)
        logging.info("User registered in database with the following data : {}".format(user_data))
        return {"status": 200, "message": "User registered in database"}
    
    except DuplicateKeyError:
        logging.error("Duplicate key error during user registration")
        return {"status": 409, "message": "Duplicate Key"}
    except Exception as e:
        logging.error("Error during user registration")
        logging.error(e)

        return {"status": 500, "message": "Error during user registration"}

def verify_user_password(user_email:str, password:str):
    """
    Verify if the given password matches the user's password.

    Args:
        user_email (str): The user token.
        password (str): The password to verify.

    Returns:
        dict: The result of the verification.
            - If the password matches, returns {"status": 200}.
            - If the user is not found, returns {"status": 404, "message": "No user found"}.
            - If the password does not match, returns {"status": 401, "message": "Password not matched"}.
            - If there is an error during the verification, returns {"status": 500, "message": "Error during password verification"}.
    """
    global users

    try:
        logging.info("Verifying password for user with email : {}".format(user_email))
        user = users.find_one({"email": user_email})
        if user is None:
            logging.info("No user found for email : {}".format(user_email))
            return {"status": 404, "message": "No user found"}

        if bcrypt.checkpw(password.encode('utf8'), user['pwd']):
            logging.info("Password matched for user with email : {}".format(user_email))
            return {"status": 200}
        else:
            return {"status": 401, "message": "Password not matched"}

    except Exception as e:
        logging.error("Error during password verification")
        logging.error(e)

        return {"status": 500, "message": "Error during password verification"}

def modify_credentials (user_token, new_pseudo, new_email) :

    global users

    try :
        logging.info("Modifying user credentials in database with the following data : {}".format({"user_token": user_token, "new_pseudo": new_pseudo, "new_email": new_email}))
        results = users.update_one({"user_token": user_token}, { "$set" : {"pseudo" : new_pseudo, "email" : new_email} })
        logging.info("User credentials modified in database with the following data : {}".format({"user_token": user_token, "new_pseudo": new_pseudo, "new_email": new_email}))

    except Exception as e :
        logging.error("Error during user credentials modification")
        logging.error(e)

        return {
            "status" : 500,
            "message" : "Could not modify user credentials"
        }

    return {
        "status" : 200
    }

def modify_user_role (user_token, new_role) :
    """
    Modify user role
    """

    global users

    try :
        logging.info("Modifying user role in database with the following data : {}".format({"user_token": user_token, "new_role": new_role}))
        results = users.update_one({"user_token": user_token}, { "$set" : {"role" : new_role} })
        logging.info("User role modified in database with the following data : {}".format({"user_token": user_token, "new_role": new_role}))
    except Exception as e :
        logging.error("Error during user role modification")
        logging.error(e)
        return {
            "status" : 500,
            "message" : "Could not modify user role"
        }

    return {
        "status" : 200
    } if results is not None else {
        "status" : 500,
        "message" : "Could not modify user role"
    }

def modify_user_password (user_token, new_pwd, new_pwd_token):
    """
    Modify user pwd
    """

    global users

    try :
        logging.info("Modifying user password in database for the following user : {}".format({"user_token": user_token}))
        results = users.update_one({"user_token": user_token}, { "$set" : {"pwd" : new_pwd, "pwd_token" : new_pwd_token} })
        logging.info("User password modified in database for the following user : {}".format({"user_token": user_token}))

    except Exception as e :
        logging.error("Error during user password modification")
        logging.error(e)

        return {
            "status" : 500,
            "message" : "Could not modify user password"
        }

    return {
        "status" : 200,
        "data" : new_pwd_token
    } if results is not None else {
        "status" : 500,
        "message" : "Could not modify user password"
    }

def activate_account(user_token):
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
    global users

    try:
        logging.info("Activating account for user with user_token : {}".format(user_token))
        result = users.update_one({"user_token" : user_token}, {"$set" : {"status": "active"}})
        logging.info("Account activated for user with user_token : {}".format(user_token))

        if result.modified_count > 0 :
            logging.info("Account activated for user with user_token : {}".format(user_token))
            return {"status": 200, "message": "Account activated"}
        else:
            logging.info("No user found for user_token : {}".format(user_token))
            return {"status": 404, "message": "No user found"}
        
    except Exception as e:
        logging.error("Error during account activation")
        logging.error(e)
        
        return {"status": 500, "message": "Error during account activation"}