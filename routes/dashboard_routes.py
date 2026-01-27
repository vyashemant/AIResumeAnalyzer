from flask import Blueprint, render_template, redirect, url_for, session
from db.supabase_client import supabase

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    return render_template("index.html")

@dashboard_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    # Fetch user's resumes
    res = supabase.table("resumes") \
        .select("ats_score") \
        .eq("user_id", session["user"]["id"]) \
        .execute()

    resumes = res.data
    resumes_count = len(resumes)

    if resumes_count > 0:
        avg_score = round(sum(r["ats_score"] for r in resumes) / resumes_count)
        best_score = max(r["ats_score"] for r in resumes)
    else:
        avg_score = 0
        best_score = 0

    return render_template("dashboard.html", avg_score=avg_score, resumes_count=resumes_count, best_score=best_score)
