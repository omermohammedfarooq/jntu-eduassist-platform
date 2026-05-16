"""Translation service using deep-translator for multilingual support."""

from deep_translator import GoogleTranslator
from typing import Optional
from functools import lru_cache

LANGUAGE_CODES = {
    "english": "en",
    "telugu": "te", 
    "hindi": "hi",
    "urdu": "ur",
    "tamil": "ta",
    "kannada": "kn",
    "marathi": "mr",
    "bengali": "bn",
    "gujarati": "gu",
    "malayalam": "ml",
    "tenglish": "te",  # Telugu-English mix (translate to Telugu)
    "hinglish": "hi"   # Hindi-English mix (translate to Hindi)
}

LANGUAGE_NAMES = {
    "english": "English",
    "telugu": "Telugu",
    "hindi": "Hindi",
    "urdu": "Urdu",
    "tamil": "Tamil",
    "kannada": "Kannada",
    "marathi": "Marathi",
    "bengali": "Bengali",
    "gujarati": "Gujarati",
    "malayalam": "Malayalam",
    "tenglish": "Tenglish",
    "hinglish": "Hinglish"
}

LANGUAGE_NATIVE = {
    "english": "English",
    "telugu": "తెలుగు",
    "hindi": "हिन्दी",
    "urdu": "اردو",
    "tamil": "தமிழ்",
    "kannada": "ಕನ್ನಡ",
    "marathi": "मराठी",
    "bengali": "বাংলা",
    "gujarati": "ગુજરાતી",
    "malayalam": "മലയാളം",
    "tenglish": "Tenglish",
    "hinglish": "Hinglish"
}

@lru_cache(maxsize=1000)
def translate_text(text: str, target_lang: str, source_lang: str = "en") -> str:
    """Translate text to target language."""
    if not text or target_lang == "english" or target_lang == source_lang:
        return text
    
    target_code = LANGUAGE_CODES.get(target_lang, "en")
    source_code = LANGUAGE_CODES.get(source_lang, "en") if source_lang != "en" else "en"
    
    try:
        translator = GoogleTranslator(source=source_code, target=target_code)
        translated = translator.translate(text)
        return translated if translated else text
    except Exception as e:
        print(f"[Translation Error] {e}")
        return text

def get_available_languages():
    """Return list of available languages with their details."""
    return [
        {"key": k, "name": v, "native": LANGUAGE_NATIVE.get(k, v), "code": LANGUAGE_CODES.get(k, "en")}
        for k, v in LANGUAGE_NAMES.items()
    ]

def translate_ui_elements(elements: dict, target_lang: str) -> dict:
    """Translate a dictionary of UI elements."""
    if target_lang == "english":
        return elements
    
    translated = {}
    for key, value in elements.items():
        if isinstance(value, str):
            translated[key] = translate_text(value, target_lang)
        elif isinstance(value, list):
            translated[key] = [translate_text(item, target_lang) if isinstance(item, str) else item for item in value]
        else:
            translated[key] = value
    return translated
