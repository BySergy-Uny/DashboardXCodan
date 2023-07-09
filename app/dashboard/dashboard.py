
from dash import html, dcc, Input, Output, ctx

from app import app_dash
import plotly.graph_objects as go
from collections import deque
from  app.tests.test import *

from app.dashboard.alert import *


node_test = NodeMeasureTest()
node_test.get_update()
df = node_test.get_frame()
dfs = deque(df, maxlen=1)
color_graph = deque(["black"], maxlen=1)
measure_graph = deque(["temperatura"], maxlen=1)
alert = deque([False], maxlen=1)


    


def getGraph(fig, responsive):
    graph = dcc.Graph(figure=fig, 
            animate=True,
              config={
        'displayModeBar': False
    },
    responsive=responsive,
        style={'display': 'inline-block', 'width':'100%', 'height':'100%', 'padding':'0'})
    return graph



app_dash.layout = html.Div(children=[
    dcc.Interval(
      id='graph-update',
      interval=2*1000
    ),
    html.Div(id="live-graph"),
    html.Div(id="out")
], style={'justify-content':'center'})



def getGraphical(type, color):
    df = dfs[0].head(10)
    datax = df['timestamp']
    datay = df[type]
    fig=go.Figure(
        go.Scatter(x=list(datax), y=list(datay), mode= 'lines+markers', marker={'color':color})
    )
    fig.update_yaxes(range = [min(datay),max(datay)])
    fig.update_xaxes(range = [min(datax),max(datax)])

    css_button  = { 'background-color': 'white',
    'color': 'black',
    'border': '2px solid #555555',
    'padding': '16px 32px',
    'text-align': 'center',
    'text-decoration': 'none',    
    'position': 'fixed',
    'top': '1rem',
    'right': '3rem',
    'font-size': '16px',
    'margin': '4px 2px',
    'transition-duration': '0.4s',
    'cursor': 'pointer',
    'font-family': '"Open Sans", verdana, arial, sans-serif'}

    css_button_hist = css_button.copy()
    css_button_hist['right'] = '10rem'

    graphical =  [
        html.Div(id="main", children=[
            html.Img(src='../../img/logotype-ligth-dashboardxcodan-withoutbg-fit.png',
                width="250vh"),
            html.A("Historico", id="history", style = css_button_hist,
                        href='/visualization/history'),
            html.A("Salir", id="salir", style = css_button,
                        href='/logout'),
            html.Br(),
            html.Div(children = [
            html.H1(children=str(type).capitalize(),
                    style={
                        'display': 'inline-block', 
                        'width':'100%', 
                        'margin': '0', 
                        'margin-top': '2rem',
                        'text-align': 'center',
                        'font-family': '"Open Sans", verdana, arial, sans-serif'}),
            getGraph(fig, responsive=True)])
        ]),
        html.Div(children=getMeasures(),
                 
        style = {'display':'grid', 'grid-auto-rows':'22rem', 'grid-template-columns':'repeat(4, 25vw)'}
        ),
        html.Div([
             dcc.ConfirmDialog(
                id='confirm-danger',
                message='Danger danger! Are you sure you want to continue?',
            )   
        ])
    ] 
    
    return graphical 


def getMeasures():
    df = dfs[0].head(2)
    check, m1c, m2c, m3c, m4c = check_values(list(df['temperatura'])[0], alert[-1])
    alert.append(check)
    measure1_color = m1c
    measure2_color = m2c
    measure3_color = m3c
    measure4_color = m4c
    return [
        html.Div(id="measure1", children=[
            getGraph(
                go.Figure(
                    go.Indicator(
                        title = "Humedad",
                        mode = "number+delta",
                        value = list(df['humedad'])[0],
                        delta = {'reference': list(df['humedad'])[1]},
                        number={'font_color':measure1_color, 'font_size':40}
                        )
                ), responsive= True
            )
        ],
        style={'width':'100%', 'height':'100%'}
        ),
        html.Div(id="measure2", children=[
            getGraph(
                go.Figure(
                    go.Indicator(
                        title = "Eco2",
                        mode = "number+delta",
                        value = list(df['eco2'])[0],
                        delta = {'reference': list(df['eco2'])[1]},
                        number={'font_color':measure2_color, 'font_size':40}
                        )
                ), responsive= True
            )
        ],
        style={'width':'100%', 'height':'100%'}
        ),
        html.Div(id="measure3", children=[
            getGraph(
                go.Figure(
                    go.Indicator(
                        title = "Tvoc",
                        mode = "number+delta",
                        value = list(df['tvoc'])[0],
                        delta = {'reference': list(df['tvoc'])[1]},
                        number={'font_color':measure3_color, 'font_size':40}
                        )
                ), responsive= True
            )
        ],
        style={'width':'100%', 'height':'100%'}
        ),
        html.Div(id="measure4", children=[
            getGraph(
                go.Figure(
                    go.Indicator(
                        title = "Temperatura",
                        mode = "number+delta",
                        value = list(df['temperatura'])[0],
                        delta = {'reference': list(df['temperatura'])[1]},
                        number={'font_color':measure4_color, 'font_size':40}
                        )
                ), responsive= True
            )
        ],
        style={'width':'100%', 'height':'100%'}
        ),
    ]+ [getAudio(alert[-1])]


@app_dash.callback(Output('confirm-danger', 'displayed'),
              Input('graph-update', 'n_intervals'))
def display_confirm(value):
    # check = check_values(list(df['temperatura'])[1], alert[-1])
    if False:
        return True
    return False

@app_dash.callback(Output('live-graph', 'children'),
    Input('graph-update', 'n_intervals'))
def update_graphs(gr):
    dfs.append(node_test.get_frame())
    node_test.get_update()
    return getGraphical(measure_graph[-1], color_graph[-1]) 

@app_dash.callback(
    Output('out', 'children'),
    Input('measure1', 'n_clicks'),
    Input('measure2', 'n_clicks'),
    Input('measure3', 'n_clicks'),
    Input('measure4', 'n_clicks')
)
def displayClick(btn1, btn2, btn3, btn4):
    button = ctx.triggered_id
    if(button=="measure1" and btn1 != None):
        alert.append(True)
        color_graph.append("red")
        measure_graph.append("humedad")
    elif(button=="measure2" and btn2 != None):
        alert.append(True)
        color_graph.append("blue")
        measure_graph.append("eco2")
    elif(button=="measure3" and btn3 != None):
        alert.append(True)
        color_graph.append("green")
        measure_graph.append("tvoc")
    elif(button=="measure4" and btn4 != None):
        alert.append(True)
        color_graph.append("black")
        measure_graph.append("temperatura") 
    