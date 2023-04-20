from flask_login import login_user, current_user, logout_user
from app import app, active_user
from flask import render_template, request, redirect, url_for
from app.tools.token import generate_token
from app.models.user import User
from deta import Deta

from dotenv import dotenv_values

config = dotenv_values("./.env")


@app.route("/login", methods=['GET'])
def login():
    try:
        print("[+]  active user: " +  active_user.name)
        print("[+]  current user: " +  current_user.name)
        if current_user == active_user:
            return redirect(url_for('visualization'))  
    except:
        print("[+] Current user: out")
    args = request.args
    try:
        print("[+] Error login -> ", eval(args.get('error')))
        error_value = eval(args.get('error'))
    except:
        print("[+] Error login -> ", "Error value" , str(args.get('error')))
        if args.get('error')==None:
            error_value = False
        else: 
            error_value = True
    return render_template('login.html', show_error=error_value)



@app.route('/login-form', methods=['POST'])
def login_form():
    
    data = request.form
    username = data['username']
    password = data['password']
    connector = Deta(config['DETA_PROJECT_KEY'])
    db_users = connector.Base('users')
    user_data = db_users.fetch({"username": username}).items
    if len(user_data) > 0 :
        user_data = user_data[0]
    else:
        return redirect(url_for('login', error=True))
    token = generate_token(password, username)
    validated_token = (user_data['token'] == token)
    print("[+] Result query mongoDB -> ", user_data, " -- validation: ", validated_token)
    if validated_token:
        active_user.name = username
        active_user.password = token
        login_user(active_user, remember=True)
        return redirect(url_for('visualization'))
    else:
        return redirect(url_for('login', error=True))
    
@app.route('/logout', methods=['GET','POST'])
def logout():
    username = current_user.name
    logout_user()
    return "LOGOUT " + username

