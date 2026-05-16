#!/usr/bin/env python3
"""
Script to add new subjects and Q&A content to JNTU EduAssist.
This helps administrators easily expand the knowledge base.
"""

import json
import os
from typing import Dict, List

def load_json(filepath: str) -> Dict:
    """Load JSON file safely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found!")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filepath}")
        return {}

def save_json(filepath: str, data: Dict) -> bool:
    """Save data to JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def add_subject_to_courses():
    """Add a new subject to courses.json"""
    print("\n=== Add New Subject to Course ===\n")
    
    courses = load_json('courses.json')
    if not courses:
        return
    
    print("Available degrees:", list(courses.get('courses', {}).keys()))
    degree = input("Enter degree key (e.g., btech): ").strip().lower()
    
    if degree not in courses.get('courses', {}):
        print(f"Degree '{degree}' not found!")
        return
    
    branches = courses['courses'][degree].get('branches', {})
    print("Available branches:", list(branches.keys()))
    branch = input("Enter branch key (e.g., cse): ").strip().lower()
    
    if branch not in branches:
        print(f"Branch '{branch}' not found!")
        return
    
    years = branches[branch].get('years', {})
    print("Available years:", list(years.keys()))
    year = input("Enter year key (e.g., year1): ").strip().lower()
    
    if year not in years:
        print(f"Year '{year}' not found!")
        return
    
    semesters = years[year].get('semesters', {})
    print("Available semesters:", list(semesters.keys()))
    semester = input("Enter semester key (e.g., sem1): ").strip().lower()
    
    if semester not in semesters:
        print(f"Semester '{semester}' not found!")
        return
    
    print("\n--- Subject Details ---")
    subject_key = input("Subject key (e.g., data_structures): ").strip().lower().replace(" ", "_")
    subject_name = input("Subject name (e.g., Data Structures): ").strip()
    subject_code = input("Subject code (e.g., CS102): ").strip()
    
    print("\n--- Google Drive Links ---")
    syllabus_link = input("Syllabus link: ").strip() or "https://drive.google.com/file/d/PLACEHOLDER/view"
    notes_link = input("Notes link: ").strip() or "https://drive.google.com/file/d/PLACEHOLDER/view"
    papers_link = input("Previous papers link: ").strip() or "https://drive.google.com/file/d/PLACEHOLDER/view"
    
    topics_input = input("Topics (comma-separated): ").strip()
    topics = [t.strip().lower().replace(" ", "_") for t in topics_input.split(",")] if topics_input else []
    
    new_subject = {
        "name": subject_name,
        "code": subject_code,
        "syllabus_link": syllabus_link,
        "notes_link": notes_link,
        "previous_papers_link": papers_link,
        "topics": topics,
        "embeddings_stored": False
    }
    
    courses['courses'][degree]['branches'][branch]['years'][year]['semesters'][semester]['subjects'][subject_key] = new_subject
    
    if save_json('courses.json', courses):
        print(f"\n✅ Subject '{subject_name}' added successfully!")
    else:
        print("\n❌ Failed to save subject!")

def add_topic_to_knowledge_base():
    """Add Q&A content for a topic."""
    print("\n=== Add Topic Q&A ===\n")
    
    kb = load_json('knowledge_base.json')
    if not kb:
        kb = {}
    
    print("Available subjects:", list(kb.keys()))
    subject_key = input("Subject key (e.g., python_programming): ").strip().lower()
    
    if subject_key not in kb:
        kb[subject_key] = {}
        print(f"Creating new subject: {subject_key}")
    
    topic_key = input("Topic key (e.g., arrays): ").strip().lower().replace(" ", "_")
    
    print("\nEnter keywords (comma-separated):")
    keywords_input = input("Keywords: ").strip()
    keywords = [k.strip().lower() for k in keywords_input.split(",")] if keywords_input else []
    
    print("\nEnter the answer (use \\n for new lines, press Enter twice to finish):")
    answer_lines = []
    while True:
        line = input()
        if line == "":
            break
        answer_lines.append(line)
    answer = "\n".join(answer_lines)
    
    kb[subject_key][topic_key] = {
        "keywords": keywords,
        "answer": answer
    }
    
    if save_json('knowledge_base.json', kb):
        print(f"\n✅ Topic '{topic_key}' added to '{subject_key}'!")
    else:
        print("\n❌ Failed to save topic!")

def bulk_add_topics():
    """Add multiple topics at once from a template."""
    print("\n=== Bulk Add Topics ===\n")
    
    template = {
        "subject_key": "data_structures",
        "topics": [
            {
                "topic_key": "arrays",
                "keywords": ["array", "arrays", "index", "indexing", "element"],
                "answer": "Arrays are collections of elements stored at contiguous memory locations..."
            },
            {
                "topic_key": "linked_lists",
                "keywords": ["linked list", "node", "pointer", "next"],
                "answer": "A linked list is a linear data structure where elements are stored in nodes..."
            }
        ]
    }
    
    template_file = "topic_template.json"
    if not os.path.exists(template_file):
        with open(template_file, 'w') as f:
            json.dump(template, f, indent=2)
        print(f"Created template file: {template_file}")
        print("Edit this file with your topics, then run this option again.")
        return
    
    with open(template_file, 'r') as f:
        data = json.load(f)
    
    kb = load_json('knowledge_base.json')
    subject_key = data.get('subject_key', '')
    
    if subject_key not in kb:
        kb[subject_key] = {}
    
    added = 0
    for topic in data.get('topics', []):
        topic_key = topic.get('topic_key', '')
        if topic_key:
            kb[subject_key][topic_key] = {
                "keywords": topic.get('keywords', []),
                "answer": topic.get('answer', '')
            }
            added += 1
    
    if save_json('knowledge_base.json', kb):
        print(f"\n✅ Added {added} topics to '{subject_key}'!")
    else:
        print("\n❌ Failed to save topics!")

def view_structure():
    """View current course structure."""
    print("\n=== Current Course Structure ===\n")
    
    courses = load_json('courses.json')
    
    for degree, degree_data in courses.get('courses', {}).items():
        print(f"\n📚 {degree_data.get('name', degree)}")
        for branch, branch_data in degree_data.get('branches', {}).items():
            print(f"  └── 🏛️ {branch_data.get('name', branch)}")
            for year, year_data in branch_data.get('years', {}).items():
                print(f"      └── 📅 {year_data.get('name', year)}")
                for sem, sem_data in year_data.get('semesters', {}).items():
                    print(f"          └── 📖 {sem_data.get('name', sem)}")
                    for subj, subj_data in sem_data.get('subjects', {}).items():
                        print(f"              └── 📝 {subj_data.get('name', subj)}")

def main():
    """Main menu for the add subject script."""
    print("=" * 50)
    print("JNTU EduAssist - Content Management")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Add new subject to course")
        print("2. Add topic Q&A to knowledge base")
        print("3. Bulk add topics from template")
        print("4. View current course structure")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            add_subject_to_courses()
        elif choice == "2":
            add_topic_to_knowledge_base()
        elif choice == "3":
            bulk_add_topics()
        elif choice == "4":
            view_structure()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
