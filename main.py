"""
JNTU EduAssist AI - Main Entry Point

A multilingual AI educational assistant for JNTU-H university students.
"""

import streamlit as st

st.set_page_config(
    page_title="JNTU EduAssist AI",
    page_icon="graduation_cap",
    layout="wide"
)

from eduassist.config import apply_theme
from eduassist.config.settings import Settings
from eduassist.data import (
    load_courses,
    load_knowledge_base,
    get_degree_options,
    get_branch_options,
    get_year_options,
    get_semester_options,
    get_subjects
)
from eduassist.ui.components import (
    render_header,
    render_top_bar,
    render_dashboard,
    render_course_selector,
    render_subject_card,
    render_sidebar
)
from eduassist.pages import (
    render_assistant_tab,
    render_results_tab,
    render_practice_tab,
    render_auth_page,
    render_forum_page
)
from eduassist.utils.session import initialize_session_state
from eduassist.data.database import init_database
from eduassist.services.translation_service import translate_text

@st.cache_resource
def setup_database():
    try:
        init_database()
        return True
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        return False


def main():
    """Main application entry point."""
    initialize_session_state()
    
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = 'english'
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    db_ready = setup_database()
    
    courses = load_courses()
    knowledge_base = load_knowledge_base()
    
    apply_theme()
    
    render_top_bar()
    
    if st.session_state.current_page == 'auth':
        render_auth_section(db_ready)
        return
    
    render_header()
    
    lang = st.session_state.get('selected_language', 'english')
    user = st.session_state.get('user')
    
    if user:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 2rem;">
                <p style="color: #a1a1aa; font-size: 1.1rem;">
                    {translate_text("Welcome back", lang)}, 
                    <span style="color: #6366f1; font-weight: 600;">{user['full_name']}</span>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.active_tab is None:
        render_dashboard()
        
        st.markdown("---")
        
        degree_options = get_degree_options(courses)
        
        selected_degree, selected_branch, selected_year, selected_semester, branch_options = render_course_selector(
            degree_options=degree_options,
            get_branch_options_fn=get_branch_options,
            get_year_options_fn=get_year_options,
            get_semester_options_fn=get_semester_options,
            courses=courses
        )
        
        st.session_state.selected_degree = selected_degree
        st.session_state.selected_branch = selected_branch
        st.session_state.selected_year = selected_year
        st.session_state.selected_semester = selected_semester
        
        subjects = get_subjects(courses, selected_degree, selected_branch, selected_year, selected_semester)
        
        if subjects:
            st.markdown("---")
            st.markdown(f"""
                <h3 class="section-title">{translate_text("Available Subjects", lang)}</h3>
            """, unsafe_allow_html=True)
            
            subject_cols = st.columns(min(len(subjects), 3))
            
            for idx, (subject_key, subject_data) in enumerate(subjects.items()):
                col_idx = idx % 3
                with subject_cols[col_idx]:
                    render_subject_card(subject_key, subject_data)
        
        year_options = get_year_options(courses, selected_degree, selected_branch) if selected_branch else {}
        semester_options = get_semester_options(courses, selected_degree, selected_branch, selected_year) if selected_year else {}
        
        render_sidebar(
            selected_degree=selected_degree,
            selected_branch=selected_branch,
            selected_year=selected_year,
            selected_semester=selected_semester,
            degree_options=degree_options,
            branch_options=branch_options,
            year_options=year_options,
            semester_options=semester_options
        )
    else:
        render_active_app(courses, knowledge_base, db_ready, lang)


def render_auth_section(db_ready):
    """Render auth page when requested."""
    lang = st.session_state.get('selected_language', 'english')
    
    st.markdown(f"""
        <div style="max-width: 500px; margin: 2rem auto;">
            <h2 style="text-align: center; margin-bottom: 2rem;">
                {translate_text("Account", lang)}
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if db_ready:
            render_auth_page()
            
            if st.session_state.get('user'):
                st.session_state.current_page = 'home'
                st.rerun()
        else:
            st.error(translate_text("Account features are unavailable. Database connection issue.", lang))
    
    if st.button(translate_text("Back to Home", lang), use_container_width=True):
        st.session_state.current_page = 'home'
        st.rerun()


def render_active_app(courses, knowledge_base, db_ready, lang):
    """Render the currently active app/tab."""
    
    if st.button(translate_text("Back to Dashboard", lang)):
        st.session_state.active_tab = None
        st.rerun()
    
    st.markdown("---")
    
    active = st.session_state.active_tab
    
    degree_options = get_degree_options(courses)
    
    selected_degree, selected_branch, selected_year, selected_semester, branch_options = render_course_selector(
        degree_options=degree_options,
        get_branch_options_fn=get_branch_options,
        get_year_options_fn=get_year_options,
        get_semester_options_fn=get_semester_options,
        courses=courses
    )
    
    st.session_state.selected_degree = selected_degree
    st.session_state.selected_branch = selected_branch
    st.session_state.selected_year = selected_year
    st.session_state.selected_semester = selected_semester
    
    subjects = get_subjects(courses, selected_degree, selected_branch, selected_year, selected_semester)
    
    st.markdown("---")
    
    if active == "ask":
        st.markdown(f"""
            <h2 class="section-title">{translate_text("Ask Questions", lang)}</h2>
        """, unsafe_allow_html=True)
        render_assistant_tab(
            knowledge_base=knowledge_base,
            subjects=subjects
        )
    elif active == "results":
        st.markdown(f"""
            <h2 class="section-title">{translate_text("Check Results", lang)}</h2>
        """, unsafe_allow_html=True)
        render_results_tab()
    elif active == "practice":
        st.markdown(f"""
            <h2 class="section-title">{translate_text("Practice Questions", lang)}</h2>
        """, unsafe_allow_html=True)
        render_practice_tab(subjects)
    elif active == "forum":
        st.markdown(f"""
            <h2 class="section-title">{translate_text("Discussion Forum", lang)}</h2>
        """, unsafe_allow_html=True)
        if db_ready:
            render_forum_page()
        else:
            st.error(translate_text("Forum is unavailable. Database connection issue.", lang))
    
    year_options = get_year_options(courses, selected_degree, selected_branch) if selected_branch else {}
    semester_options = get_semester_options(courses, selected_degree, selected_branch, selected_year) if selected_year else {}
    
    render_sidebar(
        selected_degree=selected_degree,
        selected_branch=selected_branch,
        selected_year=selected_year,
        selected_semester=selected_semester,
        degree_options=degree_options,
        branch_options=branch_options,
        year_options=year_options,
        semester_options=semester_options
    )


if __name__ == "__main__":
    main()
