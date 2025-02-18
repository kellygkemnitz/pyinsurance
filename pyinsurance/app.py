from pyinsurance.pyinsurance import Insurance

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc


insurance = Insurance()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.FONT_AWESOME])

app.layout = html.Div([
    dbc.Tabs(
        id='tabs',
        children=[
            dbc.Tab(label='Home Insurance', tab_id='tab-1', children=[
                dcc.Graph(
                    id='home-insurance-plots',
                    figure=insurance.create_home_insurance_plots,
                    config={'displayModeBar': False},
                )
            ]),
            dbc.Tab(label='Auto Insurance', tab_id='tab-2', children=[
                dcc.Graph(
                    id='auto-insurance-plots',
                    figure=insurance.create_auto_insurance_plots,
                    config={'displayModeBar': False},
                )
            ])
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)