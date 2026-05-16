"""Session state management utilities."""

import streamlit as st


def initialize_session_state():
    """Initialize all session state variables."""
    defaults = {
        "messages": [],
        "selected_degree": "",
        "selected_branch": "",
        "selected_year": "",
        "selected_semester": "",
        "selected_language": "english",
        "show_practice": False,
        "user": None,
        "reset_token_sent": False,
        "show_create_post": False,
        "viewing_post_id": None,
        "forum_page": 1
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
