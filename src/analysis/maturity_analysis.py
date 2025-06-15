import pandas as pd
import plotly.express as px
from datetime import datetime
from config import shared_color_scale

def analyze_maturity_profile(df):
    df['maturity'] = pd.to_datetime(df['maturity'], errors='coerce')

    today = pd.Timestamp(datetime.today().date())

    df['years_to_maturity'] = (df['maturity'] - today).dt.days / 365.25

    bins = [0, 5, 10, 15, 20, 30, float('inf')]
    labels = ['<5 years', '5-10 years', '10-15 years', '15-20 years', '20-30 years', '30+ years']

    df['maturity_bucket'] = pd.cut(df['years_to_maturity'], bins=bins, labels=labels, right=False)

    maturity_summary = (
        df.groupby('maturity_bucket', observed=True)['Par']
        .sum()
        .reset_index()
        .sort_values('maturity_bucket')
    )

    fig = px.bar(
        maturity_summary,
        x='maturity_bucket',
        y='Par',
        text='Par',
        title='Portfolio Maturity Profile',
        labels={'Par': 'Total Par Exposure', 'maturity_bucket': 'Maturity Bucket'},
        color='Par',
        color_continuous_scale=shared_color_scale
    )
    
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        width=900,
        height=500,
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        plot_bgcolor='white',
        xaxis_title='Maturity Bucket',
        yaxis_title='Total Par Exposure',
    )
    
    return fig