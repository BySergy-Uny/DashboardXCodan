from app import app
from flask import render_template, request, redirect, url_for
from app.tools.database_connection import db_mongo
from app.tools.token import generate_token

@app.route("/login", methods=['GET'])
def login():
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
    db_mongo.set_database('users')
    db_mongo.set_collection('operadores')
    user_data = db_mongo.search_into_collection({"username": username})
    token = generate_token(password, username)
    try:
        validated_token = (user_data['token'] == token)
        print("[+] Result query mongoDB -> ", user_data, " -- validation: ", validated_token)
        if validated_token:
            return "Ok - Logueado"
        else:
            return redirect(url_for('login', error=True))
    except:
        return redirect(url_for('login', error=True))
    

