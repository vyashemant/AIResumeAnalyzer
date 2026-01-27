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
You are a professional resume writer.

Rewrite the resume to better match the job description.
Use strong action verbs and quantify impact.
Return ONLY improved resume text.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""
    else:
        return f"""
You are a professional resume writer.

Rewrite the resume to make it more impactful and ATS-friendly.
Use strong action verbs, quantify achievements, and improve formatting.
Return ONLY improved resume text.

RESUME:
{resume_text}
"""
