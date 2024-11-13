from App.Middlewares.Database.ChromaDB.chromaDB import middleware_chroma_get_documents_from_collection, middleware_init_chromaDB
from App.Configs.configuration import load_json
from App.Configs.prompt_template import prompt_template
from App.Models.LLM.LLM import LLM

from chromadb.utils import embedding_functions

config = load_json("App/Configs/configuration.json")
llm = None
chroma_collection = None

def __load_llm () :

    config_load = load_json("App/Configs/configuration.json")

    llm = LLM(
            model = "mistral",
            prompt_template = prompt_template,
            llm_configuration = config_load["llm"]["configuration"]
        )
    
    llm.load()

    return llm

def __unload_llm () :

    try :
        llm = None
    except Exception as e :
        print (e)
        return False

    return True

def __get_chroma_collection (chroma_collection_name:str) :
    """
    Get the chroma collection
    
    Args:
    - chroma_collection_name : str : the name of the chroma collection

    Returns:
    - dict : the chroma collection
    """

    if chroma_collection is None :
       return {
              "status" : 500,
              "message" : "ERROR : 'None' collection does not exist"
       }

    return middleware_init_chromaDB(
        client_path=config["database"]["chromaDB"]["directory_path"],
        client_name=chroma_collection_name
    )

def __search_document (chroma_collection, query:str) :

    documents = middleware_chroma_get_documents_from_collection (
        chroma_collection = chroma_collection,
        query_text = query,
        n_result = config["database"]["chromaDB"]["number_of_result"]
    )

    doc_context = "\n\n".join(documents["response"]["documents"][0])

    return doc_context

def response_generator(llm, query:str, context:str, historique:str= None):

    response = llm.chat(
        query = query,
        context = context,
        historique_conversation = None
    )

    print (context)

    return response

def middle_llm_chat (query : str, chroma_collection_name:str, prompt_template:str = None) :
    """
    Chat with the LLM.

    Args:
    - query : str : the query to chat with the LLM
    - chroma_collection_name : str : the name of the chroma collection
    - prompt_template : str : the prompt template to use

    Returns:
    - dict : the response of the LLM
    """

    if prompt_template is not None :
        
        # Get the chroma collection
        chroma_collection_chat = middleware_init_chromaDB(
            client_path=config["database"]["chromaDB"]["directory_path"],
            collection_name=chroma_collection_name
        )

        if chroma_collection_chat["status"] == 500 :
            return {
                "status" : 500,
                "message" : "ERROR : While initializing the chroma collection"
            }

        documents = __search_document (chroma_collection = chroma_collection_chat["collection"]["collection"], query = query)

        response = response_generator (
            llm=llm,
            query = query,
            context = documents
        )

    else :

        llm.rechain(prompt_template)

        response = response_generator (
            llm=llm,
            query = query,
            context = prompt_template
        )

    return {
        "status" : 200,
        "response" : response
    }

def middle_llm_unload () -> dict:
    """
    Unload the llm from memory
    """
    status = __unload_llm()

    if status :
        return {
            "status" : 200,
            "message" : "LLM successfully unloaded"
        }
    else :
        return {
            "status" : 500,
            "message" : "LLM unsuccessfully unloaded"
        }
    
def middle_llm_load (chroma_collection_name:str=None):
    """
    Load the llm to memory
    """
    global llm
    global chroma_collection

    llm = __load_llm()

    if chroma_collection is not None :
        chroma_collection = __get_chroma_collection(chroma_collection_name=chroma_collection_name)["collection"]

    return llm

def middle_llm_reload () :
    """
    Reload the llm in memory
    """

    global llm
    llm = None

    config_load = load_json("App/Configs/configuration.json")

    llm = LLM(
            model_path = config_load["llm"]["path"],
            model_type = config_load["llm"]["type"],
            prompt_template = prompt_template,
            llm_configuration = config_load["llm"]["configuration"]
        )
    
    llm.load()

    return llm