from app import app
from flask import render_template


@app.route('/visualization')
def visualization():
    return render_template('visualization.html')

