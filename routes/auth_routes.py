from flask import Blueprint, render_template, request, redirect, url_for, session, flash
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

        if not username or not password:
            flash("Username and password are required", "error")
            return render_template("login.html")

        try:
            res = login_with_username(username, password)
            if not res or not res.user:
                flash("Invalid username or password", "error")
                return render_template("login.html")

            user = res.user

            # Get or create user profile
            profile = supabase.table("profiles").select("*").eq("id", user.id).execute()
            profile_data = profile.data[0] if profile.data else None

            if not profile_data:
                # Create new profile
                supabase.table("profiles").insert({
                    "id": user.id,
                    "email": user.email,
                    "username": username
                }).execute()
                session_username = username
            else:
                # Use existing profile username
                session_username = profile_data.get("username", username)

            session["user"] = {
                "id": user.id,
                "username": session_username,
                "email": user.email
            }

            flash("Login successful!", "success")
            return redirect(url_for("dashboard.dashboard"))

        except Exception as e:
            flash("An error occurred during login. Please try again.", "error")
            return render_template("login.html")

    return render_template("login.html")


# ---------- SIGNUP ----------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        if not email or not password or not username:
            flash("Email, password, and username are required", "error")
            return render_template("signup.html")

        try:
            # 1. Create auth user
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if not res or not res.user:
                flash("Signup failed.", "error")
                return render_template("signup.html")

            user = res.user

            # 2. Create profile
            supabase.table("profiles").insert({
                "id": user.id,
                "email": email,
                "username": username,
                "first_name": first_name,
                "last_name": last_name
            }).execute()

            # 3. AUTO LOGIN (THIS WAS MISSING)
            session["user"] = {
                "id": user.id,
                "email": email,
                "username": username
            }

            flash("Account created successfully!", "success")
            return redirect(url_for("dashboard.dashboard"))

        except Exception as e:
            print("Signup error:", e)
            flash("An error occurred during signup.", "error")
            return render_template("signup.html")

    return render_template("signup.html")



# ---------- GOOGLE AUTH ----------
@auth_bp.route("/auth/google")
def auth_google():
    redirect_url = url_for("auth.auth_callback", _external=True)
    return redirect(google_oauth_login(redirect_url))


@auth_bp.route("/auth/callback")
def auth_callback():
    code = request.args.get("code")
    if not code:
        flash("Google login failed.", "error")
        return redirect(url_for("auth.login"))

    redirect_url = url_for("auth.auth_callback", _external=True)

    try:
        res = exchange_google_code(code, redirect_url)

        if not res or not res.user:
            flash("Google login failed.", "error")
            return redirect(url_for("auth.login"))

        user = res.user

        profile = supabase.table("profiles").select("*").eq("id", user.id).execute()
        profile_data = profile.data[0] if profile.data else None

        session["user"] = {
            "id": user.id,
            "email": user.email
        }

        if not profile_data:
            supabase.table("profiles").insert({
                "id": user.id,
                "email": user.email
            }).execute()
            return redirect(url_for("auth.complete_profile"))

        if not profile_data.get("username"):
            return redirect(url_for("auth.complete_profile"))

        session["user"]["username"] = profile_data["username"]
        return redirect(url_for("dashboard.dashboard"))

    except Exception as e:
        print("OAuth error:", e)
        flash("Google login failed.", "error")
        return redirect(url_for("auth.login"))


# ---------- COMPLETE PROFILE ----------
@auth_bp.route("/complete-profile", methods=["GET", "POST"])
def complete_profile():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        if not username:
            flash("Username is required", "error")
            return render_template("complete_profile.html")

        try:
            existing = supabase.table("profiles").select("id").eq("username", username).execute()
            if existing.data:
                flash("Username already taken", "error")
                return render_template("complete_profile.html")

            supabase.table("profiles").update({
                "username": username,
                "first_name": first_name,
                "last_name": last_name
            }).eq("id", session["user"]["id"]).execute()

            # Update session with username
            session["user"]["username"] = username

            flash("Profile completed successfully!", "success")
            return redirect(url_for("dashboard.dashboard"))

        except Exception as e:
            flash("An error occurred while completing your profile. Please try again.", "error")
            return render_template("complete_profile.html")

    return render_template("complete_profile.html")


# ---------- LOGOUT ----------
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("auth.login"))
