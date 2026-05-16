"""
Unified AI Service for JNTU EduAssist
Supports multiple AI providers via OpenRouter (December 2025)
"""

from openai import OpenAI
import os
from typing import List, Dict, Optional

# Available AI Models (VERIFIED WORKING on OpenRouter - December 2025)
AVAILABLE_MODELS = {
    'llama-3.3': {
        'name': 'Llama 3.3 70B',
        'description': 'Meta\'s powerful 70B model, fast and capable',
        'icon': '🦙'
    },
    'deepseek': {
        'name': 'DeepSeek Chat',
        'description': 'Advanced reasoning and technical problem solving',
        'icon': '🧠'
    },
    'mistral': {
        'name': 'Mistral 7B',
        'description': 'Fast and efficient instruction-following model',
        'icon': '⚡'
    },
    'qwen': {
        'name': 'Qwen 2.5 Coder',
        'description': 'Specialized coding and programming assistant',
        'icon': '💻'
    }
}

class UnifiedAIService:
    def __init__(self, openrouter_key: str):
        """Initialize OpenRouter AI service with unified key"""
        
        self.openrouter_available = False
        
        if openrouter_key:
            try:
                self.openrouter_client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=openrouter_key
                )
                self.openrouter_available = True
                print("[OK] OpenRouter client initialized")
            except Exception as e:
                print(f"[WARNING] OpenRouter initialization failed: {e}")
        
        # Conversation histories for each model
        self.llama_history = []
        self.deepseek_history = []
        self.mistral_history = []
        self.qwen_history = []
        
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
    
    def send_message(self, message: str, model: str = 'llama-3.3', language: str = 'english') -> Dict:
        """
        Send message to selected AI model
        
        Args:
            message: User's message
            model: Model identifier (llama-3.3, deepseek, mistral, qwen)
            language: Preferred response language
        
        Returns:
            Dict with 'success', 'response', and 'model' keys
        """
        
        # Check if OpenRouter is available
        if not self.openrouter_available:
            return {'success': False, 'error': 'OpenRouter is not available. Please check API key.'}
        
        try:
            # Add language instruction if not English
            lang_message = self._add_language_instruction(message, language)
            
            # Route to appropriate model
            if model == 'llama-3.3':
                response_text = self._call_llama(lang_message)
            elif model == 'deepseek':
                response_text = self._call_deepseek(lang_message)
            elif model == 'mistral':
                response_text = self._call_mistral(lang_message)
            elif model == 'qwen':
                response_text = self._call_qwen(lang_message)
            else:
                return {'success': False, 'error': f'Unknown model: {model}'}
            
            return {
                'success': True,
                'response': response_text,
                'model': AVAILABLE_MODELS[model]['name']
            }
        
        except Exception as e:
            return {'success': False, 'error': f'Error: {str(e)}'}
    
    def _add_language_instruction(self, message: str, language: str) -> str:
        """Add language instruction to message"""
        if language.lower() == 'english':
            return message
        
        language_instructions = {
            'telugu': 'Please respond in Telugu (తెలుగు).',
            'tenglish': 'Please respond in Tenglish (Telugu written in English characters).',
            'hindi': 'Please respond in Hindi (हिंदी).',
            'hinglish': 'Please respond in Hinglish (Hindi written in English characters).',
            'urdu': 'Please respond in Urdu (اردو).'
        }
        
        instruction = language_instructions.get(language.lower(), '')
        if instruction:
            return f"{instruction}\n\n{message}"
        return message
    
    def _call_llama(self, message: str) -> str:
        """Call Meta Llama 3.3 70B via OpenRouter"""
        self.llama_history.append({"role": "user", "content": message})
        
        messages = [{"role": "system", "content": self.system_context}] + self.llama_history
        
        completion = self.openrouter_client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct",
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        response_text = completion.choices[0].message.content
        self.llama_history.append({"role": "assistant", "content": response_text})
        
        return response_text
    
    def _call_deepseek(self, message: str) -> str:
        """Call DeepSeek Chat via OpenRouter"""
        self.deepseek_history.append({"role": "user", "content": message})
        
        messages = [{"role": "system", "content": self.system_context}] + self.deepseek_history
        
        completion = self.openrouter_client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        response_text = completion.choices[0].message.content
        self.deepseek_history.append({"role": "assistant", "content": response_text})
        
        return response_text
    
    def _call_mistral(self, message: str) -> str:
        """Call Mistral 7B Instruct via OpenRouter"""
        self.mistral_history.append({"role": "user", "content": message})
        
        messages = [{"role": "system", "content": self.system_context}] + self.mistral_history
        
        completion = self.openrouter_client.chat.completions.create(
            model="mistralai/mistral-7b-instruct:free",
            messages=messages,
            temperature=0.7,
            max_tokens=2000  # Increased from 1500 to prevent truncation
        )
        
        response_text = completion.choices[0].message.content
        
        # Validate response is not empty or just special characters
        if not response_text or len(response_text.strip()) < 2:
            response_text = "I apologize, but I encountered an issue generating a response. Please try again."
        
        self.mistral_history.append({"role": "assistant", "content": response_text})
        
        return response_text
    
    def _call_qwen(self, message: str) -> str:
        """Call Qwen 2.5 Coder via OpenRouter"""
        self.qwen_history.append({"role": "user", "content": message})
        
        messages = [{"role": "system", "content": self.system_context}] + self.qwen_history
        
        completion = self.openrouter_client.chat.completions.create(
            model="qwen/qwen-2.5-coder-32b-instruct",
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        response_text = completion.choices[0].message.content
        self.qwen_history.append({"role": "assistant", "content": response_text})
        
        return response_text
    
    def clear_history(self, model: Optional[str] = None):
        """Clear chat history for specific model or all models"""
        if model is None or model == 'llama-3.3':
            self.llama_history = []
        
        if model is None or model == 'deepseek':
            self.deepseek_history = []
        
        if model is None or model == 'mistral':
            self.mistral_history = []
        
        if model is None or model == 'qwen':
            self.qwen_history = []
    
    def get_available_models(self) -> List[Dict]:
        """Get list of available AI models"""
        available = []
        
        if self.openrouter_available:
            for model_id, model_info in AVAILABLE_MODELS.items():
                available.append({**model_info, 'id': model_id})
        
        return available


# Global instance
ai_service: Optional[UnifiedAIService] = None

def initialize_ai_service(openrouter_key: str):
    """Initialize global AI service instance"""
    global ai_service
    ai_service = UnifiedAIService(openrouter_key)
    return ai_service

def get_ai_service() -> Optional[UnifiedAIService]:
    """Get the global AI service instance"""
    return ai_service
