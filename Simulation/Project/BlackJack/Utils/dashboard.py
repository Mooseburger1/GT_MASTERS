
import webbrowser
import time
import numpy as np


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from plotly import tools
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output



port = 8050
def open_browser():
    webbrowser.open_new('http://127.0.0.1:{}/'.format(port))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'BlackJack Sim'

app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Winnings/Losses Per Hand', value='tab-1'),
        dcc.Tab(label='Chip Total Per Hand', value='tab-2'),
        dcc.Tab(label='Card Totals Distribution', value='tab-3'),
        dcc.Tab(label='Wins/Losses', value='tab-4'),
        dcc.Tab(label='Max Winnings Per Trial', value='tab-5'),
    ]),
    html.Div(id='tabs-example-content')
])










class Dapp:
    def __init__(self, table, resets):
        self.table = table
        self.resets = resets
        self.app = app
        self.app.callback(Output('tabs-example-content', 'children'), Input('tabs-example', 'value'))(self.render_content)
    
    def render_content(self,tab):
        if tab == 'tab-1':
            return html.Div([
                dcc.Graph(figure=self.create_bargraph())
            ])
        elif tab == 'tab-2':
            return html.Div([
                dcc.Graph(figure=self.create_chips_totals())
            ])
        elif tab == 'tab-3':
            return html.Div([
                dcc.Graph(figure=self.create_sum_dist())
            ])
        elif tab == 'tab-4':
            return html.Div([
                dcc.Graph(figure=self.create_wins_losses())
            ])
        elif tab == 'tab-5':
            return html.Div([
                dcc.Graph(figure=self.create_maxes())
            ])

    def launch_dashboard(self):

        self.app.run_server(debug=False, port=port)

    def create_maxes(self):
        min_ = self.table.table_max
        starting_chips = self.table.players[0].starting_chips
        maxes = np.array(self.table.players[0].maxes) - starting_chips
        trace = go.Histogram(
            x=maxes,
            opacity=0.75,
            name='Max Chips Per Trial Distribution',
            marker=dict(color=r'rgb(255,255,128)', line=dict(color='rgb(0,0,0)',width=1.5)),
            text=r'(Total, Frequency)',
            nbinsx=15
        )

        trace1 = go.Box(
            x=sorted(maxes),
            marker=dict(color=r'rgb(12,12,140)'),
            name='Max Chips Per Trial Box'
        )

        layout = go.Layout(barmode='overlay',
                   title='Maximum Chips Total Per Trial Distribution',
                   xaxis=dict(title='Max Chips'),
                   yaxis=dict( title='Frequency'),
                   
        )

        fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=False, shared_yaxes=False)
        fig.append_trace(trace, 1,1)
        #fig.update_xaxes(range=(-min_-100, max(maxes)+100))
        fig.append_trace(trace1,2,1)
        # fig = go.Figure(data=[trace,trace1], layout=layout)
        
        return fig


    def create_bargraph(self):
        player = self.table.players[0]
        winnings = np.array(player.winnings_per_hand)

        color = np.array(['rgb(255,255,255)'] * len(winnings))
        color[winnings > 0] = 'rgb(0,190,0)'
        color[winnings < 0] = 'rgb(255,0,0)'

        text = np.array(['(Hand, Won)'] * len(winnings))
        text[winnings < 0] = '(Hand, Lost)'

        trace = go.Bar(
            x = tuple(range(len(player.winnings_per_hand))),
            y = player.winnings_per_hand,
            name = player.name,
            marker = dict(color=color.tolist()),
            text = text.tolist()
        )
        layout = go.Layout(barmode='overlay',
                    title='Winnings/Losses Per Hand',
                    xaxis=dict(title='Hand #'),
                    yaxis=dict( title='Winnings (green) / Losses (red)'),
        )

        fig = go.Figure(data=[trace], layout=layout)
        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                )
            )
        )
        
        
        return fig

    def create_trace(self, pos, player):
        name = player.name
        chips_per_hand = player.chips_per_hand

        if pos == 0:
            trace = go.Scatter(
                x = tuple( range( len(chips_per_hand) ) ),
                y = chips_per_hand,
                mode = 'lines',
                name = name
            )
        else:
            trace = go.Scatter(
                x = tuple( range( len(chips_per_hand) ) ),
                y = chips_per_hand,
                mode = 'lines',
                name = name,
                line = dict(dash='dot')
            )

        return trace

    def create_reset_trace(self, idx):
        max_ = np.max(self.table.players[0].chips_per_hand)

        x = [idx] * 100
        y = np.linspace(0, max_,100)

        trace = go.Scatter(
            x = x,
            y = y,
            mode='lines',
            line=dict(color='black', width=3),
            showlegend=False
        )

        return trace

    def create_chips_totals(self):

        data = [self.create_trace( pos, player ) for pos, player in enumerate(self.table.players)]
        length = len(self.table.players[0].chips_per_hand)

        layout = go.Layout(
                    title='Chip Total Per Hand',
                    xaxis=dict(title='Hand #'),
                    yaxis=dict( title='Chips')
                    
        )

        fig = go.Figure(data=data, layout=layout)

        fig = self.plot_resets_and_chips(fig)
        fig.update_xaxes(range=(-5, length + 5))
        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                )
            )
        )
        return fig

    def create_starting_chips_trace(self):
        length = len( self.table.players[0].chips_per_hand )
        x = tuple( range( length ))
        y = [self.table.players[0].starting_chips] * length

        trace = go.Scatter(
            x = x,
            y = y,
            mode='lines',
            line=dict(color='black', dash='dash'),
            showlegend=False
        )

        return trace


    def plot_resets_and_chips(self, fig):

        for pos,x in enumerate(self.resets):
            if pos != 0:
                x = x + np.sum( self.resets[:pos] )
            fig.add_trace( self.create_reset_trace(x) )

        fig.add_trace( self.create_starting_chips_trace() )

        return fig

    def create_sum_dist(self):
        tots = self.table.players[0].totals_per_hand
        tots = [x for x in tots if x != 0]
        trace = go.Histogram(
            x=tots,
            opacity=0.75,
            name='Tot. Dist.',
            marker=dict(color=r'rgba(255,255,128,0.7)', line=dict(color='rgb(0,0,0)',width=1.5)),
            text=r'(Total, Frequency)'
        )

        layout = go.Layout(barmode='overlay',
                   title='Card Totals Distribution',
                   xaxis=dict(title='Card Totals'),
                   yaxis=dict( title='Frequency'),
        )

        fig = go.Figure(data=[trace], layout=layout)
        fig.update_xaxes(range=(min(tots)-1, max(tots)+1))
        return fig

    def create_wins_losses(self):
        player = self.table.players[0]
        wins = player.wins
        loss = player.losses

        color = [r'rgb(0,0,0)', r'rgb(255,0,0)']
        

        text = ['Wins', 'Losses']
        trace = go.Bar(
            x = ['Wins', 'Losses'],
            y = [wins, loss],
            marker = dict(color=color),
            text = text,
            texttemplate = '%{y}',
            textposition='inside'
        )
        layout = go.Layout(barmode='overlay',
                    title='Winnings/Losses',
                    yaxis=dict( title='Count'),
        )

        fig = go.Figure(data=[trace], layout=layout)
        
        return fig



