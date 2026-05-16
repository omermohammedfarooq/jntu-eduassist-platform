"""Premium minimal theme for JNTU EduAssist."""

import streamlit as st


MODERN_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

/* Root variables */
:root {
    --bg-primary: #fafafa;
    --bg-secondary: #ffffff;
    --text-primary: #0a0a0a;
    --text-secondary: #666666;
    --text-muted: #999999;
    --border: #e0e0e0;
    --accent: #0a0a0a;
}

/* Global styles */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.mono {
    font-family: 'IBM Plex Mono', monospace !important;
}

/* Main app background */
.stApp {
    background-color: var(--bg-primary) !important;
}

/* Remove default padding */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1400px !important;
}

/* Headers */
h1, h2, h3 {
    font-weight: 500 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.5px !important;
}

h1 {
    font-size: 2.5rem !important;
    font-weight: 300 !important;
    letter-spacing: -1px !important;
}

/* Buttons */
.stButton > button {
    background-color: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0.6rem 1.5rem !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.9 !important;
    background-color: var(--accent) !important;
}

.stButton > button[kind="secondary"] {
    background-color: white !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
}

/* Text inputs */
.stTextInput > div > div > input {
    border-radius: 0 !important;
    border: none !important;
    border-bottom: 1px solid var(--border) !important;
    background-color: transparent !important;
    padding: 0.75rem 0 !important;
    font-size: 14px !important;
}

.stTextInput > div > div > input:focus {
    border-bottom-color: var(--accent) !important;
    box-shadow: none !important;
}

/* Select boxes */
.stSelectbox > div > div {
    border-radius: 0 !important;
    border: none !important;
    border-bottom: 1px solid var(--border) !important;
    background-color: transparent !important;
}

.stSelectbox [data-baseweb="select"] {
    border-radius: 0 !important;
}

/* Labels */
.stTextInput label, .stSelectbox label {
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    color: var(--text-secondary) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 0 !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    background-color: transparent !important;
    border-right: 1px solid var(--border) !important;
}

.stTabs [data-baseweb="tab"]:last-child {
    border-right: none !important;
}

.stTabs [aria-selected="true"] {
    background-color: var(--accent) !important;
    color: white !important;
}

/* Divider */
hr {
    margin: 2rem 0 !important;
    border: none !important;
    border-top: 1px solid var(--border) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

/* Remove Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Fix Expander - hide internal Streamlit keys */
.streamlit-expanderHeader {
    font-size: 14px !important;
    font-weight: 500 !important;
    border-radius: 0 !important;
}

/* Hide Streamlit's internal key labels in expanders */
.streamlit-expanderHeader p {
    margin: 0 !important;
}

.streamlit-expanderHeader svg {
    margin-right: 0.5rem !important;
}

/* Fix expander content spacing */
.streamlit-expanderContent {
    padding: 1rem !important;
}

/* Captions */
.stCaption {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    color: var(--text-muted) !important;
}

/* Success/Error messages */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 0 !important;
    border-left: 3px solid !important;
}

/* DataFrames */
.stDataFrame {
    border-radius: 0 !important;
}

[data-testid="stDataFrame"] {
    border-radius: 0 !important;
}
</style>
"""


def apply_theme():
    """Apply the premium minimal theme."""
    st.markdown(MODERN_THEME_CSS, unsafe_allow_html=True)
