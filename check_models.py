from google import genai
from config import Config

client = genai.Client(api_key=Config.GEMINI_API_KEY)

try:
    # List available models
    models = client.models.list()
    print("Available Gemini models:")
    for model in models:
        print(f"- {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
