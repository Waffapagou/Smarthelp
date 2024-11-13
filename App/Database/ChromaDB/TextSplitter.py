from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter

import logging

class TextSplitter () :

    def __init__(self, directory_path:str, glob:str) :

        self.__directory_path = directory_path
        self.__glob = glob

        self.__docs = None

        self.__loader = DirectoryLoader(
            path = self.__directory_path,
            glob = self.__glob
        )

    def load (self) :

        try :

            logging.info("Loading documents to split from the directory : {}".format(self.__directory_path))
            self.__docs = self.__loader.load()
            logging.info("Documents loaded successfully !")

        except Exception as e :

            logging.error("Error during loading documents")
            logging.error(e)

            return False

        return self.__docs
    
    def CharacterSplitter (self, files_to_split:list, separator:str="\n", chunk_size:int=2500, chunk_overlap:int=200, is_separator_regex:bool=False) -> bool :

        # Init the splitter
        text_splitter = CharacterTextSplitter(
                                separator=separator,
                                chunk_size=chunk_size,
                                chunk_overlap=chunk_overlap,
                                length_function=len,
                                is_separator_regex=is_separator_regex,
                            )

        try :
            # Init the documents from the files to
            logging.info("Creating documents from the files to split ...")
            documents = text_splitter.create_documents([doc.page_content for doc in files_to_split], [doc.metadata for doc in files_to_split])
            logging.info("Documents created successfully !")

        except Exception as e :

            logging.error("Error during creating documents")
            logging.error(e)

            return None

        try :
            # split the documents
            logging.info("Splitting documents ...")
            splitted_documents = text_splitter.split_documents(documents)
            logging.info("Documents splitted successfully !")

        except Exception as e:
            logging.error("Error during splitting documents")
            logging.error(e)
            return None

        return splitted_documents
    
    def get_loader (self) :
        return self.__loader