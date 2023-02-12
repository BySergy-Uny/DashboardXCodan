from app import app
from flask import render_template


@app.route('/visualization')
def visualization():
    return "OK! - Visualization"

