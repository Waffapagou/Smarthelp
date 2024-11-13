import os
from flask import Flask
from flask_dropzone import Dropzone

from App.Configs.configuration import load_json
import logging

# Define the logger here
logging.basicConfig(level=logging.DEBUG, filename='./Log/app.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.info('Starting the application...')
logging.info('Loading the configuration...')

basedir = os.path.abspath(os.path.dirname(__file__))
config_file_path = 'App/Configs/configuration.json'

app = Flask (__name__)

app.config.update(
    UPLOADED_PATH = os.path.join(os.path.join(basedir,'uploads')),
    DROPZONE_MAX_FILE_SIZE = 1024,
    DROPZONE_TIMEOUT = 5*50*1000
)
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.csv, .xlsx, .xls, .txt, .pdf'

app.secret_key = "smarthelp" # Session access

dropzone = Dropzone(app)

# Load the configuration
CONFIG_FILE = load_json(config_file_path)

logging.info('Configuration loaded successfully!')

from Api.Auth.auth import auth
from Api.Server.server import server
from Api.WebApp.webapp import web
from Api.LLM.llm import llm
from Api.Functions.file import file

logging.info('Registering the blueprints...')
# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(server)
app.register_blueprint(web)
app.register_blueprint(llm)
app.register_blueprint(file)

logging.info('Blueprints registered successfully!')
# Load LLM in database
from App.Middlewares.LLM.llm import middle_llm_load

middle_llm_load()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)