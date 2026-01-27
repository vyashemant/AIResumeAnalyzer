from google import genai
from config import Config
from utils.prompts import ats_prompt, rewrite_prompt
import json
import re

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def analyze_resume_with_gemini(resume_text, job_description):
    try:
        prompt = ats_prompt(resume_text, job_description)

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        text = response.text.strip()
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if not match:
            raise ValueError("Gemini did not return valid JSON")

        return json.loads(match.group())
    except Exception as e:
        # Handle API overload or other errors gracefully
        if "503" in str(e) or "overloaded" in str(e).lower():
            return {
                "ats_score": 0,
                "matched_skills": [],
                "missing_skills": ["Service temporarily unavailable"],
                "improvements": {
                    "summary": "The AI service is currently overloaded. Please try again in a few minutes.",
                    "experience": "Service temporarily unavailable",
                    "skills": "Service temporarily unavailable"
                }
            }
        else:
            # Re-raise other errors
            raise e


def rewrite_resume(resume_text, job_description):
    try:
        prompt = rewrite_prompt(resume_text, job_description)

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",   # ✅ SAME STABLE MODEL
            contents=prompt
        )

        return response.text.strip()
    except Exception as e:
        # Handle API overload or other errors gracefully
        if "503" in str(e) or "overloaded" in str(e).lower():
            return "The AI service is currently overloaded. Please try again in a few minutes."
        else:
            # Re-raise other errors
            raise e
