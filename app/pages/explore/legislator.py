# Page Title: Legislator Lookup
import webbrowser

import pandas as pd
import streamlit as st
from components import button_clear_cache
from components.map_utils import render_office_map


@st.cache_data
def get_legislator_data():
    df = pd.read_parquet("load/legislators_current.parquet")
    return df


@st.cache_data
def get_term_data():
    df = pd.read_parquet("load/terms_current.parquet")
    return df


@st.cache_data
def get_office_data():
    df = pd.read_parquet("load/district_offices.parquet")
    return df


def legislator_page():
    button_clear_cache.button_clear_cache()

    df_legislators = get_legislator_data()

    st.title("Congress Members")

    filter_cols = st.columns(spec=2)

    with filter_cols[0]:
        state_filter = st.selectbox(
            label="State", options=sorted(df_legislators["state_name"].unique().tolist())
        )

    with filter_cols[1]:
        # Name selectbox filtered by state, displays official full name, returns dlt_id
        df_filtered_state = df_legislators[df_legislators["state_name"] == state_filter]
        name_filter = st.selectbox(
            label="Name",
            options=sorted(df_filtered_state["dlt_id"].tolist()),
            format_func=(
                lambda x: df_filtered_state[df_filtered_state["dlt_id"] == x][
                    "official_full_name"
                ].values[0]
            ),
        )

    df = df_legislators[df_legislators["dlt_id"] == name_filter]

    header_cols = st.columns(spec=[0.8, 0.1, 0.1])

    with header_cols[0]:
        st.title(df["display_name"].values[0])

        if df["nickname"].values[0]:
            st.caption(df["nickname"].values[0])

        st.image(
            image=df["image_url"].values[0],
            # caption=df["image_attribution_text"].values[0],
            width=175,
        )

    with header_cols[1]:
        st.write("**Social Media**")

        # Social media links
        social_media = {
            "Facebook": ("facebook_url",),
            "Instagram": ("instagram_url",),
            "Mastodon": ("mastodon_url",),
            "Twitter": ("twitter_url",),
            "YouTube": ("youtube_url",),
        }

        for label, (url_key,) in social_media.items():
            url_value = df[url_key].values[0]
            if url_value and st.button(
                label=label,
                key=f"social_{label}",
                use_container_width=True,
            ):
                webbrowser.open_new_tab(url_value)

    # External links
    links = {
        "Ballotpedia": "ballotpedia_url",
        "Bioguide": "bioguide_url",
        # 'C-SPAN': 'cspan_url',
        "Google": "google_knowledge_graph_url",
        "GovTrack": "govtrack_url",
        # 'House History': 'house_history_url',
        # 'ICPSR': 'icpsr_url',
        # 'MapLight': 'maplight_url',
        # 'OpenSecrets': 'opensecrets_url',
        # 'Pictorial Directory': 'pictorial_url',
        # 'Congress.gov': 'congress_gov_url',
        # 'VoteSmart': 'votesmart_url',
        "Wikidata": "wikidata_url",
        "Wikipedia": "wikipedia_url",
    }

    # Build available links for buttons
    with header_cols[2]:
        st.write("**External Links**")
        for label, url_key in links.items():
            url = df[url_key].values[0]
            if url and st.button(
                label=label,
                key=f"external_{label}",
                use_container_width=True,
            ):
                webbrowser.open_new_tab(url)

    st.header(df["chamber_name"].values[0])

    data_cols = st.columns(spec=3)

    with data_cols[0]:
        st.metric(label="State", value=df["state_name"].values[0])
        st.metric(label="Age", value=df["age"].values[0])
        st.metric(label="Years Served", value=df["years_served"].values[0])

    with data_cols[1]:
        st.metric(label="Party", value=df["party"].values[0])
        st.metric(label="Age at First Term Start", value=df["age_first_term_start"].values[0])
        st.metric(label="Years Elected", value=df["years_elected"].values[0])

    with data_cols[2]:
        st.metric(label="Term Count", value=df["term_count"].values[0])
        st.metric(label="Age at Last Term End", value=df["age_last_term_end"].values[0])
        st.metric(label="Years Remaining", value=df["years_remaining"].values[0])

    st.header("Terms")
    df_terms = get_term_data()
    df_terms = df_terms[df_terms["dlt_parent_id"] == name_filter]
    st.dataframe(
        data=df_terms[["start_date", "end_date", "chamber_name", "state", "party"]],
        hide_index=True,
        column_config={
            "start_date": "Start Date",
            "end_date": "End Date",
            "chamber_name": "Chamber",
            "state": "State",
            "party": "Party",
        },
    )

    st.header("District Offices")
    df_offices = get_office_data()
    df_offices = df_offices[df_offices["legislator_dlt_id"] == name_filter]

    st.dataframe(
        data=df_offices[["address", "city", "state", "zip", "phone", "fax", "hours", "building"]],
        hide_index=True,
        column_config={
            "address": "Address",
            "city": "City",
            "state": "State",
            "zip": "Zip Code",
            "phone": "Phone",
            "fax": "Fax",
            "hours": "Hours",
            "building": "Building",
        },
    )

    render_office_map(df_offices, zoom=8, size_scale=15)

    st.space()
    with st.expander(label="Raw Data", expanded=False):
        st.dataframe(data=df_legislators)


if __name__ == "__main__":
    legislator_page()
