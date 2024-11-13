from langchain_community.llms import CTransformers
from langchain_core.prompts import PromptTemplate

from langchain_core.output_parsers import StrOutputParser

from langchain_community.llms import Ollama

class LLM () :

    def __init__(self, model:str, prompt_template:str, llm_configuration:dict):

        self.__model = model

        self.__llm = None
        self.__llm_configuration = llm_configuration
        self.__prompt_template = prompt_template
        
        self.__prompt = None
        self.__chain = None

    def load (self) :
        """
        load the model and the prompt in memory

        Return :
        ------- 
            Boolean
        """

        # Loading the model
        try :

            self.__llm = Ollama(
                model="mistral",
                format=None,
                num_predict = self.__llm_configuration["max_new_tokens"],
                num_ctx = self.__llm_configuration["context_length"]
            )

        except Exception as e:

            print("problème : "+ str(e))
            return False
        
        # Loading the prompt
        try :

            self.__prompt = PromptTemplate.from_template(self.__prompt_template)
            self.__chain = self.__prompt | self.__llm | StrOutputParser()

        except Exception as e:
            print("Prompt did not load")
            print(e)

            return False

        return True

    def chat (self, query:str, context:str, historique_conversation:str=None) -> str:
        """
        Chat with the llm

        args :
        ------
            - query : The question to ask to the llm
        """

        reponse = self.__chain.invoke ({"context": context, "query": query})

        return reponse
    
    def rechain (self, prompt:str) :
        """
        Rechain the prompt
        """

        self.__prompt = PromptTemplate.from_template(prompt)
        self.__chain = self.__prompt | self.__llm | StrOutputParser()

        return True