"""
Contains all the functions to add file to database
"""
from App.Database.mongoDB.connexion import get_database, connect_database

import logging

# Getting the collections "files" that stores all the files
connect_database()

database = get_database()
files = database["files"]

def add_file(file:dict) -> dict:
    """
    Add file to database.

    Args:
        file (dict): The file to add to database.

    Returns:
        dict: The result of the operation.
            - If the file is added, returns {"status": 200, "message": "File added"}.
            - If the file is not added, returns {"status": 500, "message": "Error during file addition"}.
    """

    global files

    try:

        logging.info("Adding file the following file to database : {}".format(file))
        files.insert_one(file)
        logging.info("File added successfully")

        return {
            "status": 200,
            "message": "File added"
        }
    except Exception as e:

        logging.error("Error during file addition")
        logging.error(e)

        return {
            "status": 500,
            "message": "Error during file addition"
        }
    
def get_file_info(filters:dict):
    """
    Get file information using filters.

    Args:
        filters (dict): The filters used to retrieve information from Database.
    
    Returns:
        dict: The result of the operation.
            - If the file is found, returns {"status": 200, "data": {"file_name": str, "file_extension": str, "file_size": int, "file_type": str}}.
            - If the file is not found, returns {"status": 404, "message": "No file found"}.
    """

    global files

    try:
        logging.info("Retrieving file information using the following filters : {}".format(filters))

        results = files.find_one(filters)

        if results is not None:
            logging.info("File found successfully")
            return {
                "status": 200,
                "data": results
            }
        else:
            logging.info("No file found")
            return {
                "status": 404,
                "message": "No file found"
            }
    except Exception as e:

        logging.error("Error during file information retrieval")
        logging.error(e)

        return {
            "status": 500,
            "message": "Error during file information retrieval"
        }
    
def delete_file(filters:dict) -> dict:
    """
    Delete file from database.

    Args:
        filters (dict): The filters used to retrieve information from Database.

    Returns:
        dict: The result of the operation.
            - If the file is deleted, returns {"status": 200, "message": "File deleted"}.
            - If the file is not deleted, returns {"status": 500, "message": "Error during file deletion"}.
    """

    global files

    try:
        logging.info("Deleting file using the following filters : {}".format(filters))
        files.delete_one(filters)
        logging.info("File deleted successfully")
        return {
            "status": 200,
            "message": "File deleted"
        }
    except Exception as e:

        logging.error("Error during file deletion")
        logging.error(e)

        return {
            "status": 500,
            "message": "Error during file deletion"
        }
    
def get_files(filters:dict) -> dict:
    """
    Get files information using filters.

    Args:
        filters (dict): The filters used to retrieve information from Database.

    Returns:
        dict: The result of the operation.
            - If the files are found, returns {"status": 200, "data": [{"file_name": str, "file_extension": str, "file_size": int, "file_type": str}]}.
            - If the files are not found, returns {"status": 404, "message": "No files found"}.
    """

    global files

    try:
        logging.info("Retrieving files information using the following filters : {}".format(filters))
        results = files.find(filters)
        
        if results is not None:
            logging.info("Files found successfully")
            return {
                "status": 200,
                "data": results
            }
        else:
            logging.info("No files found")
            return {
                "status": 404,
                "message": "No files found"
            }
    except Exception as e:
        logging.error("Error during files information retrieval")
        logging.error(e)
        return {
            "status": 500,
            "message": "Error during files information retrieval"
        }