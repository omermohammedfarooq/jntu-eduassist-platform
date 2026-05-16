"""Q&A Assistant page."""

import streamlit as st
from typing import Dict
from ..services.knowledge_service import KnowledgeService


def render_assistant_tab(
    knowledge_base: Dict,
    subjects: Dict
):
    """Render the Q&A assistant tab."""
    st.markdown("### Ask Your Question")
    
    selected_subject_key = None
    current_subject_data = None
    
    if subjects and isinstance(subjects, dict) and len(subjects) > 0:
        subject_keys = list(subjects.keys())
        subject_options = {key: subjects[key].get('name', key) for key in subject_keys}
        
        default_index = 0
        if "selected_subject" in st.session_state and st.session_state.selected_subject in subject_keys:
            default_index = subject_keys.index(st.session_state.selected_subject)
        
        selected_subject_key = st.selectbox(
            "Select Subject to Ask About:",
            options=subject_keys,
            index=default_index,
            format_func=lambda x: subject_options.get(x, x),
            key="assistant_subject_select"
        )
        
        current_subject_data = subjects.get(selected_subject_key)
        st.session_state.selected_subject = selected_subject_key
    else:
        st.info("Please select your Degree, Branch, Year, and Semester above to see available subjects.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("links"):
                st.markdown("**Study Materials:**")
                link_cols = st.columns(3)
                for i, (label, url) in enumerate(message["links"].items()):
                    with link_cols[i % 3]:
                        st.link_button(label, url, use_container_width=True)
    
    if prompt := st.chat_input("Ask about any topic (e.g., 'Explain loops in Python')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                subject_key = selected_subject_key if selected_subject_key else "python_programming"
                
                if current_subject_data:
                    current_subject_name = current_subject_data.get('name', '')
                    derived_key = KnowledgeService.get_subject_key(current_subject_name)
                    if derived_key:
                        subject_key = derived_key
                
                knowledge_service = KnowledgeService(knowledge_base)
                answer, match_type = knowledge_service.find_answer(prompt, subject_key)
                
                if not answer and subject_key != "python_programming":
                    answer, match_type = knowledge_service.find_answer(prompt, "python_programming")
                
                links = {}
                if current_subject_data:
                    links = {
                        "📋 Syllabus": current_subject_data.get('syllabus_link', '#'),
                        "📚 Notes": current_subject_data.get('notes_link', '#'),
                        "📝 Previous Papers": current_subject_data.get('previous_papers_link', '#')
                    }
                
                if answer:
                    st.markdown(answer)
                    
                    if links and match_type == "subject":
                        st.markdown("**📚 Study Materials:**")
                        link_cols = st.columns(3)
                        for i, (label, url) in enumerate(links.items()):
                            with link_cols[i % 3]:
                                st.link_button(label, url, use_container_width=True)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "links": links if match_type == "subject" else {}
                    })
                else:
                    no_match_response = """I couldn't find a specific answer for your question. Here are some suggestions:

1. **Be more specific** - Try asking about specific topics like:
   - "What are variables in Python?"
   - "Explain loops and how they work"
   - "What is object-oriented programming?"

2. **Check your course selection** - Make sure you've selected your Degree, Branch, Year, and Semester above.

3. **Try the Practice Questions tab** - Generate practice questions for your subjects!

Feel free to ask about any topic!"""
                    
                    st.markdown(no_match_response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": no_match_response,
                        "links": {}
                    })
