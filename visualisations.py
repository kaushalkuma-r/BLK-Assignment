import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pydeck.types import String
import pydeck as pdk

# def create_kepler_map(df):
#     # Configure tooltip based on the config
#     tooltip = {
#         "html": """
#         <b>Obligor:</b> {Obligor Name}<br>
#         <b>County:</b> {County}<br>
#         <b>State:</b> {State}<br>
#         <b>Par Amount:</b> {Par}<br>
#         <b>Rating:</b> {Rating}<br>
#         <b>Outlook:</b> {Outlook}
#         """,
#         "style": {
#             "backgroundColor": "#1a1a1a",
#             "color": "white",
#             "fontFamily": "Helvetica",
#             "fontSize": "14px"
#         }
#     }
    
#     # Create layer based on the Kepler config
#     layer = pdk.Layer(
#         "ScatterplotLayer",
#         df,
#         get_position=["Longitude", "Latitude"],
#         get_radius=10,  # Fixed radius from config
#         get_fill_color=[248, 149, 112, 204],  # RGBA from config
#         get_line_color=[0, 0, 0, 0],  # No outline
#         pickable=True,
#         opacity=0.8,  # From config
#         stroked=False,  # No outline
#         filled=True,  # From config
#         auto_highlight=True,
#         highlight_color=[252, 242, 26, 255],  # From config
#         radius_scale=1,
#         radius_min_pixels=1,
#         radius_max_pixels=50,  # From radiusRange in config
#     )
    
#     # Set initial view from config
#     view_state = pdk.ViewState(
#         latitude=46.271014210208314,
#         longitude=-113.70156439667934,
#         zoom=2.75877838326137,
#         pitch=0,
#         bearing=0
#     )
    
#     # Create map with style from config
#     return pdk.Deck(
#         map_style="light",  # positron style equivalent
#         initial_view_state=view_state,
#         layers=[layer],
#         tooltip=tooltip,
#         # Additional styling from config
#         parameters={
#             "blending": "normal",  # From layerBlending in config
#             "highlightColor": [252, 242, 26, 255],
#         }
#     )
import pandas as pd
import streamlit as st
from keplergl import KeplerGl
import tempfile
import base64
from pathlib import Path
import streamlit.components.v1 as components

# Kepler.gl configuration from your input
KEPLER_CONFIG = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [],
            "layers": [{
                "id": "g1l7m9i",
                "type": "point",
                "config": {
                    "dataId": "obligor_data",
                    "columnMode": "points",
                    "label": "point",
                    "color": [248, 149, 112],
                    "highlightColor": [252, 242, 26, 255],
                    "columns": {
                        "lat": "Latitude",
                        "lng": "Longitude"
                    },
                    "isVisible": True,
                    "visConfig": {
                        "radius": 10,
                        "fixedRadius": False,
                        "opacity": 0.8,
                        "outline": False,
                        "thickness": 2,
                        "strokeColor": None,
                        "colorRange": {
                            "name": "Global Warming",
                            "type": "sequential",
                            "category": "Uber",
                            "colors": ["#4C0035", "#880030", "#B72F15", "#D6610A", "#EF9100", "#FFC300"]
                        },
                        "strokeColorRange": {
                            "name": "Global Warming",
                            "type": "sequential",
                            "category": "Uber",
                            "colors": ["#4C0035", "#880030", "#B72F15", "#D6610A", "#EF9100", "#FFC300"]
                        },
                        "radiusRange": [0, 50],
                        "filled": True,
                        "billboard": False,
                        "allowHover": True,
                        "showNeighborOnHover": False,
                        "showHighlightColor": True
                    },
                    "hidden": False,
                    "textLabel": [{
                        "field": None,
                        "color": [255, 255, 255],
                        "size": 18,
                        "offset": [0, 0],
                        "anchor": "start",
                        "alignment": "center",
                        "outlineWidth": 0,
                        "outlineColor": [255, 0, 0, 255],
                        "background": False,
                        "backgroundColor": [0, 0, 200, 255]
                    }]
                },
                "visualChannels": {
                    "colorField": {
                        "name": "County Code",
                        "type": "real"
                    },
                    "colorScale": "quantile",
                    "strokeColorField": None,
                    "strokeColorScale": "quantile",
                    "sizeField": None,
                    "sizeScale": "linear"
                }
            }],
            "effects": [],
            "interactionConfig": {
                "tooltip": {
                    "fieldsToShow": {
                        "obligor_data": [
                            {"name": "Obligor Name", "format": None},
                            {"name": "County Code", "format": None},
                            {"name": "County", "format": None},
                            {"name": "State", "format": None}
                        ]
                    },
                    "compareMode": False,
                    "compareType": "absolute",
                    "enabled": True
                },
                "brush": {
                    "size": 0.5,
                    "enabled": False
                },
                "geocoder": {
                    "enabled": False
                },
                "coordinate": {
                    "enabled": False
                }
            },
            "layerBlending": "normal",
            "overlayBlending": "normal",
            "splitMaps": [],
            "animationConfig": {
                "currentTime": None,
                "speed": 1
            },
            "editor": {
                "features": [],
                "visible": True
            }
        },
        "mapState": {
            "bearing": 0,
            "dragRotate": False,
            "latitude": 46.271014210208314,
            "longitude": -113.70156439667934,
            "pitch": 0,
            "zoom": 2.75877838326137,
            "isSplit": False,
            "isViewportSynced": True,
            "isZoomLocked": False,
            "splitMapViewports": []
        },
        "mapStyle": {
            "styleType": "positron",
            "topLayerGroups": {},
            "visibleLayerGroups": {
                "label": True,
                "road": True,
                "border": False,
                "building": True,
                "water": True,
                "land": True,
                "3d building": False
            },
            "threeDBuildingColor": [232.7874787737094, 232.7874787737094, 230.92517894351974],
            "backgroundColor": [0, 0, 0],
            "mapStyles": {}
        },
        "uiState": {
            "mapControls": {
                "mapLegend": {
                    "active": False
                }
            }
        }
    }
}

def create_kepler_map(df):
    """
    Creates a Kepler.gl map with the provided configuration
    
    Args:
        df (pd.DataFrame): DataFrame containing obligor data
        
    Returns:
        str: HTML string of the Kepler.gl map
    """
    # Create a Kepler.gl map
    map_obj = KeplerGl(config=KEPLER_CONFIG, height=700)
    
    # Add data to the map
    map_obj.add_data(df, 'obligor_data')
    
    # Save to HTML
    html = map_obj._repr_html_()
    return html

def create_state_exposure(df):
    state_exposure = df.groupby('State')['Par'].sum().reset_index()
    fig = px.choropleth(state_exposure,
                        locations='State',
                        locationmode='USA-states',
                        color='Par',
                        scope='usa',
                        title='Exposure by U.S. State',
                        color_continuous_scale='Blues')
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    return fig

def create_sector_distribution(df):
    sector_dist = df.groupby('Sector')['Par'].sum().reset_index()
    fig = px.pie(sector_dist, names='Sector', values='Par', 
                 title='Portfolio Distribution by Sector')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_credit_risk(df):
    rating_dist = df['Rating_Bucket'].value_counts().reset_index()
    rating_dist.columns = ['Rating_Bucket', 'Count']
    fig = px.bar(rating_dist, x='Rating_Bucket', y='Count',
                 title='Credit Risk Distribution',
                 labels={'Rating_Bucket': 'Rating Bucket', 'Count': 'Count'})
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    return fig

def create_rating_coverage(df):
    rated_counts = df[df['Rating_Bucket'] != 'Unrated']['Rating_Bucket'].count()
    unrated_counts = len(df) - rated_counts
    fig = go.Figure(go.Pie(
        labels=['Rated', 'Unrated'],
        values=[rated_counts, unrated_counts],
        title='Rating Coverage',
        hole=0.4
    ))
    return fig

def create_outlook_distribution(df):
    outlook_dist = df['Outlook'].value_counts().reset_index()
    outlook_dist.columns = ['Outlook', 'Count']
    fig = px.bar(outlook_dist, x='Outlook', y='Count',
                 title='Outlook Distribution',
                 labels={'Outlook': 'Outlook', 'Count': 'Count'})
    return fig

def create_top_obligors(df):
    top_obligors = df.groupby('Obligor Name')['Par'].sum().nlargest(10).reset_index()
    fig = px.bar(top_obligors, x='Par', y='Obligor Name', orientation='h',
                 title='Top 10 Obligors by Par Value',
                 labels={'Obligor Name': 'Obligor', 'Par': 'Par Amount'})
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig

def create_maturity_profile(df):
    maturity_dist = df.groupby('Maturity_Bucket')['Par'].sum().reset_index()
    fig = px.bar(maturity_dist, x='Maturity_Bucket', y='Par',
                 title='Maturity Profile',
                 labels={'Maturity_Bucket': 'Years to Maturity', 'Par': 'Par Amount'})
    return fig

def create_jump_risk(df):
    jump_risk = df[(df['Rating_Bucket'] == 'BBB') & 
                   (df['Outlook'] == 'Negative')]
    return jump_risk[['Obligor Name', 'Rating', 'Outlook', 'Par', 'Sector', 'State']]