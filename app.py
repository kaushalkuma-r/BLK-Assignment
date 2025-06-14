import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import json


def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def load_data():
    # Load data
    portfolio_data = pd.read_excel("data/PortfolioX.xlsx")
    location_data = pd.read_excel("data/location_data.xlsx")

    # Merge on 'Obligor Name'
    merged = pd.merge(portfolio_data, location_data, on="Obligor Name", how="left")
    return portfolio_data, location_data, merged

def exposure_by_obligor(df):
    exposure_df = df.groupby("Obligor Name")["Par"].sum().reset_index().sort_values(by="Par", ascending=False)
    fig = px.bar(exposure_df.head(20), x="Obligor Name", y="Par",
                 title="Top 20 Obligors by Par Amount",
                 labels={"Par": "Par Amount ($)", "Obligor Name": "Obligor"},
                 color_discrete_sequence=["#636EFA"])
    fig.update_layout(xaxis_tickangle=-45, height=500)
    return fig

def map_obligors(df, sector_filter=None):
    if sector_filter:
        df = df[df["Sector"] == sector_filter]
    fig = px.scatter_mapbox(df.dropna(subset=['Latitude', 'Longitude']),
                             lat="Latitude",
                             lon="Longitude",
                             hover_name="Obligor Name",
                             hover_data=["State", "County", "Par"],
                             color="Par",
                             color_continuous_scale="Viridis",
                             size="Par",
                             zoom=3,
                             height=600)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig


st.set_page_config(page_title="Municipal Bonds Dashboard", layout="wide")


st_lottie(load_lottie("assets/animation.json"), height=200, speed=1.2)

st.title("BlackRock Municipal Bonds Portfolio Dashboard")


portfolio_data, location_data, merged_data = load_data()


sectors = merged_data["Sector"].dropna().unique().tolist()
selected_sector = st.sidebar.selectbox("Filter by Sector", ["All"] + sectors)


st.subheader("📍 Geographic Exposure Map")
if selected_sector == "All":
    st.plotly_chart(map_obligors(merged_data), use_container_width=True)
else:
    st.plotly_chart(map_obligors(merged_data, sector_filter=selected_sector), use_container_width=True)

st.subheader("🏢 Exposure by Obligor")
st.plotly_chart(exposure_by_obligor(merged_data), use_container_width=True)


st.markdown("---")
st.markdown("Built for BlackRock Case Study by Kaushal Kumar")
