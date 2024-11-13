from flask import Flask, request, jsonify, Blueprint
from App.Configs.configuration import load_json

config_file_path = 'App/Configs/configuration.json'
CONFIG_FILE = load_json(config_file_path)

server = Blueprint('server', __name__)

@server.route('/server/status')
def get_status():
    """
    Returns the status of the application.

    :return: A dictionary containing the status message.
    """
    return {
        'status': "Running", 
        'version': CONFIG_FILE["api"]["version"]["code"],
        'name': CONFIG_FILE["api"]["version"]["name"],
        'states': CONFIG_FILE["api"]["version"]["states"] 
    }