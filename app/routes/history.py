from app import app, login_manager
from flask import render_template, redirect, url_for
from flask_login import login_required
import pandas as pd
from app.tools.detaApp import *

import plotly.express as px
import plotly.io as px_translate
import plotly.figure_factory as ff

@app.route("/visualization/history")
@login_required
def history():
    response = dataDrive.get("reg_nodes_measures.csv")
    df = pd.read_csv(response)
    df = df.query("entity_type == 'nodo1'")
    df['fecha'] = pd.to_datetime(df['date'])
    df = df.set_index('fecha')
    df = df.sort_index()
    graph = px_translate.to_html(px.line(df,title='Temperatura', y='temperatura', render_mode='svg'))
    table = px_translate.to_html(ff.create_table(df[['date', 'tvoc', 'eco2', 'humedad', 'temperatura']].tail()))
    return render_template('history.html', graph=graph, table=table)

@app.route("/visualization/history/prediction")
@login_required
def prediction():
    response = dataDrive.get("reg_nodes_measures.csv")
    df = pd.read_csv(response)
    df = df.query("entity_type == 'nodo1'")
    df['fecha'] = pd.to_datetime(df['date'])
    df = df.set_index('fecha')
    df = df.sort_index()
    graph = px_translate.to_html(px.line(df,title='Temperatura', y='temperatura', render_mode='svg'))
    table = px_translate.to_html(ff.create_table(df[['date', 'tvoc', 'eco2', 'humedad', 'temperatura']].tail()))
    return render_template('history.html', graph=graph, table=table)


@login_manager.unauthorized_handler     # In unauthorized_handler we have a callback URL 
def unauthorized_callback():            # In call back url we can specify where we want to 
       return redirect(url_for('login')) # redirect the user in my case it is login page!


