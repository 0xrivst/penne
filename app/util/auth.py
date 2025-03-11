"""
Auth utility functions.
"""

from functools import wraps
from flask import redirect, url_for, g


def login_required(view):
    """Checks if user is present in the g namespace, otherwise redirects to login"""

    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
