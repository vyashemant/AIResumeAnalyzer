from flask import Blueprint, render_template, request, redirect, url_for, session
from db.supabase_client import supabase
from services.auth_service import (
    login_with_username,
    signup_user,
    google_oauth_login,
    exchange_google_code
)

auth_bp = Blueprint("auth", __name__)

# ---------- LOGIN ----------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        res = login_with_username(username, password)
        if not res or not res.user:
            return render_template(
                "login.html",
                error="Invalid username or password"
            )

        user = res.user

        session["user"] = {
            "id": user.id,
            "username": username,
            "email": user.email
        }

        # ✅ ENSURE profile exists (SAFE POINT)
        existing = (
            supabase
            .table("profiles")
            .select("id")
            .eq("id", user.id)
            .execute()
        )

        if not existing.data:
            supabase.table("profiles").insert({
                "id": user.id,
                "email": user.email,
                "username": username
            }).execute()

        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")


# ---------- SIGNUP ----------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if not res or not res.user:
            return render_template(
                "signup.html",
                error="Signup failed"
            )

        # ❌ NO profiles insert/update here
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


# ---------- GOOGLE AUTH ----------
@auth_bp.route("/auth/google")
def auth_google():
    redirect_url = "http://127.0.0.1:5000/auth/callback"
    return redirect(google_oauth_login(redirect_url))


@auth_bp.route("/auth/callback")
def auth_callback():
    code = request.args.get("code")
    if not code:
        return "No auth code", 400

    res = exchange_google_code(code)
    if not res or not res.user:
        return "Google login failed", 400

    user = res.user

    profile = supabase.table("profiles").select("*").eq("id", user.id).execute()
    profile_data = profile.data[0] if profile.data else None

    session["user"] = {"id": user.id, "email": user.email}

    if not profile_data or not profile_data.get("username"):
        if not profile_data:
            supabase.table("profiles").insert({
                "id": user.id,
                "email": user.email
            }).execute()

        return redirect(url_for("auth.complete_profile"))

    return redirect(url_for("dashboard.dashboard"))


# ---------- COMPLETE PROFILE ----------
@auth_bp.route("/complete-profile", methods=["GET", "POST"])
def complete_profile():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        existing = supabase.table("profiles").select("id").eq("username", username).execute()
        if existing.data:
            return "Username already taken", 400

        supabase.table("profiles").update({
            "username": username,
            "first_name": first_name,
            "last_name": last_name
        }).eq("id", session["user"]["id"]).execute()

        return redirect(url_for("dashboard.dashboard"))

    return render_template("complete_profile.html")
