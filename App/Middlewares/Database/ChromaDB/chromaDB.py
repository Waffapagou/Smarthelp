from App.Database.ChromaDB.Chroma import create_chroma_client, create_chroma_collection, add_chroma_documents_to_collection, generate_id, get_chroma_documents_from_collection, get_chroma_collection
from App.Configs.configuration import load_json

from App.Database.ChromaDB.TextSplitter import TextSplitter
from langchain_text_splitters import CharacterTextSplitter
from App.Database.ChromaDB.WebLoader import WebLoader

import chromadb

from chromadb.utils import embedding_functions


def middleware_chroma_create_client (client_path:str, persistent:bool) -> dict :
    """
    Create chroma client in system file
    """

    client = create_chroma_client(
                    client_path,
                    persistent=persistent
                )

    if client == None :
            return {
                "status" : 500,
                "message" : "ERROR : Error while creating chromaDB client"
            }
    # else
    return {
        "client" : client,
        "status" : 200,
        "message" : "Successfully created client"
    }

def middleware_chroma_create_collection(chroma_client:chromadb.Client, collection_name:str, collection_embedding) -> dict :
    """
    Create chroma collection
    """

    collection = create_chroma_collection(
        chroma_client = chroma_client,
        collection_name = collection_name,
        collection_embedding = collection_embedding
    )

    if collection == None :
         return {
                "status" : 500,
                "message" : "ERROR : Error while creating chromaDB collection"
            }
    
    # else
    return {
        "collection" : collection,
        "status" : 200,
        "message" : "Successfully created collection"
    }

def middleware_chroma_get_collection (chroma_client:chromadb.Client, collection_name:str, collection_embedding) :
    """
    Get chroma collection
    """

    collection = get_chroma_collection(
                    chroma_client = chroma_client,
                    collection_name = collection_name,
                    collection_embedding = collection_embedding
                )
    
    if collection == None :
        return {
                "status" : 500,
                "message" : "ERROR : error while getting collection"
            }

    return {
        "collection" : collection,
        "status" : 200,
        "message" : "Successfully got the collection"
    }

def middleware_init_chromaDB (client_path:str, collection_name:str, collection_embedding=embedding_functions.DefaultEmbeddingFunction(), persistent:bool=True) -> dict :
    """
    Initialize chromaDB or return the existing one

    Args:
    - client_path : str : path to the chromaDB client
    - collection_name : str : name of the collection
    - collection_embedding : embedding function
    - persistent : bool : whether the client is persistent or not

    Returns:
    - dict : status of the operation
    """
    
    # Create client
    client = middleware_chroma_create_client(
        client_path = client_path,
        persistent = persistent
    )

    # Check if client is created
    if client["status"] != 200 :
        # If not, return error
        return {
            "status" : 500,
            "message" : "ERROR : Error while creating chromaDB client"
        }
    
    # Else, check if collection already exists
    collection = middleware_chroma_get_collection(
        chroma_client = client["client"],
        collection_name = collection_name,
        collection_embedding = collection_embedding
    )

    # If collection does not exist, create it
    if collection["status"] != 200 :
        collection = middleware_chroma_create_collection(
            chroma_client = client["client"],
            collection_name = collection_name,
            collection_embedding = collection_embedding
        )

        # Check if collection is created
        if collection["status"] != 200 :
            return {
                "status" : 500,
                "message" : "ERROR : Error while creating chromaDB collection"
            }
        
    return {
        "status" : 200,
        "message" : "Successfully initialized chromaDB",
        "collection" : collection
    }

def middle_chroma_add_WebDocuments_to_collection(collection:chromadb.Collection, links_to_scrap:list ) -> dict:
     """
     Add Web Documents to collection 
     """

def middleware_chroma_add_document_to_collection (collection:chromadb.Collection, content_to_add:str, metadatas:dict, split_document:bool=False, separator:str="\n", chunk_size:int=2500, chunk_overlap:int=200, is_separator_regex:bool=False) :
     """
        Add document to chroma collection
    
        args :
            -> collection : The collection to add the document
            -> content_to_add : The content of the document
            -> metadatas : The metadatas of the document
            -> split_document : Split the document or not
            -> separator : The separator to use for splitting
            -> chunk_size : The size of the chunk
            -> chunk_overlap : The overlap of the chunk
            -> is_separator_regex : The separator is a regex or not

        return :
            Return dict
    """
     
     if split_document == True :
        ts = CharacterTextSplitter(
            separator = separator,
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            length_function = len,
            is_separator_regex = is_separator_regex
        )

        documents = ts.create_documents(
                        texts=[content_to_add],
                        metadatas=[{"author": "Jean", "file_name": "text1.txt"}]
                    )

        status = add_chroma_documents_to_collection(
                                chroma_collection=collection,
                                documents=[doc.page_content for doc in documents],
                                metadatas=[doc.metadata for doc in documents],
                                ids=[generate_id(200) for _ in range(len (documents))]
                            )
        
        if status == False :
            return {
                    "status" : 500,
                    "message" : "ERROR : error while adding documents to collection chromaDB"
                }
            
     else :

        status = add_chroma_documents_to_collection(
                                chroma_collection=collection,
                                documents=[content_to_add],
                                metadatas=[metadatas],
                                ids=[generate_id(200)]
                            )

        if status == False :
            return {
                    "status" : 500,
                    "message" : "ERROR : error while adding documents to collection"
                }

    # else
     return {
         "status" : 200,
         "message" : "Successfully added document to collection"
     }
     
def middleware_chroma_add_documents_to_collection (collection:chromadb.Collection, directory_path:str, glob:str) ->  dict :
    """
    Add documents to chroma collection
    """

    ts = TextSplitter(
        directory_path = directory_path,
        glob = glob
    )

    documents = ts.load ()

    documents_splitted = ts.CharacterSplitter(
                                files_to_split = documents
                            )
    
    status = add_chroma_documents_to_collection(
                            chroma_collection=collection,
                            documents=[doc.page_content for doc in documents_splitted],
                            metadatas=[doc.metadata for doc in documents_splitted],
                            ids=[generate_id(200) for _ in range(len (documents_splitted))]
                        )
    
    if status == False :
        return {
                "status" : 500,
                "message" : "ERROR : error while adding documents to collection"
            }
    
    # else
    return {
        "status" : 200,
        "message" : "Successfully added documents to collection"
    }

def middleware_chroma_get_documents_from_collection (chroma_collection:chromadb.Collection, query_text:str, n_result:int=3) -> dict :
    """
    Retrieve documents from collection
    """

    response = get_chroma_documents_from_collection(
                                        chroma_collection=chroma_collection,
                                        query_text=query_text,
                                        number_of_result=n_result
                                    )
    
    if response == None :
        return {
                "status" : 500,
                "message" : "ERROR : error while retrieving documents from collection"
            }
    # Else

    return {
        "response" : response,
        "status" : 200,
        "message" : "Successfully retrieved documents from collection"
    }