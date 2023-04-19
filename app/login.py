from flask import Flask, request

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    print("[+] user_id validator: " , user_id)
    return active_user

class User(UserMixin):
    id = "0"
    username = "pruebas"
    password = "pruebas"



@app.route('/')
def home():
    return "<h1>HOME</h1> \
            <a href='login'>Login Page</a> <br>\
            <a href='dashboard'>Dashboard Page</a> <br>\
            <a href='info'>Info Page</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    password = request.args.get('password')
    if password=="pepe":
        active_user.id = 1
        active_user.name = "sergio"
        active_user.password = "pepe"
        login_user(active_user)
        return "<h1>USER PAGE</h1> \
            <a href='dashboard'>Dashboard Page</a> <br>\
            <a href='info'>Info Page</a> <br>\
                <a href='logout'>Logout</a>"
    else:
        return 'Error login!!'
    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return 'Logout!!'

@app.route('/dashboard')
@login_required
def dashboard():
    return 'dashboard'

@app.route('/info')
@login_required
def info():
    return 'info'

if __name__ == '__main__':
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    active_user = User()
    app.run(debug=True)
    

