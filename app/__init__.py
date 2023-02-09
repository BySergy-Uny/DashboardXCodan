from flask import Flask
from dotenv import dotenv_values
from app.tools.database_connection import *

config = dotenv_values("./.env")


db_mongo = databaseTool(config)

app = Flask(__name__, 
            static_url_path='', 
            static_folder='static',
            template_folder='templates')


from app.routes import landing

