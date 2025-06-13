import plotly.express as px

def analyze_sector_distribution(portfolio_data):
    """
    Create a wide interactive Plotly vertical bar chart showing the Par distribution across sectors.

    Args:
        portfolio_data (pd.DataFrame): DataFrame with 'Sector' and 'Par' columns.

    Returns:
        fig (plotly.graph_objects.Figure): Interactive bar chart.
    """
    # Aggregate Par amount by sector
    sector_distribution = (
        portfolio_data.groupby('Sector', as_index=False)['Par'].sum()
    )
    
    # Calculate percentage share
    total_par = sector_distribution['Par'].sum()
    sector_distribution['Percentage'] = 100 * sector_distribution['Par'] / total_par

    # Sort by Par descending
    sector_distribution.sort_values('Par', ascending=False, inplace=True)

    # Create Plotly bar chart
    fig = px.bar(
        sector_distribution,
        x='Sector',
        y='Par',
        text=sector_distribution['Percentage'].map(lambda x: f"{x:.1f}%"),
        labels={'Par': 'Total Par Amount'},
        title='Portfolio Distribution by Sector (Par Amount)',
        color='Par',
        color_continuous_scale='Viridis'
    )

    # Update trace: smaller text, position outside
    fig.update_traces(
        textposition='outside',
        textfont_size=10
    )

    # Wider layout, smaller ticks, rotated x-axis
    fig.update_layout(
        width=1400,
        height=600,
        margin=dict(l=40, r=40, t=60, b=160),
        xaxis_tickangle=45,
        xaxis_tickfont_size=10,
        yaxis_title_font_size=12,
        title_font_size=18,
        showlegend=False
    )

    fig.show()
