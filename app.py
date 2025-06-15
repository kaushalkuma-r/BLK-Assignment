import streamlit as st
from data_loader import load_data
from visualisations import *
from src.analysis.sector_analysis import *
from src.analysis.credit_risk_analysis import *
from src.analysis.rating_analysis import *

# Load data
df = load_data()

# Configure page
st.set_page_config(layout="wide", page_title="BlackRock Portfolio Dashboard")
st.title("Municipal Bonds Portfolio Dashboard")
st.subheader("BlackRock Case Study - Portfolio Analysis")

# Key metrics
st.header("Portfolio Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Par Value", f"${df['Par'].sum():,.0f}")
col2.metric("Number of Obligors", len(df))
col3.metric("Average Coupon", f"{df['coupon'].mean():.2f}%")

jump_risk_df = create_jump_risk(df)
col4.metric("Jump Risk Exposure", len(jump_risk_df))

# Filters section above maps
st.header("Portfolio Filters")
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    sectors = ['All'] + sorted(df['Sector'].unique().tolist())
    selected_sector = st.selectbox("Sector", sectors)

with filter_col2:
    rating_buckets = ['All'] + sorted(df['Rating_Bucket'].unique().tolist())
    selected_rating = st.selectbox("Rating Bucket", rating_buckets)

with filter_col3:
    states = ['All'] + sorted(df['State'].unique().tolist())
    selected_state = st.selectbox("State", states)

# Apply filters
filtered_df = df.copy()
if selected_sector != 'All':
    filtered_df = filtered_df[filtered_df['Sector'] == selected_sector]
if selected_rating != 'All':
    filtered_df = filtered_df[filtered_df['Rating_Bucket'] == selected_rating]
if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['State'] == selected_state]

# Map and exposure visualizations
st.header("Geographic Exposure")
col1, map_col2 = st.columns([1, 1])  # Equal width columns

with col1:
    st.header("Obligor Location Map")
    map_data = filtered_df[['Obligor Name', 'County', 'State', 'ZIP', 
                            'Latitude', 'Longitude', 'Sector', 'Par', 
                            'Rating', 'Outlook']].copy()
    kepler_html = create_kepler_map(map_data)
    components.html(kepler_html, height=700)

with map_col2:
    st.subheader("State Exposure")
    state_exposure = create_state_exposure(filtered_df)
    # Increased size by adjusting height and using_container_width
    st.plotly_chart(state_exposure, use_container_width=True, height=700)

# Data table
st.header("Portfolio Data")
st.dataframe(filtered_df)