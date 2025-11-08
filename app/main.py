import pandas as pd
import streamlit as st

from components import button_clear_cache

@st.cache_data
def get_house_data():
    df = pd.read_parquet("load/house_legislators_current.parquet")
    return df

@st.cache_data
def get_senate_data():
    df = pd.read_parquet("load/senate_legislators_current.parquet")
    return df

def main():
    button_clear_cache.button_clear_cache()

    st.title("Congress Track")

if __name__ == "__main__":
    main()