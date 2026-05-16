"""Data repositories for loading and accessing course data."""

import json
import streamlit as st
from typing import Dict
from pathlib import Path


@st.cache_data
def load_courses(file_path: str = "courses.json") -> Dict:
    """Load courses data from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"{file_path} not found. Please ensure the file exists.")
        return {"courses": {}}
    except json.JSONDecodeError:
        st.error(f"Invalid JSON format in {file_path}")
        return {"courses": {}}


@st.cache_data
def load_knowledge_base(file_path: str = "knowledge_base.json") -> Dict:
    """Load knowledge base from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def get_degree_options(courses: Dict) -> Dict[str, str]:
    """Get available degree options from courses data."""
    degree_data = courses.get("courses", {})
    return {key: data.get("name", key) for key, data in degree_data.items()}


def get_branch_options(courses: Dict, degree: str) -> Dict[str, Dict]:
    """Get available branch options for a given degree."""
    if not degree:
        return {}
    branch_data = courses.get("courses", {}).get(degree, {}).get("branches", {})
    return {
        key: {
            "name": data.get("name", key),
            "abbreviation": data.get("abbreviation", key.upper())
        }
        for key, data in branch_data.items()
    }


def get_year_options(courses: Dict, degree: str, branch: str) -> Dict[str, str]:
    """Get available year options for a given degree and branch."""
    if not degree or not branch:
        return {}
    year_data = (
        courses.get("courses", {})
        .get(degree, {})
        .get("branches", {})
        .get(branch, {})
        .get("years", {})
    )
    return {key: data.get("name", key) for key, data in year_data.items()}


def get_semester_options(courses: Dict, degree: str, branch: str, year: str) -> Dict[str, str]:
    """Get available semester options."""
    if not degree or not branch or not year:
        return {}
    sem_data = (
        courses.get("courses", {})
        .get(degree, {})
        .get("branches", {})
        .get(branch, {})
        .get("years", {})
        .get(year, {})
        .get("semesters", {})
    )
    return {key: data.get("name", key) for key, data in sem_data.items()}


def get_subjects(courses: Dict, degree: str, branch: str, year: str, semester: str) -> Dict:
    """Get subjects for a given course selection."""
    if not all([degree, branch, year, semester]):
        return {}
    return (
        courses.get("courses", {})
        .get(degree, {})
        .get("branches", {})
        .get(branch, {})
        .get("years", {})
        .get(year, {})
        .get("semesters", {})
        .get(semester, {})
        .get("subjects", {})
    )
