import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Insurance:
    def __init__(self):
        self.auto_data = 'data/auto.json'
        self.home_data = 'data/home.json'
                
        self.auto_df = self._convert_to_df(self.auto_data)
        self.home_df = self._convert_to_df(self.home_data)

        self.home_premiums, self.home_coverages = self._home_premiums_and_coverages(self.home_df)
        
        self.auto_premiums = self._auto_premiums(self.auto_df)
        self.auto_premiums_by_vehicle = self._auto_premiums_by_vehicle(self.auto_df)
        self.auto_claims_by_vehicle = self._filtered_auto_claims(self.auto_df)

        self.create_auto_plots()
        self.create_home_plots()
        

    def _convert_to_df(self, file_path):
        try:
            df = pd.read_json(file_path)
            return df
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    
    def _home_premiums_and_coverages(self, home_df):
        premiums_df = home_df[['Date', 'Insurer', 'Total']].copy()
        coverages_df = home_df.drop(columns=['Total']).copy()

        return premiums_df, coverages_df
    
    def _auto_premiums(self, auto_df):
        premiums_df = auto_df[auto_df['Category'] == 'Premium'].copy()
        premiums_df = premiums_df.drop(columns=['Category'])
        
        return premiums_df[['Date', 'Total']]
    
    def _auto_premiums_by_vehicle(self, auto_df):
        premiums_df = auto_df[auto_df['Category'] == 'Premium'].copy()
        premiums_df = premiums_df.drop(columns=['Category'])
        filtered_auto_df = premiums_df.drop(columns=['Total', 'Insurer'])

        melted_auto_df = filtered_auto_df.melt(id_vars=['Date'], var_name='Vehicle', value_name='Total')
        melted_auto_df = melted_auto_df.dropna(subset=['Total'])

        return melted_auto_df

    def _filtered_auto_claims(self, auto_df):
        claims_df = auto_df[auto_df['Category'] == 'Claim'].copy()
        claims_df = claims_df.drop(columns=['Category'])
        
        return claims_df[['Date','Vehicle']]
    
    def create_auto_plots(self):
        vehicle_colors = {
            '2020 Toyota Tacoma': 'grey',
            '2012 Chevy Cruze': 'red',
            '2016 Toyota Corolla': 'orange',
            '2017 Hyundai Sonata': 'blue',
            '2003 Honda Accord': 'pink'
        }

        auto_figure = go.Figure()

        for vehicle in self.auto_premiums_by_vehicle['Vehicle'].unique():
            vehicle_df = self.auto_premiums_by_vehicle[self.auto_premiums_by_vehicle['Vehicle'] == vehicle]
            auto_figure.add_trace(go.Scatter(
                x=vehicle_df['Date'],
                y=vehicle_df['Total'],
                mode='lines+markers',
                marker=dict(color=vehicle_colors.get(vehicle)),
                name=f'{vehicle} Premium'
            ))

        for vehicle in self.auto_claims_by_vehicle['Vehicle'].unique():
            vehicle_df = self.auto_claims_by_vehicle[self.auto_claims_by_vehicle['Vehicle'] == vehicle]
            auto_figure.add_trace(go.Scatter(
                x=vehicle_df['Date'],
                y=[0]*len(vehicle_df),
                mode='markers',
                name=f'{vehicle} Claim',
                marker=dict(size=10, symbol='x', color=vehicle_colors.get(vehicle))
            ))

        auto_figure.add_trace(go.Scatter(
            x=self.auto_premiums['Date'],
            y=self.auto_premiums['Total'],
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
    
    def create_home_plots(self):
        home_figure = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=(
                'Home Insurance Premiums',
                'Home Insurance Coverages'
            )
        )

        home_figure.add_trace(go.Scatter(
            x=self.home_premiums['Date'],
            y=self.home_premiums['Total'],
            mode='lines+markers',
            name='Premium',
            marker=dict(symbol='circle')
        ), row=1, col=1)

        for col in self.home_coverages.columns[2:]:
            home_figure.add_trace(go.Scatter(
                x=self.home_coverages['Date'],
                y=self.home_coverages[col],
                mode='lines+markers',
                name=f'{col}',
                marker=dict(symbol='square')
            ), row=2, col=1)

        home_figure.update_layout(
            title='Home Insurance Premiums and Coverages',
            yaxis_title='Amount',
            yaxis2=dict(title='Amount'),
            legend_title='Premium/Coverage',
            hovermode='x unified',
            height=800
        )

        return home_figure