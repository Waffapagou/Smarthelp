import os

from flask import jsonify, request, Blueprint, session, make_response, send_from_directory

from App.Configs.configuration import load_json
from App.Database.mongoDB.file import get_file_info
from App.Utilities.FileSystem.UserDirectory import get_user_files_dir

from io import StringIO

from App.Middlewares.Database.MongoDB.file import middle_add_file, middle_delete_file
from App.Middlewares.Database.MongoDB.llm import middle_get_prompt
from App.Middlewares.Database.ChromaDB.chromaDB import middleware_chroma_add_document_to_collection, middleware_init_chromaDB
from App.Middlewares.Function.file import middle_read_pdf

CONFIGURATION = load_json("App/Configs/configuration.json")
BASE_URL_NAME = CONFIGURATION["api"]["base_name"]

# define bluePrint
file = Blueprint('file', __name__)

@file.route(BASE_URL_NAME+"/file/uploads", methods=["POST"])
def file_uploads ():

    if "user_token" not in session :
        return jsonify({
            "message" : "No sessions declared"
        }, 500)

    if request.method == 'POST':

        # Getting the files
        file = request.files.get('file')

        if file is None:
            return jsonify({
                "message" : "No file was sent"
            }, 404)
        
        # Getting the file name
        file_name = file.filename

        # Write file in the local system
        file.save(get_user_files_dir(user_token=session["user_token"])+ "/" + file_name)

        # Getting the file extension
        file_extension = file_name.split(".")[-1]
        # Getting the file size
        file_size = os.path.getsize(get_user_files_dir(user_token=session["user_token"])+ "/" + file_name)

        result = middle_add_file (
            user_token=session["user_token"],
            file_name=file_name,
            file_extension=file_extension,
            file_size=file_size
        )

        # If the file is not added to the database
        if result["status"] == 500:
            return jsonify({
                "message" : "Error during file addition"
            }, 500)
        
        # Check the file extension to trigger the right action
        if file_extension == "txt" or file_extension == "csv" or file_extension == "json" :

            # Reading the file content (Only when it txt, csv, json)
            stringio = StringIO(file.getvalue().decode("utf-8"))
            string_data = stringio.read()

        elif file_extension == "pdf":
            # Reading the file content (Only when it pdf)
            
            result = middle_read_pdf(file=get_user_files_dir(user_token=session["user_token"])+ "/" + file_name)

            if result["status"] == 500:
                return jsonify({
                    "message" : "Error during PDF reading"
                }, 500)

            string_data = result["message"]

        elif file_extension == "docx":
            # Reading the file content (Only when it docx)
            string_data = ""

        elif file_extension == "xlsx":
            # Reading the file content (Only when it xlsx)
            string_data = ""

        collection = middleware_init_chromaDB(
            client_path=CONFIGURATION["database"]["chromaDB"]["directory_path"],
            collection_name=session["user_token"],
        )

        if collection["status"] == 500:
            return jsonify({
                "message" : "Error during chromaDB initialization"
            }, 500)


        # Getting user's llm configuration
        result = middle_get_prompt({
            "user_token": session["user_token"]
        })

        if result["status"] == 500:
            return jsonify({
                "message" : "Error during llm configuration retrieval"
            }, 500)

        # Adding file to chromaDB
        status = middleware_chroma_add_document_to_collection (
            collection = collection["collection"]["collection"],
            content_to_add = string_data,
            metadatas={"source" : file.name},
            split_document=True,
            separator=result["data"]["splitter"]["separator"],
            chunk_size=result["data"]["splitter"]["chunk_size"],
            chunk_overlap=result["data"]["splitter"]["chunk_overlap"],
            is_separator_regex=False
        )

        if status ["status"] == 500 :
            jsonify({
                "message" : "Error while adding element to KB"
            }, 500)
            

        return jsonify({
            "message" : "File added to Knowledge Base"
        }, 200) 
    
# File deleted
@file.route(BASE_URL_NAME+"/file/delete", methods=["POST"])
def file_delete ():

    if "user_token" not in session :
        return jsonify({
            "message" : "No sessions declared"
        }, 500)

    data = request.get_json()

    if data is None:
        return jsonify({
            "message" : "No data was sent"
        }, 404)

    if "file_name" not in data:
        return jsonify({
            "message" : "No file name was sent"
        }, 404)

    result = get_file_info({
        "user_token": session["user_token"],
        "file_name": data["file_name"]
    })

    if result["status"] == 404:
        return jsonify({
            "message" : "No file found"
        }, 404)

    if result["status"] == 500:
        return jsonify({
            "message" : "Error during file information retrieval"
        }, 500)

    os.remove(get_user_files_dir(user_token=session["user_token"])+ "/" + data["file_name"])
    result = middle_delete_file(
        user_token=session["user_token"],
        file_name=data["file_name"]
        )

    if result["status"] == 500:
        return jsonify({
            "message" : "Error during file deletion"
        }, 500)
    
    return jsonify({
        "message" : "File deleted"
    }, 200)

@file.route(BASE_URL_NAME+"/file/download/<file_id>", methods=["GET"])
def file_download (file_id:str):
    
        if "user_token" not in session :
            return jsonify({
                "message" : "No sessions declared"
            }, 500)
    
        result = get_file_info({
            "user_token": session["user_token"],
            "file_id": file_id
        })
    
        if result["status"] == 404:
            return jsonify({
                "message" : "No file found"
            }, 404)
    
        if result["status"] == 500:
            return jsonify({
                "message" : "Error during file information retrieval"
            }, 500)
    
         
        return make_response(send_from_directory(get_user_files_dir(session["user_token"])+"/"+result["data"]["file_name"], as_attachment=True))