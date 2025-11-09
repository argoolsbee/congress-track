import pandas as pd
import streamlit as st
from components import button_clear_cache

def main():
    st.set_page_config(
        page_title="Congress Track",
        page_icon=":material/account_balance:",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            # 'Get Help': 'https://',
            # 'Report a bug': "https://",
            'About': "# Congress Track\n Answer questions about U.S. Congress members."
        }
    )
    
    button_clear_cache.button_clear_cache()

    st.title("Congress Track")


if __name__ == "__main__":
    main()
