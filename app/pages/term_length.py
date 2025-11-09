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


def term_length_page():
    button_clear_cache.button_clear_cache()

    df_house = get_house_data()
    df_senate = get_senate_data()

    age_filter = st.slider(label="Years", min_value=0, max_value=100, value=18)

    filtered_house = df_house[df_house["years_served"] >= age_filter]
    filtered_senate = df_senate[df_senate["years_served"] >= age_filter]

    st.title("House of Representatives Members")
    st.dataframe(filtered_house)

    st.title("Senate Members")
    st.dataframe(filtered_senate)

    # Group house by years_served and party
    years_party_counts = (
        df_house.groupby(["years_served", "party"]).size().reset_index(name="count")
    )
    st.subheader("House Members by Years Served and Party")
    st.dataframe(years_party_counts)

    st.bar_chart(
        data=years_party_counts,
        x="years_served",
        y="count",
        stack=True,
        color="party",
    )


if __name__ == "__main__":
    term_length_page()
