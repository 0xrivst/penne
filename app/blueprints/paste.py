"""
Paste blueprint.

This blueprint contains routes for paste operations.
"""

from datetime import timedelta
from flask import Blueprint, request, redirect, url_for, g, render_template, flash
from google.cloud.firestore_v1 import Query
from google.cloud.firestore_v1.base_query import FieldFilter, Or
from app.util.time import get_current_utc_datetime
from app.util.sqids import sqids
from app.util.auth import login_required
from app.service.firebase import firebase
from app.service.crypto import crypto
from app.models.Paste import Paste, PasteMeta

paste_bp = Blueprint("paste", __name__, url_prefix="/paste")


@paste_bp.post("/create")
def create():
    """Uploads paste to database"""

    timestamp = get_current_utc_datetime()
    paste_id = sqids.encode([int(timestamp.timestamp())])
    expires_in = int(request.form["expiresIn"])
    expires_at = (timestamp + timedelta(seconds=expires_in)) if expires_in > 0 else None
    user_id = 0

    if g.user is None and expires_at is None:
        return redirect(url_for("main.index"), 401)

    if g.user is not None:
        user_id = g.user["localId"]

    firebase.get_pastes_collection().document(paste_id).set(
        Paste(
            PasteMeta(user_id, timestamp, expires_at),
            request.form["pasteName"] if request.form["pasteName"] else "Unnamed",
            request.form["pasteText"],
            to_encrypt=True,
        ).to_dict()
    )

    return redirect(url_for("paste.get", paste_id=paste_id))


@paste_bp.get("/<string:user_id>")
def user(user_id):
    """Get a list of user's pastes"""

    pastes = __get_user_pastes(user_id)

    paste_list = []

    for paste in pastes:
        paste_tmp = paste.to_dict()
        paste_tmp["paste_id"] = paste.id
        paste_tmp["title"] = crypto.decrypt(paste_tmp["title"])
        paste_list.append(paste_tmp)

    return render_template("pastes/list.jinja", pastes=paste_list)


@paste_bp.get("/get/<string:paste_id>")
def get(paste_id):
    """Get a paste by its ID"""

    paste = firebase.get_pastes_collection().document(paste_id).get()

    if paste.exists:
        paste_dict = paste.to_dict()
        expires_at = paste_dict["expires_at"]
        paste_dict["paste_id"] = paste_id
        if expires_at is not None and expires_at < get_current_utc_datetime():
            flash("Paste not found", "warning")
            redirect(url_for("main.index"))
        paste = Paste.from_dict(paste_dict, encrypted=True)
        return render_template("pastes/view.jinja", paste=paste)

    flash("Paste not found", "warning")
    return redirect(url_for("main.index"))


@paste_bp.post("/delete/<string:paste_id>")
@login_required
def delete(paste_id):
    """Delete paste by its ID"""
    paste = firebase.get_pastes_collection().document(paste_id).get()

    if paste.exists and paste.to_dict()["user_id"] == g.user["localId"]:
        try:
            firebase.get_pastes_collection().document(paste_id).delete()
            flash("Paste deleted!", "success")
        except Exception as e:
            flash(e)
            return redirect(url_for("paste.get", paste_id=paste.paste_id))

    return redirect(url_for("paste.user", user_id=g.user["localId"]))


def __get_user_pastes(user_id):
    return (
        firebase.get_pastes_collection()
        .order_by("created_at", direction=Query.DESCENDING)
        .where(filter=FieldFilter("user_id", "==", user_id))
        .where(filter=__get_current_expiration_filter())
        .select(["title", "created_at", "user_id"])
        .stream()
    )


def __get_current_expiration_filter():
    return Or(
        filters=[
            FieldFilter("expires_at", "==", None),
            FieldFilter("expires_at", ">", get_current_utc_datetime()),
        ]
    )
