

import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px



# pip install pyorbital
from pyorbital.orbital import Orbital
satellite = Orbital('TERRA')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
        html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]


# # Multiple components can update everytime interval gets fired.
# @app.callback(Output('live-update-graph', 'figure'),
#               Input('interval-component', 'n_intervals'))
# def update_graph_live(n):
#     satellite = Orbital('TERRA')
#     data = {
#         'time': [],
#         'Latitude': [],
#         'Longitude': [],
#         'Altitude': []
#     }

#     # Collect some data
#     for i in range(180):
#         time = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
#         lon, lat, alt = satellite.get_lonlatalt(
#             time
#         )
#         data['Longitude'].append(lon)
#         data['Latitude'].append(lat)
#         data['Altitude'].append(alt)
#         data['time'].append(time)

#     # Create the graph with subplots
#     fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
#     fig['layout']['margin'] = {
#         'l': 30, 'r': 10, 'b': 30, 't': 10
#     }
#     fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

#     fig.append_trace({
#         'x': data['time'],
#         'y': data['Altitude'],
#         'name': 'Altitude',
#         'mode': 'lines+markers',
#         'type': 'scatter'
#     }, 1, 1)
#     fig.append_trace({
#         'x': data['Longitude'],
#         'y': data['Latitude'],
#         'text': data['time'],
#         'name': 'Longitude vs Latitude',
#         'mode': 'lines+markers',
#         'type': 'scatter'
#     }, 2, 1)

#     return fig



class Dapp:
    def __init__(self, game):
        self.app = app
        self.game = game

        self.app.callback(Output('live-update-graph', 'figure'),Input('interval-component', 'n_intervals'))(self.update_chips_live)

    def update_chips_live(self, n):
        chips = {}
        for player in self.game.players:
            chips[player.name] = player.chips_per_hand

        chips = pd.DataFrame(chips)
        chips['hands'] = range(len(chips))
        fig = px.line(chips, x='hands', y=[x for x in chips.columns if x != 'hands'])
        return fig

    def _run_server(self):
        self.app.run_server(debug=True)

if __name__ == '__main__':
    class test_person:
        def __init__(self, name, chips):
            self.name = name
            self.chips_per_hand = chips

    class test_game:
        def __init__(self):
            self.players = [
                test_person('hank', [1000,900,800,700,900,1200]),
                test_person('aaron', [1000,800,600,800,1000,1200]),
                test_person('brad', [1000,1200,1400,1600,1800,2000])
            ]
    
    t = test_game()
    a = Dapp(t)
    a._run_server()