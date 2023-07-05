from app import app
from flask import render_template, redirect, url_for

@app.route("/history")
def history():
    return render_template('history.html')