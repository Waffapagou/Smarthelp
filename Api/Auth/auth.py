from flask import jsonify, request, Blueprint, session, make_response

from App.Middlewares.Database.MongoDB.auth import middle_modify_password, middle_register_user, middle_get_user, middle_activate_account, middle_check_user_credentials, middle_update_credentials
from App.Middlewares.Database.MongoDB.llm import middle_create_prompt, middle_get_prompt, middle_modify_prompt, middle_modify_splitter_configurations, middle_modify_llm_configurations
from App.Configs.configuration import load_json

CONFIGURATION = load_json("App/Configs/configuration.json")
BASE_URL_NAME = CONFIGURATION["api"]["base_name"]

auth = Blueprint('auth', __name__)

@auth.route(BASE_URL_NAME+'/user/create', methods=['POST'])
def register_user():

    if request.method == 'POST' :
        data = request.get_json()
        
        result = middle_register_user({
            "name": data["name"],
            "email": data["email"],
            "pwd": data["pwd"],
            "type": data["type"]
        })

        if result["status"] == 409 :
            return jsonify({"message" : "Email already exists"}), 409


        if result["status"] == 500:
            return jsonify({"message": "Error during user registration"}), 500

        return jsonify(result["token"]), 200

# Modify user's password
@auth.route(BASE_URL_NAME+'/user/password/modify', methods=['POST'])
def modify_user_password():
    """
    Modify user's password.
    """
    # Check user session
    if "user_token" not in session:
        return jsonify({"message": "No session found"}), 404

    if request.method == 'POST':
        data = request.get_json()

        result = middle_modify_password(
            user_token=session["user_token"],
            new_pwd=data["pwd"]
        )

        if result["status"] == 404:
            return jsonify({"message": "No user found"}), 404

        if result["status"] == 500:
            return jsonify({"message": "Error during user information retrieval"}), 500

        return jsonify({"message": "Password modified"}), 200
    
# Modify user's credentials
@auth.route(BASE_URL_NAME+'/user/credentials/modify', methods=['POST'])
def modify_user_credentials():
    """
    Modify user's credentials.
    """
    # Check user session
    if "user_token" not in session:
        return jsonify({"message": "No session found"}), 404

    if request.method == 'POST':
        data = request.get_json()

        print (data)

        result = middle_update_credentials(
            user_token=session["user_token"],
            new_pseudo=data["name"],
            new_email=data["email"]
        )

        if result["status"] == 404:
            return jsonify({"message": "No user found"}), 404

        if result["status"] == 500:
            return jsonify({"message": "Error during user information retrieval"}), 500

        return jsonify({"message": "Credentials modified"}), 200

@auth.route(BASE_URL_NAME+'/user/login', methods=['POST'])
def login_user():
    """
    Login user.
    """
    # check if session exists
    if "user_token" in session:
        # Redirect to the home page
        return jsonify({"message": "User already logged in"}), 200

    if request.method == 'POST':

        data = request.get_json()

        user_credentials = {
            "email" : data["email"],
            "pwd" : data["pwd"]
        }

        result = middle_check_user_credentials(user_credentials)

        if result["status"] == 404:
            return jsonify({"message": "No user found"}), 404

        if result["status"] == 500:
            return jsonify({"message": "Error during user information retrieval"}), 500

        return jsonify(result["user_token"]), 200

@auth.route(BASE_URL_NAME+'/account/activate/<user_token>', methods=['GET'])
def activate_account(user_token):
    """
    Verify user account using token.
    """
    try:
        token = user_token
        if not token:
            return jsonify({"message": "Token is missing"}), 400

        # Verify the token and perform necessary actions
        result = middle_get_user(user_token)

        if result["status"] == 404:
            return jsonify({"message": "Account was not Activated"}), 404
            
        if result["status"] == 500:
            return jsonify({"message": "Error during account activation"}), 500

        # Change User acitvation status in database
        account_activation_result =  middle_activate_account(user_token)

        if account_activation_result["status"] == 404:
            return jsonify({"message": "No user found"}), 404
        
        if account_activation_result["status"] == 500:
            return jsonify({"message": "Error during account activation"}), 500

        return jsonify({"message": "Account verified successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@auth.route(BASE_URL_NAME+'/user/session/create/<user_token>', methods=['GET'])
def create_session(user_token:str):
    """
    Create a new session.
    """
    # Check if the token is valid
    result = middle_get_user(user_token)

    # check if session exists
    if "user_token" in session:
        # Redirect to the home page
        return jsonify({"message": "User already logged in"}), 200

    if result["status"] == 404:
        return jsonify({"message": "No user found"}), 404
    
    if result["status"] == 500:
        return jsonify({"message": "Error during user information retrieval"}), 500
    
    session["user_token"] = user_token

    resp = make_response()

    resp.set_cookie(
        "user_token",
        user_token,
        max_age=60*60*24*365*2
    )

    return resp

@auth.route(BASE_URL_NAME+'/user/session/destroy', methods=['GET'])
def destroy_session():
    """
    Destroy the current session.
    """
    # Check if the session exists
    if "user_token" not in session:
        return jsonify({"message": "No session found"}), 404
    
    # Destroy the session
    session.pop("user_token", None)

    resp = make_response()

    resp.set_cookie(
        "user_token",
        "",
        max_age=0
    )

    return resp

@auth.route(BASE_URL_NAME+'/user/llm/create', methods=['POST'])
def create_user_llm_prompt() :
    """
    Create a new prompt for the user.
    """

    if request.method == 'POST':
        data = request.get_json()

        data["llm"]["context_length"] = 256
        data["llm"]["max_length"] = 512
        data["llm"]["gpu_layers"] = 18

        data["splitter"] = {
            "chunk_size" : 256,
            "chunk_overlap" : 512,
            "separator" : "\n"
        }

        result = middle_create_prompt(data)

        if result["status"] == 409:
            return jsonify({"message": "Prompt already exists"}), 409

        if result["status"] == 500:
            return jsonify({"message": "Error during prompt creation"}), 500

        return jsonify({"message": "Prompt created"}), 200
    
@auth.route(BASE_URL_NAME+'/user/llm/get/<user_token>', methods=['GET'])
def get_user_llm_prompt(user_token:str) :
    """
    Get the user's prompt.
    """

    if request.method == 'GET':

        result = middle_get_prompt({"user_token": user_token})

        if result["status"] == 404:
            return jsonify({"message": "No prompt found"}), 404

        if result["status"] == 500:
            return jsonify({"message": "Error during prompt retrieval"}), 500

        return jsonify(result["prompt"]), 200
    
@auth.route(BASE_URL_NAME+'/user/llm/get/', methods=['GET'])
def get_user_prompt() :
    """
    Get the user's prompt. (USED WITH SESSIONS ONLY)
    """
    # Check user session
    if "user_token" not in session:
        return jsonify({"message": "No session found"}), 404

    if request.method == 'GET':

        result = middle_get_prompt({"user_token": session["user_token"]})

        if result["status"] == 404:
            return jsonify({"message": "No prompt found"}), 404

        if result["status"] == 500:
            return jsonify({"message": "Error during prompt retrieval"}), 500

        return jsonify(result["prompt"]), 200
    
@auth.route(BASE_URL_NAME+'/user/splitter/modify', methods=['POST'])
def modify_user_splitter_configurations() :
    """
    Modify the user's splitter configurations.
    """
    # Check user session
    if "user_token" not in session:
        return jsonify({"message": "No session found"}), 404

    if request.method == 'POST':
        data = request.get_json()

        data["chunk_size"] = int (data["chunk_size"])
        data["chunk_overlap"] = int (data["chunk_overlap"])
        

        result = middle_modify_splitter_configurations({"user_token": session["user_token"]},  data)

        if result["status"] == 404:
            return jsonify({"message": "No splitter configurations found"}), 404

        if result["status"] == 500:
            return jsonify({"message": "Error during splitter configurations modification"}), 500

        return jsonify({"message": "Splitter configurations modified"}), 200
    
@auth.route(BASE_URL_NAME+'/user/llm/configuration/modify', methods=['POST'])
def modify_user_llm_configuration() :
    """
    Modify the user's llm configurations.
    """
    # Check user session
    if "user_token" not in session:
        return jsonify({"message": "No session found"}), 404

    if request.method == 'POST':
        data = request.get_json()
        data["name"] = "mistral"
        data["context_length"] = int (data["context_length"])
        data["max_length"] = int (data["max_length"])
        data["gpu_layers"] = int (data["gpu_layers"])

        result = middle_modify_llm_configurations({"user_token": session["user_token"]}, data)

        if result["status"] == 404:
            return jsonify({"message": "No llm configurations found"}), 404

        if result["status"] == 500:
            return jsonify({"message": "Error during llm configurations modification"}), 500

        return jsonify({"message": "Llm configurations modified"}), 200


@auth.route(BASE_URL_NAME+'/user/llm/modify', methods=['POST'])
def modify_user_llm_prompt() :
    """
    Modify the user's prompt.
    """
    # Check user session
    if "user_token" not in session:
        return jsonify({"message": "No session found"}), 404

    if request.method == 'POST':
        data = request.get_json()
        result = middle_modify_prompt({"user_token": session["user_token"]}, data)

        if result["status"] == 404:
            return jsonify({"message": "No prompt found"}), 404

        if result["status"] == 500:
            return jsonify({"message": "Error during prompt modification"}), 500

        return jsonify({"message": "Prompt modified"}), 200