from flask import Blueprint, render_template, redirect, url_for, session

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    return render_template("index.html")

@dashboard_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html")
