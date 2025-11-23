import altair as alt
import pandas as pd
import streamlit as st
from components import button_clear_cache


@st.cache_data
def get_legislator_data():
    df = pd.read_parquet("load/legislators_current.parquet")
    return df


def age_demographics_page():
    button_clear_cache.button_clear_cache()

    df_legislators = get_legislator_data()

    st.title("Age & Demographics")

    # Overall age statistics
    st.header("Age Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Average Age", value=f"{df_legislators['age'].mean():.1f} years")

    with col2:
        st.metric(label="Median Age", value=f"{df_legislators['age'].median():.0f} years")

    with col3:
        st.metric(label="Youngest", value=f"{df_legislators['age'].min():.0f} years")

    with col4:
        st.metric(label="Oldest", value=f"{df_legislators['age'].max():.0f} years")

    # Age distribution
    st.header("Age Distribution")

    age_hist = (
        alt.Chart(df_legislators)
        .mark_bar()
        .encode(
            x=alt.X("age:Q", bin=alt.Bin(step=5), title="Age (years)"),
            y=alt.Y("count()", title="Number of Legislators"),
            color=alt.value("#4472C4"),
        )
        .properties(height=400)
    )

    st.altair_chart(age_hist, use_container_width=True)

    # Age by party
    st.header("Age by Party")

    party_age_stats = (
        df_legislators.groupby("party")
        .agg(
            {
                "age": ["mean", "median", "min", "max"],
            }
        )
        .round(1)
        .reset_index()
    )
    party_age_stats.columns = ["Party", "Average Age", "Median Age", "Youngest", "Oldest"]

    st.dataframe(
        data=party_age_stats,
        hide_index=True,
        column_config={
            "Party": "Party",
            "Average Age": st.column_config.NumberColumn(format="%.1f"),
            "Median Age": st.column_config.NumberColumn(format="%.0f"),
            "Youngest": st.column_config.NumberColumn(format="%.0f"),
            "Oldest": st.column_config.NumberColumn(format="%.0f"),
        },
    )

    # Age distribution by party (box plot style)
    age_party_chart = (
        alt.Chart(df_legislators)
        .mark_boxplot()
        .encode(
            x=alt.X("party:N", title="Party"),
            y=alt.Y("age:Q", title="Age (years)"),
            color=alt.Color("party:N", title="Party"),
        )
        .properties(height=400)
    )

    st.altair_chart(age_party_chart, use_container_width=True)

    # Age by chamber
    st.header("Age by Chamber")

    chamber_age_stats = (
        df_legislators.groupby("chamber_name")
        .agg(
            {
                "age": ["mean", "median", "min", "max"],
            }
        )
        .round(1)
        .reset_index()
    )
    chamber_age_stats.columns = [
        "Chamber",
        "Average Age",
        "Median Age",
        "Youngest",
        "Oldest",
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Age Statistics by Chamber")
        st.dataframe(
            data=chamber_age_stats,
            hide_index=True,
            column_config={
                "Chamber": "Chamber",
                "Average Age": st.column_config.NumberColumn(format="%.1f"),
                "Median Age": st.column_config.NumberColumn(format="%.0f"),
                "Youngest": st.column_config.NumberColumn(format="%.0f"),
                "Oldest": st.column_config.NumberColumn(format="%.0f"),
            },
        )

    with col2:
        age_chamber_chart = (
            alt.Chart(df_legislators)
            .mark_boxplot()
            .encode(
                x=alt.X("chamber_name:N", title="Chamber"),
                y=alt.Y("age:Q", title="Age (years)"),
                color=alt.Color("chamber_name:N", title="Chamber"),
            )
            .properties(height=400)
        )

        st.altair_chart(age_chamber_chart, use_container_width=True)

    # Gender distribution
    st.header("Gender Distribution")

    gender_counts = df_legislators.groupby("gender").size().reset_index(name="count")

    gender_pie = (
        alt.Chart(gender_counts)
        .mark_arc()
        .encode(
            theta=alt.Theta("count:Q"),
            color=alt.Color("gender:N", title="Gender"),
            tooltip=["gender:N", "count:Q"],
        )
        .properties(height=400)
    )

    col1, col2 = st.columns(2)

    with col1:
        st.altair_chart(gender_pie, use_container_width=True)

    with col2:
        st.dataframe(
            data=gender_counts,
            hide_index=True,
            column_config={
                "gender": "Gender",
                "count": "Count",
            },
        )

    # Gender by party
    st.header("Gender Distribution by Party")

    gender_party = df_legislators.groupby(["party", "gender"]).size().reset_index(name="count")

    gender_party_chart = (
        alt.Chart(gender_party)
        .mark_bar()
        .encode(
            x=alt.X("party:N", title="Party"),
            y=alt.Y("count:Q", title="Count"),
            color=alt.Color("gender:N", title="Gender"),
        )
        .properties(height=400)
    )

    st.altair_chart(gender_party_chart, use_container_width=True)

    # Age groups analysis
    st.header("Legislators by Age Group")

    def age_group(age):
        if age < 40:
            return "Under 40"
        elif age < 50:
            return "40-49"
        elif age < 60:
            return "50-59"
        elif age < 70:
            return "60-69"
        else:
            return "70+"

    df_legislators["age_group"] = df_legislators["age"].apply(age_group)

    age_group_party = (
        df_legislators.groupby(["age_group", "party"]).size().reset_index(name="count")
    )

    # Define age group order
    age_group_order = ["Under 40", "40-49", "50-59", "60-69", "70+"]
    age_group_party["age_group"] = pd.Categorical(
        age_group_party["age_group"], categories=age_group_order, ordered=True
    )
    age_group_party = age_group_party.sort_values("age_group")

    age_group_chart = (
        alt.Chart(age_group_party)
        .mark_bar()
        .encode(
            x=alt.X("age_group:N", title="Age Group", sort=age_group_order),
            y=alt.Y("count:Q", title="Count"),
            color=alt.Color("party:N", title="Party"),
        )
        .properties(height=400)
    )

    st.altair_chart(age_group_chart, use_container_width=True)


if __name__ == "__main__":
    age_demographics_page()
