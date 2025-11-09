import streamlit as st


def button_clear_cache():
    with st.sidebar:
        if st.button("Clear Cache"):
            st.cache_data.clear()
            st.rerun()
