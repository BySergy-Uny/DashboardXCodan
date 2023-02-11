from app import app
from flask import render_template, request


@app.route("/login")
def login():
    return render_template('login.html')


@app.route('/login-form', methods=['POST'])
def login_form():
    data = request.form
    return {
        'username'     : data['username'],
        'password' : data['password'],
    }

