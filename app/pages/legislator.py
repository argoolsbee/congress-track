import pandas as pd
import streamlit as st

from components import button_clear_cache

@st.cache_data
def get_legislator_data():
    df = pd.read_parquet("load/legislators_current.parquet")
    return df

def legislator_page():

    button_clear_cache.button_clear_cache()

    df_legislators = get_legislator_data()

    st.title("Congress Members")

    filter_cols = st.columns(spec = 2)
    with filter_cols[0]:
        state_filter = st.selectbox(label = "State",
                                    options = sorted(df_legislators['state'].unique().tolist())
                                   )
    df_filtered_state = df_legislators[df_legislators['state'] == state_filter]
    with filter_cols[1]:
        name_filter = st.selectbox(label = "Name",
                                   options = sorted(df_filtered_state['official_full_name'].tolist())
                                )
    
    df = df_legislators[df_legislators['official_full_name'] == name_filter]

    st.title(df['display_name'].values[0])

    if df['nickname'].values[0]:
        st.caption(df['nickname'].values[0])

    st.header(df['type'].values[0])

    data_cols = st.columns(spec = 3)

    with data_cols[0]:
        st.metric(label = "State", value = df['state'].values[0])
        st.metric(label = "Age", value = df['age'])
        st.metric(label = "Years Served", value = df['years_served'])

    with data_cols[1]:
        st.metric(label = "Party", value = df['party'].values[0])
        st.metric(label = "Age at First Term Start", value = df['age_first_term_start'])
        st.metric(label = "Years Elected", value = df['years_elected'])

    with data_cols[2]:
        st.metric(label = "Term Count", value = df['term_count'])
        st.metric(label = "Age at Last Term End", value = df['age_last_term_end'])
        st.metric(label = "Years Remaining", value = df['years_remaining'])



if __name__ == "__main__":
    legislator_page()