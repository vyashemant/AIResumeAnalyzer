from db.supabase_client import supabase
# from supabase_auth.errors import AuthApiError


def email_signup(email, password):
    return supabase.auth.sign_up({
        "email": email,
        "password": password
    })


def email_login(email, password):
    return supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })


def google_oauth_login(redirect_url):
    res = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {
            "redirect_to": redirect_url,
            "query_params": {
                "prompt": "consent"
            }
        }
    })
    return res.url


def exchange_google_code(code, redirect_url):
    return supabase.auth.exchange_code_for_session({
        "auth_code": code,
        "redirect_uri": redirect_url
    })


def signup_user(username, email, password):
    # ONLY create auth user
    res = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    if not res or not res.user:
        return None

    # ❌ DO NOT touch profiles here
    return res.user


def login_with_username(username, password):
    res = (
        supabase
        .table("profiles")
        .select("email")
        .eq("username", username)
        .single()
        .execute()
    )

    if not res.data:
        return None

    email = res.data["email"]

    try:
        return supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
    except Exception:
        return None
