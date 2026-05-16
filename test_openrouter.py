"""
Test different OpenRouter models to find which ones actually work
"""
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

openrouter_key = os.getenv('OPENROUTER_API_KEY')

# Test different model names that should be available
models_to_test = [
    "deepseek/deepseek-chat",  # DeepSeek without version
    "meta-llama/llama-3.3-70b-instruct",  # Llama 3.3
    "google/gemini-2.0-flash-exp:free",  # Gemini 2.0
    "anthropic/claude-3.5-sonnet:free",  # Claude
    "mistralai/mistral-7b-instruct:free",  # Mistral
    "qwen/qwen-2.5-72b-instruct:free",  # Qwen
]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_key
)

for model_name in models_to_test:
    try:
        print(f"Testing {model_name}...")
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": "Say hi"}
            ],
            max_tokens=20
        )
        response = completion.choices[0].message.content
        print(f"  SUCCESS: {response[:50]}")
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            print(f"  FAILED: Model not found")
        else:
            print(f"  FAILED: {error_msg[:100]}")
