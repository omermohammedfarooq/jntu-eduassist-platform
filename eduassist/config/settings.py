"""Application settings and configuration."""

from pathlib import Path


class Settings:
    """Application configuration settings."""
    
    APP_TITLE = "JNTU EduAssist AI"
    APP_ICON = "🎓"
    
    BASE_DIR = Path(__file__).parent.parent.parent
    COURSES_FILE = BASE_DIR / "courses.json"
    KNOWLEDGE_BASE_FILE = BASE_DIR / "knowledge_base.json"
    
    JNTUH_API_URL = "https://jntuhresults.dhethi.com/api/getAcademicResult"
    API_TIMEOUT = 30
    
    SUPPORTED_LANGUAGES = [
        ("english", "English", True),
        ("telugu", "Telugu", False),
        ("tenglish", "Tenglish", False),
        ("hinglish", "Hinglish", False),
        ("urdu", "Urdu", False)
    ]
    
    GRADE_COLORS = {
        "pass": ["O", "A+", "A", "B+", "B", "C"],
        "fail": ["F", "Ab"],
    }
