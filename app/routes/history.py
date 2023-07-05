from app import app
from flask import render_template, redirect, url_for

import pandas as pd
from app.tools.detaApp import *

import plotly.express as px
import plotly.io as px_translate
import plotly.figure_factory as ff

@app.route("/history")
def history():
    response = dataDrive.get("reg_nodes_measures.csv")
    df = pd.read_csv(response)
    df = df.query("entity_type == 'nodo1'")
    df['fecha'] = pd.to_datetime(df['date'])
    df = df.set_index('fecha')
    df = df.sort_index()
    graph = px_translate.to_html(px.line(df, y='temperatura', render_mode='svg'))
    table = px_translate.to_html(ff.create_table(df[['date', 'tvoc', 'eco2', 'humedad', 'temperatura']].tail()))
    return render_template('history.html', graph=graph, table=table)