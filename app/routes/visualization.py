from app import app, login_manager
from flask import redirect, url_for,  render_template
from flask_login import login_required
from app.dashboard.dashboard import app_dash

@app.route('/visualization/')
@login_required
def visualization():
    return app_dash.index()

@login_manager.unauthorized_handler     # In unauthorized_handler we have a callback URL 
def unauthorized_callback():            # In call back url we can specify where we want to 
       return redirect(url_for('login')) # redirect the user in my case it is login page!


