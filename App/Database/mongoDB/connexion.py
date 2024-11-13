"""
Gathers all the functions to connect to database
"""
from pymongo import MongoClient
from App.Configs.configuration import load_json

import logging

MONGO_CLIENT = None
MONGO_DATABASE = None

def connect_database () :
    """
    Connect to MongoDB client and database
    """

    
    # Read config file
    try :
        logging.info("Reading config file to get Database connexion's informations ")
        config_file = load_json("App/Configs/configuration.json")
        logging.info("Config file read successfully !")

    except Exception as e :
        logging.error("Error during reading config file")
        logging.error(e)


    # Connect to MongoClient
    global MONGO_CLIENT
    try :
        logging.info("Connecting to mongoDB client in this adress : localhost:27017 ...")
        MONGO_CLIENT = MongoClient("localhost",27017)
        logging.info("Connected to mongoDB client successfully")

    except Exception as e :
        logging.error("Error during connecting to mongoDB client")
        logging.error (e)

    # Connect to database
    global MONGO_DATABASE
    try :
        logging.info("Connecting to SmartHelp Database ...")
        MONGO_DATABASE = MONGO_CLIENT[config_file["database"]["mongoDB"]["database"]["name"]]
        logging.info("Connected to SmartHelp Database successfully")

    except Exception  as e :
        logging.error("Error during connecting to SmartHelp Database !")
        logging.error(e)

def get_database ():
    """
    Return database
    """
    global MONGO_DATABASE

    return MONGO_DATABASE