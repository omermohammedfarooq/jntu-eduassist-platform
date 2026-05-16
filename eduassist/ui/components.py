"""Reusable UI components for the application."""

import streamlit as st
from typing import Dict, Tuple
from ..config.settings import Settings
from ..services.translation_service import (
    translate_text, get_available_languages, 
    LANGUAGE_NAMES, LANGUAGE_NATIVE
)


def render_top_bar():
    """Render the top navigation bar."""
    # Create columns for navbar layout
    col_left, col_spacer, col_right = st.columns([2, 3, 3])
    
    with col_left:
        # Logo and title - show home button only if not on home page
        current_page = st.session_state.get('current_page', 'home')
        
        if current_page != 'home':
            if st.button("← Home", key="nav_home_btn", help="Return to dashboard"):
                st.session_state.current_page = 'home'
                st.session_state.active_tab = None
                st.rerun()
        
        # Display logo and title
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 40px; height: 40px; background: #0a0a0a; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 16px;">JE</div>
                <span style="font-size: 16px; font-weight: 600; color: #0a0a0a; letter-spacing: -0.3px;">JNTU EduAssist</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col_right:
        # Right side controls
        c1, c2, c3, c4 = st.columns([2, 1, 1.2, 1.2])
        
        with c1:
            render_language_dropdown()
        with c2:
            # Theme toggle - Streamlit limitation: can't actually toggle themes
            st.markdown('<div style="text-align: center; padding: 8px;">☀️</div>', unsafe_allow_html=True)
        with c3:
            render_auth_buttons_login()
        with c4:
            render_auth_buttons_signup()
    
    st.divider()





def render_language_dropdown():
    """Render language selector with native names."""
    languages = list(LANGUAGE_NAMES.keys())
    current_lang = st.session_state.get('selected_language', 'english')
    
    # Display language options with native names
    display_names = {
        'english': 'English',
        'telugu': 'తెలుగు (Telugu)',
        'tenglish': 'Tenglish',
        'hinglish': 'Hinglish',
        'urdu': 'اردو (Urdu)'
    }
    
    selected = st.selectbox(
        "Language",
        options=languages,
        index=languages.index(current_lang) if current_lang in languages else 0,
        format_func=lambda x: display_names.get(x, x),
        key="lang_dropdown",
        label_visibility="collapsed"
    )
    
    if selected != current_lang:
        st.session_state.selected_language = selected
        st.rerun()


def render_auth_buttons_login():
    """Render login button."""
    user = st.session_state.get('user')
    
    if user:
        if st.button("Logout", key="top_logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        # Login button with secondary style (white background, border)
        if st.button("LOGIN", key="top_login", use_container_width=True, type="secondary"):
            st.session_state.show_auth_modal = "login"
            st.session_state.current_page = "auth"
            st.rerun()


def render_auth_buttons_signup():
    """Render signup button."""
    user = st.session_state.get('user')
    
    if user:
        st.write(f"👤 {user['full_name'][:12]}")
    else:
        # Sign Up button with primary style (black background)
        if st.button("SIGN UP", key="top_signup", use_container_width=True, type="primary"):
            st.session_state.show_auth_modal = "signup"
            st.session_state.current_page = "auth"
            st.rerun()


def render_auth_buttons():
    """Render login/signup buttons or welcome message."""
    user = st.session_state.get('user')
    
    if user:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"Welcome, **{user['full_name']}**")
        with col2:
            if st.button("Logout", key="top_logout_alt", use_container_width=True):
                st.session_state.user = None
                st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", key="top_login_alt", use_container_width=True):
                st.session_state.show_auth_modal = "login"
                st.session_state.current_page = "auth"
        with col2:
            if st.button("Sign Up", key="top_signup_alt", use_container_width=True):
                st.session_state.show_auth_modal = "signup"
                st.session_state.current_page = "auth"


def render_header():
    """Render the main application header."""
    lang = st.session_state.get('selected_language', 'english')
    title = translate_text("JNTU EduAssist AI", lang)
    subtitle = translate_text("Your Multilingual Educational Assistant for JNTU Students. Advanced AI-powered platform designed to provide instant answers, study materials, and comprehensive academic support.", lang)
    
    st.caption("EDUCATIONAL PLATFORM")
    st.title(title)
    st.write(subtitle)
    st.divider()


def render_language_selector() -> str:
    """Legacy language selector."""
    return st.session_state.get('selected_language', 'english')


def render_dashboard():
    """Render the dashboard with app cards."""
    lang = st.session_state.get('selected_language', 'english')
    user = st.session_state.get('user')
    
    st.subheader("📚 " + translate_text("Your Learning Dashboard", lang))
    
    # Service cards
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.caption("SERVICE 01")
            st.markdown(f"### {translate_text('Ask Questions', lang)}")
            st.write(translate_text("Get instant answers to your coursework with AI-powered assistance.", lang))
            if st.button(f"{translate_text('Open', lang)} →", key="open_ask", use_container_width=True):
                st.session_state.active_tab = "ask"
                st.rerun()
        
        with st.container(border=True):
            st.caption("SERVICE 03")
            st.markdown(f"### {translate_text('Practice Questions', lang)}")
            st.write(translate_text("Generate practice questions to test your knowledge.", lang))
            if st.button(f"{translate_text('Open', lang)} →", key="open_practice", use_container_width=True):
                st.session_state.active_tab = "practice"
                st.rerun()
    
    with col2:
        with st.container(border=True):
            st.caption("SERVICE 02 · NEW")
            st.markdown(f"### {translate_text('Check Results', lang)}")
            st.write(translate_text("Fetch your academic results directly from JNTUH servers.", lang))
            if st.button(f"{translate_text('Open', lang)} →", key="open_results", use_container_width=True):
                st.session_state.active_tab = "results"
                st.rerun()
        
        with st.container(border=True):
            st.caption("SERVICE 04 · LOGIN REQUIRED")
            st.markdown(f"### {translate_text('Discussion Forum', lang)}")
            st.write(translate_text("Connect with fellow students and teachers.", lang))
            if st.button(f"{translate_text('Open', lang)} →", key="open_forum", use_container_width=True):
                if not user:
                    st.session_state.show_auth_modal = "login"
                    st.session_state.current_page = "auth"
                else:
                    st.session_state.active_tab = "forum"
                st.rerun()


def get_icon_svg(icon_name: str) -> str:
    """Return icon character for app cards."""
    icons = {
        "chat_bubble": "Q",
        "assessment": "R",
        "quiz": "P",
        "forum": "F"
    }
    return icons.get(icon_name, "?")


def render_course_selector(
    degree_options: Dict,
    get_branch_options_fn,
    get_year_options_fn,
    get_semester_options_fn,
    courses: Dict
) -> Tuple[str, str, str, str, Dict]:
    """Render course selection UI."""
    lang = st.session_state.get('selected_language', 'english')
    
    st.subheader("🎓 " + translate_text("Course Selection", lang))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        selected_degree = st.selectbox(
            translate_text("Degree Type", lang),
            options=[""] + list(degree_options.keys()),
            format_func=lambda x: translate_text("Select Degree", lang) if x == "" else degree_options.get(x, x),
            key="degree_select"
        )
    
    branch_options = get_branch_options_fn(courses, selected_degree) if selected_degree else {}
    
    with col2:
        branch_keys = list(branch_options.keys())
        selected_branch = st.selectbox(
            translate_text("Branch", lang),
            options=[""] + branch_keys,
            format_func=lambda x: translate_text("Select Branch", lang) if x == "" else f"{branch_options.get(x, {}).get('abbreviation', x)} - {branch_options.get(x, {}).get('name', x)}",
            key="branch_select",
            disabled=not selected_degree
        )
    
    year_options = get_year_options_fn(courses, selected_degree, selected_branch) if selected_branch else {}
    
    with col3:
        selected_year = st.selectbox(
            translate_text("Year", lang),
            options=[""] + list(year_options.keys()),
            format_func=lambda x: translate_text("Select Year", lang) if x == "" else year_options.get(x, x),
            key="year_select",
            disabled=not selected_branch
        )
    
    semester_options = get_semester_options_fn(courses, selected_degree, selected_branch, selected_year) if selected_year else {}
    
    with col4:
        selected_semester = st.selectbox(
            translate_text("Semester", lang),
            options=[""] + list(semester_options.keys()),
            format_func=lambda x: translate_text("Select Semester", lang) if x == "" else semester_options.get(x, x),
            key="semester_select",
            disabled=not selected_year
        )
    
    return selected_degree, selected_branch, selected_year, selected_semester, branch_options


def render_subject_card(subject_key: str, subject_data: Dict):
    """Render a subject card with links."""
    lang = st.session_state.get('selected_language', 'english')
    
    with st.container(border=True):
        st.markdown(f"**{subject_data.get('name', subject_key)}**")
        st.caption(f"{translate_text('Code', lang)}: {subject_data.get('code', 'N/A')}")
        
        link_col1, link_col2, link_col3 = st.columns(3)
        with link_col1:
            st.link_button(translate_text("Syllabus", lang), subject_data.get('syllabus_link', '#'), use_container_width=True)
        with link_col2:
            st.link_button(translate_text("Notes", lang), subject_data.get('notes_link', '#'), use_container_width=True)
        with link_col3:
            st.link_button(translate_text("Papers", lang), subject_data.get('previous_papers_link', '#'), use_container_width=True)
        
        topics = subject_data.get('topics', [])
        if topics:
            with st.expander(translate_text("View Topics", lang)):
                topic_list = ", ".join([topic.replace("_", " ").title() for topic in topics])
                st.write(topic_list)


def render_sidebar(
    selected_degree: str,
    selected_branch: str,
    selected_year: str,
    selected_semester: str,
    degree_options: Dict,
    branch_options: Dict,
    year_options: Dict,
    semester_options: Dict
):
    """Render the sidebar with quick tips."""
    lang = st.session_state.get('selected_language', 'english')
    
    # Quick Tips Section
    st.divider()
    st.subheader("💡 " + translate_text("Quick Tips", lang))
    
    tips = [
        translate_text("Select your course details first for context-aware responses.", lang),
        translate_text("Use the Results tab to check grades directly from servers.", lang),
        translate_text("Use specific keywords for better and more accurate answers.", lang),
        translate_text("Clear chat history anytime to start a fresh conversation.", lang),
    ]
    
    tip_cols = st.columns(4)
    for i, tip in enumerate(tips):
        with tip_cols[i]:
            with st.container(border=True):
                st.caption(f"TIP {i+1:02d}")
                st.write(tip)
    
    # About Section
    st.divider()
    with st.container(border=True):
        st.subheader("ℹ️ " + translate_text("About", lang))
        st.markdown(f"""
- JNTU EduAssist Platform
- AI Helper 2025.01 Release
- {translate_text("Designed with AI-powered semantic search", lang)}
- {translate_text("Academic results lookup integration", lang)}
- {translate_text("Practice question generator", lang)}
- {translate_text("Q&A assistance system", lang)}
        """)
    
    # Sidebar
    with st.sidebar:
        st.markdown("**🎓 JNTU EduAssist**")
        st.divider()
        
        if selected_degree:
            st.write(f"**{translate_text('Degree', lang)}:** {degree_options.get(selected_degree, '')}")
        if selected_branch and selected_branch in branch_options:
            branch_info = branch_options[selected_branch]
            st.write(f"**{translate_text('Branch', lang)}:** {branch_info.get('abbreviation', '')}")
        if selected_year:
            st.write(f"**{translate_text('Year', lang)}:** {year_options.get(selected_year, '')}")
        if selected_semester:
            st.write(f"**{translate_text('Semester', lang)}:** {semester_options.get(selected_semester, '')}")
        
        st.divider()
        
        if st.button(translate_text("Clear Chat History", lang), use_container_width=True):
            st.session_state.messages = []
            st.rerun()
