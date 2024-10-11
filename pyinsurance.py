import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots




class Insurance:
    def __init__(self):
        self._home = 'data/home.xlsx'
        self._auto = 'data/auto.xlsx'
        self._auto_claims = 'data/auto_claims.xlsx'
        
        self.home_insurance = self._convert_to_df(self._home)
        self.auto_insurance = self._convert_to_df(self._auto)
        self.auto_claims = self._convert_to_df(self._auto_claims)

        self._home_premiums, self._home_coverages = self._home_premiums_and_coverages(self.home_insurance)
        self._auto_total_premiums = self._auto_total_premiums(self.auto_insurance)
        self._auto_premium_by_vehicle = self._auto_premium_by_vehicle(self.auto_insurance)
        self._filtered_auto_claims = self._filtered_auto_claims(self.auto_claims)

        self.create_home_insurance_plots = self.create_home_insurance_plots(self._home_premiums, self._home_coverages)
        self.create_auto_insurance_plots = self.create_auto_insurance_plots(self._auto_total_premiums, self._auto_premium_by_vehicle, self._filtered_auto_claims)

    def _convert_to_df(self, file_path):
        try:
            df = pd.read_excel(file_path)
            return df
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    
    def _home_premiums_and_coverages(self, home_df):
        premiums_df = home_df[['DATE', 'INSURER', 'PREMIUM']]
        coverages_df = home_df.drop(columns=['PREMIUM'])

        return premiums_df, coverages_df
    
    def _auto_total_premiums(self, auto_df):
        return auto_df[['DATE', 'TOTAL']]
    
    def _auto_premium_by_vehicle(self, auto_df):
        filtered_auto_df = auto_df.drop(columns=['TOTAL', 'INSURER'])

        melted_auto_df = filtered_auto_df.melt(id_vars=['DATE'], var_name='VEHICLE', value_name='PREMIUM')
        melted_auto_df = melted_auto_df.dropna(subset=['PREMIUM'])

        return melted_auto_df

    def _filtered_auto_claims(self, auto_claims_df):
        return auto_claims_df[['DATE','VEHICLE']]
    
    def create_home_insurance_plots(self, home_premiums, home_coverages):
        home_figure = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=('Home Insurance Premiums', 'Home Insurance Coverages'))

        for insurer in home_premiums['INSURER'].unique():
            insurer_df = home_premiums[home_premiums['INSURER'] == insurer]
            home_figure.add_trace(go.Scatter(
                x=insurer_df['DATE'],
                y=insurer_df['PREMIUM'],
                mode='lines+markers',
                name=insurer,
                marker=dict(symbol='circle')
            ), row=1, col=1)

        for insurer in home_coverages['INSURER'].unique():
            insurer_df = home_coverages[home_coverages['INSURER'] == insurer]
            for col in home_coverages.columns[2:]:
                home_figure.add_trace(go.Scatter(
                    x=insurer_df['DATE'],
                    y=insurer_df[col],
                    mode='lines+markers',
                    name=f'{insurer} - {col}',
                    marker=dict(symbol='square')
                ), row=2, col=1)
    
        home_figure.update_layout(
            title='Home Insurance Premiums and Coverages',
            xaxis_title='Date',
            yaxis_title='Amount',
            legend_title='Insurer - Premium/Coverage',
            hovermode='x unified',
            height=800
        )

        return home_figure
    
    def create_auto_insurance_plots(self, total_premiums, premiums_by_vehicle, claims_by_vehicle):
        vehicle_colors = {
            '2020 TOYOTA TACOMA': 'blue',
            '2012 CHEVY CRUZE': 'green',
            '2016 TOYOTA COROLLA': 'purple',
            '2017 HYUNDAI SONATA': 'orange',
            '2003 HONDA ACCORD': 'red'
        }

        auto_figure = go.Figure()

        for vehicle in premiums_by_vehicle['VEHICLE'].unique():
            vehicle_df = premiums_by_vehicle[premiums_by_vehicle['VEHICLE'] == vehicle]
            auto_figure.add_trace(go.Scatter(
                x=vehicle_df['DATE'],
                y=vehicle_df['PREMIUM'],
                mode='lines+markers',
                marker=dict(color=vehicle_colors.get(vehicle)),
                name=f'{vehicle} Premium'
            ))

        for vehicle in claims_by_vehicle['VEHICLE'].unique():
            vehicle_df = claims_by_vehicle[claims_by_vehicle['VEHICLE'] == vehicle]
            auto_figure.add_trace(go.Scatter(
                x=vehicle_df['DATE'],
                y=[0]*len(vehicle_df),
                mode='markers',
                name=f'{vehicle} Claim',
                marker=dict(size=10, symbol='x', color=vehicle_colors.get(vehicle))
            ))

        auto_figure.add_trace(go.Scatter(
            x=total_premiums['DATE'],
            y=total_premiums['TOTAL'],
            mode='lines+markers',
            marker=dict(color='black'),
            name='Total Premium'
        ))

        auto_figure.update_layout (
            title='Auto Insurance',
            xaxis_title = 'Date',
            yaxis_title = 'Premium',
            legend_title = 'Legend',
            hovermode='x unified',
            height=800
        )

        return auto_figure
    

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
