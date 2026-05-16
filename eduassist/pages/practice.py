"""Practice questions page."""

import streamlit as st
from typing import Dict
from ..services.knowledge_service import KnowledgeService


def render_practice_tab(subjects: Dict):
    """Render the practice questions tab."""
    st.markdown("### 📝 Practice Question Generator")
    
    if "show_practice" not in st.session_state:
        st.session_state.show_practice = False
    
    if subjects and isinstance(subjects, dict) and len(subjects) > 0:
        subject_names = {key: data.get('name', key) for key, data in subjects.items()}
        selected_subject = st.selectbox(
            "Select Subject",
            options=list(subject_names.keys()),
            format_func=lambda x: subject_names.get(x, x),
            key="practice_subject"
        )
        
        subject_data = subjects.get(selected_subject, {})
        topics = subject_data.get('topics', ['default'])
        
        selected_topic = st.selectbox(
            "Select Topic (Optional)",
            options=['default'] + topics,
            format_func=lambda x: "All Topics" if x == 'default' else x.replace('_', ' ').title(),
            key="practice_topic"
        )
        
        if st.button("🎯 Generate Practice Questions", key="generate_practice"):
            st.session_state.show_practice = True
        
        if st.session_state.show_practice:
            questions = KnowledgeService.generate_practice_questions(selected_subject, selected_topic)
            st.markdown("#### 📋 Practice Questions:")
            for i, q in enumerate(questions, 1):
                st.markdown(f"""
                    <div class="subject-card">
                        <p><strong>Q{i}:</strong> {q}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.info("💡 Tip: Try answering these questions, then use the Ask Questions tab to verify your answers!")
    else:
        st.info("Please select your course details above to generate practice questions.")
