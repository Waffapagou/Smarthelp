from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter

class WebLoader () :
    """
    This class gathers all the function that load / splits Web Based data for Rag purpose
    """

    def __init__(self, urls_to_scrape:list) :

        self.__urls = urls_to_scrape
        self.raw_data = None
        self.cleaned_data = None

        self.documents = None

    def load(self) :
        """
        Read the data tru the loader
        """
        loader = WebBaseLoader(self.__urls)

        try : 
            self.raw_data = loader.load()
        except Exception as e :
            print (e)
            return None
        
        return self.raw_data
    
    def __clean_data (self) :

        new_list_data = []
        new_list_metadata = []

        for content in self.raw_data :

            temp_data = list ()
            new_list_metadata.append(content.metadata)
            splitted_data = content.page_content.split("\n")

            for s in splitted_data :
                if len (s) != 0 :
                    temp_data.append(s)
            
            new_list_data.append("\n".join([line for line in temp_data]))
            temp_data = list()

        self.cleaned_data = {
            "datas" : new_list_data,
            "metadatas" : new_list_metadata
        }

        return self.cleaned_data
    
    def CharacterSplitter (self, separator:str="\n", chunk_size:int=2500, chunk_overlap:int=200, is_separator_regex:bool=False) -> bool :

        # Clean the data
        self.__clean_data()

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
            documents = text_splitter.create_documents([doc for doc in self.cleaned_data["datas"]], [doc for doc in self.cleaned_data["metadatas"]])
        except Exception as e :
            print (e)
            return None

        try :
            # split the documents
            splitted_documents = text_splitter.split_documents(documents)
        except Exception as e:
            print (e)
            return None

        self.documents = splitted_documents

        return splitted_documents
    
    def get_raw_data (self) :
        """
        return the raw data
        """
        return self.__raw_data