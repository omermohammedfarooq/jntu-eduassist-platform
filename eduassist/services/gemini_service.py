"""
Gemini AI Service for JNTU EduAssist
Provides AI-powered educational assistance using Google Gemini API
"""

import google.generativeai as genai
import os
from typing import List, Dict, Optional

class GeminiService:
    def __init__(self, api_key: str):
        """Initialize Gemini service with API key"""
        genai.configure(api_key=api_key)
        
        # Use Gemini 1.5 Flash for fast, cost-effective responses
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # System context for JNTU educational assistant
        self.system_context = """You are an AI educational assistant for JNTU (Jawaharlal Nehru Technological University Hyderabad) students.

Your role:
- Help students with academic queries about courses, subjects, and university information
- Provide clear explanations of technical concepts
- Guide students on JNTU-specific processes (results, syllabi, academic calendars)
- Be encouraging and supportive
- Keep responses concise and student-friendly

Important:
- If you don't know something specific about JNTU, acknowledge it
- For official university matters, suggest checking the official JNTU website
- Maintain a helpful, professional tone
- Support multiple languages when asked (English, Telugu, Hindi)
"""
        
        # Initialize chat session
        self.chat = None
        self._start_new_chat()
    
    def _start_new_chat(self):
        """Start a new chat session"""
        self.chat = self.model.start_chat(history=[])
    
    def send_message(self, message: str, language: str = 'english') -> str:
        """
        Send a message to Gemini and get response
        
        Args:
            message: User's message
            language: Preferred response language (english, telugu, hindi, etc.)
        
        Returns:
            AI response as string
        """
        try:
            # Add language instruction if not English
            if language.lower() != 'english':
                language_instructions = {
                    'telugu': 'Please respond in Telugu (తెలుగు).',
                    'tenglish': 'Please respond in Tenglish (Telugu written in English characters).',
                    'hindi': 'Please respond in Hindi (हिंदी).',
                    'hinglish': 'Please respond in Hinglish (Hindi written in English characters).',
                    'urdu': 'Please respond in Urdu (اردو).'
                }
                instruction = language_instructions.get(language.lower(), '')
                if instruction:
                    message = f"{instruction}\n\n{message}"
            
            # Send message with system context
            full_message = f"{self.system_context}\n\nUser query: {message}"
            
            response = self.chat.send_message(full_message)
            return response.text
        
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}. Please try again."
    
    def clear_history(self):
        """Clear chat history and start fresh"""
        self._start_new_chat()
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get current chat history"""
        history = []
        for message in self.chat.history:
            history.append({
                'role': message.role,
                'content': message.parts[0].text
            })
        return history


# Global instance (will be initialized in app.py)
gemini_service: Optional[GeminiService] = None

def initialize_gemini(api_key: str):
    """Initialize global Gemini service instance"""
    global gemini_service
    gemini_service = GeminiService(api_key)
    return gemini_service

def get_gemini_service() -> Optional[GeminiService]:
    """Get the global Gemini service instance"""
    return gemini_service
