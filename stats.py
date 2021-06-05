import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# ---------- Import and clean data (importing csv into pandas)
# import ppg dataframes
df_ppg_kobe = pd.read_csv("data/PPG/kobe.csv")
df_ppg_lebron = pd.read_csv("data/PPG/lebron.csv")
df_ppg_shaq = pd.read_csv("data/PPG/shaq.csv")
ppg_frames = [df_ppg_kobe, df_ppg_lebron, df_ppg_shaq]
ppg_result = pd.concat(
    ppg_frames, keys=['Kobe Bryant', 'Lebron James', 'Shaquille Oneil']
)

# import fgp (Field Goal %) dataframes
df_fgp_kobe = pd.read_csv("data/FGP/kobe_shooting.csv")
df_fgp_lebron = pd.read_csv("data/FGP/lebron_shooting.csv")
df_fgp_shaq = pd.read_csv("data/FGP/shaq_shooting.csv")
fgp_frames = [df_fgp_kobe, df_fgp_lebron, df_fgp_shaq]
fgp_result = pd.concat(
    fgp_frames, keys=['Kobe Bryant', 'Lebron James', 'Shaquille Oneil']
)

# import salary dataframes
df_sal_kobe = pd.read_csv("data/Salary/kobe_salary.csv")
# df_fgp_lebron = pd.read_csv("data/FGP/lebron_shooting.csv")
df_sal_shaq = pd.read_csv("data/Salary/shaq_salary.csv")
df_sal_lebron = pd.read_csv("data/Salary/lebron_salary.csv")
sal_frames = [df_sal_kobe, df_sal_shaq, df_sal_lebron]
sal_result = pd.concat(
    sal_frames, keys=['Kobe Bryant', 'Shaquille Oneil', 'Lebron James']
)

# import Adjusted Shooting dataframes
df_adjShoot_lebron = pd.read_excel('data/AdjShoot/lebron_AdjShoot.xls')
df_adjShoot_kobe = pd.read_excel('data/AdjShoot/kobe_AdjShoot.xls')
df_adjShoot_lebron_Player = df_adjShoot_lebron[[
    "Season", "Age", "FG", "2P", "3P", "eFG", "FT", "TS"]]
df_adjShoot_lebron_League = df_adjShoot_lebron[[
    "Season", "Age", "FG.1", "2P.1", "3P.1", "eFG.1", "FT.1", "TS.1"]]
df_adjShoot_kobe_Player = df_adjShoot_kobe[[
    "Season", "Age", "FG", "2P", "3P", "eFG", "FT", "TS"]]

# import career % of FGA
df_PercFGA_kobe = pd.read_csv('data/Shooting/kobe_PercentFGA.csv')
df_PercFGA_Shaq = pd.read_csv('data/Shooting/shaq_PercentFGA.csv')
df_PercFGA_Lebron = pd.read_csv('data/Shooting/lebron_PercentFGA.csv')
PercFGA_frames = [df_PercFGA_kobe, df_PercFGA_Shaq, df_PercFGA_Lebron]
percFGA_result = pd.concat(
    PercFGA_frames, keys=['Kobe Bryant', 'Shaquille Oneil', 'Lebron James']
)

# import FG % by dist
df_FGPerc_kobe = pd.read_csv('data/Shooting/kobe_FGPerc.csv')
df_FGPerc_Shaq = pd.read_csv('data/Shooting/shaq_FGPerc.csv')
df_FGPerc_Lebron = pd.read_csv('data/Shooting/lebron_FGPerc.csv')
FGPerc_frames = [df_FGPerc_kobe, df_FGPerc_Shaq, df_FGPerc_Lebron]
FGPerc_result = pd.concat(
    FGPerc_frames, keys=['Kobe Bryant', 'Shaquille Oneil', 'Lebron James']
)

# ------------------------------------------------------------------------------
# App layout
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# todo: have this list generated and not manually written
# reqs me to know what players we have data for. Possible if we have a databse,
# otherwise names are found from filenames
options = [
    {"label": "Kobe Bryant", "value": "Kobe Bryant"},
    {"label": "Lebron James", "value": "Lebron James"},
    {"label": "Shaquille O'neil", "value": "Shaquille Oneil"}
]

seasons = [
    {"label": "2003-04", "value": "2003-04"},
    {"label": "2004-05", "value": "2004-05"},
    {"label": "2005-06", "value": "2005-06"},
    {"label": "2006-07", "value": "2006-07"},
    {"label": "2007-08", "value": "2007-08"},
    {"label": "2008-09", "value": "2008-09"},
    {"label": "2009-10", "value": "2009-10"},
    {"label": "2010-11", "value": "2010-11"},
    {"label": "2011-12", "value": "2011-12"}
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        html.H1("NBA Player Comparison Dashboard",
                style={'text-align': 'center'}),

        html.Label(["Compare", dcc.Dropdown(
            id='slct-1st-player',
            options=options,
            value='Kobe Bryant',
            style={'width': '40%'})]),

        html.Label(["To", dcc.Dropdown(
            id='slct-2nd-player',
            options=options,
            value='Shaquille Oneil',
            style={'width': '40%'})]),

        html.Br(),
        html.H1("Offensive Metrics",
                style={'text-align': 'center'}),


        html.Div(id='output_container', children=[]),
        html.Br(),

        dcc.Graph(id='favorite-shot'),
        dcc.Graph(id='most-successful-shot'),

        dcc.Graph(id='ppg-per-szn', figure={}),
        # html.Br(),

        dcc.Graph(id='fgp-by-dist'),

        html.Label(["Choose season to compare shooting percentage", dcc.Dropdown(
                    id='selected-season',
                    options=seasons,
                    value='2003-04',
                    style={'width': '40%'})]),
        dcc.Graph(id='shooting-player-league'),

        html.Br(),
        html.H1("Other",
                style={'text-align': 'center'}),

        html.Br(),
        html.Br(),
        dcc.Graph(id='sal-per-szn')

    ])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='favorite-shot', component_property='figure'),
     Output(component_id='most-successful-shot', component_property='figure'),
     Output(component_id='ppg-per-szn', component_property='figure'),
     Output(component_id='fgp-by-dist', component_property='figure'),
     Output(component_id='shooting-player-league',
            component_property='figure'),
     Output(component_id='sal-per-szn', component_property='figure')
     ],
    [Input(component_id='slct-1st-player', component_property='value'),
     Input(component_id='slct-2nd-player', component_property='value'),
     Input(component_id='selected-season', component_property='value')]
)
def update_graph(option1, option2, season):
    # PPG vs Season Line Graph
    fig_PPG = go.Figure()
    # Player 1 trace
    fig_PPG.add_trace(
        go.Scatter(
            x=ppg_result.loc[option1]['Season'],
            y=ppg_result.loc[option1]['PPG'],
            mode='lines',
            name=option1
        ))
    # Player 2 trace
    if option2:
        fig_PPG.add_trace(
            go.Scatter(
                x=ppg_result.loc[option2]['Season'],
                y=ppg_result.loc[option2]['PPG'],
                mode='lines',
                name=option2
            ))
    fig_PPG.update_layout(xaxis_title='Season',
                          yaxis_title='PPG', title='Points Per Game Vs Season', title_x=0.5)

    # FGP vs Season Line Graph
    fig_FGP = go.Figure()
    # Player 1 trace
    fig_FGP.add_trace(
        go.Scatter(
            x=fgp_result.loc[option1]['Season'],
            y=fgp_result.loc[option1]['FG%'],
            mode='lines',
            name=option1
        ))
    # Player 2 trace
    fig_FGP.add_trace(
        go.Scatter(
            x=fgp_result.loc[option2]['Season'],
            y=fgp_result.loc[option2]['FG%'],
            mode='lines',
            name=option2
        ))
    fig_FGP.update_layout(xaxis_title='Season',
                          yaxis_title='FG%', title='Field Goal % Vs Season', title_x=0.5)

    # Salary Per Szn Graph
    fig_sal = go.Figure()
    # Player 1 trace
    fig_sal.add_trace(
        go.Scatter(
            x=sal_result.loc[option1]['Season'],
            y=sal_result.loc[option1]['Salary'],
            mode='lines',
            name=option1
        ))
    # Player 2 trace
    fig_sal.add_trace(
        go.Scatter(
            x=sal_result.loc[option2]['Season'],
            y=sal_result.loc[option2]['Salary'],
            mode='lines',
            name=option2
        ))
    fig_sal.update_layout(xaxis_title='Season',
                          yaxis_title='Salary', title='Annual Salary Vs Season', title_x=0.5)

    # Player Shooting Vs League Bar Chart

    shotNames = df_adjShoot_lebron_Player.columns.values.tolist()[2:]
    player1ShotVals = df_adjShoot_kobe_Player[df_adjShoot_kobe_Player["Season"]
                                              == season].values.tolist()[0][2:]
    player2ShotVals = df_adjShoot_lebron_Player[df_adjShoot_lebron_Player["Season"]
                                                == season].values.tolist()[0][2:]
    leagueShotVals = df_adjShoot_lebron_League[df_adjShoot_lebron_League["Season"]
                                               == season].values.tolist()[0][2:]

    fig_ShotComp = go.Figure(data=[
        go.Bar(name=option1, x=shotNames, y=player1ShotVals),
        go.Bar(name=option2, x=shotNames, y=player2ShotVals),
        go.Bar(name='League', x=shotNames, y=leagueShotVals)
    ])
    fig_ShotComp.update_layout(barmode='group')
    fig_ShotComp.update_layout(xaxis_title='Shooting Metrics',
                               yaxis_title='Percentage', title='Average Shooting Percentage Comparisons', title_x=0.5)

    # Favorite Shot Chart
    shotTypes = percFGA_result.loc[option1].columns.values.tolist()[4:]
    p1Vals = percFGA_result.loc[option1].values.tolist()[0][4:]
    p2Vals = percFGA_result.loc[option2].values.tolist()[0][4:]

    fig_Fav_Shot = go.Figure(data=[
        go.Bar(name=option1, x=shotTypes, y=p1Vals),
        go.Bar(name=option2, x=shotTypes, y=p2Vals)
    ])
    fig_Fav_Shot.update_layout(barmode='group')
    fig_Fav_Shot.update_layout(xaxis_title='Shot Type',
                               yaxis_title='Percentage', title='Favorite Shot', title_x=0.5)

    # Best Shot
    shotTypes = FGPerc_result.loc[option1].columns.values.tolist()[4:]
    p1Vals = FGPerc_result.loc[option1].values.tolist()[0][4:]
    p2Vals = FGPerc_result.loc[option2].values.tolist()[0][4:]

    fig_Best_Shot = go.Figure(data=[
        go.Bar(name=option1, x=shotTypes, y=p1Vals),
        go.Bar(name=option2, x=shotTypes, y=p2Vals)
    ])
    fig_Best_Shot.update_layout(barmode='group')
    fig_Best_Shot.update_layout(xaxis_title='Shot Type',
                                yaxis_title='Percentage', title='Most Successful Shot by FG%', title_x=0.5)

    return fig_Fav_Shot, fig_Best_Shot, fig_PPG, fig_FGP, fig_ShotComp, fig_sal


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
