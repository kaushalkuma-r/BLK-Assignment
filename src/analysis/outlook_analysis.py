import plotly.express as px
from config import shared_color_scale

def analyze_outlook_distribution(portfolio_data):
    portfolio_data['Outlook'] = (
        portfolio_data['Outlook']
        .fillna('Unspecified')
        .astype(str)
        .str.strip()
        .str.title()
    )
    
    outlook_counts = (
        portfolio_data['Outlook']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'Outlook', 'Outlook': 'Bond_Count'})
    )

    total_bonds = outlook_counts['count'].sum()
    outlook_counts['Percentage'] = (100 * outlook_counts['count'] / total_bonds).round(1)

    fig = px.bar(
        outlook_counts.sort_values('count', ascending=True),
        x='count',
        y='Bond_Count',
        orientation='h',
        text=outlook_counts['Percentage'].apply(lambda x: f"{x}%"),
        color='Bond_Count',
        color_discrete_sequence=shared_color_scale,
        title='Outlook Distribution Across Bonds'
    )

    fig.update_traces(textposition='outside', textfont_size=12)
    fig.update_layout(
        width=900,
        height=450,
        xaxis_title='Number of Bonds',
        yaxis_title='Credit Outlook',
        showlegend=True,
        font=dict(family='Segoe UI', size=12),
        title_font_size=18,
        plot_bgcolor='white'
    )

    return fig