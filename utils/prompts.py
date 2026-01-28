def ats_prompt(resume_text, job_description):
    return f"""
You are an ATS (Applicant Tracking System).

Analyze the RESUME against the JOB DESCRIPTION.

Return ONLY valid JSON in this format:

{{
  "ats_score": number (0-100),
  "matched_skills": [],
  "missing_skills": [],
  "improvements": {{
    "summary": "",
    "experience": "",
    "skills": ""
  }}
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

def rewrite_prompt(resume_text, job_description=None):
    if job_description:
        return f"""
You are an expert resume writer with 10+ years of experience in career coaching and ATS optimization.

Your task is to completely rewrite the provided resume to make it highly tailored to the job description. Follow these guidelines:

1. **Keyword Integration**: Incorporate relevant keywords and phrases from the job description naturally throughout the resume.

2. **Strong Action Verbs**: Use powerful action verbs like "Led", "Developed", "Optimized", "Implemented", "Achieved", etc.

3. **Quantify Achievements**: Add specific numbers, percentages, or metrics to demonstrate impact (e.g., "Increased sales by 25%", "Managed a team of 5").

4. **ATS Optimization**: Ensure the resume is ATS-friendly with clear section headers, consistent formatting, and no graphics or complex layouts.

5. **Tailored Content**: Reorder and emphasize experiences, skills, and achievements that best match the job requirements.

6. **Professional Language**: Use concise, professional language that highlights accomplishments.

7. **Structure**: Maintain standard resume sections (Contact Info, Summary, Experience, Skills, Education) but optimize content within them.

Return ONLY the rewritten resume text in a clean, professional format. Do not include any explanations or additional text.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""
    else:
        return f"""
You are an expert resume writer with 10+ years of experience in career coaching and ATS optimization.

Your task is to rewrite the provided resume to make it more impactful, professional, and ATS-friendly. Follow these guidelines:

1. **Strong Action Verbs**: Replace weak verbs with powerful ones like "Led", "Developed", "Optimized", "Implemented", "Achieved".

2. **Quantify Achievements**: Add specific numbers, percentages, or metrics wherever possible to demonstrate impact.

3. **ATS Optimization**: Use clear section headers, consistent formatting, and keyword-rich content.

4. **Professional Language**: Use concise, professional language that highlights accomplishments and skills.

5. **Structure**: Maintain standard resume sections but optimize the content within them for better readability and impact.

Return ONLY the rewritten resume text in a clean, professional format. Do not include any explanations or additional text.

ORIGINAL RESUME:
{resume_text}
"""
