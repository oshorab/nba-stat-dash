import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# ---------- Import and clean data (importing csv into pandas)
df_kobe = pd.read_csv("data/PPG/kobe.csv")
df_lebron = pd.read_csv("data/PPG/lebron.csv")
df_shaq = pd.read_csv("data/PPG/shaq.csv")

df2 = pd.read_csv("data/kobe-fgp-by-dist.csv")

# ------------------------------------------------------------------------------
# App layout
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# todo: have this list generated and not manually written
# reqs me to know what players we have data for. Possible if we have a databse,
# otherwise names are found from filenames
options = [
    {"label": "Kobe Bryant", "value": "Kobe Bryant"},
    {"label": "Lebron James", "value": "Lebron James"},
    {"label": "Shaquille O'neil", "value": "Shaquille O'neil"}
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        html.H1("NBA Stat Dashboard",
                style={'text-align': 'center'}),

        html.Label(["Compare", dcc.Dropdown(
            id='slct-1st-player',
            options=options,
            style={'width': '40%'})]),
        html.Label(["To", dcc.Dropdown(
            id='slct-2nd-player',
            options=options,
            style={'width': '40%'})]
        ),

        html.Div(id='output_container', children=[]),
        html.Br(),

        dcc.Graph(id='ppg-per-szn', figure={}),
        # html.Br(),

        dcc.Graph(id='fgp-by-dist')

    ])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='ppg-per-szn', component_property='figure'),
     Output(component_id='fgp-by-dist', component_property='figure')],
    [Input(component_id='slct-1st-player', component_property='value'),
     Input(component_id='slct-2nd-player', component_property='value')]
)
def update_graph(option1, option2):
    print(option1)
    print(option2)

    dff_kobe = df_kobe.copy()
    dff_lebron = df_lebron.copy()
    dff_shaq = df_shaq.copy()
    dff2 = df2.copy()

    # PPG vs Season Line Graph
    fig = go.Figure()
    # Player 1 trace

    fig.add_trace(
        go.Scatter(
            x=dff_kobe['Season'],
            y=dff_kobe['PPG'],
            mode='lines',
            name=option1
        ))
    # Player 2 trace
    fig.add_trace(
        go.Scatter(
            x=dff_lebron['Season'],
            y=dff_lebron['PPG'],
            mode='lines',
            name=option2
        ))
    fig.add_trace(
        go.Scatter(
            x=dff_shaq['Season'],
            y=dff_shaq['PPG'],
            mode='lines',
            name=option2
        ))
    fig.update_layout(xaxis_title='Season',
                      yaxis_title='PPG')

    #
    fig2 = px.line(dff2, x='Season', y='FG%')

    return fig, fig2


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
