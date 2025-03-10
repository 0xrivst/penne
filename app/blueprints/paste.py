"""
Paste blueprint.

This blueprint contains routes for paste operations.
"""

from datetime import timedelta
from flask import Blueprint, request, redirect, url_for, g
from app.util.time import get_current_utc_datetime
from app.util.sqids import sqids
from app.service.firebase import firebase
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
        return redirect(url_for("index"), 401)

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
