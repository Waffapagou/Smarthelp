"""
Contains all the scripts to create / modify / load a prompt for LLM
"""

from App.Database.mongoDB.connexion import get_database, connect_database
from pymongo.errors import DuplicateKeyError

import logging

# Getting the collections "llm" that stores all the prompts
connect_database()

database = get_database()
llm_collection = database["llm"]

def get_prompt(filters:dict):
    """
    Get prompt information using filters.

    Args:
        filters (dict): The filters used to retrieve information from Database.

    Returns:
        dict: The result of the operation.
            - If the prompt is found, returns {"status": 200, "data": {"prompt": str, "author": str, "tags": list}}.
            - If the prompt is not found, returns {"status": 404, "message": "No prompt found"}.
    """
    global llm_collection

    try:
        logging.info("Retrieving prompt information using the following filters : {}".format(filters))
        results = llm_collection.find_one(filters)

        if results is not None:
            logging.info("Prompt found successfully")
            return {
                "status": 200,
                "data": results
            }
        else:
            logging.info("No prompt found")
            return {
                "status": 404,
                "message": "No prompt found"
            }
    except Exception as e:

        logging.error("Error during prompt information retrieval")
        logging.error(e)

        return {
            "status": 500,
            "message": "Error during prompt information retrieval"
        }
    
def modify_prompt(filters:dict, new_values:dict):
    """
    Modify prompt information using filters.

    Args:
        filters (dict): The filters used to retrieve information from Database.
        new_values (dict): The new values to update in the Database.

    Returns:
        dict: The result of the operation.
            - If the prompt is found and modified, returns {"status": 200, "message": "Prompt modified"}.
            - If the prompt is not found, returns {"status": 404, "message": "No prompt found"}.
    """
    global llm_collection

    try:
        logging.info("Modifying prompt using the following filters : {}".format(filters))
        results = llm_collection.find_one(filters)

        if results is not None:

            logging.info("Prompt found successfully")

            try :

                logging.info("Updating prompt with for the following filters : {}".format(filters))
                llm_collection.update_one(filters, {"$set": {"prompt" : new_values}})
                logging.info("Prompt modified successfully")

            except Exception as e :

                logging.error("Error during prompt modification")
                logging.error(e)

                return {
                    "status": 500,
                    "message": "Error during prompt modification"
                }

            return {
                "status": 200,
                "message": "Prompt modified"
            }
        else:

            logging.info("No prompt found")

            return {
                "status": 404,
                "message": "No prompt found"
            }
    except Exception as e:

        logging.error("Error during prompt modification")
        logging.error(e)

        return {
            "status": 500,
            "message": "Error during prompt modification"
        }
    
def create_prompt(data:dict):
    """
    Create a new prompt and splitter/ LLM configuration in the Database.

    Args:
        data (dict): The data to insert in the Database.

    Returns:
        dict: The result of the operation.
            - If the prompt is created, returns {"status": 200, "message": "Prompt created"}.
            - If the prompt already exists, returns {"status": 409, "message": "Prompt already exists"}.
    """
    
    global llm_collection

    try:
        logging.info("Creating prompt with the following data : {}".format(data))
        llm_collection.insert_one(data)
        logging.info("Prompt created successfully")

        return {
            "status": 200,
            "message": "Prompt created"
        }
    except DuplicateKeyError as dpke:
        logging.error("Prompt already exists")
        logging.error(dpke)
        return {
            "status": 409,
            "message": "Prompt already exists"
        }
    except Exception as e:
        logging.error("Error during prompt creation")
        logging.error(e)
        return {
            "status": 500,
            "message": "Error during prompt creation"
        }
    
def modify_llm_configuration (filters:dict, new_values:dict):
    """
    Modify LLM configuration using filters.

    Args:
        filters (dict): The filters used to retrieve information from Database.
        new_values (dict): The new values to update in the Database.

    Returns:
        dict: The result of the operation.
            - If the LLM configuration is found and modified, returns {"status": 200, "message": "LLM configuration modified"}.
            - If the LLM configuration is not found, returns {"status": 404, "message": "No LLM configuration found"}.
    """
    global llm_collection

    logging.info("Modifying LLM configuration using the following filters : \n {}".format(filters))

    try:
        logging.info("Retrieving LLM configuration using the following filters")
        results = llm_collection.find_one(filters)
        logging.info("LLM configuration found successfully")

        if results is not None:
            logging.info("Updating LLM configuration with the following filters : {}".format(filters))
            llm_collection.update_one(filters, {"$set": {"llm" : new_values}})
            logging.info("LLM configuration modified successfully")
            return {
                "status": 200,
                "message": "LLM configuration modified"
            }
        else:
            logging.info("No LLM configuration found")
            return {
                "status": 404,
                "message": "No LLM configuration found"
            }
    except Exception as e:

        logging.error("Error during LLM configuration modification")
        logging.error(e)

        return {
            "status": 500,
            "message": "Error during LLM configuration modification"
        }
    
def modify_splitter_configuration (filters:dict, new_values:dict):
    """
    Modify splitter configuration using filters.

    Args:
        filters (dict): The filters used to retrieve information from Database.
        new_values (dict): The new values to update in the Database.

    Returns:
        dict: The result of the operation.
            - If the splitter configuration is found and modified, returns {"status": 200, "message": "Splitter configuration modified"}.
            - If the splitter configuration is not found, returns {"status": 404, "message": "No splitter configuration found"}.
    """
    global llm_collection

    try:
        logging.info("Modifying splitter configuration using the following filters : {}".format(filters))

        logging.info("Retrieving splitter configuration using the above filters")
        results = llm_collection.find_one(filters)
        logging.info("Splitter configuration found successfully")

        if results is not None:

            try :
                logging.info("Updating splitter configuration with the following filters : {}".format(filters))
                llm_collection.update_one(filters, {"$set": {"splitter" : new_values}})
                logging.info("Splitter configuration modified successfully")

                return {
                    "status": 200,
                    "message": "Splitter configuration modified"
                }

            except Exception as e :

                logging.error("Error during splitter configuration modification")
                logging.error(e)

                return {
                    "status": 500,
                    "message": "Error during splitter configuration modification"
                }
        else:
            logging.info("No splitter configuration found")
            return {
                "status": 404,
                "message": "No splitter configuration found"
            }
        
    except Exception as e:

        logging.error("Error during splitter configuration modification")
        logging.error(e)
        return {
            "status": 500,
            "message": "Error during splitter configuration modification"
        }