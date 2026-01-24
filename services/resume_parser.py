import pdfplumber
from docx import Document
import os

def extract_text(file):
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(file)

    if filename.endswith(".docx"):
        return extract_docx_text(file)

    raise ValueError("Unsupported file format")


def extract_pdf_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_docx_text(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)
