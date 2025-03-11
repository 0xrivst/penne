"""
Home blueprint.

This blueprint contains the route for index page.
"""

from flask import Blueprint, render_template, g
from app.util.paste import construct_expiry_values

main_bp = Blueprint("main", __name__, url_prefix="/")


@main_bp.route("/")
def index():
    """
    Renders index page.
    """
    is_anonymous_user = g.user is None

    return render_template(
        "home.jinja",
        expiry_options=construct_expiry_values(is_anonymous_user),
    )
