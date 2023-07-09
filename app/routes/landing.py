from app import app
from flask import render_template, redirect, url_for

@app.route("/")
def index():
    return redirect(url_for('home'));

@app.route("/home")
def home():
    return render_template('landing.html')