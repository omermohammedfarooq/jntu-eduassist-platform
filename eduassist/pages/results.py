"""Results lookup page."""

import streamlit as st
import pandas as pd
from ..services.jntuh_client import JNTUHClient


def render_results_tab():
    """Render the JNTUH results lookup tab."""
    st.markdown("### 📊 JNTUH Results Lookup")
    
    st.markdown("""
        <div class="results-card">
            <h4>🔗 Official JNTUH Results Portals</h4>
            <p>Check your results directly on the official JNTUH websites:</p>
        </div>
    """, unsafe_allow_html=True)
    
    link_col1, link_col2 = st.columns(2)
    with link_col1:
        st.link_button("🌐 JNTUH Results Portal 1", "https://results.jntuh.ac.in/", use_container_width=True)
    with link_col2:
        st.link_button("🌐 JNTUH Results Portal 2", "http://202.63.105.184/results/", use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 📱 Quick Results Lookup")
    st.markdown("Enter your hall ticket number to fetch results:")
    
    hall_ticket = st.text_input(
        "Hall Ticket Number",
        placeholder="e.g., 21A91A0501",
        max_chars=12,
        key="hall_ticket_input"
    )
    
    if st.button("🔍 Fetch Results", key="fetch_results_btn"):
        if hall_ticket:
            with st.spinner("Fetching results from JNTUH..."):
                client = JNTUHClient()
                results = client.fetch_results(hall_ticket.strip().upper())
                
                if "error" in results:
                    st.error(results["error"])
                elif results.get("queued"):
                    st.info(results["message"])
                    st.markdown("**Tip:** Click 'Fetch Results' again after a few seconds, or use the official portals above.")
                elif results.get("success"):
                    _display_results(results.get("data", {}))
                else:
                    st.warning("No results found. Please check your hall ticket number and try again.")
        else:
            st.warning("Please enter a valid hall ticket number.")


def _display_results(data: dict):
    """Display fetched results in organized tables."""
    st.success("Results fetched successfully!")
    
    if "details" in data:
        details = data["details"]
        st.markdown("#### 👤 Student Details")
        
        details_df = pd.DataFrame([{
            "Name": details.get('name', 'N/A'),
            "Roll Number": details.get('rollNumber', 'N/A'),
            "Father Name": details.get('fatherName', 'N/A'),
            "Branch": details.get('branch', 'N/A'),
            "College Code": details.get('collegeCode', 'N/A')
        }])
        st.dataframe(details_df, use_container_width=True, hide_index=True)
    
    if "results" in data and "semesters" in data["results"]:
        st.markdown("#### 📝 Semester Results")
        
        summary_data = []
        for semester in data["results"]["semesters"]:
            sem_name = semester.get("semester", "Unknown")
            sgpa = semester.get("semesterSGPA", "N/A")
            credits = semester.get("semesterCredits", 0)
            backlogs = semester.get("backlogs", 0)
            summary_data.append({
                "Semester": f"Sem {sem_name}",
                "SGPA": sgpa,
                "Credits": credits,
                "Backlogs": int(backlogs) if backlogs else 0
            })
        
        if summary_data:
            st.markdown("##### 📊 Results Summary")
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        st.markdown("##### 📚 Detailed Subject-wise Results")
        for semester in data["results"]["semesters"]:
            sem_name = semester.get("semester", "Unknown")
            sgpa = semester.get("semesterSGPA", "N/A")
            credits = semester.get("semesterCredits", 0)
            backlogs = semester.get("backlogs", 0)
            
            # Simple header for expander
            header_text = f"Semester {sem_name}"
            
            with st.expander(header_text, expanded=False):
                # Show details inside expander
                st.markdown(f"""
                **SGPA:** {sgpa} | **Credits:** {credits} | **Backlogs:** {int(backlogs) if backlogs else 0}
                """)
                
                sem_subjects = semester.get("subjects", [])
                if sem_subjects:
                    table_data = []
                    for subj in sem_subjects:
                        grade = subj.get('grades', 'N/A')
                        grade_status = "✅" if grade in ['O', 'A+', 'A', 'B+', 'B', 'C'] else "❌" if grade in ['F', 'Ab'] else "⚪"
                        table_data.append({
                            "Subject": subj.get('subjectName', 'Unknown'),
                            "Code": subj.get('subjectCode', ''),
                            "Grade": grade,
                            "Credits": subj.get('credits', 0),
                            "Status": grade_status
                        })
                    
                    subjects_df = pd.DataFrame(table_data)
                    st.dataframe(subjects_df, use_container_width=True, hide_index=True)

