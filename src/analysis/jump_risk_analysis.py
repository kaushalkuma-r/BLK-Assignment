import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px

def analyze_jump_risk(df):
    data = df.copy()
    data['Rating'] = data['Rating'].astype(str).str.upper()
    data['Outlook'] = data['Outlook'].astype(str).str.upper()
    
    jump_risk_df = data[
        (data['Rating'].str.startswith('BBB')) &
        (data['Outlook'] == 'DETERIORATING')
    ]

    jump_risk_summary = (
        jump_risk_df.groupby(['Obligor', 'Rating', 'Outlook'], observed=True)['Par']
        .sum()
        .reset_index()
        .sort_values(by='Par', ascending=False)
    )

    if jump_risk_summary.empty:
        print("No obligors found with BBB rating and negative outlook (no jump-to-junk risk identified).")
    else:
        print("Potential jump risk obligors:")
        print(jump_risk_summary.to_string(index=False))
    
        # Plot with orange-red-yellow color scale
        fig = px.bar(
            jump_risk_summary,
            x='Obligor',
            y='Par',
            color='Rating',
            text='Par',
            title='Jump Risk Exposure: BBB-Rated Obligors with Negative Outlook',
            labels={'Par': 'Total Par Exposure'},
            color_discrete_sequence=['#FFA500', '#FF4500', '#FFD700']  # Orange, Red-Orange, Gold
        )
        
        fig.update_traces(
            textposition='outside',
            texttemplate='%{text:.0f}'
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            width=1000,
            height=500,
            plot_bgcolor='white',
            xaxis_title='Obligor',
            yaxis_title='Total Par Exposure',
            template='plotly_white'
        )
        
    return fig 