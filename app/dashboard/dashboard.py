
from dash import html, dcc, Input, Output, ctx

from app import app_dash
import plotly.express as px
import plotly.graph_objects as go
from collections import deque
import random

datax = deque([0, 1, 2, 3, 4, 5, 6, 7], maxlen=8)
datay = deque([1, 5, 5, 6, 3, 4, 5, 6], maxlen=8)

color_graph = deque(["black"], maxlen=1)


def getGraph(fig):
    graph = dcc.Graph(figure=fig, 
            animate=True,
              config={
        'displayModeBar': False
    },
    responsive=True,
        style={'display': 'inline-block', 'width':'100%', 'height':'100%'})
    return graph



app_dash.layout = html.Div(children=[
    dcc.Interval(
      id='graph-update',
      interval=5*1000
    ),
    html.Div(id="live-graph"),
    html.Div(id="out")
], style={'justify-content':'center'})



def getGraphical(color):

    fig=go.Figure(
        go.Scatter(x=list(datax), y=list(datay), mode= 'lines+markers', marker={'color':color})
    )
    fig.update_yaxes(range = [min(datay),max(datay)])
    fig.update_xaxes(range = [min(datax),max(datax)])

    graphical =  [
        html.Div(id="main", children=[
            html.Img(src='../../img/logotype-ligth-dashboardxcodan-withoutbg-fit.png',
                width="250vh"),
            html.Br(),
            html.Div(children=getGraph(fig))
        ]),
        html.Div(children=getMeasures(),
        style = {'display':'grid', 'grid-auto-rows':'22rem', 'grid-template-columns':'repeat(4, 25%)'}
        )
    ]
    return graphical


def getMeasures():

    return [
        html.Div(id="measure1", children=[
            getGraph(
                go.Figure(
                    go.Indicator(
                        title = "humedad",
                        mode = "number+delta",
                        value = list(datay)[-1],
                        delta = {'reference': list(datay)[-2]}
                        )
                )
            )
        ],
        style={'width':'100%', 'height':'100%'}
        ),
        html.Div(id="measure2", children=[
            getGraph(
                go.Figure(
                    go.Indicator(
                        title = "co2",
                        mode = "number+delta",
                        value = list(datay)[-1],
                        delta = {'reference': list(datay)[-2]}
                        )
                )
            )
        ],
        style={'width':'100%', 'height':'100%'}
        ),
        html.Div(id="measure3", children=[
            getGraph(
                go.Figure(
                    go.Indicator(
                        title = "tvoc",
                        mode = "number+delta",
                        value = list(datay)[-1],
                        delta = {'reference': list(datay)[-2]}
                        )
                )
            )
        ],
        style={'width':'100%', 'height':'100%'}
        ),
        html.Div(id="measure4", children=[
            getGraph(
                go.Figure(
                    go.Indicator(
                        title = "temperatura",
                        mode = "number+delta",
                        value = list(datay)[-1],
                        delta = {'reference': list(datay)[-2]}
                        )
                )
            )
        ],
        style={'width':'100%', 'height':'100%'}
        ),
    ]

actualizar = True

@app_dash.callback(Output('live-graph', 'children'),
    Input('graph-update', 'n_intervals'))
def update_graphs(gr):
    if actualizar and (gr!=None and gr>1):
        datax.append(datax[-1]+1)
        datay.append(random.randint(3, 9))
    return getGraphical(color_graph[-1])

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
        print("[+] Measure 1: ", button)
        color_graph.append("red")
    elif(button=="measure2" and btn2 != None):
        print("[+] Measure 2", button)
        color_graph.append("blue")
    elif(button=="measure3" and btn3 != None):
        print("[+] Measure 3", button)
        color_graph.append("green")
    elif(button=="measure4" and btn4 != None):
        print("[+] Measure 4", button)
        color_graph.append("yellow")