
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

app = dash.Dash(__name__, )
app.title = 'BlackJack Sim'

app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Player Strategies', value='tab-1'),
        dcc.Tab(label='Chip Total Per Hand', value='tab-2'),
        dcc.Tab(label='Card Totals Distribution', value='tab-3'),
        dcc.Tab(label='Wins/Losses', value='tab-4'),
        dcc.Tab(label='Maximum Winnings Per Trial', value='tab-5'),
        dcc.Tab(label='Winnings/Losses Per Hand', value='tab-6'),
    ]),
    html.Div(id='tabs-example-content', style={'height': '90vh'})
], style={'height': '100vh'})










class Dapp:
    def __init__(self, table, resets):
        self.table = table
        self.resets = resets
        self.app = app
        self.app.callback(Output('tabs-example-content', 'children'), Input('tabs-example', 'value'))(self.render_content)
    
    def div_factory(self, person, style, style2):
        name = person.name
        bet = person.betting_strategy
        play = person.strategy

        return html.Div([html.H2(name),
                         html.P('Betting: {}'.format(bet), style=style2),
                         html.P('Playing: {}'.format(play), style=style2)], style=style)

    def render_content(self,tab):
        if tab == 'tab-1':
            style={'border-style': 'solid',
                       'padding':14,
                       'border-width':3,
                       'color':'black',
                       'display':'inline-block',
                       'height':130,
                       'list-style-type':'none',
                       'margin':r'10px 40px 10px 20px',
                       'position':'relative',
                       'text-align':'center',
                       'width':270,
                       'border-radius':5,
                       'box-shadow': r'10px 10px 5px #888888',
                       'vertical-align':'top',
                       'background-image':r'-webkit-gradient(linear, left top, left bottom, color-stop(0, #CCF11B), color-stop(1, #3874FF))',
                       'background-image':r'linear-gradient(-28deg, #CCF11B 0%, #3874FF 100%)'}

            style2 = {'color':'black',
                      
                      'font-style':'italic'}

            content = [html.Legend(html.B('PLAYER STRATEGIES'))]
            for player in self.table.players:
                content.append( self.div_factory(player, style, style2) )

            return html.Div([
                html.Fieldset(
                    content
                ),
                html.Div([html.B(html.Em(html.P('PLAYER STRATEGIES shows the betting and playing strategies for every player sitting at the table. Your player will always be the first tile on the tab.')))])
            ])
        elif tab == 'tab-2':
            return html.Div([
                dcc.Graph(figure=self.create_chips_totals()),
                html.Div([html.Hr(), html.B(html.Em(html.P('CHIP TOTAL PER HAND shows the chip count for each player after each hand. The trials are seperated by the black vertical lines. The horizontal dashed line represents the starting chip amount for each player. In instances that curves are above the dashed line, this means the player has positive winnings. Anytime it is below, this signifies a player has negative winnings (losing money). You can slide the ruler at the bottom to shift the graph to focus on specific trials. Double click on the slider to move as is, or move the individual thresholds. You can hide plotted curves by clicking a players name in the legend.')))])
            ])
        elif tab == 'tab-3':
            return html.Div([
                dcc.Graph(figure=self.create_sum_dist()),
                html.Div([html.Hr(), html.B(html.Em(html.P('CARD TOTALS DISTRIBUTION shows the frequencies of card totals seen throughout all hands of all trials. This allows a user analyze how often they are busting. Conversely, it allows a user to analyze how close they are getting to 21 with the current playing strategy, as well as how often they do it.')))])

            ])
        elif tab == 'tab-4':
            return html.Div([
                dcc.Graph(figure=self.create_wins_losses()),
                html.Div([html.Hr(), html.B(html.Em(html.P('WINS/LOSSES shows the distributions of the amount of chips won when their player does win vs the distribution of the amount of chips lost when their player loses. It also shows for the given strategy, how many times they lost and won for all hands under all trials')))])

            ])
        elif tab == 'tab-5':
            return html.Div([
                dcc.Graph(figure=self.create_maxes()),
                html.Div([html.Hr(), html.B(html.Em(html.P('MAXIMUM WINNINGS PER TRIAL shows the distribution of the maximum amount of winnings achieved at any time during a trial, for all trials. This gives a user an idea of the overall maximum amount of winnings a person could walk away from the table with for the given betting and playing strategy.')))])

            ])
        elif tab == 'tab-6':
            return html.Div([
                dcc.Graph(figure=self.create_bargraph()),
                html.Div([html.Hr(), html.B(html.Em(html.P('WINNINGS/LOSSES PER HAND shows the amount won or lost for every single hand played across all trials. You can slide the ruler at the bottom to shift the graph to focus on specific trials. Double click on the slider to move as is, or move the individual thresholds.')))])

            ])

    def launch_dashboard(self):

        self.app.run_server(debug=True, port=port)

    def create_maxes(self):
        min_ = self.table.table_max
        starting_chips = self.table.players[0].starting_chips
        maxes = np.array(self.table.players[0].maxes) - starting_chips
        trace = go.Histogram(
            x=maxes,
            opacity=0.75,
            showlegend=False,
            marker=dict(color=r'rgb(255,255,128)', line=dict(color='rgb(0,0,0)',width=1.5)),
            text=r'(Total, Frequency)',
            nbinsx=15
        )

        trace1 = go.Box(
            x=sorted(maxes),
            marker=dict(color=r'rgb(12,12,140)'),
            showlegend=False,
            name='Max Chips'
            
        )

        

        fig = plotly.subplots.make_subplots(rows=2, cols=1, shared_xaxes=True, shared_yaxes=False, horizontal_spacing=1, vertical_spacing=0)
        fig.append_trace(trace, 1,1)
        fig.append_trace(trace1,2,1)

        fig.update_layout(height=650, title='Maximum Winnings Per Trial', yaxis=dict(title='Frequency'))
        
        
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
                    xaxis=dict(title='Hand # (Slide Me)'),
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
        fig.update_layout(height=650)
        initial_range = [0, 200]
        fig['layout']['xaxis'].update(range=initial_range)
        
        
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
                    xaxis=dict(title='Hand # (Slide Me)'),
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
        fig.update_layout(height=650)
        initial_range = [0, 200]
        fig['layout']['xaxis'].update(range=initial_range)
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
        fig.update_layout(height=650)
        return fig

    def create_wins_losses(self):
        player = self.table.players[0]
        wins = player.wins
        loss = player.losses
        winnings = np.array(player.winnings_per_hand)
        positive = list(winnings[winnings > 0])
        negative = list(winnings[winnings < 0])

        perc = round(len(positive) / ( len(positive) + len(negative) ), 4)

        win_med = np.median(positive)
        win_std = round(np.std(positive),2)
        loss_med = np.median(negative)
        loss_std = round(np.std(negative),2)

        color = [r'rgb(0,0,0)', r'rgb(255,0,0)']
        

        text = ['Wins', 'Losses']
        trace = go.Bar(
            x = ['Won', 'Lost'],
            y = [wins, loss],
            marker = dict(color=color),
            text = text,
            texttemplate = 'You %{x}\n%{y} Times',
            textposition='inside',
            name = 'Number of Wins/Losses',
            showlegend=False
        )

        trace1 = go.Histogram(
            x=positive,
            opacity=0.75,
            name='Winnings Distribution',
            marker=dict(color=r'rgb(0,0,0)', line=dict(color='rgb(169,169,169)',width=1.5)),
            text=r'(Total, Frequency)',
            showlegend=False
        )

        trace2 =  go.Histogram(
            x=negative,
            name='Losses Distribution',
            marker=dict(color=r'rgb(255,0,0)', line=dict(color='rgb(0,0,0)',width=1.5)),
            text=r'(Total, Frequency)',
            showlegend=False
        )
        layout = go.Layout(barmode='overlay',
                    title='Winnings/Losses',
                    yaxis=dict( title='Count'),
        )

      

        fig = plotly.subplots.make_subplots(
                            rows=2, cols=2,
                            specs=[[{}, {}],
                                [{"colspan": 2}, None]],
                            subplot_titles=("Winnings (Median: {} | Std: {})".format(win_med, win_std),"Losses (Median: {} | Std: {})".format(loss_med, loss_std), "Total Win/Loss | {}%".format(perc*100)))
        fig.add_trace(trace1, row=1, col=1)
        fig.add_trace(trace2, row=1, col=2)
        fig.add_trace(trace, row=2, col=1)
        fig.update_layout(height=650)
        
        return fig



