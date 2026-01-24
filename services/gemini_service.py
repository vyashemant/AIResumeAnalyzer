import os
from google import genai
from config import Config

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def test_gemini():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Reply with: Gemini is working"
    )
    return response.text
