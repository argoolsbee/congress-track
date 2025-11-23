import streamlit as st
from components import button_clear_cache
from pages.analysis import age_demographics, geographic_distribution, social_media, term_length
from pages.explore import district_map, legislator

# Set page config
st.set_page_config(
    page_title="Congress Track",
    page_icon=":material/account_balance:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={"About": "# Congress Track\n Answer questions about U.S. Congress members."},
)


def home():
    button_clear_cache.button_clear_cache()

    st.title("🏛️ Congress Track")
    st.markdown("---")

    st.markdown("""
    ## Welcome to Congress Track
        
    ### Explore:
    - **Legislator Lookup**: Search and view detailed information about Congress members
    - **District Map**: Visualize district offices across the United States
    
    ### Analysis:
    - **Age & Demographics**: Analyze legislator age distribution, gender representation, 
                and demographic trends
    - **Geographic Distribution**: Explore party representation and legislator density by 
                state and region
    - **Social Media**: Track social media presence and platform adoption across Congress
    - **Term Length**: Analyze the service history and tenure of House and Senate members

    """)

    st.markdown("---")
    st.subheader("Fun Facts")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("House Representatives", "435", help="House of Representatives members")
        st.metric("Years of Congress", "234", help="Years since 1789")
    with col2:
        st.metric("Senators", "100", help="U.S. Senate members")
        st.metric(
            "Longest Speech",
            "25 hours, 5 minutes",
            help="Longest filibuster in Senate history delievered by Cory Booker in 2025",
        )
    with col3:
        st.metric("Committees", "48", help="Committees across Congress")
        st.metric("Capitol Dome Weight", "4,100 tons", help="9.1 million pounds")


# Define pages
home_page = st.Page(home, title="Home", icon=":material/home:", default=True)
legislator_page = st.Page(
    legislator.legislator_page, title="Legislator Lookup", icon=":material/person:"
)
district_map_page = st.Page(
    district_map.district_map_page, title="District Map", icon=":material/map:"
)

age_demographics_page = st.Page(
    age_demographics.age_demographics_page, title="Age & Demographics", icon=":material/demography:"
)
geographic_distribution_page = st.Page(
    geographic_distribution.geographic_distribution_page,
    title="Geographic Distribution",
    icon=":material/globe:",
)
social_media_analysis_page = st.Page(
    social_media.social_media_page, title="Social Media", icon=":material/public:"
)
term_length_page = st.Page(
    term_length.term_length_page, title="Term Length", icon=":material/measuring_tape:"
)

# Group pages into sections (2-level navigation)
pages = {
    "Main": [home_page],
    "Explore": [legislator_page, district_map_page],
    "Analysis": [
        age_demographics_page,
        geographic_distribution_page,
        social_media_analysis_page,
        term_length_page,
    ],
}

# Render navigation and execute page
pg = st.navigation(pages)
pg.run()
