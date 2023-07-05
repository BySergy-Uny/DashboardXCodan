from flask import Flask
from dotenv import dotenv_values
from flask_login import LoginManager
from app.models.user import User
import dash

# import os

# os.system("start ./app/static/init.wav")

# import pygame
# pygame.mixer.init()
# sound = pygame.mixer.Sound("app/static/init.wav")
# sound.play()
 

config = dotenv_values("./.env")

app = Flask(__name__, 
            static_url_path='', 
            static_folder='static',
            template_folder='templates')


app_dash = dash.Dash(__name__, title="DashboardXCodan", update_title="DashboardXCodan ..." ,server=app, url_base_pathname='/visualiation/')
app_dash._favicon = "logomark-ligth-dashboardxcodan-withoutbg-fit.ico"

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