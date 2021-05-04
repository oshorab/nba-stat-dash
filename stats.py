import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# ---------- Import and clean data (importing csv into pandas)
df = pd.read_csv("data/kobe.csv")
df2 = pd.read_csv("data/kobe-fgp-by-dist.csv")

# ------------------------------------------------------------------------------
# App layout
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

options = [
    {"label": "Kobe Bryant", "value": "Kobe Bryant"}
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        html.H1("NBA Stat Dashboard",
                style={'text-align': 'center'}),

        html.Label(["Compare", dcc.Dropdown(
            id='slct-1st-player',
            options=options,
            value='Kobe Bryant',
            style={'width': '40%'})]),
        html.Label(["To", dcc.Dropdown(
            id='slct-2nd-player',
            options=options,
            style={'width': '40%'})]
        ),

        # dcc.Dropdown(id="slct_player",
        #             ,
        #              multi=False,
        #              value='Kobe Bryant',
        #              style={'width': "40%"}
        #              ),

        html.Div(id='output_container', children=[]),
        html.Br(),

        dcc.Graph(id='ppg-per-szn', figure={}),
        html.Br(),

        dcc.Graph(id='fgp-by-dist')

    ])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='ppg-per-szn', component_property='figure'),
     Output(component_id='fgp-by-dist', component_property='figure')],
    [Input(component_id='slct-1st-player', component_property='value'),
     Input(component_id='slct-2nd-player', component_property='value')]
)
def update_graph(option1, option2):
    print(option1)
    print(type(option1))

    container = "The player chosen by user was: {}".format(option1)

    dff = df.copy()
    dff2 = df2.copy()

    # Plotly Express
    fig = px.line(dff, x='Season', y='PPG')
    fig2 = px.line(dff2, x='Season', y='FG%')

    return container, fig, fig2


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
