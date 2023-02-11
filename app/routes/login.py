from app import app
from flask import render_template, request
from app.tools.database_connection import *

@app.route("/login")
def login():
    return render_template('login.html')


@app.route('/login-form', methods=['POST'])
def login_form():
    data = request.form
    username = data['username']
    password = data['password']
    db_mongo.set_database('users')
    db_mongo.set_collection('operadores')
    user_data = db_mongo.search_into_collection({"username": username})
    validated_token = (user_data['token'] == password)
    print("[+] Result query mongoDB -> ", user_data, " -- validation: ", validated_token)
    return render_template('login.html')

