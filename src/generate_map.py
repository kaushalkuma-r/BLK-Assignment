import folium
from folium.plugins import MarkerCluster, HeatMap
import pandas as pd

def generate_obligor_map(df):
    """
    Generates a folium map with marker clusters, multiple basemaps, and heatmap overlay.

    Args:
        location_data_unique (pd.DataFrame): DataFrame with columns:
            - 'Obligor Name', 'County', 'State', 'ZIP', 'Latitude', 'Longitude'

    Returns:
        folium.Map: Interactive map object with larger size
    """

    # Create base map with larger dimensions
    m = folium.Map(
        location=[39.8283, -98.5795],
        zoom_start=4,
        tiles=None,
        width='100%',      # full width
        height='700px'     # increased height
    )

    # Add basemap tile layers with attribution
    tile_layers = [
        {
            "name": "CartoDB Light",
            "tiles": "https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png",
            "attr": "©OpenStreetMap, ©CartoDB"
        }
    ]

    for tile in tile_layers:
        folium.TileLayer(tiles=tile["tiles"], name=tile["name"], attr=tile["attr"]).add_to(m)

    # Marker Cluster Layer
    marker_group = folium.FeatureGroup(name="Obligor Markers").add_to(m)
    marker_cluster = MarkerCluster().add_to(marker_group)

    for _, row in df.iterrows():
        if pd.isna(row['Latitude']) or pd.isna(row['Longitude']):
            continue  # skip incomplete coordinates

        popup_html = f"""
        <b>{row['Obligor Name']}</b><br>
        County: {row['County']}<br>
        State: {row['State']}<br>
        ZIP: {row['ZIP']}<br>
        Sector: {row['Sector']}<br>
        """
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row['Obligor Name']
        ).add_to(marker_cluster)

    # Heatmap layer
    heat_data = df[['Latitude', 'Longitude']].dropna().values.tolist()
    heatmap_layer = folium.FeatureGroup(name="Heat Map")
    HeatMap(heat_data, radius=15, blur=10).add_to(heatmap_layer)
    heatmap_layer.add_to(m)

    # Layer control
    folium.LayerControl(collapsed=False).add_to(m)

    return m
