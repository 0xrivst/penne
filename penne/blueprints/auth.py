"""
Authentication blueprint

This blueprint contains routes for auth operations.
"""

import json
import time
import functools
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    g,
)
from requests.exceptions import HTTPError
from penne.service.pyrebase import pyrebase
from penne.util.auth import login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

TOKEN_EXPIRATION = 60 * 60


@auth_bp.route("/signup", methods=("GET", "POST"))
def signup():
    """Creates user record in the database and redirects to login if successful"""

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None

        if not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                pyrebase.get_firebase_auth().create_user_with_email_and_password(
                    email, password
                )
            except Exception as e:
                error = e
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/signup.jinja")


@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    """Logs user in, redirects home if successful"""

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None

        try:
            user = pyrebase.get_firebase_auth().sign_in_with_email_and_password(
                email, password
            )
        except Exception as e:
            error = e
        else:
            session.clear()
            session["user"] = user
            update_signed_in_at()
            return redirect(url_for("main.index"))

        flash(error)

    return render_template("auth/login.jinja")


@auth_bp.route("/user/<string:user_id>", methods=("GET", "POST"))
def profile(user_id):

    user = session.get("user")

    error = None

    if user["localId"] != user_id:
        error = "Unauthorized"
        flash(error)
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        token = user["idToken"]
        pyrebase.get_firebase_auth().update_profile(
            token, request.form["userDisplayName"]
        )
        new_name = pyrebase.get_firebase_auth().get_account_info(token)["users"][0][
            "displayName"
        ]
        user["displayName"] = new_name
        session["user"] = user

    return render_template("auth/profile.jinja")


@auth_bp.route("/logout")
def logout():
    """Clears user's session"""

    session.clear()
    return redirect(url_for("main.index"))


@auth_bp.before_app_request
def load_logged_in_user():
    """Fetches the current user from the session and sets it in the g namespace"""

    user = session.get("user")

    if user is None:
        g.user = None
    else:
        if is_token_expired() >= TOKEN_EXPIRATION:
            try:
                fresh_token = pyrebase.get_firebase_auth().refresh(
                    user["refreshToken"]
                )["idToken"]
                session["user"]["idToken"] = fresh_token
                g.user = session["user"]
                update_signed_in_at()
            except HTTPError as e:
                session.clear()
                error = json.loads(e.strerror)["error"]["message"]
                flash(error)

        g.user = user


def update_signed_in_at():
    """Update signed in timestamp in session"""
    session["signed_in_at"] = int(time.time())


def is_token_expired():
    """Check if the token in session has expired"""
    return int(time.time()) - session.get("signed_in_at")
