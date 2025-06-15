import plotly.express as px
import pandas as pd
def analyze_rating_coverage_bar(portfolio_data):
    """
    Analyzes and plots rating coverage (Rated vs Unrated obligors) using a horizontal bar chart.
    
    Args:
        portfolio_data (pd.DataFrame): Must contain 'Rating' and 'Obligor' columns.
    """
    def is_rated(rating):
        if pd.isnull(rating):
            return False
        rating = rating.upper().strip()
        return rating not in ['NR', 'UR', '']

    # Flag each row as rated/unrated
    portfolio_data['Is_Rated'] = portfolio_data['Rating'].apply(is_rated)

    # Group by obligor — if any bond is rated, mark the obligor as rated
    obligor_rating_status = (
        portfolio_data.groupby('Obligor')['Is_Rated']
        .any()
        .reset_index()
    )

    # Label
    obligor_rating_status['Rating_Status'] = obligor_rating_status['Is_Rated'].map({True: 'Rated', False: 'Unrated'})

    # Count
    rating_coverage = obligor_rating_status['Rating_Status'].value_counts().reset_index()
    rating_coverage.columns = ['Rating_Status', 'Obligor_Count']
    total = rating_coverage['Obligor_Count'].sum()
    rating_coverage['Percentage'] = 100 * rating_coverage['Obligor_Count'] / total

    # Plot
    fig = px.bar(
        rating_coverage.sort_values('Obligor_Count', ascending=True),
        x='Obligor_Count',
        y='Rating_Status',
        orientation='h',
        color='Rating_Status',
        color_discrete_map={
            'Rated': '#1f77b4',     # Blue
            'Unrated': '#ff7f0e'    # Orange
        },
        text=rating_coverage['Percentage'].map(lambda x: f"{x:.1f}%"),
        title='Rating Coverage of Portfolio Obligors'
    )

    fig.update_traces(textposition='outside', textfont_size=12)
    fig.update_layout(
        xaxis_title='Number of Unique Obligors',
        yaxis_title='',
        width=800,
        height=400,
        showlegend=False,
        font=dict(family='Segoe UI', size=12),
        plot_bgcolor='white',
        title_font_size=18
    )

    return fig
