import altair as alt
import pandas as pd
import streamlit as st
from components import button_clear_cache


@st.cache_data
def get_legislator_data():
    df = pd.read_parquet("load/legislators_current.parquet")
    return df


def social_media_page():
    button_clear_cache.button_clear_cache()

    df_legislators = get_legislator_data()

    st.title("Social Media Presence")

    # Social media platforms
    social_media_platforms = {
        "Facebook": "facebook_url",
        "Instagram": "instagram_url",
        "Mastodon": "mastodon_url",
        "Twitter": "twitter_url",
        "YouTube": "youtube_url",
    }

    # Calculate overall statistics
    st.header("Overall Statistics")
    stats_cols = st.columns(len(social_media_platforms))

    for idx, (platform, column) in enumerate(social_media_platforms.items()):
        with stats_cols[idx]:
            count = df_legislators[column].notna().sum()
            percentage = (count / len(df_legislators)) * 100
            st.metric(label=platform, value=f"{count} ({percentage:.1f}%)")

    # Breakdown by chamber
    st.header("Social Media Presence by Chamber")

    chamber_filter = st.selectbox(
        label="Chamber",
        options=sorted(df_legislators["chamber_name"].unique().tolist()),
    )

    df_chamber = df_legislators[df_legislators["chamber_name"] == chamber_filter]

    chamber_stats = {}
    for platform, column in social_media_platforms.items():
        count = df_chamber[column].notna().sum()
        percentage = (count / len(df_chamber)) * 100
        chamber_stats[platform] = {"count": count, "percentage": percentage}

    chamber_df = pd.DataFrame(chamber_stats).T
    st.bar_chart(chamber_df["percentage"])

    st.dataframe(
        data=chamber_df.round(2),
        column_config={
            "count": "Count",
            "percentage": st.column_config.NumberColumn("Percentage (%)", format="%.2f"),
        },
    )

    # Breakdown by party
    st.header("Social Media Presence by Party")

    party_breakdown = {}
    for platform, column in social_media_platforms.items():
        party_stats = (
            df_legislators.groupby("party")[column]
            .apply(lambda x: x.notna().sum())
            .reset_index(name=platform)
        )
        party_breakdown[platform] = party_stats

    # Combine all platforms into a single dataframe
    combined_df = party_breakdown[list(social_media_platforms.keys())[0]].copy()
    for platform in list(social_media_platforms.keys())[1:]:
        combined_df = combined_df.merge(party_breakdown[platform], on="party", how="left")

    # Melt dataframe for Altair (long format)
    melted_df = combined_df.melt(id_vars=["party"], var_name="platform", value_name="count")

    # Define platform brand colors
    platform_colors = {
        "Facebook": "#004daa",
        "Instagram": "#E4405F",
        "Mastodon": "#563acc",
        "Twitter": "#31a4f1",
        "YouTube": "#FF0033",
    }

    # Create grouped bar chart with brand colors
    chart = (
        alt.Chart(melted_df)
        .mark_bar()
        .encode(
            x=alt.X("party:N", title="Party"),
            y=alt.Y("count:Q", title="Count"),
            color=alt.Color(
                "platform:N",
                title="Platform",
                scale=alt.Scale(
                    domain=list(platform_colors.keys()), range=list(platform_colors.values())
                ),
            ),
            xOffset="platform:N",
            tooltip=["party:N", "platform:N", "count:Q"],
        )
        .properties(height=400, width=600)
    )

    st.altair_chart(chart, use_container_width=True)

    # Legislators with no social media
    st.header("Legislators Without Social Media")

    no_social_media = df_legislators[
        df_legislators[[col for col in social_media_platforms.values()]].isna().all(axis=1)
    ]

    st.dataframe(
        data=no_social_media[["official_full_name", "chamber_name", "state_name", "party"]],
        hide_index=True,
        column_config={
            "official_full_name": "Name",
            "chamber_name": "Chamber",
            "state_name": "State",
            "party": "Party",
        },
    )

    # Legislators with all social media platforms
    st.header("Legislators With All Social Media Platforms")

    all_social_media = df_legislators[
        df_legislators[[col for col in social_media_platforms.values()]].notna().all(axis=1)
    ]

    st.dataframe(
        data=all_social_media[["official_full_name", "chamber_name", "state_name", "party"]],
        hide_index=True,
        column_config={
            "official_full_name": "Name",
            "chamber_name": "Chamber",
            "state_name": "State",
            "party": "Party",
        },
    )


if __name__ == "__main__":
    social_media_page()
