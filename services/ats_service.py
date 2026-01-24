from google import genai
from config import Config
from utils.prompts import ats_prompt, rewrite_prompt
import json
import re

client = genai.Client(api_key=Config.GEMINI_API_KEY)

def analyze_resume_with_gemini(resume_text, job_description):
    prompt = ats_prompt(resume_text, job_description)

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("Gemini did not return valid JSON")

    return json.loads(match.group())


def rewrite_resume(resume_text, job_description):
    prompt = rewrite_prompt(resume_text, job_description)

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",   # ✅ SAME STABLE MODEL
        contents=prompt
    )

    return response.text.strip()
