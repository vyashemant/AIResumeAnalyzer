from flask import Blueprint, request, render_template, redirect, url_for, session, send_file
from services.resume_parser import extract_text
from services.ats_service import analyze_resume_with_gemini, rewrite_resume
from services.report_service import generate_pdf
from db.supabase_client import supabase

resume_bp = Blueprint("resume", __name__)

# ---------- UPLOAD ----------
@resume_bp.route("/upload")
def upload():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return render_template("upload.html")

# ---------- ANALYZE ----------
@resume_bp.route("/analyze", methods=["POST"])
def analyze():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    resume_file = request.files.get("resume")
    job_description = request.form.get("job_description")

    resume_text = extract_text(resume_file)
    result = analyze_resume_with_gemini(resume_text, job_description)

    supabase.table("resumes").insert({
        "user_id": session["user"]["id"],
        "ats_score": result["ats_score"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "improvements": result["improvements"]
    }).execute()

    session["last_result"] = result
    session["last_resume_text"] = resume_text
    session["last_jd"] = job_description

    return render_template("analyze.html", result=result)


# ---------- HISTORY ----------
@resume_bp.route("/history")
def history():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    res = supabase.table("resumes") \
        .select("*") \
        .eq("user_id", session["user"]["id"]) \
        .order("created_at", desc=True) \
        .execute()

    return render_template("history.html", resumes=res.data)


# ---------- DOWNLOAD ----------
@resume_bp.route("/download-report")
def download_report():
    result = session.get("last_result")
    if not result:
        return redirect(url_for("dashboard.dashboard"))

    path = "report.pdf"
    generate_pdf(result, path)
    return send_file(path, as_attachment=True)


# ---------- REWRITE ----------
@resume_bp.route("/rewrite", methods=["POST"])
def rewrite():
    improved = rewrite_resume(
        session["last_resume_text"],
        session["last_jd"]
    )
    return render_template("rewrite.html", improved=improved)

# ---------- DIRECT REWRITE ----------
@resume_bp.route("/rewrite-direct", methods=["POST"])
def rewrite_direct():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    resume_file = request.files.get("resume")
    job_description = request.form.get("job_description")

    resume_text = extract_text(resume_file)
    improved = rewrite_resume(resume_text, job_description if job_description else None)

    return render_template("rewrite.html", improved=improved)
