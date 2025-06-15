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

# Initialize session state for question toggles
if 'show_questions' not in st.session_state:
    st.session_state.show_questions = [False] * 8

# Sidebar filters
st.sidebar.header("Portfolio Filters")

sectors = ['All'] + sorted(df['Sector'].unique().tolist())
selected_sector = st.sidebar.selectbox("Sector", sectors)

rating_buckets = ['All'] + sorted(df['Rating_Bucket'].unique().tolist())
selected_rating = st.sidebar.selectbox("Rating Bucket", rating_buckets)

states = ['All'] + sorted(df['State'].unique().tolist())
selected_state = st.sidebar.selectbox("State", states)

# Apply filters
filtered_df = df.copy()
if selected_sector != 'All':
    filtered_df = filtered_df[filtered_df['Sector'] == selected_sector]
if selected_rating != 'All':
    filtered_df = filtered_df[filtered_df['Rating_Bucket'] == selected_rating]
if selected_state != 'All':
    filtered_df = filtered_df[filtered_df['State'] == selected_state]

# Key metrics
st.header("Portfolio Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Par Value", f"${filtered_df['Par'].sum():,.0f}")
col2.metric("Number of Obligors", len(filtered_df))
col3.metric("Average Coupon", f"{filtered_df['coupon'].mean():.2f}%")

jump_risk_df = create_jump_risk(filtered_df)
col4.metric("Jump Risk Exposure", len(jump_risk_df))

# Map and exposure visualizations
st.header("Geographic Exposure")
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Obligor Location Map")
    map_data = filtered_df[['Obligor Name', 'County', 'State', 'ZIP', 
                            'Latitude', 'Longitude', 'Sector', 'Par', 
                            'Rating', 'Outlook']].copy()
    kepler_html = create_kepler_map(map_data)
    components.html(kepler_html, height=700)

with col2:
    st.subheader("State Exposure")
    state_exposure = create_state_exposure(filtered_df)
    st.plotly_chart(state_exposure, use_container_width=True)

# Analysis questions section
st.header("Portfolio Analysis")
st.write("Click on questions below to view analysis:")

# Question 1
with st.expander("1. How is the portfolio distributed by sector?"):
    fig = analyze_sector_distribution(filtered_df)
    st.plotly_chart(fig, use_container_width=True)

# Question 2
with st.expander("2. How is credit risk distributed across the portfolio?"):
    fig = analyze_credit_risk_distribution(filtered_df)
    st.plotly_chart(fig, use_container_width=True)

# Question 3
with st.expander("3. What is the rating coverage of the portfolio?"):
    fig = analyze_rating_coverage_bar(filtered_df)
    st.plotly_chart(fig, use_container_width=True)

# Question 4
with st.expander("4. What is the outlook distribution across obligors?"):
    fig = create_outlook_distribution(filtered_df)
    st.plotly_chart(fig, use_container_width=True)

# Question 5
with st.expander("5. Who are the largest obligors in the portfolio?"):
    fig = create_top_obligors(filtered_df)
    st.plotly_chart(fig, use_container_width=True)

# Question 6
with st.expander("6. What is the portfolio's maturity profile?"):
    fig = create_maturity_profile(filtered_df)
    st.plotly_chart(fig, use_container_width=True)

# Question 7
with st.expander("7. Does the portfolio have any jump risk exposure?"):
    jump_risk = create_jump_risk(filtered_df)
    if not jump_risk.empty:
        st.dataframe(jump_risk)
    else:
        st.success("No jump risk exposure found in the portfolio")

# Question 8
with st.expander("8. How geographically diversified is the portfolio?"):
    state_exposure = create_state_exposure(filtered_df)
    st.plotly_chart(state_exposure, use_container_width=True)
    st.write("Geographic diversification is measured by the distribution of exposure across different U.S. states.")

# Data table
st.header("Portfolio Data")
st.dataframe(filtered_df)