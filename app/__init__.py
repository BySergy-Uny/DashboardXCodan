from flask import Flask
from dotenv import dotenv_values
from app.tools.database_connection import *
from flask_login import LoginManager
from app.models.user import User

config = dotenv_values("./.env")



app = Flask(__name__, 
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    id = user_id
    print("[+] user_id: ", active_user.id, id)
    return active_user

active_user = User()

from app.routes import landing, login, visualization