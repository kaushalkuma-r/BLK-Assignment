import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import shared_color_scale

def analyze_geographic_diversity(df):

    if 'State' not in df.columns:
        print("The dataset does not contain a 'State' column. Please provide the correct column for geographic info.")
        return

    state_exposure = (
        df.groupby('State', observed=True)['Par']
        .sum()
        .reset_index()
        .sort_values(by='Par', ascending=False)
    )
    
    
    fig = px.bar(
        state_exposure,
        x='State',
        y='Par',
        text='Par',
        title='Portfolio Exposure by U.S. State',
        labels={'Par': 'Total Par Exposure'},
        color='Par',
        color_continuous_scale=shared_color_scale
    )
    
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        xaxis_tickangle=-45,
        width=1000,
        height=500,
        plot_bgcolor='white'
    )
    
    return fig
