import pandas as pd
import streamlit as st
from components import button_clear_cache


@st.cache_data
def get_legislator_data():
    df = pd.read_parquet("load/legislators_current.parquet")
    return df


@st.cache_data
def get_term_data():
    df = pd.read_parquet("load/terms_current.parquet")
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

    header_cols = st.columns(spec = 3)

    with header_cols[0]:
        st.title(df["display_name"].values[0])

        if df["nickname"].values[0]:
            st.caption(df["nickname"].values[0])

    with header_cols[1]:
        st.page_link(
            page=f"https://ballotpedia.org/{df['ballotpedia_id'].values[0]}", label="Ballotpedia"
        )
        
        st.page_link(
            page=f"https://bioguide.congress.gov/search/bio/{df['bioguide_id'].values[0]}", label="Bioguide"
        )

        # st.page_link(
        #     page=f"https://www.cspan.org/person/?{df['cspan_id'].values[0]}", label="C-SPAN"
        # )

        trimmed = df['google_entity_id'].values[0].split(":", 1)[-1]
        st.page_link(
            page=f"https://www.google.com/search?kgmid={trimmed}", label="Google Knowledge Graph"
        )

        st.page_link(
            page=f"https://www.govtrack.us/congress/members/{df['govtrack_id'].values[0]}", label="GovTrack"
        )

        # st.page_link(
        #     page=f"https://history.house.gov/People/Detail/{df['house_history_id'].values[0]}", label="House History"
        # )

        # st.page_link(
        #     page=f"https://icpsr.umich.edu/web/ICPSR/studies/{df['icpsr_id'].values[0]}", label="ICPSR"
        # )

        # st.page_link(
        #     page=f"https://maplight.org/us-congress/legislator/{df['maplight_id'].values[0]}", label="MapLight"
        # )

    with header_cols[2]:
        # st.page_link(
        #     page=f"https://www.opensecrets.org/members-of-congress/{df['opensecrets_id'].values[0]}", label="OpenSecrets"
        # )

        # st.page_link(
        #     page=f"https://www.pictoraldirectory.com/house/{df['pictorial_id'].values[0]}", label="Pictorial Directory"
        # )

        # st.page_link(
        #     page=f"https://www.congress.gov/member/{df['thomas_id'].values[0]}", label="Congress.gov"
        # )

        # st.page_link(
        #     page=f"https://justfacts.votesmart.org/candidate/{df['votesmart_id'].values[0]}", label="VoteSmart"
        # )

        st.page_link(
            page=f"https://www.wikidata.org/wiki/{df['wikidata_id'].values[0]}", label="Wikidata"
        )

        st.page_link(
            page=f"https://www.wikipedia.org/wiki/{df['wikipedia_id'].values[0]}", label="Wikipedia"
        )

    st.header(df["chamber_name"].values[0])

    data_cols = st.columns(spec=3)

    with data_cols[0]:
        st.metric(label="State", value=df["state_name"].values[0])
        st.metric(label="Age", value=df["age"])
        st.metric(label="Years Served", value=df["years_served"])

    with data_cols[1]:
        st.metric(label="Party", value=df["party"].values[0])
        st.metric(label="Age at First Term Start", value=df["age_first_term_start"])
        st.metric(label="Years Elected", value=df["years_elected"])

    with data_cols[2]:
        st.metric(label="Term Count", value=df["term_count"])
        st.metric(label="Age at Last Term End", value=df["age_last_term_end"])
        st.metric(label="Years Remaining", value=df["years_remaining"])

    df_terms = get_term_data()
    df_terms = df_terms[df_terms["dlt_parent_id"] == name_filter]
    st.dataframe(
        data=df_terms[["start_date", "end_date", "chamber_name", "state", "party"]], hide_index=True
    )

    with st.expander(label="Raw Data", expanded=False):
        st.dataframe(data=df_legislators)


if __name__ == "__main__":
    legislator_page()
