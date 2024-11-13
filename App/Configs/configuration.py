import json

def load_json(file_path:str) :

    try :
        file = open(file_path)
        data = json.load(file)

    except Exception as e :
        print (e)
        return None

    return data

def save_json (dict_to_save:dict, path_to_save:str) :
    with open(path_to_save, "w") as outfile: 
        json.dump(dict_to_save, outfile)