import pandas as pd
import pydeck as pdk
import streamlit as st


def render_office_map(
    df_offices: pd.DataFrame,
    zoom: int = 2,
    size_scale: int = 5,
) -> None:
    """
    Render an interactive map of office locations using pydeck.

    Args:
        df_offices: DataFrame with latitude, longitude columns
        zoom: Initial zoom level (default 2 for full US, use 8 for state-level)
        size_scale: Size scale for icons (default 5)
    """
    if df_offices.empty:
        st.warning("No offices to display on map")
        return

    # Create a copy to avoid modifying the original
    df = df_offices.copy()

    # Icon data for markers
    icon_data = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/88/Map_marker.svg",
        "width": 512,
        "height": 786,
        "anchorY": 786,
    }
    df["icon_data"] = [icon_data] * len(df)

    # Calculate center of map
    latitude = df["latitude"].mean() if not df.empty else 39.833333
    longitude = df["longitude"].mean() if not df.empty else -98.583333

    st.pydeck_chart(
        pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=latitude,
                longitude=longitude,
                zoom=zoom,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    "IconLayer",
                    data=df,
                    get_icon="icon_data",
                    get_position=["longitude", "latitude"],
                    get_size=4,
                    size_scale=size_scale,
                    pickable=True,
                    auto_highlight=True,
                ),
            ],
            tooltip={"text": "{address}\n{city}, {state} {zip}"},  # pyright: ignore[reportArgumentType]
        ),
        height=600,
    )
