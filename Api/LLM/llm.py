from flask import jsonify, request, Blueprint, session
from App.Configs.configuration import load_json

from App.Middlewares.LLM.llm import middle_llm_chat
from App.Middlewares.Database.MongoDB.llm import middle_get_prompt

from App.Middlewares.Database.ChromaDB.chromaDB import middleware_init_chromaDB

CONFIGURATION = load_json("App/Configs/configuration.json")
BASE_URL_NAME = CONFIGURATION["api"]["base_name"]

llm = Blueprint('llm', __name__)

@llm.route(BASE_URL_NAME+'/llm/chat', methods=['POST'])
def chat():
    """
    Chat with the LLM.
    """
    if request.method == 'POST':

        data = request.get_json()

        if "user_token" in session :
            data["user_token"] = session["user_token"]

        if "user_token" not in data :
            return jsonify({"message" : "user_token is required"}), 400

        prompt_result = middle_get_prompt(
            {
                "user_token": data["user_token"]
            }
        )

        if prompt_result["status"] == 404:
            return jsonify({"message": "No prompt found"}), 404
        
        if prompt_result["status"] == 500:
            return jsonify({"message": "Internal server error"}), 500 

        response = middle_llm_chat (
            query=data["query"],
            chroma_collection_name=data["user_token"],
            prompt_template=prompt_result["data"]["prompt"]
        )

        if response["status"] == 500:
            return jsonify({"message": "Internal server error. No ChromaDB detected !"}), 500

        return jsonify({"message" : "ok", "response" : response["response"]}), 200
    
    return jsonify({"message" : "Method not allowed"}), 405