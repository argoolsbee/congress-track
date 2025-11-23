# Page Title: Geographic Distribution
import altair as alt
import pandas as pd
import streamlit as st
from components import button_clear_cache


@st.cache_data
def get_legislator_data():
    df = pd.read_parquet("load/legislators_current.parquet")
    return df


def geographic_distribution_page():
    button_clear_cache.button_clear_cache()

    df_legislators = get_legislator_data()

    st.title("Geographic Distribution")

    # Overall statistics by state
    st.header("Legislators by State")

    state_counts = (
        df_legislators.groupby("state_name")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    st.dataframe(
        data=state_counts,
        hide_index=True,
        column_config={
            "state_name": "State",
            "count": "Number of Legislators",
        },
    )

    # Party distribution by state
    st.header("Party Distribution by State")

    state_party = df_legislators.groupby(["state_name", "party"]).size().reset_index(name="count")

    chart = (
        alt.Chart(state_party)
        .mark_bar()
        .encode(
            y=alt.Y("state_name:N", title="State", sort="-x"),
            x=alt.X("count:Q", title="Number of Legislators"),
            color=alt.Color("party:N", title="Party"),
        )
        .properties(height=800)
    )

    st.altair_chart(chart, use_container_width=True)

    # Chamber distribution by state
    st.header("Chamber Distribution by State")

    chamber_filter = st.selectbox(
        label="Analyze by Chamber",
        options=sorted(df_legislators["chamber_name"].unique().tolist()),
    )

    df_chamber = df_legislators[df_legislators["chamber_name"] == chamber_filter]

    state_chamber = (
        df_chamber.groupby("state_name")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    chart_chamber = (
        alt.Chart(state_chamber)
        .mark_bar()
        .encode(
            x=alt.X("state_name:N", title="State", sort="-y"),
            y=alt.Y("count:Q", title="Number of Legislators"),
            color=alt.value("#4472C4"),
        )
        .properties(height=400)
    )

    st.altair_chart(chart_chamber, use_container_width=True)

    # Party representation statistics
    st.header("Party Representation Statistics")

    col1, col2, col3 = st.columns(3)
    parties = df_legislators["party"].unique()

    for idx, party in enumerate(sorted(parties)):
        party_data = df_legislators[df_legislators["party"] == party]
        col = [col1, col2, col3][idx % 3]

        with col:
            st.metric(
                label=party,
                value=len(party_data),
                delta=f"{len(party_data.groupby('state_name'))} states",
            )

    # Regional comparison
    st.header("Legislators by State and Party")

    state_party_pivot = state_party.pivot(
        index="state_name", columns="party", values="count"
    ).fillna(0)

    st.dataframe(
        data=state_party_pivot.astype(int),
        column_config={
            col: st.column_config.NumberColumn(format="%d") for col in state_party_pivot.columns
        },
    )


if __name__ == "__main__":
    geographic_distribution_page()
