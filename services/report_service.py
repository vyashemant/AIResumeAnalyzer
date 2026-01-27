from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(result, filepath):
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>ATS Score:</b> {result['ats_score']}%", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Matched Skills</b>", styles['Heading3']))
    story.append(Paragraph(", ".join(result['matched_skills']), styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Missing Skills</b>", styles['Heading3']))
    story.append(Paragraph(", ".join(result['missing_skills']), styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Improvements</b>", styles['Heading3']))
    for k, v in result["improvements"].items():
        story.append(Paragraph(f"<b>{k.title()}:</b> {v}", styles['Normal']))
        story.append(Spacer(1, 8))

    doc.build(story)

def generate_resume_pdf(resume_text, filepath):
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Split resume text into lines and add as paragraphs
    lines = resume_text.split('\n')
    for line in lines:
        if line.strip():  # Skip empty lines
            story.append(Paragraph(line.strip(), styles['Normal']))
            story.append(Spacer(1, 6))

    doc.build(story)
