
from dash import html, dcc, Input, Output, ctx

from app import app_dash
import plotly.graph_objects as go
from collections import deque
from  app.tests.test import *

get_update()
df = get_frame()
dfs = deque(df, maxlen=1)
color_graph = deque(["black"], maxlen=1)
measure_graph = deque(["temperatura"], maxlen=1)

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



def getGraphical(type, color):
    df = dfs[0].head(10)
    datax = df['timestamp']
    datay = df[type]
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
    df = dfs[0].head(2)
    return [
        html.Div(id="measure1", children=[
            getGraph(
                go.Figure(
                    go.Indicator(
                        title = "humedad",
                        mode = "number+delta",
                        value = list(df['humedad'])[0],
                        delta = {'reference': list(df['humedad'])[1]}
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
                        value = list(df['eco2'])[0],
                        delta = {'reference': list(df['eco2'])[1]}
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
                        value = list(df['tvoc'])[0],
                        delta = {'reference': list(df['tvoc'])[1]}
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
                        value = list(df['temperatura'])[0],
                        delta = {'reference': list(df['temperatura'])[1]}
                        )
                )
            )
        ],
        style={'width':'100%', 'height':'100%'}
        ),
    ]


@app_dash.callback(Output('live-graph', 'children'),
    Input('graph-update', 'n_intervals'))
def update_graphs(gr):
    get_update()
    dfs.append(get_frame())
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
        print("[+] Measure 1: ", button)
        color_graph.append("red")
        measure_graph.append("humedad")
    elif(button=="measure2" and btn2 != None):
        print("[+] Measure 2", button)
        color_graph.append("blue")
        measure_graph.append("eco2")
    elif(button=="measure3" and btn3 != None):
        print("[+] Measure 3", button)
        color_graph.append("green")
        measure_graph.append("tvoc")
    elif(button=="measure4" and btn4 != None):
        print("[+] Measure 4", button)
        color_graph.append("yellow")
        measure_graph.append("temperatura") 