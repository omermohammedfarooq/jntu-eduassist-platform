"""Data access module for loading courses and knowledge base."""

from .repositories import (
    load_courses,
    load_knowledge_base,
    get_degree_options,
    get_branch_options,
    get_year_options,
    get_semester_options,
    get_subjects
)

__all__ = [
    "load_courses",
    "load_knowledge_base",
    "get_degree_options",
    "get_branch_options",
    "get_year_options",
    "get_semester_options",
    "get_subjects"
]
