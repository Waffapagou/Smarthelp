import chromadb
import random
import string

import logging

def create_chroma_client (client_path:str, persistent:bool=True) -> chromadb.Client:
    """
    Create ChromaDB's client

    args :
        -> client_path : The path of the client
        -> persistent : Weither or not to create a persistent database or not

    return :
        Return Client
    """

    if persistent :

        try :
            logging.info("Creating persistent client in this path : {}".format(client_path))
            client = chromadb.PersistentClient(path=client_path)
            logging.info("Persistent client created successfully !")
            
        except Exception as e :
            logging.error("Error during creating persistent client")
            logging.error(e)
            return None
        
    else :
        try :
            logging.info("Creating non persistent client ...")
            client = chromadb.Client()
            logging.info("Non persistent client created successfully !")
            
        except Exception as e :
            logging.error("Error during creating non persistent client")
            logging.error(e)

            return None

    return client

def create_chroma_collection (chroma_client:chromadb.Client, collection_name:str, collection_embedding) -> chromadb.Collection :
    """
    Create collection in ChromaDB

    args :
        -> collection_name : The name of the collection
        -> collection_embedding : The embedding used in the collection

    return :
        Return Collection
    """

    try :
        logging.info("Creating collection in ChromaDB with the following name : {} and embedding : {}".format(collection_name, collection_embedding))
        collection = chroma_client.create_collection(name=collection_name, embedding_function=collection_embedding)
        logging.info("Collection created successfully !")
    
    except Exception as e :
        logging.error("Error during creating collection")
        logging.error(e)
        return None

    return collection
    
def get_chroma_collection (chroma_client:chromadb.Client, collection_name:str, collection_embedding:str) -> chromadb.Collection :
    """
    Get a created collection in ChromaDB

    args :
        -> collection_name : The name of the collection
        -> collection_embedding : The embedding used in the collection

    return :
        Return ChromaDB's collection
    """

    try :

        logging.info("Getting collection in ChromaDB with the following name : {} and embedding : {}".format(collection_name, collection_embedding))
        collection = chroma_client.get_collection(name=collection_name, embedding_function=collection_embedding)
        logging.info("Collection got successfully !")

    except Exception as e :

        logging.error("Error during getting collection")
        logging.error(e)

        return None

    return collection

def delete_chroma_collection (chroma_client:chromadb.Client, collection_name:str) -> bool :
    """
    Delete collection in ChromaDB

    args :
        -> chroma_client : The chromaDB client
        -> collection_name : The name of the collection to delete

    return :
        Return boolean
    """

    try :
        logging.info("Deleting collection in ChromaDB with the following name : {}".format(collection_name))
        chroma_client.delete_collection(name=collection_name)
        logging.info("Collection deleted successfully !")

    except Exception as e :
        logging.error("Error during deleting collection")
        logging.error(e)

        return False

    return True

def add_chroma_documents_to_collection (chroma_collection:chromadb.Collection, documents:list, metadatas:list, ids:list) -> bool :
    """
    Add documents to collection

    args :
        -> chroma_collection : The chromaDB collection
        -> documents : All the documents to add in the collection
        -> metadatas : The metadatas for all the documents to add
        -> ids : The ids for all the documents to add

    return :
        Return boolean
    """

    try :

        logging.info("Adding documents to collection ...")
        chroma_collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
        logging.info("Documents added successfully !")
    
    except Exception as e :

        logging.error("Error during adding documents to collection")
        logging.error(e)

        return False
    
    return True

def get_chroma_documents_from_collection (chroma_collection:chromadb.Collection, query_text:str, number_of_result:int=3) :
    """
    Get documents from collection

    args :
        -> chroma_collection : The chromaDB collection
        -> query_text : The text used for query
        -> number_of_result : The number of documents to return


    return :
        Return list of result
    """

    try :
        logging.info("Querying documents from vector collection ...")
        result = chroma_collection.query(
            query_texts=query_text,
            n_results=number_of_result
        )
        logging.info("Documents queried successfully !")
    
    except Exception as e :

        logging.error("Error during querying documents from collection")
        logging.error(e)

        return None
    
    return result

def generate_id (length) :

    logging.info("Generating id ...")

    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))

    logging.info("Id generated successfully !")

    return result_str