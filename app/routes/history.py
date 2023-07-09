from app import app, login_manager
from flask import render_template, redirect, url_for
from flask_login import login_required
import pandas as pd
from app.tools.detaApp import *

import plotly.graph_objs as go
import plotly.express as px
import plotly.io as px_translate
import plotly.figure_factory as ff
from skforecast.utils import load_forecaster

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
    forecaster = load_forecaster("app/assets/forecaster_temp.ml")
    response = dataDrive.get("reg_nodes_measures.csv")
    df = pd.read_csv(response)
    df = df.query("entity_type == 'nodo1'")
    df['fecha'] = pd.to_datetime(df['date'])
    df = df.set_index('fecha')
    df = df.sort_index()
    df = df["2021-08-30":"2021-10-10"]
    df = df.resample('5min').first()
    df.fillna(method="bfill", inplace=True)
    forecaster.fit(df.temperatura)
    predictions = forecaster.predict(steps=4000)
    fig = go.Figure()
    graph_pred = px.line(predictions, title='Predicción Temperatura', y='pred', render_mode='svg')
    graph_pred.update_traces(line_color='red')
    graph_temp = px.line(df, title='Predicción Temperatura', y='temperatura', render_mode='svg')
    graph_temp.update_traces(line_color='green')
    fig.add_trace(
        graph_pred.data[0]
    )

    fig.add_trace(
        graph_temp.data[0]
    )
    graph = px_translate.to_html(fig)
    table = px_translate.to_html(ff.create_table(pd.DataFrame(predictions).tail()))
    return render_template('prediction.html', graph=graph, table=table)


@login_manager.unauthorized_handler     # In unauthorized_handler we have a callback URL 
def unauthorized_callback():            # In call back url we can specify where we want to 
       return redirect(url_for('login')) # redirect the user in my case it is login page!


