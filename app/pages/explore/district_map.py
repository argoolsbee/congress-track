import pandas as pd
import streamlit as st
from components import button_clear_cache
from components.map_utils import render_office_map


@st.cache_data
def get_office_data():
    df = pd.read_parquet("load/district_offices.parquet")
    return df


def district_map_page():
    button_clear_cache.button_clear_cache()

    df_offices = get_office_data()

    st.title("District Map")

    render_office_map(df_offices, zoom=2, size_scale=5)

    st.space()
    with st.expander(label="Raw Data", expanded=False):
        st.dataframe(data=df_offices)


if __name__ == "__main__":
    district_map_page()
