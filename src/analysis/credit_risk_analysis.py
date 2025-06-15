import plotly.express as px
import pandas as pd
def analyze_credit_risk_distribution(portfolio_data):
    """
    Analyzes and plots the distribution of credit risk across obligors in defined rating buckets.
    
    Args:
        portfolio_data (pd.DataFrame): Must contain 'Rating' and 'Obligor' columns.
    """
    def map_rating_to_bucket(rating):
        if pd.isnull(rating):
            return None
        rating = rating.upper().strip()
        if rating == 'AAA':
            return 'AAA'
        elif rating.startswith('AA'):
            return 'AA'
        elif rating.startswith('A'):
            return 'A'
        elif rating.startswith('BBB'):
            return 'BBB'
        elif rating.startswith(('BB', 'B', 'CCC', 'CC', 'C', 'D')):
            return 'HY'
        else:
            return None

    # Apply rating bucketing
    portfolio_data['Rating_Bucket'] = portfolio_data['Rating'].apply(map_rating_to_bucket)

    # Filter out unrated
    rated_data = portfolio_data.dropna(subset=['Rating_Bucket'])

    # Count obligors
    rating_counts = (
        rated_data.groupby('Rating_Bucket')['Obligor']
        .nunique()
        .reindex(['AAA', 'AA', 'A', 'BBB', 'HY'])
        .reset_index(name='Obligor_Count')
    )

    # Calculate percentage
    total = rating_counts['Obligor_Count'].sum()
    rating_counts['Percentage'] = 100 * rating_counts['Obligor_Count'] / total

    # Use Plotly color palette (clean, professional)
    fig = px.bar(
        rating_counts,
        x='Rating_Bucket',
        y='Obligor_Count',
        text=rating_counts['Percentage'].map(lambda x: f"{x:.1f}%"),
        color='Rating_Bucket',
        color_discrete_sequence=px.colors.qualitative.Plotly,
        title='Credit Risk Distribution Across Obligor Ratings',
        labels={'Rating_Bucket': 'Rating Bucket', 'Obligor_Count': 'Number of Obligors'}
    )

    fig.update_traces(textposition='outside', textfont_size=10)
    fig.update_layout(
        width=900,
        height=500,
        xaxis_title='Rating Bucket',
        yaxis_title='Number of Unique Obligors',
        title_font_size=18,
        showlegend=False,
        plot_bgcolor='white',
        font=dict(family="Segoe UI, sans-serif", size=12)
    )

    return fig
