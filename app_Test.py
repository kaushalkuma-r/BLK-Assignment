import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Load and preprocess data
def load_data():
    # Load dataset (replace with actual file path)
    df = pd.read_csv('test.csv')
    
    # Preprocessing
    df['maturity'] = pd.to_datetime(df['maturity'])
    df['years_to_maturity'] = (df['maturity'] - datetime.now()).dt.days / 365
    df['Rating_Bucket'] = df['Rating'].str.extract(r'([A-Z]+)')[0]
    df['Rating_Bucket'] = df['Rating_Bucket'].replace({
        'AAA': 'AAA',
        'AA': 'AA',
        'A': 'A',
        'BBB': 'BBB',
        'BB': 'HY', 'B': 'HY', 'CCC': 'HY', 'CC': 'HY', 'C': 'HY', 'D': 'HY'
    }).fillna('Unrated')
    
    return df

# Create visualizations
def create_visualizations(df):
    # 1. Sector Distribution
    sector_dist = df.groupby('Sector')['Par'].sum().reset_index()
    fig_sector = px.pie(sector_dist, names='Sector', values='Par', 
                        title='Portfolio Distribution by Sector')
    
    # 2. Credit Risk Distribution
    rating_dist = df['Rating_Bucket'].value_counts().reset_index()
    rating_dist.columns = ['Rating_Bucket', 'Count']
    fig_rating = px.bar(rating_dist, x='Rating_Bucket', y='Count',
                        title='Credit Risk Distribution',
                        labels={'Rating_Bucket': 'Rating Bucket', 'Count': 'Count'})
    
    # 3. Rating Coverage
    rated_counts = df[df['Rating_Bucket'] != 'Unrated']['Rating_Bucket'].count()
    unrated_counts = len(df) - rated_counts
    fig_coverage = go.Figure(go.Pie(
        labels=['Rated', 'Unrated'],
        values=[rated_counts, unrated_counts],
        title='Rating Coverage'
    ))
    
    # 4. Outlook Distribution
    outlook_dist = df['Outlook'].value_counts().reset_index()
    outlook_dist.columns = ['Outlook', 'Count']
    fig_outlook = px.bar(outlook_dist, x='Outlook', y='Count',
                         title='Outlook Distribution',
                         labels={'Outlook': 'Outlook', 'Count': 'Count'})
    
    # 5. Top Obligors
    top_obligors = df.groupby('Obligor Name')['Par'].sum().nlargest(10).reset_index()
    fig_top = px.bar(top_obligors, x='Obligor Name', y='Par',
                     title='Top 10 Obligors by Par Value')
    
    # 6. Maturity Profile
    bins = [0, 5, 10, 15, 20, 30, 100]
    labels = ['<5', '5-10', '10-15', '15-20', '20-30', '30+']
    df['Maturity_Bucket'] = pd.cut(df['years_to_maturity'], bins=bins, labels=labels)
    maturity_dist = df.groupby('Maturity_Bucket')['Par'].sum().reset_index()
    fig_maturity = px.bar(maturity_dist, x='Maturity_Bucket', y='Par',
                          title='Maturity Profile')
    
    # 7. Jump Risk
    jump_risk = df[(df['Rating_Bucket'] == 'BBB') & 
                  (df['Outlook'] == 'Negative')]
    
    # 8. Geographic Distribution
    state_exposure = df.groupby('State')['Par'].sum().reset_index()
    fig_geo = px.choropleth(state_exposure,
                            locations='State',
                            locationmode='USA-states',
                            color='Par',
                            scope='usa',
                            title='Exposure by U.S. State')
    
    # 9. Map Visualization
    fig_map = px.scatter_geo(df,
                             lat='Latitude',
                             lon='Longitude',
                             size='Par',
                             hover_name='Obligor Name',
                             scope='usa',
                             title='Obligor Locations')
    
    return {
        'sector': fig_sector,
        'rating': fig_rating,
        'coverage': fig_coverage,
        'outlook': fig_outlook,
        'top': fig_top,
        'maturity': fig_maturity,
        'jump_risk': jump_risk,
        'geo': fig_geo,
        'map': fig_map
    }

# Main dashboard
def main():
    st.set_page_config(layout="wide")
    st.title("Municipal Bonds Portfolio Dashboard")
    st.subheader("BlackRock Case Study - Portfolio Analysis")
    
    # Load data
    df = load_data()
    
    # Create visualizations
    visuals = create_visualizations(df)
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        selected_sectors = st.multiselect(
            "Filter Sectors",
            options=df['Sector'].unique(),
            default=df['Sector'].unique()
        )
    
    with col2:
        rating_options = ['All'] + sorted(df['Rating_Bucket'].unique().tolist())
        selected_rating = st.selectbox(
            "Filter Rating Bucket",
            options=rating_options
        )
    
    # Apply filters
    filtered_df = df.copy()
    if selected_sectors:
        filtered_df = filtered_df[filtered_df['Sector'].isin(selected_sectors)]
    if selected_rating != 'All':
        filtered_df = filtered_df[filtered_df['Rating_Bucket'] == selected_rating]
    
    # Key Metrics
    st.header("Portfolio Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Par Value", f"${filtered_df['Par'].sum():,.0f}")
    col2.metric("Number of Obligors", len(filtered_df))
    col3.metric("Average Coupon", f"{filtered_df['coupon'].mean():.2f}%")
    col4.metric("Jump Risk Exposure", len(visuals['jump_risk']))
    
    # Map and Geo Distribution
    st.header("Geographic Analysis")
    st.plotly_chart(visuals['map'], use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(visuals['geo'], use_container_width=True)
    with col2:
        st.plotly_chart(visuals['sector'], use_container_width=True)
    
    # Risk Analysis
    st.header("Risk Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(visuals['rating'], use_container_width=True)
    with col2:
        st.plotly_chart(visuals['coverage'], use_container_width=True)
    
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(visuals['outlook'], use_container_width=True)
    with col4:
        st.plotly_chart(visuals['maturity'], use_container_width=True)
    
    # Top Obligors
    st.header("Top Obligors")
    st.plotly_chart(visuals['top'], use_container_width=True)
    
    # Jump Risk Details
    st.header("Jump Risk Exposure")
    st.dataframe(visuals['jump_risk'][['Obligor Name', 'Rating', 'Outlook', 'Par']])
    
    # Data Table
    st.header("Portfolio Data")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main()