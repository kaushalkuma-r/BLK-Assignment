import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import json
from src.generate_map import generate_obligor_map
from streamlit_folium import st_folium
import datetime

# ---------------- Streamlit Config ----------------
st.set_page_config(page_title="Municipal Bonds Dashboard", layout="wide")
st.toast(f"🔁 Last run: {datetime.datetime.now().strftime('%H:%M:%S.%f')}")

# ---------------- Caching & Data Loading ----------------
@st.cache_data
def load_data():
    portfolio_data = pd.read_excel("data/PortfolioX.xlsx")
    location_data = pd.read_excel("data/location_data.xlsx")
    return portfolio_data, location_data

@st.cache_data
def merge_portfolio_with_location(portfolio_data, location_data):
    portfolio_data = portfolio_data.copy()
    location_data = location_data.copy()
    
    portfolio_data['Obligor Name'] = portfolio_data['Obligor Name'].str.upper().str.strip()
    location_data['Obligor Name'] = location_data['Obligor Name'].str.upper().str.strip()
    
    merged = pd.merge(
        portfolio_data,
        location_data[['Obligor Name', 'County', 'State', 'ZIP', 'Latitude', 'Longitude']],
        on='Obligor Name',
        how='left'
    )

    unmatched_count = merged['Latitude'].isna().sum()
    if unmatched_count > 0:
        st.warning(f"⚠️ Unmatched rows without location: {unmatched_count}")
    return merged

@st.cache_data
def clean_data(df):
    df_clean = df.dropna(subset=["Latitude", "Longitude", "Obligor Name"])
    df_unique = df_clean.drop_duplicates(subset=["Obligor Name", "Latitude", "Longitude"]).reset_index(drop=True)
    return df_unique

# ---------------- Visualizations ----------------
def exposure_by_obligor(portfolio_data):
    exposure_df = portfolio_data.groupby('Obligor Name', as_index=False)['Par'].sum()
    exposure_df = exposure_df.sort_values(by='Par', ascending=False).head(20)

    fig = px.bar(
        exposure_df,
        x='Par',
        y='Obligor Name',
        orientation='h',
        title='Top 20 Obligors by Par Exposure',
        labels={'Par': 'Par Amount', 'Obligor Name': 'Obligor'},
        color='Par',
        color_continuous_scale='blackbody'
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=600,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

# ---------------- Load & Process Data (Session State) ----------------
if "portfolio_data" not in st.session_state:
    portfolio_data, location_data = load_data()
    merged_data = merge_portfolio_with_location(portfolio_data, location_data)
    merged_data_unique = clean_data(merged_data)

    st.session_state["portfolio_data"] = portfolio_data
    st.session_state["merged_data"] = merged_data
    st.session_state["processed_data"] = merged_data_unique
else:
    portfolio_data = st.session_state["portfolio_data"]
    merged_data = st.session_state["merged_data"]
    merged_data_unique = st.session_state["processed_data"]

# ---------------- UI Layout ----------------
st.title("📊 BlackRock Municipal Bonds Portfolio Dashboard")

tab1, tab2 = st.tabs(["📍 Map", "📊 Obligor Exposure"])

with tab1:
    map_obj = generate_obligor_map(merged_data_unique)
    st_folium(map_obj, width=900, height=600)

with tab2:
    chart = exposure_by_obligor(merged_data)
    st.plotly_chart(chart, use_container_width=True)

# ---------------- Footer ----------------
st.markdown("---")
st.markdown("👨‍💻 Built for BlackRock Case Study by **Kaushal Kumar**")
